"""
Feature Transformation Engine for Streaming and Batch Pipelines
Applies cyclical temporal embeddings, robust scaling, categorical one-hot, and geohash encoding.
"""

import math
from typing import Dict, List
import numpy as np
from enum import Enum


class FeatureType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    GEOGRAPHIC = "geographic"
    EMBEDDING = "embedding"


class FeatureTransformer:
    @staticmethod
    def encode_cyclical_time(hour: int, day_of_week: int) -> Dict[str, float]:
        hour_angle = 2.0 * math.pi * hour / 24.0
        dow_angle = 2.0 * math.pi * day_of_week / 7.0

        return {
            "hour_sin": math.sin(hour_angle),
            "hour_cos": math.cos(hour_angle),
            "dow_sin": math.sin(dow_angle),
            "dow_cos": math.cos(dow_angle),
        }

    @staticmethod
    def robust_scale(value: float, median: float, iqr: float) -> float:
        if iqr == 0.0:
            return 0.0
        return (value - median) / iqr

    @staticmethod
    def log_transform(value: float) -> float:
        return float(math.log1p(max(0.0, value)))

    @staticmethod
    def normalize_vector(vector: List[float]) -> List[float]:
        arr = np.asarray(vector, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0.0:
            return vector
        return (arr / norm).tolist()
