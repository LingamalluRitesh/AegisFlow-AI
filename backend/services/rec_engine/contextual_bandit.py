"""
Contextual Multi-Armed Bandits (LinUCB & Thompson Sampling)
Balances exploitation of known high-converting items with exploration of new items.
"""

import math
from typing import Dict, List, Tuple
import numpy as np
import threading


class LinUCBBandit:
    def __init__(self, dimension: int = 8, alpha: float = 0.25):
        self.dimension = dimension
        self.alpha = alpha
        self._A: Dict[str, np.ndarray] = {}
        self._b: Dict[str, np.ndarray] = {}
        self._lock = threading.Lock()

    def get_exploration_bonus(self, arm_id: str, context_vec: List[float]) -> float:
        with self._lock:
            if arm_id not in self._A:
                self._A[arm_id] = np.identity(self.dimension, dtype=np.float64)
                self._b[arm_id] = np.zeros((self.dimension, 1), dtype=np.float64)

            x = np.asarray(context_vec[:self.dimension], dtype=np.float64).reshape(-1, 1)
            if len(x) < self.dimension:
                x = np.pad(x, ((0, self.dimension - len(x)), (0, 0)))

            A_inv = np.linalg.inv(self._A[arm_id])
            prod = np.dot(np.dot(x.T, A_inv), x)
            val = float(prod.item()) if hasattr(prod, "item") else float(prod)
            ucb_bonus = self.alpha * math.sqrt(max(0.0, val))
            return float(ucb_bonus)

    def update_arm(self, arm_id: str, context_vec: List[float], reward: float) -> None:
        with self._lock:
            if arm_id not in self._A:
                self._A[arm_id] = np.identity(self.dimension, dtype=np.float64)
                self._b[arm_id] = np.zeros((self.dimension, 1), dtype=np.float64)

            x = np.asarray(context_vec[:self.dimension], dtype=np.float64).reshape(-1, 1)
            if len(x) < self.dimension:
                x = np.pad(x, ((0, self.dimension - len(x)), (0, 0)))

            self._A[arm_id] += np.dot(x, x.T)
            self._b[arm_id] += reward * x


class ThompsonSamplingBandit:
    def __init__(self):
        self._alpha_beta: Dict[str, Tuple[float, float]] = {}
        self._lock = threading.Lock()

    def sample_reward(self, arm_id: str) -> float:
        with self._lock:
            a, b = self._alpha_beta.get(arm_id, (1.0, 1.0))
            return float(np.random.beta(a, b))

    def update_arm(self, arm_id: str, converted: bool) -> None:
        with self._lock:
            a, b = self._alpha_beta.get(arm_id, (1.0, 1.0))
            if converted:
                self._alpha_beta[arm_id] = (a + 1.0, b)
            else:
                self._alpha_beta[arm_id] = (a, b + 1.0)
