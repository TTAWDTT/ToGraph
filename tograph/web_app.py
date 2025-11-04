#!/usr/bin/env python3
"""Web frontend for ToGraph - interactive knowledge graph viewer."""

import os
import tempfile
import shutil
import uuid
import time
import atexit
from pathlib import Path
from threading import Lock
from flask import Flask, render_template_string, request, send_file, jsonify
from werkzeug.utils import secure_filename
from .parser import PDFParser, MarkdownParser
from .graph_builder import GraphBuilder
from .visualizer import GraphVisualizer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Store mapping of file IDs to (path, temp_dir, timestamp)
# Files expire after 1 hour
file_storage = {}
storage_lock = Lock()
FILE_EXPIRY_SECONDS = 3600  # 1 hour

def cleanup_expired_files():
    """Remove expired files from storage."""
    current_time = time.time()
    expired_ids = []
    
    with storage_lock:
        for file_id, (filepath, temp_dir, timestamp) in list(file_storage.items()):
            if current_time - timestamp > FILE_EXPIRY_SECONDS:
                expired_ids.append(file_id)
                # Clean up temporary directory
                try:
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Warning: Failed to clean up {temp_dir}: {e}")
        
        # Remove expired entries
        for file_id in expired_ids:
            del file_storage[file_id]
    
    return len(expired_ids)

def cleanup_all_files():
    """Clean up all temporary files on shutdown."""
    with storage_lock:
        for file_id, (filepath, temp_dir, timestamp) in file_storage.items():
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Failed to clean up {temp_dir}: {e}")
        file_storage.clear()

# Register cleanup on exit
atexit.register(cleanup_all_files)

# HTML template for the web interface
HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToGraph - Interactive Knowledge Graph Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .upload-section {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 10px;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f1f5;
        }
        
        .upload-area.dragover {
            border-color: #764ba2;
            background: #e8e9f0;
        }
        
        .upload-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 1.2em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .upload-hint {
            color: #666;
            font-size: 0.9em;
        }
        
        .file-input {
            display: none;
        }
        
        .options {
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .option-group {
            display: flex;
            flex-direction: column;
        }
        
        .option-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        
        .option-group select,
        .option-group input {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }
        
        .option-group select:focus,
        .option-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 25px;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-top: 20px;
            width: 100%;
            font-weight: 600;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .result-section {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: none;
        }
        
        .result-section.visible {
            display: block;
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }
        
        .result-title {
            font-size: 1.5em;
            color: #333;
        }
        
        .download-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
        }
        
        .download-btn:hover {
            background: #218838;
        }
        
        .graph-container {
            width: 100%;
            height: 700px;
            border: 1px solid #ddd;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 1.2em;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            display: none;
        }
        
        .error-message.visible {
            display: block;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 ToGraph</h1>
            <p>Transform documents into beautiful interactive knowledge graphs</p>
        </div>
        
        <div class="upload-section">
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📄</div>
                    <div class="upload-text">Click to upload or drag and drop</div>
                    <div class="upload-hint">PDF or Markdown files (max 16MB)</div>
                    <input type="file" id="fileInput" name="file" class="file-input" accept=".pdf,.md,.markdown">
                </div>
                
                <div class="options">
                    <div class="option-group">
                        <label for="theme">Theme:</label>
                        <select id="theme" name="theme">
                            <option value="light">Light</option>
                            <option value="dark">Dark</option>
                        </select>
                    </div>
                    
                    <div class="option-group">
                        <label for="title">Graph Title:</label>
                        <input type="text" id="title" name="title" value="Knowledge Graph" placeholder="Enter graph title">
                    </div>
                </div>
                
                <button type="submit" class="button" id="generateBtn">Generate Knowledge Graph</button>
            </form>
            
            <div class="error-message" id="errorMessage"></div>
        </div>
        
        <div class="result-section" id="resultSection">
            <div class="result-header">
                <div class="result-title">📊 Your Knowledge Graph</div>
                <button class="download-btn" id="downloadBtn">Download HTML</button>
            </div>
            
            <div class="stats" id="stats"></div>
            
            <div class="graph-container">
                <iframe id="graphFrame" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
        </div>
        
        <div class="loading" id="loading" style="display: none;">
            <div class="spinner"></div>
            <p>Processing your document...</p>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadForm = document.getElementById('uploadForm');
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const resultSection = document.getElementById('resultSection');
        const errorMessage = document.getElementById('errorMessage');
        const graphFrame = document.getElementById('graphFrame');
        const downloadBtn = document.getElementById('downloadBtn');
        const statsDiv = document.getElementById('stats');
        
        let currentFileId = null;
        
        // Upload area interactions
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateUploadArea(files[0].name);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                updateUploadArea(e.target.files[0].name);
            }
        });
        
        function updateUploadArea(filename) {
            uploadArea.querySelector('.upload-text').textContent = filename;
            uploadArea.querySelector('.upload-hint').textContent = 'File selected - ready to generate!';
        }
        
        // Form submission
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!fileInput.files.length) {
                showError('Please select a file first!');
                return;
            }
            
            const formData = new FormData(uploadForm);
            
            // Show loading, hide results and errors
            loading.style.display = 'block';
            resultSection.classList.remove('visible');
            errorMessage.classList.remove('visible');
            generateBtn.disabled = true;
            
            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentFileId = data.file_id;
                    showResult(data);
                } else {
                    showError(data.error || 'An error occurred during conversion');
                }
            } catch (error) {
                showError('Failed to connect to server: ' + error.message);
            } finally {
                loading.style.display = 'none';
                generateBtn.disabled = false;
            }
        });
        
        function showResult(data) {
            // Update stats
            statsDiv.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${data.stats.nodes}</div>
                    <div class="stat-label">Nodes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${data.stats.edges}</div>
                    <div class="stat-label">Edges</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${data.stats.sections}</div>
                    <div class="stat-label">Sections</div>
                </div>
            `;
            
            // Load graph in iframe
            graphFrame.src = '/view/' + data.file_id;
            
            // Show result section
            resultSection.classList.add('visible');
            
            // Scroll to results
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.add('visible');
        }
        
        // Download button
        downloadBtn.addEventListener('click', () => {
            if (currentFileId) {
                window.location.href = '/download/' + currentFileId;
            }
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """Main page with upload form."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/convert', methods=['POST'])
def convert():
    """Convert uploaded file to knowledge graph."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get parameters
        theme = request.form.get('theme', 'light')
        title = request.form.get('title', 'Knowledge Graph')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_ext = Path(filename).suffix.lower()
        
        if file_ext not in ['.pdf', '.md', '.markdown']:
            return jsonify({'error': 'Invalid file format. Please upload PDF or Markdown files.'}), 400
        
        # Create temporary directory for this conversion
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        
        # Parse document
        if file_ext == '.pdf':
            parser_obj = PDFParser(input_path)
            nodes = parser_obj.parse()
            raw_content = '\n'.join([tc['text'] for tc in parser_obj.get_text_content()])
        else:
            parser_obj = MarkdownParser(input_path)
            nodes = parser_obj.parse()
            raw_content = parser_obj.get_raw_content()
        
        # Build graph
        builder = GraphBuilder(nodes, raw_content)
        graph = builder.build()
        entity_content = builder.get_entity_content()
        
        # Generate HTML
        visualizer = GraphVisualizer(graph, entity_content)
        output_filename = f"graph_{os.path.basename(filename).rsplit('.', 1)[0]}.html"
        output_path = os.path.join(temp_dir, output_filename)
        visualizer.save_html(output_path, theme=theme, title=title)
        
        # Clean up expired files before adding new one
        cleanup_expired_files()
        
        # Generate unique ID for this file and store with timestamp
        file_id = str(uuid.uuid4())
        with storage_lock:
            file_storage[file_id] = (output_path, temp_dir, time.time())
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'stats': {
                'nodes': graph.number_of_nodes(),
                'edges': graph.number_of_edges(),
                'sections': len(nodes)
            }
        })
        
    except Exception as e:
        # Log the error internally but don't expose stack trace
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during file conversion. Please try again.'}), 500


@app.route('/view/<file_id>')
def view_graph(file_id):
    """Serve the generated HTML file."""
    try:
        with storage_lock:
            if file_id not in file_storage:
                return "File not found or expired", 404
            
            filepath, temp_dir, timestamp = file_storage[file_id]
        
        if not os.path.exists(filepath):
            return "File not found", 404
            
        return send_file(filepath, mimetype='text/html')
    except Exception as e:
        # Log error but don't expose details to user
        print(f"Error viewing graph {file_id}: {e}")
        return "Error loading graph", 500


@app.route('/download/<file_id>')
def download_graph(file_id):
    """Download the generated HTML file."""
    try:
        with storage_lock:
            if file_id not in file_storage:
                return "File not found or expired", 404
            
            filepath, temp_dir, timestamp = file_storage[file_id]
        
        if not os.path.exists(filepath):
            return "File not found", 404
            
        return send_file(filepath, as_attachment=True, download_name='knowledge_graph.html')
    except Exception as e:
        # Log error but don't expose details to user
        print(f"Error downloading file {file_id}: {e}")
        return "Error downloading file", 500


def main(host='127.0.0.1', port=5000, debug=False):
    """Run the web application.
    
    Args:
        host: Host to bind to. Defaults to 127.0.0.1 (localhost only).
              Use 0.0.0.0 to expose on all network interfaces.
        port: Port to listen on. Defaults to 5000.
        debug: Enable Flask debug mode. Defaults to False.
    """
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                    ToGraph Web Server                    ║
╚══════════════════════════════════════════════════════════╝

🌐 Server running at: http://{host}:{port}
📊 Upload your PDF or Markdown files to generate knowledge graphs
🎨 Choose themes and customize your graphs
💾 Download generated HTML files

Press Ctrl+C to stop the server
""")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
