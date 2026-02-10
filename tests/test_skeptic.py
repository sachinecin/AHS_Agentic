import numpy as np
import pytest
from ahs_agentic.core.skeptic import SkepticSubroutine


class TestSkepticSubroutine:
    """Test suite for conflict detection and threshold calibration."""
    
    def test_identical_vectors_no_conflict(self):
        """Identical vectors should produce zero delta."""
        skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
        
        vec1 = np.array([1.0, 0.0, 0.5])
        vec2 = np.array([1.0, 0.0, 0.5])
        
        delta = skeptic.compute_conflict_delta(vec1, vec2)
        
        assert delta < 0.01, "Identical vectors should have near-zero delta"
        assert not skeptic.should_trigger(delta)
    
    def test_opposite_vectors_high_conflict(self):
        """Opposite vectors should trigger skeptic."""
        skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
        
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])
        
        delta = skeptic.compute_conflict_delta(vec1, vec2)
        
        assert delta > 0.85, "Orthogonal vectors should produce high delta"
        assert skeptic.should_trigger(delta)
    
    def test_threshold_calibration(self):
        """Test different threshold values for false positive rate."""
        vec1 = np.array([1.0, 0.5, 0.3])
        vec2 = np.array([0.9, 0.6, 0.2])
        
        # Conservative threshold (fewer triggers)
        skeptic_conservative = SkepticSubroutine(sensitivity_threshold=0.95)
        delta_conservative = skeptic_conservative.compute_conflict_delta(vec1, vec2)
        
        # Aggressive threshold (more triggers)
        skeptic_aggressive = SkepticSubroutine(sensitivity_threshold=0.75)
        delta_aggressive = skeptic_aggressive.compute_conflict_delta(vec1, vec2)
        
        assert delta_conservative == delta_aggressive, "Delta should be independent of threshold"
        
    def test_conflict_report_generation(self):
        """Test structured conflict report generation."""
        skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
        
        report = skeptic.generate_conflict_report(
            existing_premise="Policy A requires X",
            new_evidence="Regulation B prohibits X",
            delta=0.92
        )
        
        assert report["conflict_detected"] is True
        assert report["delta_score"] == 0.92
        assert report["resolution_strategy"] in ["dormant_fact_reactivation", "incremental_merge"]
        assert "requires_human_review" in report
