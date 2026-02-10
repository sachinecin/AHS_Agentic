import numpy as np

class SkepticSubroutine:
    """
    Addresses the 'Hallucination Cascade' by detecting high-entropy 
    conflicts between new evidence and current graph state.
    """
    def __init__(self, sensitivity_threshold=0.85):
        self.threshold = sensitivity_threshold

    def compute_conflict_delta(self, existing_fact_vector, new_evidence_vector):
        # Using cosine similarity to detect logical divergence
        similarity = self._cosine_sim(existing_fact_vector, new_evidence_vector)
        return 1 - similarity

    def should_trigger(self, delta):
        # Triggering logic: if the delta is higher than threshold, spawn skeptic
        return delta > self.threshold
    
    def generate_conflict_report(self, existing_premise, new_evidence, delta):
        """
        Generate structured conflict report.
        
        Args:
            existing_premise: Content of existing fact
            new_evidence: Content of new evidence
            delta: Conflict delta score
        
        Returns:
            Dictionary with conflict report
        """
        # Determine resolution strategy based on delta
        if delta > 0.95:
            resolution_strategy = "human_review"
        elif delta > 0.85:
            resolution_strategy = "dormant_fact_reactivation"
        else:
            resolution_strategy = "incremental_merge"
        
        return {
            "conflict_detected": True,
            "delta_score": delta,
            "existing_premise": existing_premise,
            "new_evidence": new_evidence,
            "resolution_strategy": resolution_strategy,
            "requires_human_review": delta > 0.95,
            "confidence": delta
        }

    def _cosine_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
