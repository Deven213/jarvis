from typing import Callable, Optional
from ..domain.interfaces import LLMProvider, MemoryStorage, CommandRegistry
from ..domain.models import Message, MessageRole, Intent
from .services import IntentService
from .voice_manager import VoiceManager
import asyncio
import threading

class AssistantCore:
    """
    Main Application Controller.
    Orchestrates: User Input -> Intent Analysis -> Command Execution -> Response Generation
    """
    def __init__(
        self, 
        llm: LLMProvider, 
        memory: MemoryStorage, 
        commands: CommandRegistry,
        on_thought_update: Optional[Callable[[str], None]] = None,
        voice_manager: Optional[VoiceManager] = None
    ):
        self.llm = llm
        self.memory = memory
        self.commands = commands
        self.intent_service = IntentService(llm)
        self.on_thought_update = on_thought_update # Callback for GUI updates
        self.voice_manager = voice_manager

    def start_voice_loop(self):
        """Starts the main voice interaction loop in a separate thread."""
        if not self.voice_manager:
            return
        threading.Thread(target=self._voice_loop_thread, daemon=True).start()

    def _voice_loop_thread(self):
        # We need an asyncio loop for the async TTS parts if running in a thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            # 1. Listen
            user_text = self.voice_manager.listen()
            
            if user_text:
                # 2. Process (Logic acts as "Thinking")
                response = self.process_input(user_text)
                
                # 3. Speak
                if response:
                    loop.run_until_complete(self.voice_manager.speak(response))
            
            # Small delay to prevent tight loop if mic fails
            # time.sleep(0.1)

    def _log_thought(self, text: str):
        if self.on_thought_update:
            self.on_thought_update(text)

    def process_input(self, user_text: str) -> str:
        """Full processing pipeline for a user message."""
        
        # 1. Update Memory
        user_msg = Message(role=MessageRole.USER, content=user_text)
        self.memory.add_message(user_msg)
        
        # 2. Analyze Intent
        self._log_thought(f"Analyzing intent for: '{user_text}'...")
        history = self.memory.get_history()
        intent = self.intent_service.analyze(user_text, history)
        self._log_thought(f"Detected Intent: {intent.action} (Conf: {intent.confidence})")

        command_result_str = ""
        
        # 3. Execute Command (if applicable)
        if intent.confidence > 0.7 and intent.action != "unknown":
            command = self.commands.get_command(intent.action)
            if command:
                self._log_thought(f"Executing command: {command.name} with {intent.parameters}")
                try:
                    result = command.execute(**intent.parameters)
                    command_result_str = f"\n[System] Command '{intent.action}' executed. Result: {result.message}"
                    if result.data:
                         command_result_str += f" Data: {result.data}"
                    self._log_thought(f"Command Success: {result.message}")
                except Exception as e:
                    command_result_str = f"\n[System] Command execution failed: {str(e)}"
                    self._log_thought(f"Command Error: {str(e)}")
            else:
                self._log_thought(f"Command '{intent.action}' not found in registry.")
        
        # 4. Generate Response
        self._log_thought("Generating final response...")
        # Add a temporary system message with the tool result to help the LLM form a response
        context_with_tool = history + ([Message(role=MessageRole.SYSTEM, content=command_result_str)] if command_result_str else [])
        
        response_text = self.llm.generate_response(
            prompt=user_text, 
            history=context_with_tool
        )
        
        # 5. Save & Return
        bot_msg = Message(role=MessageRole.ASSISTANT, content=response_text)
        self.memory.add_message(bot_msg)
        self._log_thought("Idle.")
        return response_text
