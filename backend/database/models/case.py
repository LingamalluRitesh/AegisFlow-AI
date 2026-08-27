"""
Database Models for Fraud Case Management & Investigation Workflow
"""

from sqlalchemy import Column, String, Float, Text, JSON, DateTime
from backend.database.models.base import TimeStampedUUIDModel


class FraudCaseModel(TimeStampedUUIDModel):
    """Analyst case management record for flagged financial transactions."""
    __tablename__ = "fraud_cases"

    case_number = Column(String(64), unique=True, nullable=False, index=True)
    transaction_id = Column(String(64), nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    severity = Column(String(32), default="HIGH", index=True)
    status = Column(String(32), default="OPEN", index=True)
    assigned_analyst = Column(String(64), nullable=True, index=True)
    risk_score = Column(Float, nullable=False)
    evidence_payload = Column(JSON, default=dict)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
