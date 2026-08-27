"""
Vortex Feature View Definition: ip_network_profile
Maintains ASN reputation, VPN/proxy indicators, and IP geolocation volatility
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import FeatureView, Feature, FeatureDataType

def get_ip_network_profile_definition() -> FeatureView:
    """Returns full schema definition for ip_network_profile."""
    return FeatureView(
        name="ip_network_profile",
        entity="user_id",
        ttl_seconds=86400 * 30,
        online_enabled=True,
        offline_enabled=True,
        features=[
            Feature(
                name="feature_ip_network_profile_01",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #1 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_02",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #2 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_03",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #3 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_04",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #4 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_05",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #5 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_06",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #6 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_07",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #7 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_08",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #8 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_09",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #9 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_10",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #10 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_11",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #11 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_12",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #12 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_13",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #13 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_14",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #14 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
            Feature(
                name="feature_ip_network_profile_15",
                data_type=FeatureDataType.FLOAT,
                description="Computed statistical metric #15 for maintains asn reputation, vpn/proxy indicators, and ip geolocation volatility.",
                default_value=0.0,
            ),
        ],
    )

def compute_ip_network_profile_transformations(raw_payload: Dict[str, Any], historical_state: Dict[str, Any]) -> Dict[str, float]:
    """Calculates online feature vector for ip_network_profile."""
    features = {}
    amt = float(raw_payload.get("amount", 0.0))
    for i in range(1, 16):
        features[f"feature_ip_network_profile_{i:02d}"] = (amt * (i * 0.1)) + float(historical_state.get(f"hist_{i}", 1.0))
    return features
