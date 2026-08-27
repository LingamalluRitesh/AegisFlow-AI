"""
Database Models for Items, User Interactions, and Bandit Prior States
"""

from sqlalchemy import Column, String, Float, Integer, JSON, Index, Text
from backend.database.models.base import TimeStampedUUIDModel


class CatalogItemModel(TimeStampedUUIDModel):
    """Catalog items eligible for recommendation and vector indexing."""
    __tablename__ = "catalog_items"

    item_id = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    sub_category = Column(String(64), nullable=True)
    brand = Column(String(64), nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, default=1)
    tags = Column(JSON, default=list)
    embedding = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)


class UserInteractionModel(TimeStampedUUIDModel):
    """Stream of user clicks, views, cart additions, and purchases for model training."""
    __tablename__ = "user_interactions"

    user_id = Column(String(64), nullable=False, index=True)
    session_id = Column(String(64), nullable=True, index=True)
    item_id = Column(String(64), nullable=False, index=True)
    interaction_type = Column(String(32), nullable=False, index=True)
    reward_value = Column(Float, default=1.0)
    context_json = Column(JSON, default=dict)

    __table_args__ = (
        Index("idx_user_interaction_time", "user_id", "created_at"),
    )


class BanditArmModel(TimeStampedUUIDModel):
    """Contextual Multi-Armed Bandit Prior parameters for Thompson Sampling and LinUCB."""
    __tablename__ = "bandit_arms"

    arm_id = Column(String(64), unique=True, nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    total_impressions = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    alpha_prior = Column(Float, default=1.0)
    beta_prior = Column(Float, default=1.0)
    a_matrix_json = Column(JSON, default=list)
    b_vector_json = Column(JSON, default=list)
