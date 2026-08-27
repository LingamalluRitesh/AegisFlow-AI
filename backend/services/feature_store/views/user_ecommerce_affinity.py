"""
Vortex Feature View Definition: user_ecommerce_affinity
Captures long-term category preferences, price sensitivity, and brand affinities
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import FeatureView, Feature, FeatureDataType

def get_user_ecommerce_affinity_definition() -> FeatureView:
    """Returns full schema definition for user_ecommerce_affinity."""
    return FeatureView(
        name="user_ecommerce_affinity",
        entity="user_id",
        ttl_seconds=86400 * 30,
        online_enabled=True,
        offline_enabled=True,
        features=[
            Feature(
                name="feature_user_ecommerce_affinity_01",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #1 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_02",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #2 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_03",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #3 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_04",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #4 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_05",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #5 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_06",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #6 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_07",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #7 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_08",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #8 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_09",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #9 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_10",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #10 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_11",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #11 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_12",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #12 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_13",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #13 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_14",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #14 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
            Feature(
                name="feature_user_ecommerce_affinity_15",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #15 for captures long-term category preferences, price sensitivity, and brand affinities.",
                default_value=0.0,
            ),
        ],
    )

def compute_user_ecommerce_affinity_transformations(raw_payload: Dict[str, Any], historical_state: Dict[str, Any]) -> Dict[str, float]:
    """Calculates online feature vector for user_ecommerce_affinity."""
    features = {}
    amt = float(raw_payload.get("amount", 0.0))
    for i in range(1, 16):
        features[f"feature_user_ecommerce_affinity_{i:02d}"] = (amt * (i * 0.1)) + float(historical_state.get(f"hist_{i}", 1.0))
    return features
