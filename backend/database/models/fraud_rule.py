"""
Database Models for Dynamic CEP Fraud Rules and Rule Audits
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, Text
from backend.database.models.base import TimeStampedUUIDModel
from backend.core.types import RiskLevel, ActionType


class FraudRuleModel(TimeStampedUUIDModel):
    """Dynamic Complex Event Processing (CEP) Rule definition."""
    __tablename__ = "fraud_rules"

    rule_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=100, nullable=False)
    condition_expression = Column(Text, nullable=False)
    compiled_ast_json = Column(JSON, default=dict)
    action = Column(String(32), default=ActionType.BLOCK.value, nullable=False)
    risk_score_override = Column(Float, nullable=True)
    is_enabled = Column(Boolean, default=True, nullable=False)
    total_evaluations = Column(Integer, default=0)
    total_triggers = Column(Integer, default=0)
    created_by = Column(String(64), default="system")
