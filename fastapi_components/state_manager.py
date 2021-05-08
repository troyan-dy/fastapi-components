from typing import List

from fastapi import FastAPI
from pydantic import BaseSettings

from fastapi_components.components.base import BaseComponent
from fastapi_components.lifecycle import Lifecycle
from fastapi_components.state import State


class StateManager(Lifecycle):
    """Манагер стейта."""

    def __init__(self, components: List[BaseComponent], settings: BaseSettings) -> None:
        """
        Args:
            components: список компонентов
            settings: настройки
        """
        self.settings = settings
        self.components = components

        self.state = State()
        self.state.settings = settings
        self.started = False

    async def startup(self) -> None:
        """Последовательно вызовет startup каждого компонента передавая в него state.
        В state можно писать, из него можно читать. Изначально в state только settings."""
        for component in self.components:
            self.state = await component.startup(self.state)

        self.started = True

    async def shutdown(self) -> None:
        """Вызовет shutdown каждого компонента в обратном порядке."""
        if self.started:
            for component in reversed(self.components):
                await component.shutdown()


class FastAPIStateManager(StateManager):
    """Манагер стейта для FastAPI."""

    def set_startup_hook(self, app: FastAPI) -> None:
        """Проставит startup hook FastAPI приложению,
        в котором вызовет у себя startup и перезапишет FastAPI.state на свой state"""

        async def hook() -> None:
            await self.startup()

            # this is dangerous
            app.state = self.state  # type: ignore

        app.router.add_event_handler("startup", hook)

    def set_shutdown_hook(self, app: FastAPI) -> None:
        """Проставит shutdown hook FastAPI приложению, в котором вызовет у себя shutdown"""

        async def hook() -> None:
            await self.shutdown()

        app.router.add_event_handler("shutdown", hook)
