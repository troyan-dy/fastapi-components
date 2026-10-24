from typing import Any, Dict, Optional


class State:
    """Контейнер стейта приложения"""

    def __init__(self, state: Optional[Dict[str, Any]] = None) -> None:
        if state is None:
            state = {}
        # `_state` goes straight into the instance dict to bypass `__setattr__` below.
        self.__dict__["_state"] = state

    # `value` mirrors the `object.__setattr__(name, value)` protocol signature.
    def __setattr__(self, key: str, value: Any) -> None:  # noqa: WPS110
        self._state[key] = value

    def __getattr__(self, key: str) -> Any:
        try:
            return self._state[key]
        except KeyError:
            class_name = type(self).__name__
            raise AttributeError(f"'{class_name}' object has no attribute '{key}'")

    # Public API: `del state.attr` removes the value from the state.
    def __delattr__(self, key: str) -> None:  # noqa: WPS603
        self._state.pop(key)
