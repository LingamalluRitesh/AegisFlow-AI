"""
Unit tests for Vortex As-Of Temporal Merge Engine.
"""

from backend.services.feature_store.asof_join_engine import AsOfTemporalJoinEngine


def test_asof_temporal_lookup_exact():
    engine = AsOfTemporalJoinEngine()
    engine.ingest_feature_record("user_vel", "usr_1", 100.0, {"tx_cnt": 1, "sum": 50.0})
    engine.ingest_feature_record("user_vel", "usr_1", 200.0, {"tx_cnt": 2, "sum": 150.0})
    engine.ingest_feature_record("user_vel", "usr_1", 300.0, {"tx_cnt": 5, "sum": 450.0})

    # Query before first event
    assert engine.point_in_time_lookup("user_vel", "usr_1", 50.0) is None

    # Query at exact timestamp 100
    res_100 = engine.point_in_time_lookup("user_vel", "usr_1", 100.0)
    assert res_100["tx_cnt"] == 1

    # Query between 100 and 200 (e.g. 150) -> should get state at 100
    res_150 = engine.point_in_time_lookup("user_vel", "usr_1", 150.0)
    assert res_150["tx_cnt"] == 1

    # Query at 250 -> should get state at 200
    res_250 = engine.point_in_time_lookup("user_vel", "usr_1", 250.0)
    assert res_250["tx_cnt"] == 2


def test_batch_asof_join_enrichment():
    engine = AsOfTemporalJoinEngine()
    engine.ingest_feature_record("user_vel", "usr_A", 100.0, {"risk_score": 0.12})
    engine.ingest_feature_record("user_vel", "usr_A", 200.0, {"risk_score": 0.85})

    driver_events = [
        {"tx_id": "tx_1", "user_id": "usr_A", "timestamp": 120.0, "amount": 25.0},
        {"tx_id": "tx_2", "user_id": "usr_A", "timestamp": 250.0, "amount": 900.0},
    ]

    joined = engine.batch_asof_join(driver_events, "user_vel")
    assert len(joined) == 2
    assert joined[0]["user_vel__risk_score"] == 0.12
    assert joined[1]["user_vel__risk_score"] == 0.85
