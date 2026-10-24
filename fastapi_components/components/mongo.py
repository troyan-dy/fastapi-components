from typing import Annotated, Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import AnyUrl, UrlConstraints

from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State

MongoDsn = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["mongodb"])]


class MotorComponent(BaseComponent):
    required_settings = {"mongo_dsn": (MongoDsn, ...)}

    mongo: Optional[AsyncIOMotorClient[Dict[str, Any]]]

    async def startup(self, state: State) -> State:
        self.mongo = AsyncIOMotorClient(str(state.settings.mongo_dsn))
        state.mongo = self.mongo
        return state

    async def shutdown(self) -> None:
        if self.mongo:
            self.mongo.close()
