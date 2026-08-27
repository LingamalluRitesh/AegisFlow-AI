"""
Streaming Population Stability Index (PSI) with Exponential Decay Histograms
Computes dynamic distribution drift metrics over continuous unbounded event streams.
"""

from typing import List, Dict, Any, Tuple
import math
import numpy as np
from backend.core.logging import get_logger

logger = get_logger("mlops.streaming_psi")


class StreamingPSICalculator:
    """Computes streaming PSI against baseline reference bin quantiles."""

    def __init__(self, num_bins: int = 10, decay_alpha: float = 0.995):
        self.num_bins = num_bins
        self.decay_alpha = decay_alpha
        self._bin_edges: np.ndarray = np.array([])
        self._baseline_probs: np.ndarray = np.array([])
        self._streaming_counts: np.ndarray = np.zeros(num_bins, dtype=np.float64)

    def fit_baseline(self, baseline_samples: List[float]) -> None:
        arr = np.asarray(baseline_samples, dtype=np.float64)
        quantiles = np.linspace(0, 100, self.num_bins + 1)
        self._bin_edges = np.percentile(arr, quantiles)
        # Ensure unique bin edges
        self._bin_edges = np.unique(self._bin_edges)
        self.num_bins = len(self._bin_edges) - 1
        self._streaming_counts = np.zeros(self.num_bins, dtype=np.float64)

        hist, _ = np.histogram(arr, bins=self._bin_edges)
        total = np.sum(hist)
        self._baseline_probs = np.maximum(1e-5, hist / max(1.0, float(total)))

    def update_stream_sample(self, value: float) -> None:
        if len(self._bin_edges) < 2:
            return
        # Exponential decay
        self._streaming_counts *= self.decay_alpha
        bin_idx = np.digitize([value], self._bin_edges)[0] - 1
        bin_idx = max(0, min(self.num_bins - 1, bin_idx))
        self._streaming_counts[bin_idx] += 1.0

    def compute_current_psi(self) -> float:
        if len(self._bin_edges) < 2:
            return 0.0

        total = np.sum(self._streaming_counts)
        if total == 0:
            return 0.0

        actual_probs = np.maximum(1e-5, self._streaming_counts / total)
        # Formula: sum((Actual - Expected) * ln(Actual / Expected))
        psi_contributions = (actual_probs - self._baseline_probs) * np.log(actual_probs / self._baseline_probs)
        return float(np.sum(psi_contributions))


streaming_psi_calculator = StreamingPSICalculator()
