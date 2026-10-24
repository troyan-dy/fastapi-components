from typing import Optional

import aiohttp

from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State


class AIOHTTPSessionComponent(BaseComponent):
    # Class-level default is public API: `component.session` is None before startup,
    # even in subclasses that override __init__ without calling super().
    session: Optional[aiohttp.ClientSession] = None

    async def startup(self, state: State) -> State:
        self.session = aiohttp.ClientSession()  # noqa: WPS601 public API, see the class attribute
        state.session = self.session
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
