"""
Dynamic Capsule Routing Multi-Interest Extraction Engine (PulseRec)
Extracts distinct multi-modal user intent clusters from long engagement sequences.
"""

from typing import List, Dict, Any, Tuple
import math
import numpy as np
from backend.core.logging import get_logger

logger = get_logger("rec_engine.capsule_extractor")


class MultiInterestCapsuleExtractor:
    """Dynamic routing capsule network extracting k interest vectors per user."""

    def __init__(self, embedding_dim: int = 128, max_interests_k: int = 4, routing_iterations: int = 3):
        self.dim = embedding_dim
        self.k = max_interests_k
        self.iterations = routing_iterations

    def squash(self, s: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(s, axis=-1, keepdims=True)
        norm_sq = norm ** 2
        return (norm_sq / (1.0 + norm_sq)) * (s / np.maximum(1e-7, norm))

    def extract_user_interests(self, interaction_embeddings: List[List[float]]) -> List[List[float]]:
        if len(interaction_embeddings) == 0:
            return [np.zeros(self.dim, dtype=np.float32).tolist()]

        items = np.asarray(interaction_embeddings, dtype=np.float32)
        n_items = len(items)

        # Initialize routing logits b_ij to zero: shape (k, n_items)
        b = np.zeros((self.k, n_items), dtype=np.float32)
        v = np.zeros((self.k, self.dim), dtype=np.float32)

        for it in range(self.iterations):
            # Softmax across capsules k for each item
            exp_b = np.exp(b - np.max(b, axis=0, keepdims=True))
            c = exp_b / np.sum(exp_b, axis=0, keepdims=True)

            # Compute weighted sum s_j
            s = np.dot(c, items)  # shape (k, dim)
            v = self.squash(s)

            # Update routing logits: b_ij += v_j . u_i
            if it < self.iterations - 1:
                b += np.dot(v, items.T)

        return [v[i].tolist() for i in range(self.k)]


multi_interest_extractor = MultiInterestCapsuleExtractor()
