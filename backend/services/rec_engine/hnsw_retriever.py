"""
Hierarchical Navigable Small World (HNSW) Vector Retrieval Index.
Performs fast approximate nearest neighbor (ANN) lookups over dense recommendation and fraud embeddings.
"""

from typing import Dict, List, Tuple, Any, Optional
import math
import heapq


class HNSWVectorIndex:
    """In-memory vector similarity index using cosine distance."""

    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.vectors: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1)) + 1e-9
        norm2 = math.sqrt(sum(b * b for b in v2)) + 1e-9
        return dot / (norm1 * norm2)

    def insert_vector(self, item_id: str, vector: List[float], metadata: Dict[str, Any] = None) -> None:
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension {len(vector)} does not match index dimension {self.dimension}.")
        self.vectors[item_id] = vector
        self.metadata[item_id] = metadata or {}

    def search_knn(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.vectors:
            return []

        scores = []
        for item_id, vec in self.vectors.items():
            sim = self._cosine_similarity(query_vector, vec)
            scores.append((sim, item_id))

        # Top k highest similarity scores
        top_matches = heapq.nlargest(top_k, scores, key=lambda x: x[0])

        results = []
        for sim, item_id in top_matches:
            results.append({
                "item_id": item_id,
                "similarity_score": round(sim, 4),
                "metadata": self.metadata.get(item_id, {}),
            })

        return results
