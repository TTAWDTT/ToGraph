# ToGraph Web Interface Guide

## Quick Start

### Starting the Web Server

```bash
# Default: runs on http://127.0.0.1:5000 (localhost only)
tograph-web

# Custom port
tograph-web --port 8080

# Expose to network (use with caution)
tograph-web --host 0.0.0.0 --port 5000
```

## Using the Web Interface

### Step 1: Upload Your Document

1. Open your browser and navigate to `http://localhost:5000`
2. Click the upload area or drag and drop your file
3. Supported formats: PDF (`.pdf`) and Markdown (`.md`, `.markdown`)
4. Maximum file size: 16MB

### Step 2: Customize Your Graph

- **Theme**: Choose between Light (default) or Dark theme
- **Graph Title**: Enter a custom title for your knowledge graph (default: "Knowledge Graph")

### Step 3: Generate

Click the "Generate Knowledge Graph" button. The server will:
1. Parse your document structure
2. Build the knowledge graph with relationships
3. Generate an interactive HTML visualization
4. Display statistics (nodes, edges, sections)

### Step 4: View and Download

- The graph appears directly in your browser
- Interactive features:
  - **Pan**: Click and drag to move the graph
  - **Zoom**: Use mouse wheel to zoom in/out
  - **Hover**: Move mouse over nodes to see content preview
  - **Click**: Click nodes to see full details
  - **Fit to Screen**: Click button to fit the entire graph
  - **Toggle Physics**: Enable/disable physics simulation
- Click "Download HTML" to save the standalone HTML file

## File Management

### Automatic Cleanup
- Generated files are automatically deleted after 1 hour
- Files are also cleaned up when you stop the server
- This prevents disk space issues from accumulating files

### Security Features
- Files are stored with random UUID identifiers
- No direct file path access
- Localhost-only binding by default
- Stack traces are not exposed to users

## Command-Line Interface

For batch processing or automation, use the CLI:

```bash
# Convert PDF to HTML
tograph input.pdf -o output.html

# Convert Markdown with dark theme
tograph document.md -o graph.html -t dark --title "My Graph"

# Convert to multiple formats
tograph paper.pdf -o output.html -f html png pdf

# Convert PDF to PNG image
tograph paper.pdf -o graph.png -f png --dpi 300
```

## Troubleshooting

### Web Server Won't Start

**Error**: "Address already in use"
- **Solution**: Port 5000 is already in use. Try a different port:
  ```bash
  tograph-web --port 8080
  ```

### File Upload Fails

**Error**: "File too large"
- **Solution**: Maximum file size is 16MB. Try reducing your document size or use the CLI.

**Error**: "Invalid file format"
- **Solution**: Only PDF and Markdown files are supported. Convert your document to one of these formats.

### Graph Doesn't Display

**Problem**: Graph area is blank
- **Solution**: This usually means your browser blocked the CDN resources. Try:
  1. Download the HTML file and open it in a different browser
  2. Check your browser's console for errors
  3. Disable browser extensions that might block CDN content

### File Not Found After Generation

**Problem**: "File not found or expired"
- **Solution**: Files expire after 1 hour. Generate a new graph or download immediately after generation.

## Tips and Best Practices

### For Best Results

1. **Document Structure**: Use clear headers and sections in your documents
   - Markdown: Use `#`, `##`, `###` for hierarchical structure
   - PDF: Use numbered sections like "1. Introduction", "1.1 Background"

2. **Document Size**: 
   - Optimal: Under 50 pages or 5000 lines
   - Large documents (>100 pages) may create complex graphs

3. **Theme Selection**:
   - Light theme: Better for printing and daytime viewing
   - Dark theme: Easier on eyes during night work

4. **Download Immediately**: 
   - Files expire after 1 hour
   - Download your graph if you need it later

### Performance Tips

- For large documents, PNG output may be better than interactive HTML
- Close unused browser tabs when generating large graphs
- Consider splitting very large documents into sections

## Examples

### Example 1: Research Paper

Upload `research_paper.pdf`, set:
- Theme: Light
- Title: "Research Paper Analysis"

Result: Hierarchical graph showing paper structure with sections, subsections, and relationships.

### Example 2: Documentation

Upload `documentation.md`, set:
- Theme: Dark
- Title: "API Documentation Map"

Result: Interactive graph perfect for navigating large documentation sets.

### Example 3: Meeting Notes

Upload `notes.md`, set:
- Theme: Light
- Title: "Meeting Notes - 2024-11-03"

Result: Visual representation of discussion topics and relationships.

## Security Considerations

### For Local Use (Default)

The default configuration (`127.0.0.1:5000`) is secure for local use:
- Only accessible from your computer
- No network exposure
- Safe for sensitive documents

### For Network Use

If you need to expose the server (`--host 0.0.0.0`):
- ⚠️ Use only on trusted networks
- ⚠️ Consider using a reverse proxy with HTTPS
- ⚠️ Implement authentication if needed
- ⚠️ Use a firewall to restrict access
- ⚠️ This is a development server, not for production

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/TTAWDTT/ToGraph
- Issues: https://github.com/TTAWDTT/ToGraph/issues

## License

MIT License - See LICENSE file for details
