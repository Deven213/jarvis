import os
import sys
from dotenv import load_dotenv

# Ensure the root directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.domain.models import Message
from app.infrastructure.llm.gemini_provider import GeminiLLMProvider
from app.infrastructure.llm.mock_provider import MockLLMProvider
from app.infrastructure.memory.local_memory import LocalMemory
from app.infrastructure.plugins.registry import SimpleCommandRegistry
from app.application.assistant import AssistantCore
from app.presentation.gui import JarvisGUI

from app.infrastructure.voice.microphone import MicrophoneService
from app.infrastructure.voice.stt import OnlineSTT
from app.infrastructure.voice.tts import EdgeTTS
from app.infrastructure.voice.identity import SimpleVoiceIdentity
from app.application.voice_manager import VoiceManager
from app.domain.events import VoiceEvent, AssistantState

from app.application.startup.startup_manager import StartupManager
import time
import threading
import asyncio

def main():
    load_dotenv()
    
    # ... (Infrastructure setup remains same) ...
    # 1. Setup Infrastructure
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("Using Gemini Provider")
        llm = GeminiLLMProvider(api_key=api_key)
    else:
        print("WARNING: GEMINI_API_KEY not found. Using Mock Provider.")
        llm = MockLLMProvider()

    memory = LocalMemory()
    registry = SimpleCommandRegistry()

    # Voice Infrastructure
    mic = MicrophoneService()
    stt = OnlineSTT()
    tts = EdgeTTS()
    identity = SimpleVoiceIdentity()
    
    # 2. Load Plugins
    plugins_dir = os.path.join(current_dir, "plugins")
    if os.path.exists(plugins_dir):
        registry.load_plugins_from_folder(plugins_dir)
    else:
        print(f"Plugins dir not found: {plugins_dir}")

    # 3. Setup Application Core
    gui = None # Forward definition
    
    def on_thought(text):
        if gui:
            gui.update_thought(text)

    def on_voice_event(event: VoiceEvent):
        if gui:
            gui.update_voice_state(event.state.value)

    voice_manager = VoiceManager(stt, tts, mic, identity, on_voice_event)
    
    startup_manager = StartupManager(
        llm, stt, tts, mic, identity,
        on_status_update=on_thought, # Reuse chat log for checking status
        on_voice_event=on_voice_event
    )

    assistant = AssistantCore(
        llm=llm,
        memory=memory,
        commands=registry,
        on_thought_update=on_thought,
        voice_manager=voice_manager
    )

    # 4. Setup GUI
    gui = JarvisGUI(process_callback=assistant.process_input)
    
    # 5. Boot Sequence & Loop (Run in background thread)
    def run_system():
        # Needed for async boot 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        gui.update_voice_state(AssistantState.BOOTING.value)
        success = loop.run_until_complete(startup_manager.boot())
        
        if success:
            print("System Check Passed. Starting Voice Loop...")
            # Assistant Core starts its own thread, we can call it here or direct.
            # assistant.start_voice_loop() creates a thread.
            # But wait, start_voice_loop expects to be called from main thread? No, it spawns a thread.
            # However, we are ALREADY in a background thread here (run_system).
            # We can just run the voice loop logic here if we wanted, or call the method.
            assistant.start_voice_loop()
        else:
            print("System Check Failed.")

    threading.Thread(target=run_system, daemon=True).start()
    
    print("Jarvis GUI Launching...")
    gui.start()

if __name__ == "__main__":
    main()
