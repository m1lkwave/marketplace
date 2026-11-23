from sqlalchemy.ext.asyncio import AsyncSession

from src.db.transaction import TransactionManager

class SqlAlchemyTransactionManager(TransactionManager):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()