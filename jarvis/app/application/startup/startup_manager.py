import time
import random
from datetime import datetime
from typing import List, Callable
from ...domain.interfaces import LLMProvider, STTProvider, TTSProvider, AudioSource, SpeakerRecognizer
from ...domain.events import AssistantState, VoiceEvent

class StartupManager:
    def __init__(
        self,
        llm: LLMProvider,
        stt: STTProvider,
        tts: TTSProvider,
        mic: AudioSource,
        identity: SpeakerRecognizer,
        on_status_update: Callable[[str], None],
        on_voice_event: Callable[[VoiceEvent], None]
    ):
        self.llm = llm
        self.stt = stt
        self.tts = tts
        self.mic = mic
        self.identity = identity
        self.on_status_update = on_status_update
        self.on_voice_event = on_voice_event

    def _get_greeting(self) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_greeting = "Good morning."
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon."
        elif 17 <= hour < 22:
            time_greeting = "Good evening."
        else:
            time_greeting = "Welcome back."

        greetings = [
            f"{time_greeting} I am online.",
            f"{time_greeting} Systems operational.",
            f"{time_greeting} How can I help you?",
            "I am ready.",
            "Online and listening."
        ]
        return random.choice(greetings)

    async def boot(self) -> bool:
        self.on_voice_event(VoiceEvent(AssistantState.BOOTING, message="Starting up..."))
        
        checks = [
            ("Microphone", self.mic),
            ("Speech-to-Text", self.stt),
            ("Text-to-Speech", self.tts),
            ("Neural Engine (LLM)", self.llm),
            ("Identity System", self.identity)
        ]

        all_passed = True
        
        for name, provider in checks:
            self.on_status_update(f"Checking {name}...")
            # Simulate small delay for visual feedback if check is too fast
            start = time.time()
            is_healthy = provider.check_health()
            if time.time() - start < 0.5:
                time.sleep(0.3)
                
            if is_healthy:
                self.on_status_update(f"{name}: OK")
            else:
                self.on_status_update(f"{name}: FAILED")
                all_passed = False
                # We might continue checking others to show full status
        
        if all_passed:
            self.on_status_update("All systems nominal.")
            greeting = self._get_greeting()
            
            # Use voice manager flow effectively by direct invocation or event?
            # We can use TTS directly here since voice loop isn't running yet.
            self.on_voice_event(VoiceEvent(AssistantState.SPEAKING, message=greeting))
            await self.tts.speak(greeting)
            self.on_voice_event(VoiceEvent(AssistantState.IDLE))
            return True
        else:
            self.on_status_update("Startup Failed. Check logs.")
            return False
