import functools
from typing import List

from fastapi import FastAPI
from pydantic_settings import BaseSettings

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
            # Sequential by contract: each component receives the state built by the previous ones.
            self.state = await component.startup(self.state)  # noqa: WPS476

        self.started = True

    async def shutdown(self) -> None:
        """Вызовет shutdown каждого компонента в обратном порядке."""
        if self.started:
            for component in reversed(self.components):
                # Sequential by contract: components stop in the reverse order of startup.
                await component.shutdown()  # noqa: WPS476


class FastAPIStateManager(StateManager):
    """Манагер стейта для FastAPI."""

    def set_startup_hook(self, app: FastAPI) -> None:
        """Проставит startup hook FastAPI приложению,
        в котором вызовет у себя startup и перезапишет FastAPI.state на свой state"""
        app.router.add_event_handler("startup", functools.partial(self._startup_app, app))

    def set_shutdown_hook(self, app: FastAPI) -> None:
        """Проставит shutdown hook FastAPI приложению, в котором вызовет у себя shutdown"""
        app.router.add_event_handler("shutdown", self._shutdown_app)

    async def _startup_app(self, app: FastAPI) -> None:
        await self.startup()
        # this is dangerous
        app.state = self.state  # type: ignore

    async def _shutdown_app(self) -> None:
        await self.shutdown()
