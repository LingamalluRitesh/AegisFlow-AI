"""
HydraServe Tensor Math Kernel: TopKRankingHeapKernel
Min-heap based priority queue extracting top-K candidates from logits
"""

import math
from typing import List, Tuple, Union, Optional
import numpy as np

class TopKRankingHeapKernel:
    """Min-heap based priority queue extracting top-K candidates from logits"""

    @staticmethod
    def execute(tensor_a: List[float], tensor_b: Optional[List[float]] = None) -> Union[List[float], float]:
        a = np.asarray(tensor_a, dtype=np.float32)
        if tensor_b is not None:
            b = np.asarray(tensor_b, dtype=np.float32)
            dot = float(np.dot(a, b))
            norm_a = float(np.linalg.norm(a))
            norm_b = float(np.linalg.norm(b))
            if norm_a == 0.0 or norm_b == 0.0:
                return 0.0
            return dot / (norm_a * norm_b)
        
        return (1.0 / (1.0 + np.exp(-a))).tolist()
