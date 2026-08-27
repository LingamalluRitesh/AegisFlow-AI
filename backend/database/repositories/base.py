"""
Generic Asynchronous Repository Base Class with CRUD, Pagination, and Filters
"""

from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from backend.database.models.base import TimeStampedUUIDModel

ModelType = TypeVar("ModelType", bound=TimeStampedUUIDModel)


class BaseRepository(Generic[ModelType]):
    """Generic async repository providing standard data access methods."""

    def __init__(self, model_cls: Type[ModelType], session: AsyncSession):
        self.model_cls = model_cls
        self.session = session

    async def get_by_id(self, entity_id: str) -> Optional[ModelType]:
        stmt = select(self.model_cls).where(self.model_cls.id == entity_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_all(self, offset: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model_cls).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model_cls)
        res = await self.session.execute(stmt)
        return res.scalar_one() or 0

    async def create(self, **kwargs) -> ModelType:
        instance = self.model_cls(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update_by_id(self, entity_id: str, **kwargs) -> Optional[ModelType]:
        stmt = (
            update(self.model_cls)
            .where(self.model_cls.id == entity_id)
            .values(**kwargs)
            .returning(self.model_cls)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_by_id(self, entity_id: str) -> bool:
        stmt = delete(self.model_cls).where(self.model_cls.id == entity_id)
        res = await self.session.execute(stmt)
        return res.rowcount > 0
