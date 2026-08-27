"""
Streaming Unsupervised Anomaly Detector
Evaluates multi-variate continuous feature vectors against expected baseline distributions.
"""

import math
from typing import Dict, Any
from backend.core.logging import get_logger

logger = get_logger("fraud.anomaly_detector")


class StreamingAnomalyDetector:
    def __init__(self):
        self._baselines = {
            "amount": (85.0, 120.0),
            "tx_count_5m": (0.8, 1.2),
            "tx_amount_sum_24h": (250.0, 400.0),
            "max_geo_leap_speed_kmh": (25.0, 60.0),
        }

    def score_features(self, feature_dict: Dict[str, Any]) -> float:
        z_scores = []

        for feature_name, (mean, std) in self._baselines.items():
            if feature_name in feature_dict and feature_dict[feature_name] is not None:
                val = float(feature_dict[feature_name])
                z = max(0.0, (val - mean) / max(1.0, std))
                z_scores.append(z)

        if not z_scores:
            return 0.05

        max_z = max(z_scores)
        mean_z = sum(z_scores) / len(z_scores)
        combined_z = 0.7 * max_z + 0.3 * mean_z

        anomaly_score = 1.0 / (1.0 + math.exp(-1.2 * (combined_z - 2.5)))
        return float(max(0.0, min(1.0, anomaly_score)))
