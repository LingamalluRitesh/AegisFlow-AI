"""
High-Performance Mathematical & Statistical Utilities for ML, Vectors, and Drift Detection
Implements fast cosine distance, Euclidean metrics, Population Stability Index (PSI),
and Kolmogorov-Smirnov test statistics without heavy native dependency lock-in.
"""

import math
from typing import List, Tuple, Sequence, Dict, Optional
import numpy as np


def vector_cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Computes cosine similarity between two float vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vector dimensions must match for cosine similarity.")
    
    a = np.asarray(vec_a, dtype=np.float32)
    b = np.asarray(vec_b, dtype=np.float32)
    
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    
    return float(np.dot(a, b) / (norm_a * norm_b))


def vector_euclidean_distance(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Computes Euclidean L2 distance between two vectors."""
    a = np.asarray(vec_a, dtype=np.float32)
    b = np.asarray(vec_b, dtype=np.float32)
    return float(np.linalg.norm(a - b))


def calculate_haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two geographic coordinates in kilometers.
    Crucial for velocity anomaly and impossible travel fraud checks.
    """
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_population_stability_index(
    expected_dist: Sequence[float],
    actual_dist: Sequence[float],
    num_bins: int = 10,
    epsilon: float = 1e-4
) -> float:
    """
    Calculates Population Stability Index (PSI) to detect feature and model prediction drift.
    PSI < 0.10: No significant change
    0.10 <= PSI < 0.25: Moderate change / warning
    PSI >= 0.25: Significant drift requiring retraining
    """
    if len(expected_dist) == 0 or len(actual_dist) == 0:
        return 0.0

    exp_arr = np.asarray(expected_dist, dtype=np.float64)
    act_arr = np.asarray(actual_dist, dtype=np.float64)

    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(exp_arr, percentiles)
    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf

    exp_counts, _ = np.histogram(exp_arr, bins=bin_edges)
    act_counts, _ = np.histogram(act_arr, bins=bin_edges)

    exp_pct = (exp_counts + epsilon) / (len(exp_arr) + epsilon * num_bins)
    act_pct = (act_counts + epsilon) / (len(act_arr) + epsilon * num_bins)

    psi_val = np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))
    return float(psi_val)


def compute_kolmogorov_smirnov_statistic(sample1: Sequence[float], sample2: Sequence[float]) -> Tuple[float, float]:
    """
    Computes two-sample Kolmogorov-Smirnov statistic D and asymptotic p-value.
    D represents the maximum difference between the cumulative empirical distributions.
    """
    s1 = np.sort(np.asarray(sample1, dtype=np.float64))
    s2 = np.sort(np.asarray(sample2, dtype=np.float64))
    n1 = len(s1)
    n2 = len(s2)

    if n1 == 0 or n2 == 0:
        return 0.0, 1.0

    data_all = np.concatenate([s1, s2])
    cdf1 = np.searchsorted(s1, data_all, side="right") / n1
    cdf2 = np.searchsorted(s2, data_all, side="right") / n2

    d_stat = float(np.max(np.abs(cdf1 - cdf2)))
    
    en = math.sqrt((n1 * n2) / (n1 + n2))
    lambda_val = (en + 0.12 + 0.11 / en) * d_stat
    
    p_val = 0.0
    for j in range(1, 101):
        term = 2 * ((-1) ** (j - 1)) * math.exp(-2 * (j ** 2) * (lambda_val ** 2))
        p_val += term
        if abs(term) < 1e-6:
            break
    p_val = max(0.0, min(1.0, p_val))

    return d_stat, p_val


def compute_wasserstein_distance_1d(u_values: Sequence[float], v_values: Sequence[float]) -> float:
    """
    Computes the First Wasserstein (Earth Mover's) distance between two 1D empirical distributions.
    """
    u = np.sort(np.asarray(u_values, dtype=np.float64))
    v = np.sort(np.asarray(v_values, dtype=np.float64))
    if len(u) == 0 or len(v) == 0:
        return 0.0

    all_vals = np.unique(np.concatenate([u, v]))
    u_cdf = np.searchsorted(u, all_vals, side="right") / len(u)
    v_cdf = np.searchsorted(v, all_vals, side="right") / len(v)

    deltas = np.diff(all_vals)
    return float(np.sum(np.abs(u_cdf[:-1] - v_cdf[:-1]) * deltas))
