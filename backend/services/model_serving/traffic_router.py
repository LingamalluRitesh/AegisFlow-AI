"""
Canary & Shadow Traffic Splitter
Safely routes inference traffic across Production, Canary, and Shadow model deployments.
"""

import random
from typing import Dict, Tuple
from enum import Enum


class DeploymentStrategy(str, Enum):
    DIRECT = "DIRECT"
    CANARY = "CANARY"
    SHADOW = "SHADOW"
    AB_TEST = "AB_TEST"


class TrafficRouter:
    def __init__(self):
        self._canary_weights: Dict[str, float] = {}

    def set_canary_weight(self, model_id: str, percentage: float) -> None:
        self._canary_weights[model_id] = max(0.0, min(100.0, percentage))

    def route_request(self, model_id: str) -> Tuple[str, bool]:
        canary_pct = self._canary_weights.get(model_id, 0.0)
        if canary_pct > 0 and random.uniform(0, 100) < canary_pct:
            return "canary", False
        return "primary", False


traffic_router = TrafficRouter()
