import json
import os

from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    @abstractmethod
    def save_state(self, state: dict) -> None:
        """Save state to storage."""
        pass

    @abstractmethod
    def retrieve_state(self) -> dict:
        """Get state from storage."""
        pass


class JsonFileStorage(BaseStorage):
    """Save and retrieve state to file as JSON."""
    def __init__(self, file_path: str | bytes | os.PathLike):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Save state to storage."""
        with open(self.file_path, 'w') as state_json:
            json.dump(state, state_json)

    def retrieve_state(self) -> dict:
        """Get state from storage."""
        try:
            with open(self.file_path, 'r') as state_json:
                return json.load(state_json)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {}


class State:
    """Provides methods for keeping and restoring state while retrieving data.
    If the process was interrupted it allows to continue retrieving data starting
    from the save point.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Set state for key."""
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Get state by key."""
        state = self.storage.retrieve_state()
        return state.get(key)
