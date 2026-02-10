"""
Pytest configuration and shared fixtures.
"""

import pytest
import numpy as np
from ahs_agentic import SkepticSubroutine, SpeculativeRetriever
from ahs_agentic.graph import HyperGraph
from ahs_agentic.memory import LatentMemoryManager, FactNode


@pytest.fixture
def sample_vector():
    """Generate a sample embedding vector."""
    return np.random.rand(768)


@pytest.fixture
def skeptic():
    """Create a Skeptic Subroutine instance."""
    return SkepticSubroutine(sensitivity_threshold=0.85)


@pytest.fixture
def retriever():
    """Create a Speculative Retriever instance."""
    return SpeculativeRetriever(max_parallel_hops=5)


@pytest.fixture
def hyper_graph():
    """Create a HyperGraph instance."""
    return HyperGraph()


@pytest.fixture
def memory_manager():
    """Create a Latent Memory Manager instance."""
    return LatentMemoryManager(
        tier1_size=256,
        tier2_size=2048,
        tier3_enabled=True
    )


@pytest.fixture
def sample_fact(sample_vector):
    """Create a sample FactNode."""
    return FactNode(
        id="fact_001",
        content="Sample fact content",
        vector=sample_vector,
        salience_score=0.9,
        tier=1,
        source_metadata={"source": "test", "timestamp": "2026-02-10"}
    )


@pytest.fixture
def sample_facts(sample_vector):
    """Create multiple sample facts."""
    return [
        FactNode(
            id=f"fact_{i:03d}",
            content=f"Fact content {i}",
            vector=np.random.rand(768),
            salience_score=0.8 + (i * 0.01),
            tier=1,
            source_metadata={"source": "test", "index": i}
        )
        for i in range(10)
    ]
