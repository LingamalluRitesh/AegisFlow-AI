"""
Database Models for Feature Store Catalog, Schemas, and Drift Logs
"""

from sqlalchemy import Column, String, Integer, Float, JSON, Boolean, Text
from backend.database.models.base import TimeStampedUUIDModel


class FeatureViewDefinition(TimeStampedUUIDModel):
    """Registered Feature Views within Vortex Feature Store."""
    __tablename__ = "feature_views"

    name = Column(String(128), unique=True, nullable=False, index=True)
    entity_name = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=True)
    ttl_seconds = Column(Integer, default=86400)
    schema_definition = Column(JSON, nullable=False)
    transformation_code = Column(Text, nullable=True)
    online_enabled = Column(Boolean, default=True)
    offline_enabled = Column(Boolean, default=True)


class FeatureDriftRecord(TimeStampedUUIDModel):
    """Historical record of detected feature drift scores across time windows."""
    __tablename__ = "feature_drift_logs"

    feature_name = Column(String(128), nullable=False, index=True)
    feature_view = Column(String(128), nullable=False, index=True)
    psi_score = Column(Float, nullable=False)
    ks_statistic = Column(Float, nullable=True)
    ks_pvalue = Column(Float, nullable=True)
    wasserstein_distance = Column(Float, nullable=True)
    sample_count = Column(Integer, nullable=False)
    status = Column(String(32), default="HEALTHY")
    baseline_distribution = Column(JSON, default=list)
    current_distribution = Column(JSON, default=list)
