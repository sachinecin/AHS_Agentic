"""Tests for Latent Memory Manager."""

import pytest
import numpy as np
from ahs_agentic.memory import LatentMemoryManager, FactNode


class TestLatentMemoryManager:
    """Test suite for multi-tier memory management."""
    
    def test_initialization(self, memory_manager):
        """Test memory manager initialization."""
        assert memory_manager.tier1_size == 256
        assert memory_manager.tier2_size == 2048
        assert memory_manager.tier3_enabled is True
        assert len(memory_manager.tier1) == 0
        assert len(memory_manager.tier2) == 0
    
    def test_add_high_salience_fact_to_tier1(self, memory_manager):
        """High salience facts should go to Tier 1."""
        fact = FactNode(
            id="fact_001",
            content="Important fact",
            vector=np.random.rand(768),
            salience_score=0.95,
            tier=1,
            source_metadata={}
        )
        
        memory_manager.add_fact(fact)
        
        assert "fact_001" in memory_manager.tier1
        assert fact.tier == 1
    
    def test_add_medium_salience_fact_to_tier2(self, memory_manager):
        """Medium salience facts should go to Tier 2."""
        fact = FactNode(
            id="fact_002",
            content="Medium fact",
            vector=np.random.rand(768),
            salience_score=0.70,
            tier=2,
            source_metadata={}
        )
        
        memory_manager.add_fact(fact)
        
        assert "fact_002" in memory_manager.tier2
        assert fact.tier == 2
    
    def test_add_low_salience_fact_to_tier3(self, memory_manager):
        """Low salience facts should go to Tier 3."""
        fact = FactNode(
            id="fact_003",
            content="Low priority fact",
            vector=np.random.rand(768),
            salience_score=0.50,
            tier=3,
            source_metadata={}
        )
        
        memory_manager.add_fact(fact)
        
        assert "fact_003" in memory_manager.tier3_ids
        assert fact.tier == 3
    
    def test_promote_from_tier2_to_tier1(self, memory_manager):
        """Test fact promotion from Tier 2 to Tier 1."""
        fact = FactNode(
            id="fact_004",
            content="To be promoted",
            vector=np.random.rand(768),
            salience_score=0.70,
            tier=2,
            source_metadata={}
        )
        
        memory_manager.add_fact(fact)
        assert "fact_004" in memory_manager.tier2
        
        promoted = memory_manager.promote_to_tier1("fact_004")
        
        assert promoted is not None
        assert "fact_004" in memory_manager.tier1
        assert "fact_004" not in memory_manager.tier2
        assert promoted.tier == 1
    
    def test_demote_from_tier1_to_tier2(self, memory_manager):
        """Test fact demotion from Tier 1 to Tier 2."""
        fact = FactNode(
            id="fact_005",
            content="To be demoted",
            vector=np.random.rand(768),
            salience_score=0.90,
            tier=1,
            source_metadata={}
        )
        
        memory_manager.add_fact(fact)
        assert "fact_005" in memory_manager.tier1
        
        demoted = memory_manager.demote_to_tier2("fact_005")
        
        assert demoted is not None
        assert "fact_005" in memory_manager.tier2
        assert "fact_005" not in memory_manager.tier1
        assert demoted.tier == 2
    
    def test_get_active_facts(self, memory_manager, sample_facts):
        """Test retrieving all active (Tier 1) facts."""
        for fact in sample_facts[:5]:
            fact.salience_score = 0.90
            memory_manager.add_fact(fact)
        
        active = memory_manager.get_active_facts()
        
        assert len(active) == 5
        assert all(f.tier == 1 for f in active)
    
    def test_get_metrics(self, memory_manager, sample_facts):
        """Test metrics reporting."""
        for i, fact in enumerate(sample_facts):
            if i < 3:
                fact.salience_score = 0.90  # Tier 1
            elif i < 6:
                fact.salience_score = 0.70  # Tier 2
            else:
                fact.salience_score = 0.50  # Tier 3
            memory_manager.add_fact(fact)
        
        metrics = memory_manager.get_metrics()
        
        assert metrics["tier1_count"] == 3
        assert metrics["tier2_count"] == 3
        assert metrics["tier3_count"] == 4
        assert "tier1_utilization" in metrics
