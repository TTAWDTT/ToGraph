# ToGraph Visualization Guide

This guide explains the different visualization modes and how to use them effectively.

## Overview

ToGraph offers four distinct visualization modes to help you understand your documents in different ways:

1. **2D Knowledge Graph** - Traditional network visualization
2. **3D Knowledge Graph** - Immersive spatial visualization  
3. **2D Mind Map** - Hierarchical radial layout
4. **3D Mind Map** - Spatial mind mapping with depth

## Visualization Modes

### 2D Knowledge Graph

**Best for:** General document exploration, printing, and presentations

The 2D Knowledge Graph uses a force-directed layout where:
- Nodes represent document sections and concepts
- Edges show relationships (containment and similarity)
- Node size indicates hierarchy level
- Colors distinguish different section levels

**Features:**
- Physics-based layout for natural organization
- Hover to see content previews
- Click nodes for detailed information
- Smooth zooming and panning
- Navigation controls

### 3D Knowledge Graph

**Best for:** Large documents, interactive exploration, immersive presentations

The 3D Knowledge Graph adds a spatial dimension:
- Nodes are positioned in 3D space
- Edges connect through 3D space
- Camera can orbit around the entire structure
- Lighting creates depth perception
- Smooth animations and transitions

**Controls:**
- **Left-click + drag**: Rotate camera around the graph
- **Right-click + drag**: Pan the camera
- **Scroll**: Zoom in/out
- **Double-click node**: Focus camera on specific node

**Interactive Features:**
- **Search Box**: Type to filter and highlight nodes
- **Auto-Rotate**: Continuous rotation for presentations
- **Speed Control**: Adjust animation speed (0.1x - 3.0x)
- **Reset View**: Return to default camera position
- **Fit to View**: Auto-frame all nodes
- **Toggle Labels**: Show/hide text labels

### 2D Mind Map

**Best for:** Understanding document structure, learning hierarchies

The 2D Mind Map uses a hierarchical radial layout:
- Root concept at the center
- Child concepts radiate outward
- Clear parent-child relationships
- Curved edges for visual flow

**Features:**
- Tree-based organization
- Level separation for clarity
- Ellipse nodes for softer appearance
- Curved connections between levels

### 3D Mind Map

**Best for:** Complex hierarchies, spatial understanding, presentations

The 3D Mind Map extends the radial layout into 3D space:
- Central concept with 3D branches
- Z-axis adds depth variation
- Spatial arrangement prevents overlap
- Dynamic lighting enhances depth

**Use Cases:**
- Presenting complex document structures
- Understanding multi-level hierarchies
- Creating engaging visualizations
- Export for interactive displays

## Choosing the Right Mode

### Document Type

- **Research Papers**: 3D Knowledge Graph (many interconnected concepts)
- **Textbooks**: 2D Mind Map (clear hierarchical structure)
- **Technical Docs**: 2D Knowledge Graph (easier to read and print)
- **Presentations**: 3D Mind Map (engaging and impressive)

### Use Case

- **Quick Overview**: 2D modes (faster to understand at a glance)
- **Deep Exploration**: 3D modes (discover hidden relationships)
- **Printing**: 2D modes (work better on paper)
- **Interactive Demo**: 3D modes (more engaging for audiences)

### Audience

- **Technical Readers**: Knowledge Graph modes (show relationships)
- **General Audience**: Mind Map modes (clearer structure)
- **Presentations**: 3D modes (more visually impressive)
- **Reports**: 2D modes (easier to include in documents)

## Tips for Best Results

### 2D Visualizations

1. **Use physics controls** to adjust node spacing
2. **Hover over nodes** to see content without clicking
3. **Zoom out first** to see the overall structure
4. **Click nodes** for detailed information panel

### 3D Visualizations

1. **Start with auto-rotate** to get familiar with the structure
2. **Use search** to quickly find specific topics
3. **Double-click** frequently visited nodes
4. **Adjust speed** based on content complexity
5. **Toggle labels** when structure is clear
6. **Reset view** if you get lost

### Mind Maps

1. **Identify the root** concept first
2. **Follow branches** systematically
3. **Use for planning** and brainstorming
4. **Export as image** for documentation

### Knowledge Graphs

1. **Look for clusters** of related concepts
2. **Trace paths** between topics
3. **Identify hub nodes** (highly connected)
4. **Use for research** and analysis

## Performance Tips

### For Large Documents (100+ nodes)

1. Use **2D modes** for better performance
2. **Disable physics** after initial layout
3. **Toggle labels** to improve rendering
4. **Filter nodes** using search

### For Complex Relationships

1. Use **3D modes** to reduce visual clutter
2. **Rotate view** to see different perspectives
3. **Focus on clusters** one at a time
4. **Use mind map** for simpler hierarchy view

## Exporting and Sharing

All visualizations are exported as standalone HTML files that:
- Work without internet connection (CDN fallbacks included)
- Can be opened in any modern browser
- Preserve all interactive features
- Include embedded styles and scripts

### Export Options

1. **Download HTML**: Full interactive version
2. **Screenshot**: Use browser tools (Ctrl+P or screenshot)
3. **PDF**: Print to PDF from browser
4. **PNG**: Use ToGraph CLI for static images

## Troubleshooting

### Nodes Overlap

- **2D**: Increase spring length in physics settings
- **3D**: Use fit-to-view or zoom out
- **Mind Map**: Check that hierarchy is detected correctly

### Performance Issues

- **Disable shadows** in browser console
- **Reduce node count** by filtering
- **Use 2D mode** instead of 3D
- **Close other browser tabs**

### Can't See Nodes

- **Click "Fit to View"** button
- **Reset camera** position
- **Check zoom level**
- **Try different browser**

## Keyboard Shortcuts

### 3D Mode

- **Arrow Keys**: Rotate view
- **+/-**: Zoom in/out
- **R**: Reset view
- **Space**: Toggle auto-rotate
- **L**: Toggle labels
- **F**: Fit to view

## Advanced Features

### Custom Styling

Edit the exported HTML file to customize:
- Colors and themes
- Node sizes and shapes
- Edge styles and widths
- Background and lighting

### API Integration

Use ToGraph programmatically:

```python
from tograph.visualizer import GraphVisualizer

# Create visualizer
viz = GraphVisualizer(graph, entity_content)

# Generate 3D mind map
viz.save_html('output.html', 
              theme='dark',
              visualization_mode='mindmap',
              use_3d=True)
```

## Examples

See the `examples/` directory for sample files and generated visualizations.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review example files

---

**Enjoy exploring your documents in new dimensions!** 🌐✨
