from typing import List
from ...domain.interfaces import MemoryStorage
from ...domain.models import Message

class LocalMemory(MemoryStorage):
    """Simple in-memory list storage for chat context."""
    
    def __init__(self):
        self._messages: List[Message] = []

    def add_message(self, message: Message) -> None:
        self._messages.append(message)

    def get_history(self, limit: int = 20) -> List[Message]:
        return self._messages[-limit:]

    def clear(self) -> None:
        self._messages.clear()
