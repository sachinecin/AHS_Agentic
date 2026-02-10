"""
Agentic Hyper-Graph Synapse (AHS)
A next-generation framework for synthetic reasoning with living graph state.
"""

__version__ = "1.0.0"

from ahs_agentic.core.hypergraph import HyperGraphAgent
from ahs_agentic.core.skeptic import SkepticSubroutine
from ahs_agentic.core.retrieval import SpeculativeRetriever

__all__ = ["HyperGraphAgent", "SkepticSubroutine", "SpeculativeRetriever"]