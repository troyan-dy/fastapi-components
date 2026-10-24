import abc


class Lifecycle(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def startup(self) -> None:
        """Запускает объект."""

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """Останавливает объект."""
