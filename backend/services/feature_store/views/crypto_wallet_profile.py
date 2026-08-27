"""
Vortex Feature View Definition: crypto_wallet_profile
Tracks blockchain address risk scores, mixer hops, and fiat on/off ramps
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import FeatureView, Feature, FeatureDataType

def get_crypto_wallet_profile_definition() -> FeatureView:
    """Returns full schema definition for crypto_wallet_profile."""
    return FeatureView(
        name="crypto_wallet_profile",
        entity="user_id",
        ttl_seconds=86400 * 30,
        online_enabled=True,
        offline_enabled=True,
        features=[
            Feature(
                name="feature_crypto_wallet_profile_01",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #1 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_02",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #2 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_03",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #3 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_04",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #4 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_05",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #5 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_06",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #6 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_07",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #7 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_08",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #8 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_09",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #9 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_10",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #10 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_11",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #11 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_12",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #12 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_13",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #13 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_14",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #14 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
            Feature(
                name="feature_crypto_wallet_profile_15",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #15 for tracks blockchain address risk scores, mixer hops, and fiat on/off ramps.",
                default_value=0.0,
            ),
        ],
    )

def compute_crypto_wallet_profile_transformations(raw_payload: Dict[str, Any], historical_state: Dict[str, Any]) -> Dict[str, float]:
    """Calculates online feature vector for crypto_wallet_profile."""
    features = {}
    amt = float(raw_payload.get("amount", 0.0))
    for i in range(1, 16):
        features[f"feature_crypto_wallet_profile_{i:02d}"] = (amt * (i * 0.1)) + float(historical_state.get(f"hist_{i}", 1.0))
    return features
