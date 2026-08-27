"""
Ultra-Low Latency Online Feature Store Client
Supports Redis Cluster pipelining and high-concurrency In-Memory fallback for sub-2ms lookups.
"""

import time
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import threading
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager

logger = get_logger("feature_store.online")


class OnlineStoreClient(ABC):
    @abstractmethod
    async def read_features(
        self,
        feature_view_name: str,
        entity_keys: List[str],
        feature_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def write_features(
        self,
        feature_view_name: str,
        features_by_entity: Dict[str, Dict[str, Any]],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        pass


class InMemoryOnlineStore(OnlineStoreClient):
    def __init__(self):
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    async def read_features(
        self,
        feature_view_name: str,
        entity_keys: List[str],
        feature_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        results = []
        start_time = time.perf_counter()

        with self._lock:
            view_store = self._store.get(feature_view_name, {})
            for ek in entity_keys:
                entity_feats = view_store.get(str(ek), {})
                if feature_names:
                    filtered = {fn: entity_feats.get(fn) for fn in feature_names}
                    results.append(filtered)
                else:
                    results.append(dict(entity_feats))

        latency = time.perf_counter() - start_time
        telemetry_manager.get_histogram("aegis_feature_retrieval_latency_seconds").observe(latency)
        return results

    async def write_features(
        self,
        feature_view_name: str,
        features_by_entity: Dict[str, Dict[str, Any]],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        with self._lock:
            if feature_view_name not in self._store:
                self._store[feature_view_name] = {}

            for ek, feats in features_by_entity.items():
                if str(ek) not in self._store[feature_view_name]:
                    self._store[feature_view_name][str(ek)] = {}
                self._store[feature_view_name][str(ek)].update(feats)

        telemetry_manager.get_counter("aegis_online_feature_cache_size").inc(len(features_by_entity))


class RedisOnlineStore(OnlineStoreClient):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._redis = None
        self._redis_disabled = False
        self._fallback = InMemoryOnlineStore()

    async def _get_connection(self):
        if self._redis_disabled:
            return None
        if self._redis is None:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=0.05,
                    socket_timeout=0.05,
                    retry_on_timeout=False,
                )
            except Exception as e:
                self._redis_disabled = True
                self._redis = None
        return self._redis

    async def read_features(
        self,
        feature_view_name: str,
        entity_keys: List[str],
        feature_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        client = await self._get_connection()
        if client is None:
            return await self._fallback.read_features(feature_view_name, entity_keys, feature_names)

        start_time = time.perf_counter()
        results = []

        try:
            pipe = client.pipeline()
            for key in entity_keys:
                redis_key = f"vortex:{feature_view_name}:{key}"
                if feature_names:
                    pipe.hmget(redis_key, feature_names)
                else:
                    pipe.hgetall(redis_key)

            raw_records = await pipe.execute()
            for record in raw_records:
                if isinstance(record, dict):
                    results.append({k: float(v) if str(v).replace('.', '', 1).isdigit() else v for k, v in record.items()})
                elif isinstance(record, list) and feature_names:
                    record_dict = {}
                    for fn, val in zip(feature_names, record):
                        if val is not None:
                            record_dict[fn] = float(val) if str(val).replace('.', '', 1).isdigit() else val
                    results.append(record_dict)
                else:
                    results.append({})

            latency = time.perf_counter() - start_time
            telemetry_manager.get_histogram("aegis_feature_retrieval_latency_seconds").observe(latency)
            return results

        except Exception as exc:
            self._redis_disabled = True
            logger.warn_ctx("Redis read error, falling back to local memory", error=str(exc))
            return await self._fallback.read_features(feature_view_name, entity_keys, feature_names)

    async def write_features(
        self,
        feature_view_name: str,
        features_by_entity: Dict[str, Dict[str, Any]],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        client = await self._get_connection()
        if client is None:
            await self._fallback.write_features(feature_view_name, features_by_entity, ttl_seconds)
            return

        try:
            pipe = client.pipeline()
            ttl = ttl_seconds or 86400 * 30
            for entity_key, feats in features_by_entity.items():
                redis_key = f"vortex:{feature_view_name}:{entity_key}"
                pipe.hset(redis_key, mapping={k: str(v) for k, v in feats.items()})
                pipe.expire(redis_key, ttl)

            await pipe.execute()

        except Exception as e:
            logger.error_ctx("Redis write failure, caching in local memory", exc=e)
            await self._fallback.write_features(feature_view_name, features_by_entity, ttl_seconds)
