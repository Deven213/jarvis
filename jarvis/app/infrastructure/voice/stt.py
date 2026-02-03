import speech_recognition as sr
from ...domain.interfaces import STTProvider, AudioSource
from .microphone import MicrophoneService

class OnlineSTT(STTProvider):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_and_transcribe(self, source: AudioSource) -> str:
        if not isinstance(source, MicrophoneService):
            raise ValueError("OnlineSTT requires MicrophoneService")
            
        mic_source = source.get_source()
        
        try:
            with mic_source as src:
                print("[STT] Listening...")
                # timeout = wait time for start, phrase_time_limit = max duration
                audio = self.recognizer.listen(src, timeout=5, phrase_time_limit=10)
            
            print("[STT] Transcribing...")
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"[STT Error] {e}")
            return ""

    def check_health(self) -> bool:
        # Check internet connectivity or STT API reachability
        # For now, we assume if we can import the library and init, it's mostly OK.
        # Ideally, check internet connection.
        return True
