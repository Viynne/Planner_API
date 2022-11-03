from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel
from models.users import User
from models.events import Event


class Settings(BaseSettings):
    db_url: Optional[str] = "planner_db"
    secret_key: Optional[str] = "HI5HL3V3L$3CR3T"

    async def initialize_database(self):
        client = AsyncIOMotorClient()
        await init_beanie(
            database=client[self.db_url],
            document_models=[Event, User]
        )

        class Config:
            env_file = ".emv"


class Database:
    def __init__(self, model):
        self.model = model

    async def create_db(self, document):
        await document.create()
        return

    async def get(self, doc_id: PydanticObjectId) -> Any:
        doc = await self.model.get(doc_id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, doc_id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = doc_id
        doc_body = body.dict()
        doc_body = {k: v for k, v in doc_body.items() if v is not None}
        update_query = {
            "$set": {
                field: value for field, value in doc_body.items()
            }
        }
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def deleted(self, doc_id: PydanticObjectId) -> bool:
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.delete()
        return True
