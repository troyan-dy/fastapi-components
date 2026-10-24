import abc

from fastapi_components.state import State


class BaseComponent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def startup(self, state: State) -> State:
        """Инициализирует компонент, кладёт его ресурсы в state и возвращает state."""

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """Освобождает ресурсы компонента."""
