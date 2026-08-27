import pytest
from backend.services.feature_store.registry import registry
from backend.services.feature_store.aggregations import SlidingWindowAggregator
from backend.services.feature_store.transformations import FeatureTransformer


def test_feature_registry_catalog():
    views = registry.list_feature_views()
    assert len(views) >= 3
    user_view = registry.get_feature_view("user_fraud_velocity_features")
    assert user_view is not None
    assert "tx_count_5m" in user_view.feature_names()


def test_sliding_window_aggregator():
    agg = SlidingWindowAggregator(entity_id="usr_agg_test")
    agg.add_event(100.0, amount=50.0)
    agg.add_event(110.0, amount=150.0)
    stats = agg.compute_window_stats(60, current_time=120.0)
    assert stats["count"] == 2.0
    assert stats["sum"] == 200.0
    assert stats["mean"] == 100.0


def test_feature_transformations():
    cyclical = FeatureTransformer.encode_cyclical_time(hour=12, day_of_week=3)
    assert "hour_sin" in cyclical
    assert "hour_cos" in cyclical
    scaled = FeatureTransformer.robust_scale(100.0, median=50.0, iqr=25.0)
    assert scaled == 2.0
