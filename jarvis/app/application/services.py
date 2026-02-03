from typing import List
from ..domain.interfaces import LLMProvider
from ..domain.models import Message, Intent

class IntentService:
    """Application service to interpret user input."""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def analyze(self, query: str, context: List[Message]) -> Intent:
        # We can add pre-processing logic here (e.g. regex for fast commands)
        return self.llm.analyze_intent(query, context)
