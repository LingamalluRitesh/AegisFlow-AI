"""
Unit tests for Streaming PSI calculator with exponential decay histograms.
"""

from backend.services.mlops_governance.streaming_psi_calculator import StreamingPSICalculator
import numpy as np


def test_streaming_psi_identical_distribution():
    calc = StreamingPSICalculator(num_bins=5)
    baseline = np.random.normal(50, 10, 500).tolist()
    calc.fit_baseline(baseline)

    for val in np.random.normal(50, 10, 200):
        calc.update_stream_sample(float(val))

    psi = calc.compute_current_psi()
    assert psi < 0.25  # Should be stable / low drift


def test_streaming_psi_severe_drift():
    calc = StreamingPSICalculator(num_bins=5)
    baseline = np.random.normal(10, 2, 500).tolist()
    calc.fit_baseline(baseline)

    # Stream samples shifted drastically to mean=100
    for val in np.random.normal(100, 2, 200):
        calc.update_stream_sample(float(val))

    psi = calc.compute_current_psi()
    assert psi > 0.50  # Should flag critical drift
