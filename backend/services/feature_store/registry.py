"""
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
