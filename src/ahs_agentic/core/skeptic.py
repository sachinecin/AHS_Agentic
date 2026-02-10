"""
Skeptic Subroutine: Conflict Detection & Resolution
Addresses the 'Hallucination Cascade' by detecting high-entropy 
conflicts between new evidence and current graph state.
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ConflictReport:
    """Structured output from conflict detection."""
    conflict_detected: bool
    delta_score: float
    existing_fact: str
    new_evidence: str
    resolution_strategy: str
    confidence: float


class SkepticSubroutine:
    """
    The Skeptic Subroutine is a transient verification agent that spawns
    when the Synapse Core detects logical divergence between premises.
    
    Technical Approach:
    - Uses cosine similarity to measure semantic divergence
    - Implements adaptive thresholds based on domain context
    - Triggers 'Dormant Fact Re-activation' when conflicts exceed threshold
    
    Args:
        sensitivity_threshold: Delta threshold for conflict detection (0-1)
        domain_context: Optional domain-specific calibration ('medical', 'legal', 'technical')
    """
    
    # Domain-specific threshold calibrations
    DOMAIN_THRESHOLDS = {
        'medical': 0.92,  # High precision required
        'legal': 0.88,    # Balance precision/recall
        'technical': 0.85, # More permissive for technical jargon
        'default': 0.85
    }
    
    def __init__(self, 
        sensitivity_threshold: Optional[float] = None,
        domain_context: str = 'default'
    ):
        """Initialize the Skeptic with calibrated thresholds."""
        if sensitivity_threshold is not None:
            self.threshold = sensitivity_threshold
        else:
            self.threshold = self.DOMAIN_THRESHOLDS.get(
                domain_context, 
                self.DOMAIN_THRESHOLDS['default']
            )
        
        self.domain_context = domain_context
        self.conflict_history = []
    
    def evaluate_conflict(
        self, 
        existing_fact_vector: np.ndarray,
        new_evidence_vector: np.ndarray,
        existing_fact_text: str = "",
        new_evidence_text: str = ""
    ) -> ConflictReport:
        """Compute conflict delta and determine if Skeptic should trigger."""
        
        Args:
            existing_fact_vector: Embedding of existing graph node
            new_evidence_vector: Embedding of new incoming evidence
            existing_fact_text: Original text for traceability
            new_evidence_text: New evidence text for traceability
            
        Returns:
            ConflictReport with detection results and resolution strategy
        """
        # Compute semantic divergence
        delta = self.compute_conflict_delta(
            existing_fact_vector, 
            new_evidence_vector
        )
        
        # Determine if conflict exceeds threshold
        conflict_detected = self.should_trigger(delta)
        
        # Select resolution strategy
        if conflict_detected:
            if delta > 0.95:
                strategy = "HARD_CONFLICT_REPLACE"
            elif delta > self.threshold:
                strategy = "DORMANT_FACT_REACTIVATION"
            else:
                strategy = "SOFT_MERGE"
        else:
            strategy = "ACCEPT_NEW_EVIDENCE"
        
        # Calculate confidence score
        confidence = self._calculate_confidence(delta)
        
        report = ConflictReport(
            conflict_detected=conflict_detected,
            delta_score=delta,
            existing_fact=existing_fact_text,
            new_evidence=new_evidence_text,
            resolution_strategy=strategy,
            confidence=confidence
        )
        
        # Track for adaptive learning
        self.conflict_history.append(report)
        
        return report
    
    def compute_conflict_delta(
        self, 
        existing_fact_vector: np.ndarray, 
        new_evidence_vector: np.ndarray
    ) -> float:
        """Compute logical divergence using cosine similarity."""
        
        Returns:
            Delta score (0 = identical, 1 = complete divergence)
        """
        similarity = self._cosine_sim(existing_fact_vector, new_evidence_vector)
        return 1 - similarity
    
    def should_trigger(self, delta: float) -> bool:
        """Triggering logic: if delta exceeds threshold, spawn Skeptic.""" 
        
        This is the critical decision point that prevents both:
        - False positives (too sensitive → unnecessary re-activation)
        - False negatives (too lenient → missed contradictions)
        """  
        return delta > self.threshold
    
    def adaptive_recalibration(self, feedback_score: float):
        """Adjust threshold based on downstream validation feedback.""" 
        
        Args:
            feedback_score: Human or automated validation score (0-1)
        """  
        # Simple adaptive learning: adjust threshold by 5% based on feedback
        adjustment = 0.05 * (feedback_score - 0.5)
        self.threshold = np.clip(self.threshold + adjustment, 0.7, 0.98)
    
    def _cosine_sim(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors.""" 
        dot_product = np.dot(v1, v2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        
        # Prevent division by zero
        if norm_product == 0:
            return 0.0
        
        return dot_product / norm_product
    
    def _calculate_confidence(self, delta: float) -> float:
        """Calculate confidence in conflict detection."
        Higher delta = higher confidence in conflict.
        """ 
        if delta > 0.95:
            return 0.99
        elif delta > self.threshold:
            return 0.85
        else:
            return 0.70
    
    def get_conflict_statistics(self) -> Dict[str, float]:
        """Return aggregate statistics on detected conflicts.""" 
        if not self.conflict_history:
            return {"total_conflicts": 0, "avg_delta": 0.0}
        
        conflicts = [r for r in self.conflict_history if r.conflict_detected]
        
        return {
            "total_evaluations": len(self.conflict_history),
            "total_conflicts": len(conflicts),
            "conflict_rate": len(conflicts) / len(self.conflict_history),
            "avg_delta": np.mean([r.delta_score for r in self.conflict_history]),
            "current_threshold": self.threshold
        }