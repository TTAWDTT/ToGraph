"""Build knowledge graph from parsed documents."""

import re
from collections import Counter
from typing import List, Dict, Set, Tuple
import networkx as nx
from .parser import DocumentNode


class GraphBuilder:
    """Build a knowledge graph from document nodes."""
    
    # Sections to filter out as they are usually redundant
    REDUNDANT_SECTIONS = {
        'abstract', 'references', 'bibliography', 'acknowledgments', 'acknowledgements',
        'author', 'authors', 'author information', 'authors information',
        'funding', 'conflicts of interest', 'conflict of interest',
        'appendix', 'supplementary material', 'supplementary materials',
        'copyright', 'license', 'permissions', 'keywords', 'key words',
        'abbreviations', 'glossary', 'nomenclature'
    }
    
    def __init__(self, nodes: List[DocumentNode], raw_content: str = ""):
        self.nodes = nodes
        self.raw_content = raw_content
        self.graph = nx.DiGraph()
        self.entity_content = {}  # Map entities to their content
        self.max_relationships_per_node = 3  # Limit connections to prevent clutter
        
    def build(self) -> nx.DiGraph:
        """Build the knowledge graph."""
        # Filter out redundant nodes before building
        filtered_nodes = self._filter_redundant_nodes(self.nodes)
        self._add_nodes_to_graph(filtered_nodes)
        self._extract_relationships()
        return self.graph
    
    def _filter_redundant_nodes(self, nodes: List[DocumentNode]) -> List[DocumentNode]:
        """Filter out redundant sections like abstract, references, author names."""
        filtered = []
        for node in nodes:
            title_lower = node.title.lower().strip()
            
            # Check if title is in redundant sections
            if title_lower not in self.REDUNDANT_SECTIONS:
                # Filter children recursively
                if node.children:
                    node.children = self._filter_redundant_nodes(node.children)
                filtered.append(node)
        
        return filtered
    
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
        """Extract additional relationships between nodes based on content (optimized)."""
        nodes = list(self.graph.nodes(data=True))
        
        # Limit total nodes to process for performance
        if len(nodes) > 50:
            # For large graphs, only extract relationships for top-level nodes
            nodes = [(nid, attrs) for nid, attrs in nodes if attrs.get('level', 1) <= 2]
        
        # Extract key terms from each node
        node_terms = {}
        for node_id, attrs in nodes:
            terms = self._extract_key_terms(attrs.get('full_content', ''))
            node_terms[node_id] = terms
        
        # Find connections based on shared terms (optimized)
        relationship_counts = {node_id: 0 for node_id in node_terms.keys()}
        
        for i, (node_id1, terms1) in enumerate(node_terms.items()):
            # Stop adding relationships if this node already has enough
            if relationship_counts[node_id1] >= self.max_relationships_per_node:
                continue
                
            for node_id2, terms2 in list(node_terms.items())[i+1:]:
                # Stop if target node also has enough relationships
                if relationship_counts[node_id2] >= self.max_relationships_per_node:
                    continue
                
                # Check if nodes share significant terms (increased threshold)
                shared = terms1 & terms2
                if len(shared) >= 3:  # Increased from 2 to 3 for more selective connections
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
                        relationship_counts[node_id1] += 1
                        relationship_counts[node_id2] += 1
                        
                        # Early exit if both nodes have enough relationships
                        if relationship_counts[node_id1] >= self.max_relationships_per_node:
                            break
    
    def _extract_key_terms(self, text: str) -> Set[str]:
        """Extract key terms from text (optimized for performance)."""
        if not text:
            return set()
        
        # Limit text length for processing
        text = text[:1000]  # Only analyze first 1000 characters
        
        # Simple extraction: words longer than 5 characters, not too common
        words = re.findall(r'\b[A-Za-z]{6,}\b', text.lower())  # Increased from 5 to 6
        
        # Common words to exclude (expanded list)
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
            'might', 'would', 'shall', 'upon', 'within', 'without', 'therefore',
            'however', 'moreover', 'furthermore', 'likewise', 'nonetheless',
            'otherwise', 'whereas', 'whereby', 'wherein', 'herein', 'therein'
        }
        
        # Filter and count (limit to most frequent for performance)
        filtered = [w for w in words if w not in stopwords and len(w) > 5]
        
        # Return fewer key terms (reduced from 10 to 5)
        counter = Counter(filtered)
        return set([term for term, count in counter.most_common(5)])
    
    def get_graph(self) -> nx.DiGraph:
        """Get the built graph."""
        return self.graph
    
    def get_entity_content(self) -> Dict[str, str]:
        """Get mapping of entity IDs to their content."""
        return self.entity_content
