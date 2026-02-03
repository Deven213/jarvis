from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import Message, Intent, ToolResult

class LLMProvider(ABC):
    """Abstract Base Class for AI Providers (Gemini, OpenAI, etc.)"""
    
    @abstractmethod
    def generate_response(self, prompt: str, history: List[Message], system_prompt: Optional[str] = None) -> str:
        """Generates a text response from the LLM."""
        pass

    @abstractmethod
    def analyze_intent(self, query: str, context: List[Message]) -> Intent:
        """Analyzes user input to determine intent and extract parameters."""
        pass

    @abstractmethod
    def check_health(self) -> bool:
        """Verifies connection to the LLM service."""
        pass

class Command(ABC):
    """Interface for a single actionable command/skill."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique key for the command (e.g., 'open_app')."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description for the generic system prompt."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Executes the command logic."""
        pass

class CommandRegistry(ABC):
    """Interface for managing available commands."""
    
    @abstractmethod
    def register(self, command: Command) -> None:
        pass
        
    @abstractmethod
    def get_command(self, name: str) -> Optional[Command]:
        pass
        
    @abstractmethod
    def list_commands(self) -> List[Command]:
        pass

class MemoryStorage(ABC):
    """Interface for context/history storage."""
    
    @abstractmethod
    def add_message(self, message: Message) -> None:
        pass
        
    @abstractmethod
    def get_history(self, limit: int = 20) -> List[Message]:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass

class AudioSource(ABC):
    """Abstract interface for audio input stream."""
    @abstractmethod
    def start_stream(self): pass
    
    @abstractmethod
    def get_audio_chunk(self) -> bytes: pass
    
    @abstractmethod
    def stop_stream(self): pass

    @abstractmethod
    def check_health(self) -> bool:
        pass

class STTProvider(ABC):
    """Speech-to-Text Provider Interface."""
    @abstractmethod
    def listen_and_transcribe(self, source: AudioSource) -> str:
        """Captures audio from source and returns text."""
        pass

    @abstractmethod
    def check_health(self) -> bool:
        pass

class TTSProvider(ABC):
    """Text-to-Speech Provider Interface."""
    @abstractmethod
    async def speak(self, text: str) -> None:
        """Converts text to speech and plays it."""
        pass

    @abstractmethod
    def check_health(self) -> bool:
        pass

class SpeakerRecognizer(ABC):
    """Speaker Identity Verification Interface."""
    @abstractmethod
    def identify_speaker(self, audio_data: bytes) -> float:
        """Returns confidence score (0.0 to 1.0) that speaker is the authorized user."""
        pass

    @abstractmethod
    def check_health(self) -> bool:
        pass

