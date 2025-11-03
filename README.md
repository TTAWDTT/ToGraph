# ToGraph

Convert PDF and Markdown documents to beautiful, interactive knowledge graphs with day and night themes.

## Features

- 📄 **Multiple Input Formats**: Support for PDF and Markdown files
- 🎨 **Beautiful Visualizations**: Clean, professional-looking knowledge graphs
- 🌓 **Day/Night Themes**: Switch between light and dark color schemes
- 📊 **Multiple Output Formats**: HTML (interactive), PNG (high-resolution), and PDF
- 🖱️ **Interactive HTML**: Mouse hover to display original text content
- 🔗 **Smart Relationships**: Automatically detects hierarchical and related connections
- 🚀 **Pure Code Implementation**: No AI dependencies, fast and reliable

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

### Basic Usage

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