import os
import google.generativeai as genai
from typing import List, Optional
import json
from ...domain.interfaces import LLMProvider
from ...domain.models import Message, Intent, MessageRole

class GeminiLLMProvider(LLMProvider):
    """Google Gemini Implementation."""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        try:
            print("Available Models:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f" - {m.name}")
            # self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        except Exception as e:
            print(f"Error listing models or init: {e}")
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def _format_history(self, history: List[Message]) -> List[dict]:
        formatted = []
        for msg in history:
            role = "user" if msg.role == MessageRole.USER else "model"
            parts = [msg.content]
            formatted.append({"role": role, "parts": parts})
        return formatted

    def generate_response(self, prompt: str, history: List[Message], system_prompt: Optional[str] = None) -> str:
        # Note: Gemini system prompt is usually set at model creation or separate config, 
        # simplistic implementation here.
        
        chat = self.model.start_chat(history=self._format_history(history))
        response = chat.send_message(prompt)
        return response.text

    def analyze_intent(self, query: str, context: List[Message]) -> Intent:
        system_prompt = """
        You are an intent analyzer for a voice assistant named JARVIS.
        Analyze the user's input and determine the intent.
        
        Available Commands:
        1. "open_website" - Opens websites in browser
           - Parameters: {"site_name": "google|youtube|gmail|facebook|twitter|instagram|linkedin|github|stackoverflow|reddit|amazon|netflix|spotify|whatsapp|maps|drive|docs|sheets|slides|calendar|meet|zoom|chatgpt|claude|gemini"}
           - Examples: "open google", "open youtube", "go to gmail"
           
        2. "open_application" - Opens applications
           - Parameters: {"app_name": "notepad|calculator|paint|explorer|cmd|powershell|chrome|edge|vscode|word|excel|powerpoint"}
           - Examples: "open calculator", "launch notepad", "start chrome"
           
        3. "search_web" - Searches Google
           - Parameters: {"query": "search terms"}
           - Examples: "search for python tutorials", "google artificial intelligence"
           
        4. "get_time" - Returns current time
           - Parameters: {}
           - Examples: "what time is it", "current time"
           
        5. "system_info" - Returns system information
           - Parameters: {}
           - Examples: "system info", "what's my OS"
        
        Return ONLY a JSON object with:
        {
            "action": "command_name_or_unknown",
            "confidence": 0.0_to_1.0,
            "parameters": { ...extracted args... }
        }
        
        Rules:
        - If user says "open [website]" or "go to [website]", use "open_website" with site_name
        - If user says "open [app]" or "launch [app]", use "open_application" with app_name
        - If user says "search for X" or "google X", use "search_web" with query
        - Set confidence to 0.9+ for clear matches, 0.5-0.8 for partial matches
        - Use "unknown" action if no command matches
        """
        response = self.model.generate_content(f"{system_prompt}\n\nUser Input: {query}")
        text = response.text.replace('```json', '').replace('```', '').strip()
        
        try:
            data = json.loads(text)
            return Intent(
                action=data.get("action", "unknown"),
                confidence=data.get("confidence", 0.0),
                parameters=data.get("parameters", {}),
                raw_query=query
            )
        except Exception as e:
            print(f"Error parsing intent: {e}")
            return Intent(action="unknown", confidence=0.0, raw_query=query)

    def check_health(self) -> bool:
        try:
            # Simple ping with a token count or minimal generation
            self.model.count_tokens("Ping")
            return True
        except Exception as e:
            print(f"[Health Check Failed] Gemini: {e}")
            return False
