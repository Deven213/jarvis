# Jarvis Phase 3 Sequence Diagram (Startup + Voice)
# Includes Boot Sequence and Readiness Checks.

Main -> GUI: Launch (Status: Booting)
Main -> StartupThread: run_system()
StartupThread -> StartupManager: boot()
StartupManager -> GUI: update_state("Booting")
StartupManager -> Mic: check_health()
Mic --> StartupManager: OK
StartupManager -> STT: check_health()
STT --> StartupManager: OK
StartupManager -> LLM: check_health()
LLM --> StartupManager: OK
StartupManager -> TTS: check_health()
TTS --> StartupManager: OK
StartupManager --> GUI: update_log("All systems nominal")
StartupManager -> TTS: speak("System Online. Good Afternoon.")
StartupThread -> Assistant: start_voice_loop()
Assistant -> Microphone: Start Listening
loop VoiceLoop:
    VoiceLoop -> GUI: update_state("Listening")
    User -> Microphone: Speaks
    Microphone --> VoiceLoop: Audio
    VoiceLoop -> STT: transcribe()
    ... (Standard Voice Flow) ...
