"""
Database Models for Transactions, Fraud Evaluations, and Velocity State
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, JSON, ForeignKey, Enum as SQLEnum, Index
from backend.database.models.base import TimeStampedUUIDModel
from backend.core.types import RiskLevel, ActionType


class TransactionRecord(TimeStampedUUIDModel):
    """Persistent storage for all ingested financial transactions."""
    __tablename__ = "transactions"

    transaction_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    source_account_id = Column(String(64), nullable=False, index=True)
    target_account_id = Column(String(64), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="USD", nullable=False)
    merchant_id = Column(String(64), nullable=True, index=True)
    merchant_category_code = Column(String(16), nullable=True)
    device_id = Column(String(64), nullable=True, index=True)
    ip_address = Column(String(45), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    channel = Column(String(32), default="web")
    raw_payload = Column(JSON, default=dict)
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    __table_args__ = (
        Index("idx_tx_user_timestamp", "user_id", "event_timestamp"),
        Index("idx_tx_device_timestamp", "device_id", "event_timestamp"),
    )


class FraudEvaluationRecord(TimeStampedUUIDModel):
    """Persistent ledger of AegisGuard fraud scoring decisions and explainability data."""
    __tablename__ = "fraud_evaluations"

    transaction_id = Column(String(64), ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    risk_score = Column(Float, nullable=False, index=True)
    risk_level = Column(SQLEnum(RiskLevel), nullable=False, index=True)
    action = Column(SQLEnum(ActionType), nullable=False, index=True)
    triggered_rules = Column(JSON, default=list)
    reasons = Column(JSON, default=list)
    shap_values = Column(JSON, default=dict)
    feature_snapshot = Column(JSON, default=dict)
    latency_ms = Column(Float, nullable=False)
    model_version = Column(String(32), nullable=False)
    is_chargeback = Column(Integer, default=0, index=True)
    chargeback_reported_at = Column(DateTime(timezone=True), nullable=True)
