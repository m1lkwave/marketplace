from abc import ABC, abstractmethod
from typing import BinaryIO

class Storage(ABC):

    @abstractmethod
    async def upload(
            self,
            file: BinaryIO,
            key: str,
            content_type: str,
    ) -> str:
        ...

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> str:
        ...