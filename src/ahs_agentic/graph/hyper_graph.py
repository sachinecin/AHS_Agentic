"""
Probabilistic Hyper-Graph implementation.

This module implements the core graph structure that maintains
the Living Graph State across queries.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import networkx as nx
import numpy as np


@dataclass
class SemanticEdge:
    """Represents a relationship between facts."""
    
    source_id: str
    target_id: str
    relationship_type: str  # 'supports', 'contradicts', 'elaborates'
    confidence: float
    conflict_delta: float
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class HyperGraph:
    """
    Probabilistic hyper-graph for maintaining fact relationships.
    
    The graph structure enables:
    - O(1) node lookup
    - Efficient neighborhood queries
    - Conflict detection via edge analysis
    - Persistent state across queries
    """
    
    def __init__(self):
        """Initialize empty hyper-graph."""
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[SemanticEdge] = []
    
    def add_node(
        self,
        node_id: str,
        content: str,
        vector: np.ndarray,
        **metadata
    ) -> None:
        """
        Add a node to the graph.
        
        Args:
            node_id: Unique node identifier
            content: Human-readable content
            vector: Embedding vector
            **metadata: Additional node attributes
        """
        node_data = {
            "content": content,
            "vector": vector,
            **metadata
        }
        
        self.nodes[node_id] = node_data
        self.graph.add_node(node_id, **node_data)
    
    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        confidence: float = 1.0,
        conflict_delta: float = 0.0,
        **metadata
    ) -> None:
        """
        Add an edge between nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Type of relationship
            confidence: Confidence score (0.0-1.0)
            conflict_delta: Conflict score (0.0-1.0)
            **metadata: Additional edge attributes
        """
        edge = SemanticEdge(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            confidence=confidence,
            conflict_delta=conflict_delta,
            metadata=metadata
        )
        
        self.edges.append(edge)
        self.graph.add_edge(
            source_id,
            target_id,
            relationship_type=relationship_type,
            confidence=confidence,
            conflict_delta=conflict_delta,
            **metadata
        )
    
    def get_node(self, node_id: str) -> Optional[Dict]:
        """
        Get node data by ID.
        
        Args:
            node_id: Node identifier
        
        Returns:
            Node data dictionary or None
        """
        return self.nodes.get(node_id)
    
    def find_neighbors(
        self,
        node_id: str,
        relationship_type: Optional[str] = None
    ) -> List[str]:
        """
        Find neighboring nodes.
        
        Args:
            node_id: Node to find neighbors for
            relationship_type: Filter by relationship type
        
        Returns:
            List of neighbor node IDs
        """
        if node_id not in self.graph:
            return []
        
        neighbors = list(self.graph.successors(node_id))
        
        if relationship_type:
            # Filter by relationship type
            filtered = []
            for neighbor in neighbors:
                edge_data = self.graph[node_id][neighbor]
                if edge_data.get("relationship_type") == relationship_type:
                    filtered.append(neighbor)
            return filtered
        
        return neighbors
    
    def find_conflicts(self, threshold: float = 0.85) -> List[Tuple[str, str]]:
        """
        Find pairs of nodes with high conflict delta.
        
        Args:
            threshold: Conflict delta threshold
        
        Returns:
            List of (source_id, target_id) tuples with conflicts
        """
        conflicts = []
        
        for edge in self.edges:
            if edge.conflict_delta > threshold:
                conflicts.append((edge.source_id, edge.target_id))
        
        return conflicts
    
    def find_related_facts(
        self,
        node_id: str,
        max_depth: int = 2
    ) -> List[str]:
        """
        Find facts related to a node within max_depth.
        
        Args:
            node_id: Starting node
            max_depth: Maximum graph distance
        
        Returns:
            List of related node IDs
        """
        if node_id not in self.graph:
            return []
        
        # BFS to find nodes within max_depth
        visited = set()
        queue = [(node_id, 0)]
        related = []
        
        while queue:
            current, depth = queue.pop(0)
            
            if current in visited or depth > max_depth:
                continue
            
            visited.add(current)
            if current != node_id:
                related.append(current)
            
            # Add neighbors to queue
            for neighbor in self.graph.successors(current):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        return related
    
    def get_subgraph(self, node_ids: List[str]) -> nx.DiGraph:
        """
        Extract a subgraph containing specified nodes.
        
        Args:
            node_ids: List of node IDs to include
        
        Returns:
            NetworkX DiGraph subgraph
        """
        return self.graph.subgraph(node_ids).copy()
    
    def get_metrics(self) -> Dict:
        """
        Get graph statistics.
        
        Returns:
            Dictionary with graph metrics
        """
        return {
            "num_nodes": len(self.nodes),
            "num_edges": len(self.edges),
            "density": nx.density(self.graph),
            "num_conflicts": len([
                e for e in self.edges if e.conflict_delta > 0.85
            ]),
        }
    
    def to_dict(self) -> Dict:
        """
        Serialize graph to dictionary.
        
        Returns:
            Dictionary representation of graph
        """
        return {
            "nodes": self.nodes,
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "type": e.relationship_type,
                    "confidence": e.confidence,
                    "conflict_delta": e.conflict_delta,
                    "metadata": e.metadata
                }
                for e in self.edges
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "HyperGraph":
        """
        Deserialize graph from dictionary.
        
        Args:
            data: Dictionary representation
        
        Returns:
            HyperGraph instance
        """
        graph = cls()
        
        # Add nodes
        for node_id, node_data in data["nodes"].items():
            graph.add_node(node_id, **node_data)
        
        # Add edges
        for edge_data in data["edges"]:
            graph.add_edge(
                source_id=edge_data["source"],
                target_id=edge_data["target"],
                relationship_type=edge_data["type"],
                confidence=edge_data["confidence"],
                conflict_delta=edge_data["conflict_delta"],
                **edge_data.get("metadata", {})
            )
        
        return graph
