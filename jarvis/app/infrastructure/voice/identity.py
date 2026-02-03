from ...domain.interfaces import SpeakerRecognizer

class SimpleVoiceIdentity(SpeakerRecognizer):
    """
    Mock/Basic implementation of speaker identity.
    In a real scenario, this would generate embeddings (e.g., using Resemblyzer or pyannote) 
    and compare with a stored profile.
    
    Since 'No local ML' is a constraint for the initial request (avoiding heavy torch),
    we act as a passthrough or use a simple heuristic if possible.
    For now, we trust the microphone user is the authorized user (Confidence 1.0).
    """
    def identify_speaker(self, audio_data: bytes) -> float:
        # TODO: Implement spectral gating or cloud-based verification
        return 1.0

    def check_health(self) -> bool:
        return True
