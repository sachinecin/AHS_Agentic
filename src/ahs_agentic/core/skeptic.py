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

    def _cosine_sim(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
