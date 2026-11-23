from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.db.transaction import TransactionManager
from src.db.sqlalchemy_transaction import SqlAlchemyTransactionManager
from src.db.connection import get_async_session

async def get_transaction_manager(session: AsyncSession = Depends(get_async_session)) -> TransactionManager:
    return SqlAlchemyTransactionManager(session)