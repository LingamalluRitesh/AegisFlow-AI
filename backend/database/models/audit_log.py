"""
Cryptographically Hash-Chained Audit Ledger for SOC2 & GDPR Compliance
"""

from sqlalchemy import Column, String, Integer, JSON, Text, DateTime
from backend.database.models.base import TimeStampedUUIDModel


class AuditChainRecord(TimeStampedUUIDModel):
    """Immutable hash-linked audit block guaranteeing non-repudiation."""
    __tablename__ = "audit_chain_ledger"

    sequence_index = Column(Integer, unique=True, nullable=False, index=True)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), unique=True, nullable=False, index=True)
    actor_id = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    payload_json = Column(Text, nullable=False)
    hmac_signature = Column(String(64), nullable=False)
