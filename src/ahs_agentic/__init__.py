"""
Agentic Hyper-Graph Synapse (AHS)
A next-generation framework for synthetic reasoning with living graph state.
"""

__version__ = "1.0.0"

from ahs_agentic.agents.hypergraph_agent import HyperGraphAgent
from ahs_agentic.core.skeptic import SkepticSubroutine
from ahs_agentic.core.retrieval import SpeculativeRetriever
from ahs_agentic.utils.cost_tracker import (
    CostTracker,
    track_tokens,
    get_tracker,
    TokenUsage
)
from ahs_agentic.utils.safety_check import safety_check

__all__ = [
    "HyperGraphAgent",
    "SkepticSubroutine",
    "SpeculativeRetriever",
    "CostTracker",
    "track_tokens",
    "get_tracker",
    "TokenUsage",
    "safety_check",
]