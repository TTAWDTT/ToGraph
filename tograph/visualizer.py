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
    
    # Color schemes with enhanced deep blue theme
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
            'background': '#0a1931',  # Deep blue background
            'node': '#185adb',  # Medium blue for nodes
            'node_border': '#00d9ff',  # Accent blue for borders
            'text': '#e8f4fd',  # Light blue text
            'edge': '#4a90e2',  # Light blue edges
            'highlight': '#00ff88',  # Green highlight
            'accent': '#00d9ff',  # Accent cyan
        }
    }
    
    def __init__(self, graph: nx.DiGraph, entity_content: Dict[str, str] = None):
        self.graph = graph
        self.entity_content = entity_content or {}
        
    def save_html_3d(self, output_path: str, theme: str = 'light', title: str = "Knowledge Graph 3D", visualization_mode: str = "graph"):
        """Save graph as interactive 3D HTML using Three.js with enhanced user experience.
        
        Args:
            output_path: Path to save the HTML file
            theme: Color theme ('light' or 'dark')
            title: Title for the visualization
            visualization_mode: 'graph' for knowledge graph or 'mindmap' for mind map layout
        """
        output_path = Path(output_path)
        colors = self.THEMES[theme]
        
        # Prepare graph data for Three.js
        nodes_data = []
        edges_data = []
        
        # Calculate node positions based on visualization mode
        if visualization_mode == "mindmap":
            pos = self._calculate_mindmap_layout()
        else:
            pos = nx.spring_layout(self.graph, dim=3, k=2, iterations=50, seed=42) if len(self.graph.nodes()) > 0 else {}
        
        # Add nodes with 3D positions
        for node_id, attrs in self.graph.nodes(data=True):
            label = attrs.get('label', node_id)
            level = attrs.get('level', 1)
            content = self.entity_content.get(node_id, attrs.get('content', ''))
            
            # Get position
            if node_id in pos:
                x, y, z = pos[node_id]
            else:
                x, y, z = 0, 0, 0
            
            # Scale positions for better visualization
            x, y, z = x * 300, y * 300, z * 300
            
            # Determine color and size based on level
            if level == 1:
                color = colors['node']
                size = 25
            elif level == 2:
                color = colors['accent']
                size = 20
            else:
                color = colors['highlight']
                size = 15
            
            # Truncate content for display
            hover_content = content[:300] if content else "No content"
            if len(content) > 300:
                hover_content += "..."
            
            nodes_data.append({
                'id': node_id,
                'label': label,
                'x': x,
                'y': y,
                'z': z,
                'color': color,
                'size': size,
                'content': hover_content,
                'level': level
            })
        
        # Add edges
        for source, target, attrs in self.graph.edges(data=True):
            relation = attrs.get('relation', 'related')
            
            edge_color = colors['edge']
            if relation == 'contains':
                width = 2
            else:
                width = 1
            
            edges_data.append({
                'source': source,
                'target': target,
                'color': edge_color,
                'width': width,
                'relation': relation
            })
        
        # Generate HTML with Three.js
        html_content = self._generate_3d_html_template(
            title=title,
            nodes=nodes_data,
            edges=edges_data,
            colors=colors,
            visualization_mode=visualization_mode
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"3D HTML saved to: {output_path}")
    
    def _calculate_mindmap_layout(self):
        """Calculate mind map layout with radial positioning."""
        pos = {}
        
        # Find root nodes (nodes with no incoming edges)
        root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
        if not root_nodes:
            # If no clear root, pick the first node
            root_nodes = [list(self.graph.nodes())[0]] if len(self.graph.nodes()) > 0 else []
        
        if not root_nodes:
            return pos
        
        # Place root at center
        root = root_nodes[0]
        pos[root] = (0, 0, 0)
        
        # BFS to place children in radial pattern
        visited = {root}
        queue = [(root, 0, 0)]  # (node, angle_start, radius)
        
        import math
        while queue:
            parent, angle_base, radius = queue.pop(0)
            
            # Get children
            children = [n for n in self.graph.successors(parent) if n not in visited]
            if not children:
                continue
            
            # Calculate positions for children
            num_children = len(children)
            angle_step = 2 * math.pi / max(num_children, 1)
            next_radius = radius + 1
            
            for i, child in enumerate(children):
                angle = angle_base + i * angle_step
                x = next_radius * math.cos(angle)
                y = next_radius * math.sin(angle)
                z = next_radius * 0.3  # Add some depth variation
                
                pos[child] = (x, y, z)
                visited.add(child)
                queue.append((child, angle, next_radius))
        
        return pos
    
    def _generate_3d_html_template(self, title, nodes, edges, colors, visualization_mode):
        """Generate HTML template with Three.js for 3D visualization."""
        nodes_json = json.dumps(nodes)
        edges_json = json.dumps(edges)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: {colors['background']};
            color: {colors['text']};
            overflow: hidden;
        }}
        
        #container {{
            width: 100vw;
            height: 100vh;
            position: relative;
        }}
        
        #info-panel {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(26, 49, 98, 0.9);
            padding: 20px;
            border-radius: 12px;
            border: 2px solid {colors['accent']};
            max-width: 350px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 100;
        }}
        
        #info-panel h2 {{
            margin: 0 0 10px 0;
            color: {colors['accent']};
            font-size: 1.4em;
        }}
        
        #info-content {{
            color: {colors['text']};
            line-height: 1.6;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(26, 49, 98, 0.9);
            padding: 20px;
            border-radius: 12px;
            border: 2px solid {colors['accent']};
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 100;
        }}
        
        .controls h3 {{
            margin: 0 0 15px 0;
            color: {colors['accent']};
            font-size: 1.2em;
        }}
        
        .control-group {{
            margin-bottom: 15px;
        }}
        
        .control-group label {{
            display: block;
            margin-bottom: 5px;
            color: {colors['text']};
            font-size: 0.9em;
        }}
        
        .button {{
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            background: linear-gradient(135deg, #185adb 0%, #00d9ff 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 217, 255, 0.4);
        }}
        
        .button:active {{
            transform: translateY(0);
        }}
        
        input[type="range"] {{
            width: 100%;
            margin: 5px 0;
        }}
        
        #search-box {{
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            background: rgba(10, 25, 49, 0.8);
            border: 2px solid {colors['accent']};
            border-radius: 8px;
            color: {colors['text']};
            font-size: 14px;
        }}
        
        #search-box:focus {{
            outline: none;
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.3);
        }}
        
        .stats {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(26, 49, 98, 0.9);
            padding: 15px 20px;
            border-radius: 8px;
            border: 2px solid {colors['accent']};
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 100;
            font-size: 0.9em;
        }}
        
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 1000;
        }}
        
        .spinner {{
            border: 4px solid rgba(74, 144, 226, 0.2);
            border-top: 4px solid {colors['accent']};
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        #mode-indicator {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(26, 49, 98, 0.9);
            padding: 10px 25px;
            border-radius: 20px;
            border: 2px solid {colors['accent']};
            backdrop-filter: blur(10px);
            font-weight: 600;
            color: {colors['accent']};
            z-index: 100;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <div style="color: {colors['text']}; font-size: 1.2em;">Loading 3D Visualization...</div>
    </div>
    
    <div id="mode-indicator">
        {"🧠 Mind Map Mode" if visualization_mode == "mindmap" else "🌐 Knowledge Graph Mode"}
    </div>
    
    <div id="info-panel">
        <h2 id="node-title">Welcome</h2>
        <div id="info-content">
            <p>Click on any node to view details.</p>
            <p style="margin-top: 10px; font-size: 0.9em; color: #a8c5da;">
                💡 Controls:<br>
                • Left click + drag: Rotate<br>
                • Right click + drag: Pan<br>
                • Scroll: Zoom<br>
                • Double-click node: Focus
            </p>
        </div>
    </div>
    
    <div class="controls">
        <h3>🎮 Controls</h3>
        
        <div class="control-group">
            <input type="text" id="search-box" placeholder="Search nodes...">
        </div>
        
        <div class="control-group">
            <label>Animation Speed: <span id="speed-value">1.0</span>x</label>
            <input type="range" id="speed-slider" min="0.1" max="3" step="0.1" value="1.0">
        </div>
        
        <button class="button" onclick="resetView()">🎯 Reset View</button>
        <button class="button" onclick="toggleRotation()">🔄 <span id="rotation-text">Start</span> Auto-Rotate</button>
        <button class="button" onclick="fitToView()">📐 Fit All Nodes</button>
        <button class="button" onclick="toggleLabels()">🏷️ Toggle Labels</button>
    </div>
    
    <div class="stats">
        <strong>📊 Statistics</strong><br>
        Nodes: <span id="node-count">0</span> | 
        Edges: <span id="edge-count">0</span>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        const nodesData = {nodes_json};
        const edgesData = {edges_json};
        
        let scene, camera, renderer, controls;
        let nodeObjects = {{}};
        let edgeObjects = [];
        let labelSprites = [];
        let selectedNode = null;
        let autoRotate = false;
        let showLabels = true;
        
        function init() {{
            // Scene setup
            scene = new THREE.Scene();
            scene.background = new THREE.Color("{colors['background']}");
            scene.fog = new THREE.Fog("{colors['background']}", 500, 2000);
            
            // Camera setup
            camera = new THREE.PerspectiveCamera(
                60,
                window.innerWidth / window.innerHeight,
                1,
                10000
            );
            camera.position.set(0, 0, 800);
            
            // Renderer setup
            renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            document.getElementById('container').appendChild(renderer.domElement);
            
            // Controls setup
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = false;
            controls.minDistance = 100;
            controls.maxDistance = 2000;
            controls.maxPolarAngle = Math.PI;
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            const pointLight1 = new THREE.PointLight(0x00d9ff, 0.8, 1000);
            pointLight1.position.set(200, 200, 200);
            scene.add(pointLight1);
            
            const pointLight2 = new THREE.PointLight(0x185adb, 0.6, 1000);
            pointLight2.position.set(-200, -200, -200);
            scene.add(pointLight2);
            
            // Create graph visualization
            createNodes();
            createEdges();
            
            // Update stats
            document.getElementById('node-count').textContent = nodesData.length;
            document.getElementById('edge-count').textContent = edgesData.length;
            
            // Event listeners
            window.addEventListener('resize', onWindowResize);
            renderer.domElement.addEventListener('click', onNodeClick);
            document.getElementById('search-box').addEventListener('input', onSearch);
            document.getElementById('speed-slider').addEventListener('input', onSpeedChange);
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
            
            // Start animation
            animate();
        }}
        
        function createNodes() {{
            nodesData.forEach(node => {{
                // Create sphere for node
                const geometry = new THREE.SphereGeometry(node.size, 32, 32);
                const material = new THREE.MeshPhongMaterial({{
                    color: node.color,
                    emissive: node.color,
                    emissiveIntensity: 0.2,
                    shininess: 100,
                    transparent: true,
                    opacity: 0.9
                }});
                
                const sphere = new THREE.Mesh(geometry, material);
                sphere.position.set(node.x, node.y, node.z);
                sphere.userData = node;
                scene.add(sphere);
                
                nodeObjects[node.id] = sphere;
                
                // Add glow effect
                const glowGeometry = new THREE.SphereGeometry(node.size * 1.2, 32, 32);
                const glowMaterial = new THREE.MeshBasicMaterial({{
                    color: node.color,
                    transparent: true,
                    opacity: 0.2
                }});
                const glow = new THREE.Mesh(glowGeometry, glowMaterial);
                glow.position.copy(sphere.position);
                scene.add(glow);
                
                // Create label
                createLabel(node.label, sphere.position, node.color);
            }});
        }}
        
        function createLabel(text, position, color) {{
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = 256;
            canvas.height = 64;
            
            context.fillStyle = 'rgba(26, 49, 98, 0.8)';
            context.fillRect(0, 0, canvas.width, canvas.height);
            
            context.font = 'Bold 24px Arial';
            context.fillStyle = color;
            context.textAlign = 'center';
            context.textBaseline = 'middle';
            context.fillText(text, canvas.width / 2, canvas.height / 2);
            
            const texture = new THREE.CanvasTexture(canvas);
            const material = new THREE.SpriteMaterial({{ map: texture, transparent: true }});
            const sprite = new THREE.Sprite(material);
            
            sprite.position.set(position.x, position.y + 30, position.z);
            sprite.scale.set(100, 25, 1);
            
            scene.add(sprite);
            labelSprites.push(sprite);
        }}
        
        function createEdges() {{
            edgesData.forEach(edge => {{
                const sourceNode = nodeObjects[edge.source];
                const targetNode = nodeObjects[edge.target];
                
                if (sourceNode && targetNode) {{
                    const points = [];
                    points.push(sourceNode.position);
                    points.push(targetNode.position);
                    
                    const geometry = new THREE.BufferGeometry().setFromPoints(points);
                    const material = new THREE.LineBasicMaterial({{
                        color: edge.color,
                        linewidth: edge.width,
                        transparent: true,
                        opacity: 0.6
                    }});
                    
                    const line = new THREE.Line(geometry, material);
                    scene.add(line);
                    edgeObjects.push(line);
                }}
            }});
        }}
        
        function onNodeClick(event) {{
            const mouse = new THREE.Vector2();
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
            
            const raycaster = new THREE.Raycaster();
            raycaster.setFromCamera(mouse, camera);
            
            const intersects = raycaster.intersectObjects(Object.values(nodeObjects));
            
            if (intersects.length > 0) {{
                const node = intersects[0].object;
                selectNode(node);
            }}
        }}
        
        function selectNode(node) {{
            // Reset previous selection
            if (selectedNode) {{
                selectedNode.material.emissiveIntensity = 0.2;
                selectedNode.scale.set(1, 1, 1);
            }}
            
            // Highlight new selection
            selectedNode = node;
            node.material.emissiveIntensity = 0.8;
            node.scale.set(1.3, 1.3, 1.3);
            
            // Update info panel
            document.getElementById('node-title').textContent = node.userData.label;
            document.getElementById('info-content').innerHTML = 
                `<p>${{node.userData.content}}</p>
                <p style="margin-top: 10px; font-size: 0.85em; color: #a8c5da;">
                Level: ${{node.userData.level}} | Position: (${{Math.round(node.position.x)}}, ${{Math.round(node.position.y)}}, ${{Math.round(node.position.z)}})
                </p>`;
            
            // Smoothly move camera to focus on node
            const targetPos = node.position.clone();
            animateCameraToTarget(targetPos);
        }}
        
        function animateCameraToTarget(target) {{
            const startPos = controls.target.clone();
            const duration = 1000;
            const startTime = Date.now();
            
            function update() {{
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Ease out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                
                controls.target.lerpVectors(startPos, target, eased);
                
                if (progress < 1) {{
                    requestAnimationFrame(update);
                }}
            }}
            
            update();
        }}
        
        function onSearch(event) {{
            const searchTerm = event.target.value.toLowerCase();
            
            Object.values(nodeObjects).forEach(node => {{
                const matches = node.userData.label.toLowerCase().includes(searchTerm);
                node.material.opacity = matches || searchTerm === '' ? 0.9 : 0.3;
                
                if (matches && searchTerm !== '') {{
                    node.material.emissiveIntensity = 0.8;
                }} else {{
                    node.material.emissiveIntensity = 0.2;
                }}
            }});
        }}
        
        function onSpeedChange(event) {{
            const speed = parseFloat(event.target.value);
            document.getElementById('speed-value').textContent = speed.toFixed(1);
            controls.rotateSpeed = speed;
        }}
        
        function resetView() {{
            camera.position.set(0, 0, 800);
            controls.target.set(0, 0, 0);
            controls.update();
            
            if (selectedNode) {{
                selectedNode.material.emissiveIntensity = 0.2;
                selectedNode.scale.set(1, 1, 1);
                selectedNode = null;
            }}
        }}
        
        function toggleRotation() {{
            autoRotate = !autoRotate;
            controls.autoRotate = autoRotate;
            document.getElementById('rotation-text').textContent = autoRotate ? 'Stop' : 'Start';
        }}
        
        function fitToView() {{
            // Calculate bounding box of all nodes
            const box = new THREE.Box3();
            Object.values(nodeObjects).forEach(node => {{
                box.expandByObject(node);
            }});
            
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            const cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;
            
            camera.position.set(center.x, center.y, center.z + cameraZ);
            controls.target.copy(center);
            controls.update();
        }}
        
        function toggleLabels() {{
            showLabels = !showLabels;
            labelSprites.forEach(sprite => {{
                sprite.visible = showLabels;
            }});
        }}
        
        function onWindowResize() {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            
            controls.update();
            
            // Pulse effect for nodes
            const time = Date.now() * 0.001;
            Object.values(nodeObjects).forEach((node, index) => {{
                if (node !== selectedNode) {{
                    node.material.emissiveIntensity = 0.2 + Math.sin(time + index) * 0.05;
                }}
            }});
            
            renderer.render(scene, camera);
        }}
        
        // Initialize on page load
        init();
    </script>
</body>
</html>'''
        
    def save_html(self, output_path: str, theme: str = 'light', title: str = "Knowledge Graph", 
                  visualization_mode: str = "graph", use_3d: bool = False):
        """Save graph as interactive HTML with hover functionality.
        
        Args:
            output_path: Path to save the HTML file
            theme: Color theme ('light' or 'dark')
            title: Title for the visualization
            visualization_mode: 'graph' for knowledge graph or 'mindmap' for mind map layout
            use_3d: If True, use Three.js 3D visualization instead of vis.js 2D
        """
        # Use 3D visualization if requested
        if use_3d:
            return self.save_html_3d(output_path, theme, title, visualization_mode)
        
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
        
        # Configure physics and layout based on visualization mode
        if visualization_mode == "mindmap":
            # Mind map uses hierarchical radial layout
            layout_config = {
                "improvedLayout": True,
                "hierarchical": {
                    "enabled": True,
                    "levelSeparation": 200,
                    "nodeSpacing": 150,
                    "treeSpacing": 250,
                    "blockShifting": True,
                    "edgeMinimization": True,
                    "parentCentralization": True,
                    "direction": "UD",  # Up-Down
                    "sortMethod": "directed"
                }
            }
            # For mind maps, use different node shapes
            node_shape = "ellipse"
        else:
            # Knowledge graph uses force-directed layout
            layout_config = {
                "improvedLayout": True,
                "hierarchical": {
                    "enabled": False
                }
            }
            node_shape = "box"
        
        net.set_options(f"""
        {{
            "physics": {{
                "enabled": true,
                "barnesHut": {{
                    "gravitationalConstant": -12000,
                    "centralGravity": 0.5,
                    "springLength": 200,
                    "springConstant": 0.02,
                    "damping": 0.15,
                    "avoidOverlap": 0.3
                }},
                "stabilization": {{
                    "enabled": true,
                    "iterations": 300,
                    "updateInterval": 25
                }},
                "maxVelocity": 50,
                "minVelocity": 0.75
            }},
            "nodes": {{
                "font": {{
                    "size": 16,
                    "face": "Arial, sans-serif",
                    "strokeWidth": 4,
                    "strokeColor": "#000000"
                }},
                "borderWidth": 3,
                "shadow": {{
                    "enabled": true,
                    "color": "rgba(0, 217, 255, 0.5)",
                    "size": 10,
                    "x": 0,
                    "y": 0
                }},
                "shape": "{node_shape}",
                "margin": 10
            }},
            "edges": {{
                "color": {{
                    "inherit": false
                }},
                "smooth": {{
                    "enabled": true,
                    "type": "{'curvedCW' if visualization_mode == 'mindmap' else 'cubicBezier'}",
                    "roundness": 0.5
                }},
                "arrows": {{
                    "to": {{
                        "enabled": true,
                        "scaleFactor": 1.2
                    }}
                }},
                "shadow": {{
                    "enabled": true,
                    "color": "rgba(74, 144, 226, 0.3)",
                    "size": 5,
                    "x": 0,
                    "y": 0
                }}
            }},
            "interaction": {{
                "hover": true,
                "navigationButtons": true,
                "keyboard": {{
                    "enabled": true
                }},
                "tooltipDelay": 100,
                "zoomView": true,
                "dragView": true
            }},
            "layout": {json.dumps(layout_config)}
        }}
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
