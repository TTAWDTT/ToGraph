# Quick Start Guide

Get started with ToGraph in 5 minutes!

## Installation (One Command)

```bash
# Clone, install dependencies, and install package
git clone https://github.com/TTAWDTT/ToGraph.git && cd ToGraph && pip install -r requirements.txt && pip install -e .
```

## Basic Usage

### 1. Convert Markdown to Interactive HTML

```bash
tograph examples/sample.md -o output.html
```

Open `output.html` in your browser to see an interactive knowledge graph!

### 2. Use Dark Theme

```bash
tograph examples/sample.md -o output_dark.html -t dark
```

Perfect for night work or presentations.

### 3. Generate High-Resolution Image

```bash
tograph examples/sample.md -o graph.png -f png --dpi 300
```

Great for papers, presentations, or printing.

### 4. Create All Formats at Once

```bash
tograph examples/sample.md -o output.html -f html png pdf
```

Generates:
- `output.html` - Interactive web version
- `output.png` - High-resolution image
- `output.pdf` - Printable PDF

### 5. Convert PDF Document

```bash
tograph examples/sample_paper.pdf -o paper_graph.html --title "My Research Paper"
```

## Interactive Features (HTML)

When you open the HTML file in a browser:

1. **Pan**: Click and drag to move around
2. **Zoom**: Scroll with mouse wheel
3. **Hover**: Move mouse over nodes to see content
4. **Click**: Click nodes for detailed information
5. **Controls**: Use buttons at top to control the graph

## Common Patterns

### Research Paper Analysis
```bash
# Convert your paper to an interactive graph
tograph my_paper.pdf -o analysis.html -t light --title "Research Analysis"
```

### Documentation Visualization
```bash
# Visualize project documentation
tograph README.md -o docs_graph.html -t dark
```

### Presentation Material
```bash
# Create high-quality images for slides
tograph outline.md -o presentation.png -f png --dpi 300 -t light
```

### Study Notes
```bash
# Convert study notes to visual format
tograph notes.md -o study_graph.html -t dark
```

## Tips

### Tip 1: Document Structure
For best results, structure your documents with clear headings:

**Markdown:**
```markdown
# Main Topic
## Subtopic 1
### Detail 1
## Subtopic 2
```

**PDF:**
Use numbered sections:
```
1. Introduction
1.1 Background
2. Methods
2.1 Data Collection
```

### Tip 2: Content Length
- Works best with documents that have 5-50 sections
- Very large documents may produce complex graphs
- Consider breaking very large documents into parts

### Tip 3: Theme Selection
- **Light theme**: Better for printing and daytime viewing
- **Dark theme**: Easier on eyes, better for presentations

### Tip 4: Output Format Selection
- **HTML**: Best for exploration and sharing (interactive)
- **PNG**: Best for presentations and papers (static)
- **PDF**: Best for printing and archiving

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [INSTALL.md](INSTALL.md) if you encounter installation issues
- Try your own documents!

## Help

```bash
# Show all options
tograph --help

# Get version
python3 -c "import tograph; print(tograph.__version__)"
```

## Examples

The `examples/` directory contains:
- `sample.md` - A markdown document about machine learning
- `sample_paper.pdf` - A sample research paper about neural networks
- `create_sample_pdf.py` - Script to regenerate the sample PDF

Try them all:
```bash
# Markdown example
tograph examples/sample.md -o ml_graph.html -t light

# PDF example  
tograph examples/sample_paper.pdf -o nn_graph.html -t dark
```

Enjoy visualizing your knowledge! 🚀
