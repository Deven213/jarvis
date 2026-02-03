import asyncio
from typing import Optional, Callable
from ..domain.interfaces import STTProvider, TTSProvider, SpeakerRecognizer, AudioSource
from ..domain.events import AssistantState, VoiceEvent

class VoiceManager:
    def __init__(
        self, 
        stt: STTProvider, 
        tts: TTSProvider, 
        mic: AudioSource, 
        identity: SpeakerRecognizer,
        on_event: Callable[[VoiceEvent], None]
    ):
        self.stt = stt
        self.tts = tts
        self.mic = mic
        self.identity = identity
        self.on_event = on_event
        self._running = False

    async def speak(self, text: str):
        self.on_event(VoiceEvent(AssistantState.SPEAKING, message=text))
        await self.tts.speak(text)
        self.on_event(VoiceEvent(AssistantState.IDLE))

    def stop(self):
        """Stop current speech"""
        if hasattr(self.tts, 'stop'):
            self.tts.stop()
        self.on_event(VoiceEvent(AssistantState.IDLE))

    def listen(self) -> str:
        self.on_event(VoiceEvent(AssistantState.LISTENING))
        text = self.stt.listen_and_transcribe(self.mic)
        
        if text:
            self.on_event(VoiceEvent(AssistantState.TRANSCRIBING, message=text))
            # Optional: Identity check here if we had raw audio
            # confidence = self.identity.identify_speaker(...)
            
        return text
