import pytest
from backend.core.prometheus_exporter import AegisMetricsRegistry


def test_prometheus_metrics_exporter():
    registry = AegisMetricsRegistry()
    registry.record_decision("APPROVE", 12.5)
    registry.record_decision("APPROVE", 14.0)
    registry.record_decision("DECLINE", 25.0)

    registry.record_cache_lookup(hit=True)
    registry.record_cache_lookup(hit=True)
    registry.record_cache_lookup(hit=False)

    summary = registry.get_summary()
    assert summary["total_evaluations"] == 3
    assert summary["decisions"]["APPROVE"] == 2
    assert summary["decisions"]["DECLINE"] == 1
    assert 0.60 <= summary["feature_cache_hit_rate"] <= 0.70

    prom = registry.export_prometheus()
    assert 'aegisflow_decisions_total{decision="APPROVE"} 2' in prom
    assert "aegisflow_feature_cache_hits_total 2" in prom
