from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .base import DatabaseClient

class BeanieClient(DatabaseClient):
    async def connect(self) -> None:
        self._client = AsyncIOMotorClient(self.uri)
        self._db = self._client[self.database]
        # Beanie 초기화
        await init_beanie(database=self._db, document_models=[...])

    async def disconnect(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    # 비동기 컨텍스트 매니저 지원
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()