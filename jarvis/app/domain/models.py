from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass
class Message:
    role: MessageRole
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Intent:
    """Represents the interpreted user intent."""
    action: str
    confidence: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    raw_query: str = ""

@dataclass
class ToolResult:
    """Result returned from a command execution."""
    success: bool
    data: Any
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
