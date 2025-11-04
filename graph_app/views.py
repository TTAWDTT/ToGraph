import os
import tempfile
import shutil
import uuid
import time
import logging
from pathlib import Path
from threading import Lock
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from tograph.parser import PDFParser, MarkdownParser
from tograph.graph_builder import GraphBuilder
from tograph.visualizer import GraphVisualizer

# Configure logging
logger = logging.getLogger(__name__)

# Store mapping of file IDs to (path, temp_dir, timestamp)
# Files expire after 1 hour
# NOTE: This in-memory storage is suitable for single-process development servers.
# For production with multiple workers, consider using Django's cache framework
# with Redis/Memcached, or storing file references in the database.
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
                    logger.warning(f"Failed to clean up {temp_dir}: {e}")
        
        # Remove expired entries
        for file_id in expired_ids:
            del file_storage[file_id]
    
    return len(expired_ids)


def index(request):
    """Main page with upload form."""
    return render(request, 'index.html')


@csrf_exempt
def convert(request):
    """Convert uploaded file to knowledge graph."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        file = request.FILES['file']
        if not file.name:
            return JsonResponse({'error': 'No file selected'}, status=400)
        
        # Get parameters
        theme = request.POST.get('theme', 'light')
        title = request.POST.get('title', 'Knowledge Graph')
        
        # Check file extension
        filename = file.name
        file_ext = Path(filename).suffix.lower()
        
        if file_ext not in ['.pdf', '.md', '.markdown']:
            return JsonResponse({'error': 'Invalid file format. Please upload PDF or Markdown files.'}, status=400)
        
        # Create temporary directory for this conversion
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        
        # Save uploaded file
        with open(input_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
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
        
        return JsonResponse({
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
        logger.exception(f"Error during conversion: {e}")
        return JsonResponse({'error': 'An error occurred during file conversion. Please try again.'}, status=500)


def view_graph(request, file_id):
    """Serve the generated HTML file."""
    try:
        with storage_lock:
            if file_id not in file_storage:
                return HttpResponse("File not found or expired", status=404)
            
            filepath, temp_dir, timestamp = file_storage[file_id]
        
        if not os.path.exists(filepath):
            return HttpResponse("File not found", status=404)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HttpResponse(content, content_type='text/html')
    except Exception as e:
        logger.error(f"Error viewing graph {file_id}: {e}")
        return HttpResponse("Error loading graph", status=500)


def download_graph(request, file_id):
    """Download the generated HTML file."""
    try:
        with storage_lock:
            if file_id not in file_storage:
                return HttpResponse("File not found or expired", status=404)
            
            filepath, temp_dir, timestamp = file_storage[file_id]
        
        if not os.path.exists(filepath):
            return HttpResponse("File not found", status=404)
        
        response = FileResponse(open(filepath, 'rb'), content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="knowledge_graph.html"'
        return response
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {e}")
        return HttpResponse("Error downloading file", status=500)
