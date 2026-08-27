"""
Transaction and Fraud Evaluation Data Access Repository
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.database.models.transaction import TransactionRecord, FraudEvaluationRecord
from backend.database.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[TransactionRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(TransactionRecord, session)

    async def get_by_transaction_id(self, tx_id: str) -> Optional[TransactionRecord]:
        stmt = select(TransactionRecord).where(TransactionRecord.transaction_id == tx_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_recent_user_transactions(self, user_id: str, limit: int = 50) -> List[TransactionRecord]:
        stmt = (
            select(TransactionRecord)
            .where(TransactionRecord.user_id == user_id)
            .order_by(desc(TransactionRecord.event_timestamp))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


class FraudEvaluationRepository(BaseRepository[FraudEvaluationRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(FraudEvaluationRecord, session)

    async def get_by_transaction_id(self, tx_id: str) -> Optional[FraudEvaluationRecord]:
        stmt = select(FraudEvaluationRecord).where(FraudEvaluationRecord.transaction_id == tx_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_recent_high_risk(self, limit: int = 50) -> List[FraudEvaluationRecord]:
        stmt = (
            select(FraudEvaluationRecord)
            .where(FraudEvaluationRecord.risk_score >= 0.70)
            .order_by(desc(FraudEvaluationRecord.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
