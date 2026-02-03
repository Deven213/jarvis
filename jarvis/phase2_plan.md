# Jarvis Phase 2: Voice Integration Plan

## Goal
Upgrade Jarvis to a voice-first assistant with human-like presence, speaker identity verification, and real-time GUI feedback.

## Architecture: Clean / Hexagonal
Extension of the existing structure.
New Interfaces in `domain`:
- `bAudioSource`: Abstract microphone/stream.
- `STTProvider`: Audio -> Text.
- `TTSProvider`: Text -> Audio.
- `SpeakerRecognizer`: Audio -> Identity/Confidence.

New Implementations in `infrastructure`:
- `MicrophoneService`: Uses `pyaudio`.
- `OnlineSTT`: Uses `SpeechRecognition` (Google Web Speech API for default cloud STT).
- `EdgeTTS`: Uses `edge-tts` (High quality neural voices, free).
- `VoiceIdentity`: Basic spectral feature comparison (to avoid heavy ML models like PyTorch/TensorFlow if possible, or placeholder for API).

## Proposed Changes

### 1. Domain Layer (`app/domain`)
- **[NEW]** `interfaces.py` (Additions): `STTProvider`, `TTSProvider`, `SpeakerRecognizer`.
- **[NEW]** `events.py`: Define events for `Listening`, `Transcribing`, `Speaking` to decouple GUI updates.

### 2. Infrastructure Layer (`app/infrastructure/voice`)
- **[NEW]** `microphone.py`: Async audio capture.
- **[NEW]** `stt.py`: Adapter for SpeechRecognition.
- **[NEW]** `tts.py`: Adapter for EdgeTTS.
- **[NEW]** `identity.py`: Simple audio fingerprinting or Mock (since "No local ML" constraint makes robust local speaker ID hard without heavy deps. Will implement valid interface).

### 3. Application Layer (`app/application`)
- **[MODIFY]** `AssistantCore`:
    - Add `VoiceLoop` management.
    - Handle `Wake Word` (optional/future) or simple "Listen" toggle.
    - Integrate `SpeakerRecognizer` check before processing commands.

### 4. Presentation Layer (`app/presentation`)
- **[MODIFY]** `gui.py`:
    - Add State Indicators: 🎤 Listening, ⏳ Transcribing, 🗣️ Speaking.
    - Add "Confidence" meter.
    - Visualize Speaker Identity status.

## Steps
1.  **Dependencies**: Add `SpeechRecognition`, `pyaudio`, `edge-tts`, `pygame` (for audio playback).
2.  **Domain**: Define Voice interfaces.
3.  **Humble implementations**:
    -   `Microphone`: Capture audio.
    -   `STT`: Send to Google.
    -   `TTS`: Generate MP3 -> Play.
4.  **Wiring**: Update `main.py` and `AssistantCore`.
5.  **GUI**: Visual updates.

## Verification
-   **Test Mic**: Verify audio capture.
-   **Test STT**: Speak "Hello" -> Text appears.
-   **Test TTS**: Bot responds with voice.
-   **Test Identity**: (If implemented) Verify it distinguishes/mocks correctly.
