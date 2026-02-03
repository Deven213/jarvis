from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

class AssistantState(Enum):
    IDLE = "idle"
    BOOTING = "booting"
    LISTENING = "listening"
    TRANSCRIBING = "transcribing"
    THINKING = "thinking"
    SPEAKING = "speaking"
    ERROR = "error"

@dataclass
class VoiceEvent:
    state: AssistantState
    payload: Optional[Any] = None
    message: str = ""
