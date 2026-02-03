from typing import List, Optional
from ...domain.interfaces import LLMProvider
from ...domain.models import Message, Intent, MessageRole

class MockLLMProvider(LLMProvider):
    """Mock Provider for testing without API keys."""
    
    def generate_response(self, prompt: str, history: List[Message], system_prompt: Optional[str] = None) -> str:
        return f"Mock response to: {prompt}"

    def analyze_intent(self, query: str, context: List[Message]) -> Intent:
        # Simple heuristic for testing
        if "open" in query.lower():
            return Intent(action="open_app", confidence=0.9, parameters={"app": query.split("open")[-1].strip()}, raw_query=query)
        return Intent(action="unknown", confidence=0.0, raw_query=query)

    def check_health(self) -> bool:
        return True
