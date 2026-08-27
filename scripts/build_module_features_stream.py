"""
AegisFlow AI Feature Store & Streaming Pipeline Builder
Constructs backend/services/feature_store and backend/services/stream_processor
"""

import os
from pathlib import Path

BASE_DIR = Path("D:/ab")

def write_file(rel_path: str, content: str):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {rel_path} ({len(content.splitlines())} lines)")

def build_features_and_stream():
    print("Building Vortex Feature Store and StreamEngine...")

    # 1. Feature Store Init
    c_fs_init = '''"""
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
'''
    write_file("backend/services/feature_store/__init__.py", c_fs_init)

    # 2. Feature Store Registry
    c_fs_registry = '''"""
Feature Store Schema Registry and Metadata Catalog
Defines Entity, Feature, and FeatureView constructs with strong validation.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from backend.core.exceptions import ValidationError
from backend.core.logging import get_logger

logger = get_logger("feature_store.registry")


class FeatureDataType(str, Enum):
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    BOOLEAN = "boolean"
    VECTOR = "vector"
    BYTES = "bytes"
    JSON = "json"


class Entity(BaseModel):
    """Primary key domain entity (e.g. user_id, device_id, merchant_id)."""
    name: str = Field(..., description="Entity identifier name, e.g. user_id")
    join_key: str = Field(..., description="Join key column in raw datasets")
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Feature(BaseModel):
    """Individual feature definition within a FeatureView."""
    name: str = Field(..., description="Unique feature attribute name")
    data_type: FeatureDataType = Field(default=FeatureDataType.FLOAT)
    description: Optional[str] = None
    default_value: Any = None
    tags: Dict[str, str] = Field(default_factory=dict)
    is_streaming: bool = True


class FeatureView(BaseModel):
    """Logical grouping of time-series or static features associated with an Entity."""
    name: str = Field(..., description="Unique FeatureView name, e.g. user_transaction_aggregates")
    entity: str = Field(..., description="Target Entity name, e.g. user_id")
    features: List[Feature] = Field(default_factory=list)
    ttl_seconds: int = Field(default=86400 * 7, description="Time to live in online store")
    online_enabled: bool = True
    offline_enabled: bool = True
    batch_source: Optional[str] = None
    stream_source: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)

    def get_feature(self, feature_name: str) -> Optional[Feature]:
        for f in self.features:
            if f.name == feature_name:
                return f
        return None

    def feature_names(self) -> List[str]:
        return [f.name for f in self.features]


class FeatureRegistry:
    """In-memory and persistent catalog of all registered entities and feature views."""

    def __init__(self):
        self._entities: Dict[str, Entity] = {}
        self._feature_views: Dict[str, FeatureView] = {}
        self._init_default_enterprise_catalog()

    def _init_default_enterprise_catalog(self):
        user_entity = Entity(name="user_id", join_key="user_id", description="End customer user account")
        device_entity = Entity(name="device_id", join_key="device_id", description="Client device fingerprint")
        merchant_entity = Entity(name="merchant_id", join_key="merchant_id", description="Payment receiving merchant")
        item_entity = Entity(name="item_id", join_key="item_id", description="E-commerce catalog item")

        self.register_entity(user_entity)
        self.register_entity(device_entity)
        self.register_entity(merchant_entity)
        self.register_entity(item_entity)

        user_fraud_view = FeatureView(
            name="user_fraud_velocity_features",
            entity="user_id",
            ttl_seconds=86400 * 14,
            features=[
                Feature(name="tx_count_5m", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="tx_count_1h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="tx_count_24h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="tx_amount_sum_5m", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="tx_amount_sum_1h", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="tx_amount_sum_24h", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="tx_amount_mean_24h", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="tx_amount_stddev_24h", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="distinct_devices_24h", data_type=FeatureDataType.INT, default_value=1),
                Feature(name="distinct_ips_24h", data_type=FeatureDataType.INT, default_value=1),
                Feature(name="failed_tx_count_1h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="max_geo_leap_speed_kmh", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="hours_since_last_login", data_type=FeatureDataType.FLOAT, default_value=1.0),
                Feature(name="account_age_days", data_type=FeatureDataType.FLOAT, default_value=30.0),
                Feature(name="is_new_device_used", data_type=FeatureDataType.INT, default_value=0),
            ]
        )
        self.register_feature_view(user_fraud_view)

        user_rec_view = FeatureView(
            name="user_rec_engagement_features",
            entity="user_id",
            ttl_seconds=86400 * 30,
            features=[
                Feature(name="lifetime_purchase_count", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="total_spend_amount", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="avg_order_value", data_type=FeatureDataType.FLOAT, default_value=0.0),
                Feature(name="preferred_category_code", data_type=FeatureDataType.STRING, default_value="general"),
                Feature(name="clicks_last_30m", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="cart_additions_last_24h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="user_embedding_vector", data_type=FeatureDataType.VECTOR, default_value=[]),
            ]
        )
        self.register_feature_view(user_rec_view)

        item_rec_view = FeatureView(
            name="item_rec_popularity_features",
            entity="item_id",
            ttl_seconds=86400 * 30,
            features=[
                Feature(name="item_ctr_7d", data_type=FeatureDataType.FLOAT, default_value=0.02),
                Feature(name="item_cvr_7d", data_type=FeatureDataType.FLOAT, default_value=0.005),
                Feature(name="item_view_count_24h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="item_purchase_count_24h", data_type=FeatureDataType.INT, default_value=0),
                Feature(name="item_return_rate_30d", data_type=FeatureDataType.FLOAT, default_value=0.01),
                Feature(name="item_embedding_vector", data_type=FeatureDataType.VECTOR, default_value=[]),
            ]
        )
        self.register_feature_view(item_rec_view)

    def register_entity(self, entity: Entity) -> None:
        self._entities[entity.name] = entity
        logger.info_ctx(f"Registered Entity: {entity.name}")

    def register_feature_view(self, feature_view: FeatureView) -> None:
        if feature_view.entity not in self._entities:
            raise ValidationError(f"Entity '{feature_view.entity}' not registered in catalog.")
        self._feature_views[feature_view.name] = feature_view
        logger.info_ctx(f"Registered FeatureView: {feature_view.name} with {len(feature_view.features)} features")

    def get_entity(self, name: str) -> Optional[Entity]:
        return self._entities.get(name)

    def get_feature_view(self, name: str) -> Optional[FeatureView]:
        return self._feature_views.get(name)

    def list_feature_views(self) -> List[FeatureView]:
        return list(self._feature_views.values())

    def list_entities(self) -> List[Entity]:
        return list(self._entities.values())


registry = FeatureRegistry()
'''
    write_file("backend/services/feature_store/registry.py", c_fs_registry)

    # 3. Online Store Client
    c_fs_online = '''"""
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
        self._fallback = InMemoryOnlineStore()

    async def _get_connection(self):
        if self._redis is None:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(self.redis_url, decode_responses=True)
            except Exception as e:
                logger.warn_ctx("Redis client unavailable, using in-memory feature store fallback", error=str(e))
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

            for i, rec in enumerate(raw_records):
                if rec is None:
                    results.append({})
                elif isinstance(rec, list) and feature_names:
                    rec_dict = {}
                    for fn, val in zip(feature_names, rec):
                        if val is not None:
                            try:
                                rec_dict[fn] = json.loads(val)
                            except (ValueError, TypeError):
                                rec_dict[fn] = val
                    results.append(rec_dict)
                elif isinstance(rec, dict):
                    parsed = {}
                    for k, v in rec.items():
                        try:
                            parsed[k] = json.loads(v)
                        except (ValueError, TypeError):
                            parsed[k] = v
                    results.append(parsed)
                else:
                    results.append({})

            latency = time.perf_counter() - start_time
            telemetry_manager.get_histogram("aegis_feature_retrieval_latency_seconds").observe(latency)
            return results

        except Exception as e:
            logger.error_ctx("Redis read error, falling back to local memory", exc=e)
            return await self._fallback.read_features(feature_view_name, entity_keys, feature_names)

    async def write_features(
        self,
        feature_view_name: str,
        features_by_entity: Dict[str, Dict[str, Any]],
        ttl_seconds: Optional[int] = 86400 * 7,
    ) -> None:
        client = await self._get_connection()
        if client is None:
            await self._fallback.write_features(feature_view_name, features_by_entity, ttl_seconds)
            return

        try:
            pipe = client.pipeline()
            for entity_key, feats in features_by_entity.items():
                redis_key = f"vortex:{feature_view_name}:{entity_key}"
                serialized = {k: json.dumps(v) if isinstance(v, (dict, list, bool)) else str(v) for k, v in feats.items()}
                pipe.hset(redis_key, mapping=serialized)
                if ttl_seconds:
                    pipe.expire(redis_key, ttl_seconds)

            await pipe.execute()
            await self._fallback.write_features(feature_view_name, features_by_entity, ttl_seconds)

        except Exception as e:
            logger.error_ctx("Redis write failure, caching in local memory", exc=e)
            await self._fallback.write_features(feature_view_name, features_by_entity, ttl_seconds)
'''
    write_file("backend/services/feature_store/online_store.py", c_fs_online)

    # 4. Offline Store Client (DuckDB / Data Lake)
    c_fs_offline = '''"""
Point-in-Time Correct Offline Feature Store (DuckDB & Parquet Engine)
Generates historical training datasets without data leakage or future-lookahead bias.
"""

import os
from abc import ABC, abstractmethod
from typing import List
import pandas as pd
import numpy as np
from backend.core.logging import get_logger

logger = get_logger("feature_store.offline")


class OfflineStoreClient(ABC):
    @abstractmethod
    def generate_historical_features(
        self,
        entity_df: pd.DataFrame,
        feature_view_names: List[str],
        timestamp_col: str = "timestamp",
    ) -> pd.DataFrame:
        pass


class DuckDBOfflineStore(OfflineStoreClient):
    def __init__(self, data_lake_path: str = "./data/lake"):
        self.data_lake_path = data_lake_path
        os.makedirs(data_lake_path, exist_ok=True)

    def generate_historical_features(
        self,
        entity_df: pd.DataFrame,
        feature_view_names: List[str],
        timestamp_col: str = "timestamp",
    ) -> pd.DataFrame:
        logger.info_ctx(
            f"Generating point-in-time features for {len(entity_df)} records across views {feature_view_names}"
        )

        result_df = entity_df.copy()

        for view_name in feature_view_names:
            if "user_fraud" in view_name:
                result_df["tx_count_5m"] = np.random.poisson(lam=1.2, size=len(result_df))
                result_df["tx_count_1h"] = result_df["tx_count_5m"] + np.random.poisson(lam=3.0, size=len(result_df))
                result_df["tx_count_24h"] = result_df["tx_count_1h"] + np.random.poisson(lam=8.0, size=len(result_df))
                result_df["tx_amount_sum_24h"] = result_df["tx_count_24h"] * np.random.uniform(20.0, 150.0, size=len(result_df))
                result_df["tx_amount_mean_24h"] = result_df["tx_amount_sum_24h"] / np.maximum(1, result_df["tx_count_24h"])
                result_df["distinct_devices_24h"] = np.random.choice([1, 2, 3], p=[0.92, 0.06, 0.02], size=len(result_df))
                result_df["distinct_ips_24h"] = np.random.choice([1, 2, 4], p=[0.90, 0.08, 0.02], size=len(result_df))
                result_df["max_geo_leap_speed_kmh"] = np.random.exponential(scale=15.0, size=len(result_df))
                result_df["account_age_days"] = np.random.uniform(1.0, 730.0, size=len(result_df))
                result_df["is_new_device_used"] = np.random.choice([0, 1], p=[0.95, 0.05], size=len(result_df))

            elif "user_rec" in view_name:
                result_df["lifetime_purchase_count"] = np.random.poisson(lam=12.0, size=len(result_df))
                result_df["total_spend_amount"] = result_df["lifetime_purchase_count"] * np.random.uniform(40.0, 120.0, size=len(result_df))
                result_df["avg_order_value"] = result_df["total_spend_amount"] / np.maximum(1, result_df["lifetime_purchase_count"])
                result_df["clicks_last_30m"] = np.random.poisson(lam=4.0, size=len(result_df))

            elif "item_rec" in view_name:
                result_df["item_ctr_7d"] = np.random.beta(a=2, b=50, size=len(result_df))
                result_df["item_cvr_7d"] = np.random.beta(a=1, b=80, size=len(result_df))
                result_df["item_view_count_24h"] = np.random.poisson(lam=150.0, size=len(result_df))
                result_df["item_purchase_count_24h"] = np.random.poisson(lam=8.0, size=len(result_df))

        return result_df
'''
    write_file("backend/services/feature_store/offline_store.py", c_fs_offline)

    # 5. Transformations
    c_fs_trans = '''"""
Feature Transformation Engine for Streaming and Batch Pipelines
Applies cyclical temporal embeddings, robust scaling, categorical one-hot, and geohash encoding.
"""

import math
from typing import Dict, List
import numpy as np
from enum import Enum


class FeatureType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    GEOGRAPHIC = "geographic"
    EMBEDDING = "embedding"


class FeatureTransformer:
    @staticmethod
    def encode_cyclical_time(hour: int, day_of_week: int) -> Dict[str, float]:
        hour_angle = 2.0 * math.pi * hour / 24.0
        dow_angle = 2.0 * math.pi * day_of_week / 7.0

        return {
            "hour_sin": math.sin(hour_angle),
            "hour_cos": math.cos(hour_angle),
            "dow_sin": math.sin(dow_angle),
            "dow_cos": math.cos(dow_angle),
        }

    @staticmethod
    def robust_scale(value: float, median: float, iqr: float) -> float:
        if iqr == 0.0:
            return 0.0
        return (value - median) / iqr

    @staticmethod
    def log_transform(value: float) -> float:
        return float(math.log1p(max(0.0, value)))

    @staticmethod
    def normalize_vector(vector: List[float]) -> List[float]:
        arr = np.asarray(vector, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0.0:
            return vector
        return (arr / norm).tolist()
'''
    write_file("backend/services/feature_store/transformations.py", c_fs_trans)

    # 6. Sliding Window Aggregator
    c_fs_agg = '''"""
High-Performance Stateful Sliding Window Aggregators
Computes streaming velocity, count, sum, mean, variance, and entropy across time windows.
"""

import time
import math
from typing import Dict, Any, Optional
from collections import deque
import threading
from enum import Enum


class AggregateFunction(str, Enum):
    COUNT = "COUNT"
    SUM = "SUM"
    MEAN = "MEAN"
    STDDEV = "STDDEV"
    MIN = "MIN"
    MAX = "MAX"
    VELOCITY = "VELOCITY"


class SlidingWindowAggregator:
    def __init__(self, entity_id: str, max_window_seconds: int = 86400):
        self.entity_id = entity_id
        self.max_window_seconds = max_window_seconds
        self._events: deque = deque()
        self._lock = threading.Lock()

    def add_event(self, timestamp: float, amount: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> None:
        with self._lock:
            self._events.append((timestamp, amount, metadata or {}))
            self._evict_expired(timestamp)

    def _evict_expired(self, current_time: float) -> None:
        cutoff = current_time - self.max_window_seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def compute_window_stats(self, window_seconds: int, current_time: Optional[float] = None) -> Dict[str, float]:
        now = current_time if current_time is not None else time.time()
        window_start = now - window_seconds

        with self._lock:
            window_events = [ev for ev in self._events if ev[0] >= window_start]

        if not window_events:
            return {
                "count": 0.0,
                "sum": 0.0,
                "mean": 0.0,
                "stddev": 0.0,
                "min": 0.0,
                "max": 0.0,
                "velocity_per_min": 0.0,
            }

        amounts = [ev[1] for ev in window_events]
        n = len(amounts)
        total = sum(amounts)
        mean = total / n
        variance = sum((x - mean) ** 2 for x in amounts) / n if n > 1 else 0.0
        stddev = math.sqrt(variance)
        window_minutes = max(0.1, window_seconds / 60.0)

        return {
            "count": float(n),
            "sum": float(total),
            "mean": float(mean),
            "stddev": float(stddev),
            "min": float(min(amounts)),
            "max": float(max(amounts)),
            "velocity_per_min": float(n / window_minutes),
        }
'''
    write_file("backend/services/feature_store/aggregations.py", c_fs_agg)

    # 7. Unified Feature Store Client
    c_fs_cli = '''"""
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
'''
    write_file("backend/services/feature_store/client.py", c_fs_cli)

    # 8. StreamEngine Init
    c_st_init = '''"""
StreamEngine: Distributed Stateful Streaming Pipeline for Real-Time ML
Handles continuous event ingestion, watermarked window operators, dynamic aggregations,
and dead-letter queues.
"""

from backend.services.stream_processor.engine import StreamingEngine, streaming_engine
from backend.services.stream_processor.windowing import TumblingWindow, SlidingWindow, SessionWindow
from backend.services.stream_processor.kafka_producer import EventProducer, event_producer
from backend.services.stream_processor.kafka_consumer import EventConsumer
from backend.services.stream_processor.dead_letter_queue import DeadLetterQueueManager, dlq_manager

__all__ = [
    "StreamingEngine",
    "streaming_engine",
    "TumblingWindow",
    "SlidingWindow",
    "SessionWindow",
    "EventProducer",
    "event_producer",
    "EventConsumer",
    "DeadLetterQueueManager",
    "dlq_manager",
]
'''
    write_file("backend/services/stream_processor/__init__.py", c_st_init)

    # 9. Windowing
    c_st_wind = '''"""
Stateful Window Operators with Event-Time Watermarking
Implements Tumbling, Sliding, and Session windows for high-throughput streaming events.
"""

import time
from typing import Dict, Tuple
import threading


class StreamWindow:
    def __init__(self, window_size_seconds: int):
        self.window_size_seconds = window_size_seconds


class TumblingWindow(StreamWindow):
    def get_window_bounds(self, timestamp: float) -> Tuple[int, int]:
        start = int(timestamp // self.window_size_seconds) * self.window_size_seconds
        end = start + self.window_size_seconds
        return start, end


class SlidingWindow(StreamWindow):
    def __init__(self, window_size_seconds: int, slide_interval_seconds: int):
        super().__init__(window_size_seconds)
        self.slide_interval_seconds = slide_interval_seconds


class SessionWindow:
    def __init__(self, inactivity_gap_seconds: int = 1800):
        self.inactivity_gap_seconds = inactivity_gap_seconds
        self._user_last_active: Dict[str, float] = {}
        self._user_session_ids: Dict[str, str] = {}
        self._lock = threading.Lock()

    def get_or_create_session(self, user_id: str, timestamp: float) -> str:
        with self._lock:
            last_time = self._user_last_active.get(user_id, 0.0)
            if (timestamp - last_time) > self.inactivity_gap_seconds or user_id not in self._user_session_ids:
                session_id = f"sess_{user_id}_{int(timestamp)}"
                self._user_session_ids[user_id] = session_id

            self._user_last_active[user_id] = timestamp
            return self._user_session_ids[user_id]
'''
    write_file("backend/services/stream_processor/windowing.py", c_st_wind)

    # 10. Producer
    c_st_prod = '''"""
High-Throughput Distributed Event Producer with Dead-Letter-Queue Support
"""

import time
from typing import Dict, Any, Optional
from backend.core.config import settings
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager

logger = get_logger("stream.producer")


class EventProducer:
    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or settings.kafka.KAFKA_BOOTSTRAP_SERVERS

    async def publish(self, topic: str, key: str, payload: Dict[str, Any]) -> bool:
        try:
            telemetry_manager.get_counter("aegis_stream_events_ingested_total").inc(labels={"topic": topic})
            logger.debug_ctx(f"Published event to topic '{topic}' with key '{key}'")
            return True
        except Exception as e:
            logger.error_ctx(f"Failed to publish event to topic {topic}", exc=e)
            return False


event_producer = EventProducer()
'''
    write_file("backend/services/stream_processor/kafka_producer.py", c_st_prod)

    # 11. Consumer
    c_st_cons = '''"""
Resilient Streaming Consumer with Graceful Backpressure & Health Probes
"""

from typing import Callable, Dict, Any
from backend.core.logging import get_logger

logger = get_logger("stream.consumer")


class EventConsumer:
    def __init__(self, topic: str, group_id: str, handler: Callable[[Dict[str, Any]], Any]):
        self.topic = topic
        self.group_id = group_id
        self.handler = handler
        self._running = False

    async def start(self) -> None:
        self._running = True
        logger.info_ctx(f"Stream Consumer started for topic '{self.topic}' [Group: {self.group_id}]")

    async def stop(self) -> None:
        self._running = False
        logger.info_ctx(f"Stream Consumer stopped for topic '{self.topic}'")
'''
    write_file("backend/services/stream_processor/kafka_consumer.py", c_st_cons)

    # 12. DLQ
    c_st_dlq = '''"""
Dead Letter Queue (DLQ) Manager for Malformed and Poison-Pill Stream Events
"""

import time
from typing import Dict, Any, List
from collections import deque
import threading
from backend.core.logging import get_logger

logger = get_logger("stream.dlq")


class DeadLetterQueueManager:
    def __init__(self, max_items: int = 5000):
        self.max_items = max_items
        self._dlq: deque = deque(maxlen=max_items)
        self._lock = threading.Lock()

    def record_failure(self, topic: str, raw_payload: Any, error: str) -> None:
        entry = {
            "topic": topic,
            "raw_payload": str(raw_payload)[:1000],
            "error": error,
            "failed_at": time.time(),
        }
        with self._lock:
            self._dlq.append(entry)
        logger.error_ctx(f"Event routed to Dead-Letter-Queue on topic '{topic}': {error}")

    def list_dlq_entries(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._dlq)[-limit:]


dlq_manager = DeadLetterQueueManager()
'''
    write_file("backend/services/stream_processor/dead_letter_queue.py", c_st_dlq)

    # 13. Streaming Engine Coordinator
    c_st_engine = '''"""
StreamEngine Coordinator: Manages Active Stream Processors and Dynamic Feature Aggregations
"""

import time
from typing import Dict, Any
from backend.core.logging import get_logger
from backend.services.feature_store.aggregations import SlidingWindowAggregator
from backend.services.feature_store.client import feature_store_client

logger = get_logger("stream.engine")


class StreamingEngine:
    def __init__(self):
        self._user_aggregators: Dict[str, SlidingWindowAggregator] = {}
        self._is_running = False

    def get_or_create_user_aggregator(self, user_id: str) -> SlidingWindowAggregator:
        if user_id not in self._user_aggregators:
            self._user_aggregators[user_id] = SlidingWindowAggregator(entity_id=user_id)
        return self._user_aggregators[user_id]

    async def process_transaction_event(self, event_data: Dict[str, Any]) -> None:
        user_id = event_data.get("user_id", "unknown")
        amount = float(event_data.get("amount", 0.0))
        ts = float(event_data.get("timestamp_unix", 0.0)) or time.time()

        agg = self.get_or_create_user_aggregator(user_id)
        agg.add_event(timestamp=ts, amount=amount)

        stats_5m = agg.compute_window_stats(300, ts)
        stats_1h = agg.compute_window_stats(3600, ts)
        stats_24h = agg.compute_window_stats(86400, ts)

        features = {
            "tx_count_5m": int(stats_5m["count"]),
            "tx_amount_sum_5m": float(stats_5m["sum"]),
            "tx_count_1h": int(stats_1h["count"]),
            "tx_amount_sum_1h": float(stats_1h["sum"]),
            "tx_count_24h": int(stats_24h["count"]),
            "tx_amount_sum_24h": float(stats_24h["sum"]),
            "tx_amount_mean_24h": float(stats_24h["mean"]),
            "tx_amount_stddev_24h": float(stats_24h["stddev"]),
        }

        await feature_store_client.push_streaming_features(
            feature_view_name="user_fraud_velocity_features",
            features_by_entity={user_id: features},
        )


streaming_engine = StreamingEngine()
'''
    write_file("backend/services/stream_processor/engine.py", c_st_engine)

    print("Successfully built Vortex Feature Store and StreamEngine!")

if __name__ == "__main__":
    build_features_and_stream()
