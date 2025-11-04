# ToGraph

Convert PDF and Markdown documents to beautiful, interactive knowledge graphs with day and night themes.

## ✨ New: Django Framework with Enhanced UI & 3D Visualization

ToGraph now includes a **Django-based web application** with stunning visualizations and multiple viewing modes!

- 🎨 **Gorgeous Deep Blue Theme**: Modern, elegant interface with gradient effects
- ✨ **Animated UI**: Particle backgrounds and smooth transitions
- 🌐 **Full 3D Visualization**: Interactive 3D knowledge graphs powered by Three.js
- 🧠 **Mind Map Mode**: Generate intuitive, radial mind maps from your documents
- 🎮 **Enhanced Interactions**: Search, filter, auto-rotate, and smooth camera controls
- 🚀 **Enhanced PDF Parsing**: Better section detection and content extraction
- 📊 **Optimized Layout**: Improved graph physics and visual depth
- 🌍 **Chinese Interface**: Fully localized for Chinese users

👉 See [DJANGO_GUIDE.md](DJANGO_GUIDE.md) for Django version documentation

## Features

### Visualization Modes
- 🌐 **2D Knowledge Graphs**: Traditional force-directed network visualization
- 🎯 **3D Knowledge Graphs**: Fully interactive 3D visualization with Three.js
- 🧠 **2D Mind Maps**: Hierarchical radial layout for clear structure
- 🌟 **3D Mind Maps**: Spatial mind mapping with depth and perspective

### Core Features
- 🌐 **Dual Web Frameworks**: Choose between Flask (simple) or Django (full-featured)
- 📄 **Multiple Input Formats**: Support for PDF and Markdown files
- 🎨 **Beautiful Visualizations**: Clean, professional-looking graphs with multiple modes
- 🌓 **Day/Night Themes**: Switch between light and dark color schemes
- 📊 **Multiple Output Formats**: HTML (interactive), PNG (high-resolution), and PDF
- 🖱️ **Interactive HTML**: Mouse hover to display original text content
- 🔗 **Smart Relationships**: Automatically detects hierarchical and related connections
- 🚀 **Pure Code Implementation**: No AI dependencies, fast and reliable
- ✅ **Standalone HTML Files**: Generated files work independently with embedded CDN links

### 3D Visualization Controls
- 🎮 **Orbit Controls**: Left-click drag to rotate, right-click to pan, scroll to zoom
- 🔍 **Search & Filter**: Real-time node search with highlighting
- 🔄 **Auto-Rotate**: Optional automatic rotation for presentations
- 🎯 **Focus Mode**: Double-click nodes to smoothly focus camera
- 📐 **Smart Fitting**: Auto-fit all nodes in view
- 🏷️ **Toggle Labels**: Show/hide node labels for cleaner views
- ⚡ **Animation Speed Control**: Adjust rotation and animation speeds

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/TTAWDTT/ToGraph.git
cd ToGraph

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Alternative: Install from source

```bash
# Install directly from the repository
pip install git+https://github.com/TTAWDTT/ToGraph.git
```

## Usage

### Django Web Interface (New & Recommended)

Start the enhanced Django server with deep blue theme:

```bash
# Quick start
./run_django.sh

# Or manually
python manage.py runserver
```

Then open your browser to `http://localhost:8000` and:
1. Upload your PDF or Markdown file (drag & drop supported)
2. Choose theme (dark theme with deep blue recommended)
3. Select visualization type (2D or 3D)
4. Choose display mode (Knowledge Graph or Mind Map)
5. Click "生成知识图谱" (Generate Knowledge Graph)
6. Interact with the 3D visualization using mouse controls
7. Download the HTML file for offline use

**3D Visualization Tips:**
- Use left-click + drag to rotate the view
- Right-click + drag to pan the camera
- Scroll to zoom in/out
- Double-click a node to focus on it
- Use the search box to find specific nodes
- Toggle auto-rotate for presentations

See [DJANGO_GUIDE.md](DJANGO_GUIDE.md) for detailed Django documentation.

### Flask Web Interface (Classic)

The original Flask interface is still available:

```bash
# Start the web server
tograph-web

# Or specify custom host/port
tograph-web --host 0.0.0.0 --port 8080
```

Then open your browser to `http://localhost:5000` and:
1. Upload your PDF or Markdown file (drag & drop supported)
2. Choose theme (light/dark) and customize the title
3. Click "Generate Knowledge Graph"
4. View the interactive graph directly in your browser
5. Download the HTML file for offline use

### Command-Line Interface

```bash
# Convert PDF to interactive HTML with light theme
tograph input.pdf -o output.html

# Convert Markdown to HTML with dark theme
tograph document.md -o output.html -t dark

# Convert PDF to PNG image
tograph paper.pdf -o graph.png -f png

# Convert to multiple formats at once
tograph document.md -o graph.html -f html png pdf
```

### Command-Line Options

```
positional arguments:
  input                 Input file (PDF or Markdown)

optional arguments:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output file path (required)
  -f, --formats [html|png|pdf ...]
                        Output formats (default: html)
  -t, --theme [light|dark]
                        Color theme (default: light)
  --title TITLE         Title for the graph (default: Knowledge Graph)
  --dpi DPI             DPI for PNG output (default: 300)
```

### Examples

#### Example 1: Convert Research Paper to Interactive Graph

```bash
tograph research_paper.pdf -o paper_graph.html -t light --title "Research Paper Analysis"
```

This creates an interactive HTML file where you can:
- Pan and zoom the graph
- Hover over nodes to see content
- Click nodes for detailed information
- Toggle physics simulation

#### Example 2: Generate High-Resolution PNG

```bash
tograph document.md -o visualization.png -f png --dpi 300 -t dark
```

Creates a 300 DPI PNG image with dark theme, suitable for presentations or publications.

#### Example 3: Export All Formats

```bash
tograph paper.pdf -o output.html -f html png pdf -t light
```

Generates three files:
- `output.html` - Interactive web version
- `output.png` - High-resolution image
- `output.pdf` - Printable PDF version

## How It Works

1. **Document Parsing**: Extracts structure and content from PDF or Markdown files
2. **Graph Construction**: Identifies sections, subsections, and relationships between concepts
3. **Visualization**: Creates beautiful, themed visualizations with multiple output options

### Supported Document Structures

- **Markdown**: Headers (#, ##, ###, etc.)
- **PDF**: Numbered sections (1. Introduction, 1.1 Background, etc.) and title patterns

## Interactive Features (HTML Output)

When you open the HTML output in a browser, you can:

- **Pan**: Click and drag to move the graph
- **Zoom**: Use mouse wheel to zoom in/out
- **Hover**: Move mouse over nodes to see content preview
- **Click**: Click nodes to see full details in the info panel
- **Controls**: Use buttons to fit the graph or toggle physics

## Themes

### Light Theme
- Clean white background
- Blue nodes with dark borders
- Optimized for daytime viewing and printing

### Dark Theme
- Dark background for reduced eye strain
- Lighter colored nodes
- Perfect for night work or presentations

## Project Structure

```
ToGraph/
├── tograph/           # Main package
│   ├── __init__.py    # Package initialization
│   ├── parser.py      # PDF and Markdown parsers
│   ├── graph_builder.py  # Graph construction logic
│   ├── visualizer.py  # Visualization engine
│   └── main.py        # CLI interface
├── examples/          # Example documents
├── requirements.txt   # Python dependencies
├── setup.py          # Package setup
└── README.md         # This file
```

## Troubleshooting

### Issue: "Module not found" errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: PDF parsing errors

Some PDFs with complex formatting may not parse correctly. Try:
- Using a simpler PDF layout
- Converting the PDF to Markdown first

### Issue: Graph is too cluttered

For large documents, the graph may be complex. Try:
- Using PNG output with higher DPI for better clarity
- Filtering or preprocessing the document to focus on key sections

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for any purpose.

## Acknowledgments

Built with:
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF parsing
- [NetworkX](https://networkx.org/) for graph processing
- [PyVis](https://pyvis.readthedocs.io/) for interactive visualizations
- [Matplotlib](https://matplotlib.org/) for static visualizations