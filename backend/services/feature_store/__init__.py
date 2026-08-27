"""
Vortex Feature Store: Unified Online and Offline Feature Store for Real-Time ML
Provides sub-millisecond online feature hydration and point-in-time correct offline joins.
"""

from backend.services.feature_store.registry import FeatureRegistry, FeatureView, Feature, Entity, registry
from backend.services.feature_store.online_store import OnlineStoreClient, RedisOnlineStore, InMemoryOnlineStore
from backend.services.feature_store.offline_store import OfflineStoreClient, DuckDBOfflineStore
from backend.services.feature_store.transformations import FeatureTransformer, FeatureType
from backend.services.feature_store.aggregations import SlidingWindowAggregator, AggregateFunction
from backend.services.feature_store.client import VortexFeatureStoreClient, feature_store_client

__all__ = [
    "FeatureRegistry",
    "FeatureView",
    "Feature",
    "Entity",
    "registry",
    "OnlineStoreClient",
    "RedisOnlineStore",
    "InMemoryOnlineStore",
    "OfflineStoreClient",
    "DuckDBOfflineStore",
    "FeatureTransformer",
    "FeatureType",
    "SlidingWindowAggregator",
    "AggregateFunction",
    "VortexFeatureStoreClient",
    "feature_store_client",
]
