# ToGraph Features

A comprehensive overview of all features in ToGraph.

## Core Capabilities

### 📄 Input Format Support

#### PDF Documents
- **Automatic Structure Detection**: Identifies sections using numbered patterns (1., 1.1, etc.)
- **Title Recognition**: Detects all-caps and title-case headers
- **Full Text Extraction**: Preserves document content for display
- **Multi-Page Support**: Handles documents of any length
- **Academic Paper Optimized**: Works well with research papers and technical documents

#### Markdown Documents
- **Standard Markdown**: Supports all standard markdown syntax
- **Header Hierarchy**: Respects # header levels (H1-H6)
- **Code Blocks**: Preserves code and formatting
- **Lists and Tables**: Handles structured content
- **Mixed Content**: Works with text, lists, code, and more

### 🎨 Visualization Themes

#### Light Theme (Default)
- Clean white background (#ffffff)
- Blue primary nodes (#4A90E2)
- Orange accent nodes (#F39C12)
- Red detail nodes (#E74C3C)
- High contrast for readability
- Perfect for printing and daytime viewing

#### Dark Theme
- Dark background (#1a1a1a)
- Lighter node colors for contrast
- Reduced eye strain for night work
- Modern, professional appearance
- Ideal for presentations and demos

### 📊 Output Formats

#### HTML (Interactive)
**Features:**
- Fully interactive web-based visualization
- Pan and zoom with mouse/trackpad
- Physics simulation for natural layout
- Control buttons (Fit to Screen, Toggle Physics)
- Info panel with detailed node information
- Works in all modern browsers
- No internet connection required after generation

**Interactive Elements:**
- **Hover**: Move mouse over nodes to see content preview (up to 300 characters)
- **Click**: Click nodes to see full content in info panel
- **Drag**: Move individual nodes or pan entire graph
- **Zoom**: Mouse wheel to zoom in/out
- **Physics**: Toggle physics simulation on/off

#### PNG (High-Resolution Image)
**Features:**
- Publication-quality output (300 DPI default)
- Customizable DPI (100-600)
- Large dimensions (4770x3570 pixels at 300 DPI)
- Color-coded by hierarchy level
- Legend showing node types
- Perfect for papers, presentations, posters
- RGBA with transparency support

#### PDF (Printable Document)
**Features:**
- Professional document format
- Includes title and metadata
- High-quality embedded images
- Landscape orientation for better fit
- Ready for printing or sharing
- Compatible with all PDF readers

### 🕸️ Graph Construction

#### Automatic Relationship Detection

**Hierarchical Relationships:**
- Parent-child connections from document structure
- Maintains document hierarchy (sections → subsections)
- Visual distinction with solid lines

**Content-Based Relationships:**
- Analyzes text to find related concepts
- Connects sections with shared terminology
- Visual distinction with dashed lines
- Shows shared terms as edge metadata

#### Smart Node Sizing
- **Level 1 (Main Sections)**: Largest nodes
- **Level 2 (Subsections)**: Medium nodes
- **Level 3+ (Details)**: Smaller nodes
- Visual hierarchy makes structure obvious

#### Intelligent Layout
- **Spring Layout Algorithm**: Natural, aesthetically pleasing
- **Collision Avoidance**: Nodes don't overlap
- **Edge Routing**: Smooth curves avoid node intersections
- **Stabilization**: Graph settles into optimal position

### 🖥️ Command-Line Interface

#### Simple and Intuitive
```bash
tograph input.md -o output.html
```

#### Full Control
```bash
tograph input.pdf -o graph.html -f html png pdf -t dark --title "My Graph" --dpi 600
```

#### Built-in Help
```bash
tograph --help
```

#### Features:
- Clear error messages
- Input validation
- Progress indicators
- Success confirmation
- File size reporting

### 🔍 Content Processing

#### Text Analysis
- **Key Term Extraction**: Identifies important concepts
- **Stopword Filtering**: Removes common words
- **Frequency Analysis**: Finds most significant terms
- **Relationship Mapping**: Connects related sections

#### Structure Preservation
- Maintains document hierarchy
- Preserves section order
- Keeps content associations
- Respects nesting levels

### 🚀 Performance

#### Fast Processing
- **Small documents** (<10 pages): < 5 seconds
- **Medium documents** (10-50 pages): < 15 seconds
- **Large documents** (50+ pages): < 30 seconds

#### Memory Efficient
- Streams large PDFs
- Processes incrementally
- Minimal memory footprint
- Handles documents of any size

### 🛡️ Reliability

#### Pure Code Implementation
- No AI or API dependencies
- Deterministic output
- Offline operation
- Fast and predictable

#### Error Handling
- Graceful failure modes
- Clear error messages
- Input validation
- Helpful troubleshooting hints

### 📦 Package Features

#### Easy Installation
```bash
pip install -r requirements.txt
pip install -e .
```

#### Virtual Environment Support
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Cross-Platform
- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (Intel and Apple Silicon)
- Windows (10, 11)

### 🧪 Testing & Validation

#### Automated Testing
- Installation verification script
- 14 comprehensive tests
- Functional testing
- Error handling validation

#### Example Suite
- Sample Markdown document
- Sample PDF generator
- Multiple output examples
- One-command example runner

### 📚 Documentation

#### Comprehensive Guides
- **README.md**: Complete overview
- **INSTALL.md**: Step-by-step installation
- **QUICKSTART.md**: 5-minute getting started
- **FEATURES.md**: This document

#### Code Examples
- Simple usage examples
- Advanced configurations
- Common patterns
- Troubleshooting scenarios

### 🔧 Extensibility

#### Modular Design
- **Parser Module**: Pluggable document parsers
- **Graph Builder**: Customizable relationship logic
- **Visualizer**: Multiple rendering backends
- **CLI**: Easy to extend with new options

#### Python API
```python
from tograph import PDFParser, GraphBuilder, GraphVisualizer

# Parse document
parser = PDFParser("document.pdf")
nodes = parser.parse()

# Build graph
builder = GraphBuilder(nodes)
graph = builder.build()

# Visualize
visualizer = GraphVisualizer(graph)
visualizer.save_html("output.html", theme="dark")
```

## Comparison with Alternatives

| Feature | ToGraph | Manual Mind Maps | AI Tools | Other Graph Tools |
|---------|---------|-----------------|----------|-------------------|
| Automatic | ✅ | ❌ | ✅ | ✅ |
| Offline | ✅ | ✅ | ❌ | Varies |
| Interactive | ✅ | ❌ | ✅ | Varies |
| Free | ✅ | Varies | ❌ | Varies |
| No AI Required | ✅ | ✅ | ❌ | ✅ |
| Multiple Outputs | ✅ | ❌ | ❌ | Varies |
| Themes | ✅ | Varies | ❌ | Varies |
| Open Source | ✅ | ❌ | ❌ | Varies |

## Use Cases

### Academic Research
- Visualize research papers
- Map literature reviews
- Present thesis structure
- Analyze paper relationships

### Documentation
- Project documentation overview
- API structure visualization
- Technical specification mapping
- Knowledge base organization

### Study & Learning
- Convert notes to visual format
- Create study guides
- Understand complex topics
- Memorization aid

### Content Creation
- Blog post structure
- Book chapter mapping
- Article organization
- Content planning

### Presentations
- Create visual aids
- Explain complex systems
- Show relationships
- Engage audiences

## Future Enhancements (Potential)

While the current version is complete and fully functional, potential future enhancements could include:

- Additional input formats (DOCX, HTML, LaTeX)
- More layout algorithms (hierarchical, circular, force-directed)
- Custom color schemes
- Graph filtering and search
- Export to more formats (SVG, GraphML)
- Batch processing
- Web interface
- Plugin system

## Contributing

ToGraph is open source and welcomes contributions! See the main README for contribution guidelines.

## License

MIT License - Use freely for any purpose.
