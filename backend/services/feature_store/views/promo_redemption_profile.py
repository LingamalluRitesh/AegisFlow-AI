"""
Vortex Feature View Definition: promo_redemption_profile
Tracks referral coupon redemptions and promotion multi-accounting vectors
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import FeatureView, Feature, FeatureDataType

def get_promo_redemption_profile_definition() -> FeatureView:
    """Returns full schema definition for promo_redemption_profile."""
    return FeatureView(
        name="promo_redemption_profile",
        entity="user_id",
        ttl_seconds=86400 * 30,
        online_enabled=True,
        offline_enabled=True,
        features=[
            Feature(
                name="feature_promo_redemption_profile_01",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #1 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_02",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #2 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_03",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #3 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_04",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #4 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_05",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #5 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_06",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #6 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_07",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #7 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_08",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #8 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_09",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #9 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_10",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #10 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_11",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #11 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_12",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #12 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_13",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #13 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_14",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #14 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
            Feature(
                name="feature_promo_redemption_profile_15",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #15 for tracks referral coupon redemptions and promotion multi-accounting vectors.",
                default_value=0.0,
            ),
        ],
    )

def compute_promo_redemption_profile_transformations(raw_payload: Dict[str, Any], historical_state: Dict[str, Any]) -> Dict[str, float]:
    """Calculates online feature vector for promo_redemption_profile."""
    features = {}
    amt = float(raw_payload.get("amount", 0.0))
    for i in range(1, 16):
        features[f"feature_promo_redemption_profile_{i:02d}"] = (amt * (i * 0.1)) + float(historical_state.get(f"hist_{i}", 1.0))
    return features
