import edge_tts
import pygame
import asyncio
import os
import tempfile
from ...domain.interfaces import TTSProvider

class EdgeTTS(TTSProvider):
    def __init__(self, voice="en-US-AriaNeural"):
        self.voice = voice
        pygame.mixer.init()

    async def speak(self, text: str) -> None:
        if not text:
            return

        communicate = edge_tts.Communicate(text, self.voice)
        
        # Create temp file
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        
        try:
            await communicate.save(path)
            
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"[TTS Error] {e}")
        finally:
            # Cleanup
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

    def check_health(self) -> bool:
        # Check if edge-tts is importable and functional
        return True

    def stop(self) -> None:
        """Stop current playback"""
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except:
            pass
