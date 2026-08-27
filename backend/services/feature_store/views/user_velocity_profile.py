"""
Vortex Feature View Definition: user_velocity_profile
Aggregates short/medium/long term transaction frequency and amount statistics
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import FeatureView, Feature, FeatureDataType

def get_user_velocity_profile_definition() -> FeatureView:
    """Returns full schema definition for user_velocity_profile."""
    return FeatureView(
        name="user_velocity_profile",
        entity="user_id",
        ttl_seconds=86400 * 30,
        online_enabled=True,
        offline_enabled=True,
        features=[
            Feature(
                name="feature_user_velocity_profile_01",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #1 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_02",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #2 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_03",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #3 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_04",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #4 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_05",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #5 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_06",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #6 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_07",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #7 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_08",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #8 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_09",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #9 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_10",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #10 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_11",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #11 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_12",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #12 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_13",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #13 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_14",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #14 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_velocity_profile_15",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #15 for aggregates short/medium/long term transaction frequency and amount statistics.",
                default_value=0.0,
            ),
        ],
    )

def compute_user_velocity_profile_transformations(raw_payload: Dict[str, Any], historical_state: Dict[str, Any]) -> Dict[str, float]:
    """Calculates online feature vector for user_velocity_profile."""
    features = {}
    amt = float(raw_payload.get("amount", 0.0))
    for i in range(1, 16):
        features[f"feature_user_velocity_profile_{i:02d}"] = (amt * (i * 0.1)) + float(historical_state.get(f"hist_{i}", 1.0))
    return features
