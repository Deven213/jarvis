import speech_recognition as sr
from ...domain.interfaces import AudioSource

class MicrophoneService(AudioSource):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # Adjust for ambient noise on init
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def get_source(self):
        return self.mic

    def start_stream(self):
        pass

    def get_audio_chunk(self) -> bytes:
        pass

    def stop_stream(self):
        pass

    def check_health(self) -> bool:
        try:
            with self.mic as source:
                return True
        except Exception as e:
            print(f"[Health Check Failed] Microphone: {e}")
            return False
