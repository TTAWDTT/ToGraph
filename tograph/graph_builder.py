"""Build knowledge graph from parsed documents."""

import re
from typing import List, Dict, Set, Tuple
import networkx as nx
from .parser import DocumentNode


class GraphBuilder:
    """Build a knowledge graph from document nodes."""
    
    def __init__(self, nodes: List[DocumentNode], raw_content: str = ""):
        self.nodes = nodes
        self.raw_content = raw_content
        self.graph = nx.DiGraph()
        self.entity_content = {}  # Map entities to their content
        
    def build(self) -> nx.DiGraph:
        """Build the knowledge graph."""
        self._add_nodes_to_graph(self.nodes)
        self._extract_relationships()
        return self.graph
    
    def _add_nodes_to_graph(self, nodes: List[DocumentNode], parent: str = None):
        """Recursively add document nodes to graph."""
        for node in nodes:
            node_id = self._create_node_id(node)
            
            # Add node with attributes
            self.graph.add_node(
                node_id,
                label=node.title,
                level=node.level,
                content=node.content[:500] if node.content else "",  # Truncate for display
                full_content=node.content,
                type="section"
            )
            
            # Store full content for hover display
            self.entity_content[node_id] = node.content
            
            # Connect to parent
            if parent:
                self.graph.add_edge(parent, node_id, relation="contains")
            
            # Process children
            if node.children:
                self._add_nodes_to_graph(node.children, node_id)
    
    def _create_node_id(self, node: DocumentNode) -> str:
        """Create a unique node ID."""
        # Clean title for ID
        clean_title = re.sub(r'[^\w\s-]', '', node.title)
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        return f"{clean_title}_{node.position}"
    
    def _extract_relationships(self):
        """Extract additional relationships between nodes based on content."""
        nodes = list(self.graph.nodes(data=True))
        
        # Extract key terms from each node
        node_terms = {}
        for node_id, attrs in nodes:
            terms = self._extract_key_terms(attrs.get('full_content', ''))
            node_terms[node_id] = terms
        
        # Find connections based on shared terms
        for i, (node_id1, terms1) in enumerate(node_terms.items()):
            for node_id2, terms2 in list(node_terms.items())[i+1:]:
                # Check if nodes share significant terms
                shared = terms1 & terms2
                if len(shared) >= 2:  # At least 2 shared terms
                    # Don't add edge if there's already a parent-child relationship
                    if not self.graph.has_edge(node_id1, node_id2) and \
                       not self.graph.has_edge(node_id2, node_id1):
                        # Add bidirectional relationship
                        self.graph.add_edge(
                            node_id1, 
                            node_id2, 
                            relation="related",
                            shared_terms=list(shared)[:3]  # Store some shared terms
                        )
    
    def _extract_key_terms(self, text: str) -> Set[str]:
        """Extract key terms from text."""
        if not text:
            return set()
        
        # Simple extraction: words longer than 4 characters, not too common
        words = re.findall(r'\b[A-Za-z]{5,}\b', text.lower())
        
        # Common words to exclude
        stopwords = {
            'about', 'above', 'after', 'again', 'against', 'all', 'and', 'any', 'are',
            'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but',
            'cannot', 'could', 'did', 'does', 'doing', 'down', 'during', 'each',
            'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
            'here', 'how', 'into', 'more', 'most', 'must', 'not', 'now',
            'once', 'only', 'other', 'our', 'out', 'over', 'own', 'same',
            'should', 'some', 'such', 'than', 'that', 'the', 'their', 'them',
            'then', 'there', 'these', 'they', 'this', 'those', 'through', 'under',
            'until', 'very', 'was', 'were', 'what', 'when', 'where', 'which',
            'while', 'who', 'will', 'with', 'would', 'your', 'could', 'should',
            'might', 'would', 'shall', 'upon', 'within', 'without'
        }
        
        # Filter and count
        filtered = [w for w in words if w not in stopwords and len(w) > 4]
        
        # Return most common terms
        from collections import Counter
        counter = Counter(filtered)
        return set([term for term, count in counter.most_common(10)])
    
    def get_graph(self) -> nx.DiGraph:
        """Get the built graph."""
        return self.graph
    
    def get_entity_content(self) -> Dict[str, str]:
        """Get mapping of entity IDs to their content."""
        return self.entity_content
