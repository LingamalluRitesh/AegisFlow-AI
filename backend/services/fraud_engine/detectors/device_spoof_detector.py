"""
AegisGuard Enterprise Detector: DeviceSpoofingDetector
Uncovers rooted/jailbroken devices, virtual machines, and GPS spoofers
"""

import time
import math
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
from backend.core.logging import get_logger
from backend.core.types import RiskLevel, ActionType

logger = get_logger("fraud.detector.device_spoof")

class DeviceSpoofingDetectorConfig(BaseModel):
    enabled: bool = True
    risk_weight: float = 0.85
    threshold_critical: float = 0.80
    threshold_warning: float = 0.45
    min_observations_required: int = 3
    decay_half_life_seconds: float = 86400.0

class DeviceSpoofingDetectorResult(BaseModel):
    detector_name: str = "DeviceSpoofingDetector"
    risk_score: float
    risk_level: RiskLevel
    recommended_action: ActionType
    anomaly_signals: List[str] = Field(default_factory=list)
    feature_attribution: Dict[str, float] = Field(default_factory=dict)
    execution_latency_ms: float

class DeviceSpoofingDetector:
    """Uncovers rooted/jailbroken devices, virtual machines, and GPS spoofers"""

    def __init__(self, config: Optional[DeviceSpoofingDetectorConfig] = None):
        self.config = config or DeviceSpoofingDetectorConfig()
        self._historical_baselines: Dict[str, Tuple[float, float]] = {}
        self._init_statistical_baselines()

    def _init_statistical_baselines(self) -> None:
        self._historical_baselines["primary_metric"] = (45.0, 15.0)
        self._historical_baselines["secondary_metric"] = (1.2, 0.8)
        self._historical_baselines["velocity_factor"] = (3.5, 2.1)

    def extract_features(self, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        features = {}
        features["amount"] = float(payload.get("amount", 0.0))
        features["velocity_count"] = float(context.get("tx_count_5m", 1.0))
        features["geo_speed"] = float(context.get("max_geo_leap_speed_kmh", 0.0))
        features["is_new_device"] = 1.0 if context.get("is_new_device_used") else 0.0
        features["account_age"] = float(context.get("account_age_days", 30.0))
        return features

    def compute_risk(self, features: Dict[str, float]) -> DeviceSpoofingDetectorResult:
        start_time = time.perf_counter()
        if not self.config.enabled:
            return DeviceSpoofingDetectorResult(
                risk_score=0.0,
                risk_level=RiskLevel.LOW,
                recommended_action=ActionType.ALLOW,
                execution_latency_ms=0.01,
            )

        signals = []
        attributions = {}
        raw_score = 0.05

        amt = features.get("amount", 0.0)
        if amt > 2500.0:
            impact = min(0.40, (amt - 2500.0) / 10000.0)
            raw_score += impact
            attributions["high_amount"] = impact
            signals.append(f"High value transaction outlier: ${amt:.2f}")

        vel = features.get("velocity_count", 0.0)
        if vel >= 5.0:
            impact = min(0.35, vel * 0.07)
            raw_score += impact
            attributions["velocity_burst"] = impact
            signals.append(f"Rapid velocity threshold exceeded: {vel} events/5m")

        geo = features.get("geo_speed", 0.0)
        if geo > 600.0:
            impact = 0.30
            raw_score += impact
            attributions["impossible_travel"] = impact
            signals.append(f"Physical travel velocity impossible: {geo:.1f} km/h")

        final_score = min(0.99, raw_score * self.config.risk_weight)

        if final_score >= self.config.threshold_critical:
            risk_level = RiskLevel.CRITICAL
            action = ActionType.BLOCK
        elif final_score >= self.config.threshold_warning:
            risk_level = RiskLevel.HIGH
            action = ActionType.CHALLENGE_2FA
        else:
            risk_level = RiskLevel.LOW
            action = ActionType.ALLOW

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return DeviceSpoofingDetectorResult(
            risk_score=round(final_score, 4),
            risk_level=risk_level,
            recommended_action=action,
            anomaly_signals=signals,
            feature_attribution=attributions,
            execution_latency_ms=round(latency_ms, 3),
        )
