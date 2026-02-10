"""
Agentic Hyper-Graph Synapse (AHS)
A next-generation framework for synthetic reasoning with living graph state.
"""

__version__ = "1.0.0"

# Core components
from ahs_agentic.core.skeptic import SkepticSubroutine
from ahs_agentic.core.retrieval import SpeculativeRetriever

# Graph and memory components
from ahs_agentic.graph.hyper_graph import HyperGraph, SemanticEdge
from ahs_agentic.memory.latent_layer import LatentMemoryManager, FactNode

# Utilities
from ahs_agentic.utils.metrics import MetricsTracker, PerformanceTimer

# Note: HyperGraphAgent import removed as core.hypergraph doesn't exist yet
# This will be added in a future implementation

__all__ = [
    "SkepticSubroutine",
    "SpeculativeRetriever",
    "HyperGraph",
    "SemanticEdge",
    "LatentMemoryManager",
    "FactNode",
    "MetricsTracker",
    "PerformanceTimer",
]