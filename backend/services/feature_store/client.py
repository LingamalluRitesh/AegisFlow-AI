"""
Unified Vortex Feature Store Client Gateway
Provides a seamless high-level API to retrieve features, register schemas, and write updates.
"""

from typing import Dict, Any, List, Optional
from backend.services.feature_store.registry import registry, FeatureRegistry
from backend.services.feature_store.online_store import OnlineStoreClient, RedisOnlineStore
from backend.services.feature_store.offline_store import OfflineStoreClient, DuckDBOfflineStore
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger("feature_store.client")


class VortexFeatureStoreClient:
    def __init__(
        self,
        registry_instance: Optional[FeatureRegistry] = None,
        online_store: Optional[OnlineStoreClient] = None,
        offline_store: Optional[OfflineStoreClient] = None,
    ):
        self.registry = registry_instance or registry
        self.online_store = online_store or RedisOnlineStore(redis_url=settings.redis.ONLINE_STORE_URL)
        self.offline_store = offline_store or DuckDBOfflineStore(data_lake_path=settings.feature_store.OFFLINE_DATA_LAKE_PATH)

    async def get_online_features(
        self,
        feature_view_name: str,
        entity_keys: List[str],
        feature_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        view = self.registry.get_feature_view(feature_view_name)
        raw_results = await self.online_store.read_features(feature_view_name, entity_keys, feature_names)

        hydrated = []
        for rec in raw_results:
            filled = dict(rec)
            if view:
                for f in view.features:
                    if (feature_names is None or f.name in feature_names) and f.name not in filled:
                        filled[f.name] = f.default_value
            hydrated.append(filled)

        return hydrated

    async def push_streaming_features(
        self,
        feature_view_name: str,
        features_by_entity: Dict[str, Dict[str, Any]],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        await self.online_store.write_features(feature_view_name, features_by_entity, ttl_seconds)


feature_store_client = VortexFeatureStoreClient()
