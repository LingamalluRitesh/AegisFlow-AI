"""
Real-Time Feature & Model Drift Detection Engine
Calculates Population Stability Index (PSI), Kolmogorov-Smirnov test statistic, and Wasserstein distance.
"""

from typing import Dict, List, Optional
from collections import deque
import threading
from pydantic import BaseModel
from backend.core.math_utils import (
    compute_population_stability_index,
    compute_kolmogorov_smirnov_statistic,
    compute_wasserstein_distance_1d,
)
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager

logger = get_logger("mlops.drift")


class FeatureDriftSummary(BaseModel):
    feature_name: str
    psi_score: float
    ks_statistic: float
    ks_pvalue: float
    wasserstein_distance: float
    sample_size: int
    status: str


class DriftDetector:
    def __init__(self, sample_window_size: int = 1000):
        self.sample_window_size = sample_window_size
        self._reference_distributions: Dict[str, List[float]] = {}
        self._current_buffers: Dict[str, deque] = {}
        self._lock = threading.Lock()
        self._init_default_baselines()

    def _init_default_baselines(self):
        import numpy as np
        rng = np.random.RandomState(42)
        self.set_reference_distribution("amount", rng.exponential(scale=75.0, size=500).tolist())
        self.set_reference_distribution("tx_count_5m", rng.poisson(lam=1.0, size=500).astype(float).tolist())
        self.set_reference_distribution("max_geo_leap_speed_kmh", rng.exponential(scale=20.0, size=500).tolist())

    def set_reference_distribution(self, feature_name: str, values: List[float]) -> None:
        with self._lock:
            self._reference_distributions[feature_name] = values
            if feature_name not in self._current_buffers:
                self._current_buffers[feature_name] = deque(maxlen=self.sample_window_size)

    def record_feature_observation(self, feature_name: str, value: float) -> None:
        with self._lock:
            if feature_name in self._current_buffers:
                self._current_buffers[feature_name].append(float(value))

    def evaluate_feature_drift(self, feature_name: str) -> Optional[FeatureDriftSummary]:
        with self._lock:
            ref_dist = self._reference_distributions.get(feature_name)
            curr_dist = list(self._current_buffers.get(feature_name, []))

        if not ref_dist or len(curr_dist) < 20:
            return None

        psi = compute_population_stability_index(ref_dist, curr_dist, num_bins=10)
        ks_stat, ks_pval = compute_kolmogorov_smirnov_statistic(ref_dist, curr_dist)
        wass = compute_wasserstein_distance_1d(ref_dist, curr_dist)

        status = "HEALTHY"
        if psi >= 0.25:
            status = "CRITICAL"
            logger.warn_ctx(f"CRITICAL Drift Detected for feature '{feature_name}': PSI={psi:.4f}")
        elif psi >= 0.10:
            status = "WARNING"

        telemetry_manager.get_gauge("aegis_model_drift_psi_score").set(psi, labels={"feature": feature_name})

        return FeatureDriftSummary(
            feature_name=feature_name,
            psi_score=round(psi, 4),
            ks_statistic=round(ks_stat, 4),
            ks_pvalue=round(ks_pval, 4),
            wasserstein_distance=round(wass, 4),
            sample_size=len(curr_dist),
            status=status,
        )

    def evaluate_all_features(self) -> List[FeatureDriftSummary]:
        results = []
        for feat in list(self._reference_distributions.keys()):
            summary = self.evaluate_feature_drift(feat)
            if summary:
                results.append(summary)
        return results


drift_detector = DriftDetector()
