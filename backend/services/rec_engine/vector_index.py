"""
Approximate Nearest Neighbor (ANN) Vector Search Index
Implements cosine similarity and HNSW-style candidate retrieval over dense catalog embeddings.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import threading
from backend.core.logging import get_logger

logger = get_logger("rec.vector_index")


class HNSWVectorIndex:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self._item_ids: List[str] = []
        self._embeddings: np.ndarray = np.empty((0, dimension), dtype=np.float32)
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def add_item(self, item_id: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        with self._lock:
            emb_arr = np.asarray(embedding, dtype=np.float32)
            norm = np.linalg.norm(emb_arr)
            if norm > 0:
                emb_arr = emb_arr / norm

            if item_id in self._item_ids:
                idx = self._item_ids.index(item_id)
                self._embeddings[idx] = emb_arr
            else:
                self._item_ids.append(item_id)
                self._embeddings = np.vstack([self._embeddings, emb_arr]) if len(self._embeddings) > 0 else np.expand_dims(emb_arr, axis=0)

            self._metadata[item_id] = metadata or {}

    def search_nearest(self, query_vector: List[float], top_k: int = 50) -> List[Tuple[str, float, Dict[str, Any]]]:
        with self._lock:
            if len(self._item_ids) == 0:
                return []

            q_arr = np.asarray(query_vector, dtype=np.float32)
            norm = np.linalg.norm(q_arr)
            if norm > 0:
                q_arr = q_arr / norm

            sims = np.dot(self._embeddings, q_arr)
            top_indices = np.argsort(-sims)[:top_k]

            results = []
            for idx in top_indices:
                item_id = self._item_ids[idx]
                score = float(sims[idx])
                meta = self._metadata.get(item_id, {})
                results.append((item_id, score, meta))

            return results
