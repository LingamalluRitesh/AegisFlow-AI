"""
PulseRec Neural Architecture: SelfAttentiveItemGraphRec
Item-to-item relational graph network augmented with self-attentive neighborhood aggregation
"""

import math
import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger("rec.neural.item_graph_rec")

class SelfAttentiveItemGraphRecConfig(BaseModel):
    embedding_dim: int = 128
    hidden_layers: List[int] = Field(default_factory=lambda: [256, 128, 64])
    dropout_rate: float = 0.15
    learning_rate: float = 0.0005
    temperature: float = 0.08
    num_attention_heads: int = 4
    max_history_length: int = 50

class SelfAttentiveItemGraphRec:
    """Item-to-item relational graph network augmented with self-attentive neighborhood aggregation"""

    def __init__(self, config: Optional[SelfAttentiveItemGraphRecConfig] = None):
        self.config = config or SelfAttentiveItemGraphRecConfig()
        self._init_neural_weights()

    def _init_neural_weights(self) -> None:
        dim = self.config.embedding_dim
        self.w_query = np.random.normal(0, 0.04, (dim, dim)).astype(np.float32)
        self.w_key = np.random.normal(0, 0.04, (dim, dim)).astype(np.float32)
        self.w_value = np.random.normal(0, 0.04, (dim, dim)).astype(np.float32)
        self.w_mlp1 = np.random.normal(0, 0.04, (dim * 2, 64)).astype(np.float32)
        self.b_mlp1 = np.zeros(64, dtype=np.float32)
        self.w_mlp2 = np.random.normal(0, 0.04, (64, 1)).astype(np.float32)
        self.b_mlp2 = np.zeros(1, dtype=np.float32)

    def compute_attention(self, query: np.ndarray, keys: np.ndarray, values: np.ndarray) -> np.ndarray:
        q = np.dot(query, self.w_query)
        k = np.dot(keys, self.w_key)
        v = np.dot(values, self.w_value)
        scale = math.sqrt(self.config.embedding_dim)
        attn_weights = np.dot(k, q) / scale
        exp_w = np.exp(attn_weights - np.max(attn_weights))
        softmax_w = exp_w / np.maximum(1e-7, np.sum(exp_w))
        return np.sum(softmax_w[:, np.newaxis] * v, axis=0)

    def score_candidates(self, user_history: List[List[float]], target_items: List[List[float]]) -> List[float]:
        if len(user_history) == 0 or len(target_items) == 0:
            return [0.5] * len(target_items)

        hist_arr = np.asarray(user_history, dtype=np.float32)
        target_arr = np.asarray(target_items, dtype=np.float32)
        scores = []

        for item_vec in target_arr:
            user_interest = self.compute_attention(item_vec, hist_arr, hist_arr)
            cross_input = np.concatenate([user_interest, item_vec])
            h1 = np.maximum(0.0, np.dot(cross_input, self.w_mlp1) + self.b_mlp1)
            logit = float(np.dot(h1, self.w_mlp2) + self.b_mlp2)
            prob = 1.0 / (1.0 + math.exp(-logit))
            scores.append(float(prob))

        return scores
