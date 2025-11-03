"""Visualize knowledge graphs with multiple output formats."""

import json
import re
import tempfile
from pathlib import Path
from typing import Dict
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw, ImageFont
from jinja2 import Template
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class GraphVisualizer:
    """Visualize knowledge graphs in multiple formats."""
    
    # Color schemes
    THEMES = {
        'light': {
            'background': '#ffffff',
            'node': '#4A90E2',
            'node_border': '#2E5C8A',
            'text': '#333333',
            'edge': '#999999',
            'highlight': '#E74C3C',
            'accent': '#F39C12',
        },
        'dark': {
            'background': '#1a1a1a',
            'node': '#3A7BC8',
            'node_border': '#5DADE2',
            'text': '#E0E0E0',
            'edge': '#666666',
            'highlight': '#E74C3C',
            'accent': '#F39C12',
        }
    }
    
    def __init__(self, graph: nx.DiGraph, entity_content: Dict[str, str] = None):
        self.graph = graph
        self.entity_content = entity_content or {}
        
    def save_html(self, output_path: str, theme: str = 'light', title: str = "Knowledge Graph"):
        """Save graph as interactive HTML with hover functionality."""
        output_path = Path(output_path)
        colors = self.THEMES[theme]
        
        # Create pyvis network
        net = Network(
            height="800px",
            width="100%",
            bgcolor=colors['background'],
            font_color=colors['text'],
            directed=True
        )
        
        # Configure physics
        net.set_options("""
        {
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.3,
                    "springLength": 150,
                    "springConstant": 0.04,
                    "damping": 0.09,
                    "avoidOverlap": 0.1
                },
                "stabilization": {
                    "enabled": true,
                    "iterations": 200
                }
            },
            "nodes": {
                "font": {
                    "size": 14,
                    "face": "arial"
                }
            },
            "edges": {
                "color": {
                    "inherit": false
                },
                "smooth": {
                    "enabled": true,
                    "type": "continuous"
                }
            }
        }
        """)
        
        # Add nodes
        for node_id, attrs in self.graph.nodes(data=True):
            label = attrs.get('label', node_id)
            level = attrs.get('level', 1)
            content = self.entity_content.get(node_id, attrs.get('content', ''))
            
            # Size based on level
            size = 30 - (level * 3)
            size = max(size, 15)
            
            # Color based on level
            if level == 1:
                color = colors['node']
            elif level == 2:
                color = colors['accent']
            else:
                color = colors['highlight']
            
            # Truncate content for hover
            hover_content = content[:300] if content else "No content"
            if len(content) > 300:
                hover_content += "..."
            
            net.add_node(
                node_id,
                label=label,
                title=hover_content,  # Hover text
                color=color,
                size=size,
                borderWidth=2,
                borderWidthSelected=4,
            )
        
        # Add edges
        for source, target, attrs in self.graph.edges(data=True):
            relation = attrs.get('relation', 'related')
            
            if relation == 'contains':
                color = colors['edge']
                width = 2
                dashes = False
            else:
                color = colors['edge']
                width = 1
                dashes = True
            
            net.add_edge(
                source,
                target,
                title=relation,
                color=color,
                width=width,
                dashes=dashes
            )
        
        # Generate HTML
        html_template = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    
    <!-- Vis Network CDN with fallbacks -->
    <link rel="stylesheet" href="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.css" />
    <script src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
    
    <!-- Fallback CDN if unpkg fails -->
    <script>
        if (typeof vis === 'undefined') {
            document.write('<script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"><\/script>');
        }
    </script>
    
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: {{ bg_color }};
            color: {{ text_color }};
        }
        .header {
            padding: 20px;
            text-align: center;
            background-color: {{ header_bg }};
            border-bottom: 2px solid {{ border_color }};
        }
        h1 {
            margin: 0;
            color: {{ text_color }};
        }
        .controls {
            padding: 10px 20px;
            background-color: {{ control_bg }};
            border-bottom: 1px solid {{ border_color }};
        }
        .button {
            padding: 8px 16px;
            margin-right: 10px;
            background-color: {{ button_bg }};
            color: {{ button_text }};
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .button:hover {
            opacity: 0.8;
        }
        #mynetwork {
            width: 100%;
            height: 800px;
            border: none;
        }
        .info-panel {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: {{ panel_bg }};
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            max-width: 300px;
            display: none;
        }
        .info-panel.visible {
            display: block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
    </div>
    <div class="controls">
        <button class="button" onclick="network.fit()">Fit to Screen</button>
        <button class="button" onclick="togglePhysics()">Toggle Physics</button>
        <button class="button" onclick="exportImage()">Export as Image</button>
    </div>
    {{ network_html }}
    <div id="info-panel" class="info-panel">
        <h3 id="info-title">Node Information</h3>
        <p id="info-content">Click on a node to see details</p>
    </div>
    
    <script type="text/javascript">
        var physicsEnabled = true;
        
        function togglePhysics() {
            physicsEnabled = !physicsEnabled;
            network.setOptions({physics: {enabled: physicsEnabled}});
        }
        
        function exportImage() {
            alert('Use browser screenshot or print to PDF functionality to save the graph');
        }
        
        // Add click event for nodes
        network.on("click", function(params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                var node = network.body.data.nodes.get(nodeId);
                var panel = document.getElementById('info-panel');
                var title = document.getElementById('info-title');
                var content = document.getElementById('info-content');
                
                title.textContent = node.label || nodeId;
                content.textContent = node.title || 'No additional information';
                panel.classList.add('visible');
            } else {
                document.getElementById('info-panel').classList.remove('visible');
            }
        });
        
        // Close info panel when clicking outside
        network.on("click", function(params) {
            if (params.nodes.length === 0) {
                document.getElementById('info-panel').classList.remove('visible');
            }
        });
    </script>
</body>
</html>
        """
        
        # Generate network HTML
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_file:
            temp_html_path = tmp_file.name
        
        net.save_graph(temp_html_path)
        with open(temp_html_path, 'r') as f:
            pyvis_html = f.read()
        
        # Clean up temp file
        Path(temp_html_path).unlink()
        
        # Extract the network div and scripts
        match = re.search(r'(<div id="mynetwork".*?</div>.*?<script type="text/javascript">.*?</script>)', 
                         pyvis_html, re.DOTALL)
        if match:
            network_html = match.group(1)
        else:
            network_html = pyvis_html
        
        # Render final template
        template = Template(html_template)
        final_html = template.render(
            title=title,
            bg_color=colors['background'],
            text_color=colors['text'],
            header_bg=colors['background'],
            control_bg=colors['background'],
            panel_bg=colors['background'],
            border_color=colors['edge'],
            button_bg=colors['node'],
            button_text='#ffffff',
            network_html=network_html
        )
        
        # Save final HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"HTML saved to: {output_path}")
    
    def save_png(self, output_path: str, theme: str = 'light', dpi: int = 300):
        """Save graph as PNG image."""
        output_path = Path(output_path)
        colors = self.THEMES[theme]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor(colors['background'])
        ax.set_facecolor(colors['background'])
        
        # Layout
        if len(self.graph.nodes()) > 0:
            pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)
        else:
            pos = {}
        
        # Draw edges first
        for source, target, attrs in self.graph.edges(data=True):
            relation = attrs.get('relation', 'related')
            
            if relation == 'contains':
                style = 'solid'
                width = 2
                alpha = 0.6
            else:
                style = 'dashed'
                width = 1
                alpha = 0.3
            
            nx.draw_networkx_edges(
                self.graph,
                pos,
                [(source, target)],
                edge_color=colors['edge'],
                style=style,
                width=width,
                alpha=alpha,
                arrows=True,
                arrowsize=15,
                ax=ax,
                connectionstyle="arc3,rad=0.1"
            )
        
        # Draw nodes
        for node_id, attrs in self.graph.nodes(data=True):
            level = attrs.get('level', 1)
            
            if level == 1:
                node_color = colors['node']
                node_size = 3000
            elif level == 2:
                node_color = colors['accent']
                node_size = 2000
            else:
                node_color = colors['highlight']
                node_size = 1500
            
            nx.draw_networkx_nodes(
                self.graph,
                pos,
                [node_id],
                node_color=node_color,
                node_size=node_size,
                edgecolors=colors['node_border'],
                linewidths=2,
                ax=ax
            )
        
        # Draw labels
        labels = {node_id: attrs.get('label', node_id) 
                 for node_id, attrs in self.graph.nodes(data=True)}
        
        nx.draw_networkx_labels(
            self.graph,
            pos,
            labels,
            font_size=10,
            font_color=colors['text'],
            font_weight='bold',
            ax=ax
        )
        
        # Add legend
        legend_elements = [
            mpatches.Patch(color=colors['node'], label='Level 1 (Main Sections)'),
            mpatches.Patch(color=colors['accent'], label='Level 2 (Subsections)'),
            mpatches.Patch(color=colors['highlight'], label='Level 3+ (Details)'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', 
                 facecolor=colors['background'], edgecolor=colors['edge'],
                 labelcolor=colors['text'])
        
        ax.axis('off')
        plt.tight_layout()
        
        # Save
        plt.savefig(output_path, dpi=dpi, facecolor=colors['background'], 
                   bbox_inches='tight')
        plt.close()
        
        print(f"PNG saved to: {output_path}")
    
    def save_pdf(self, output_path: str, theme: str = 'light'):
        """Save graph as PDF."""
        output_path = Path(output_path)
        
        # First create PNG at high resolution
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            temp_png = tmp_file.name
        
        self.save_png(temp_png, theme=theme, dpi=300)
        
        # Create PDF
        c = canvas.Canvas(str(output_path), pagesize=landscape(A4))
        
        # Add title
        colors = self.THEMES[theme]
        c.setFillColor(colors['text'])
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 550, "Knowledge Graph")
        
        # Add image
        img = ImageReader(temp_png)
        c.drawImage(img, 50, 50, width=700, height=450, preserveAspectRatio=True)
        
        c.save()
        
        # Clean up temp file
        Path(temp_png).unlink()
        
        print(f"PDF saved to: {output_path}")
