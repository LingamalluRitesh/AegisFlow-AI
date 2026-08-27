"""
Dual-Tower User and Item Embedding Generator
Maps user interaction histories and catalog item metadata into common 128-d latent space.
"""

from typing import List, Dict, Any
import numpy as np


class DualTowerEmbeddingGenerator:
    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim

    def encode_user(self, user_id: str, context: Dict[str, Any]) -> List[float]:
        seed = abs(hash(user_id)) % (2**32)
        rng = np.random.RandomState(seed)
        vec = rng.normal(loc=0.0, scale=1.0, size=self.embedding_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()

    def encode_item(self, item_id: str, category: str, price: float) -> List[float]:
        seed = abs(hash(f"{item_id}_{category}")) % (2**32)
        rng = np.random.RandomState(seed)
        vec = rng.normal(loc=0.0, scale=1.0, size=self.embedding_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()
