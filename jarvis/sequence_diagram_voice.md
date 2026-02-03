# Jarvis Phase 2 Sequence Diagram (Voice)
# The system now runs an Async Voice Loop in parallel with the GUI.

VoiceLoop -> Microphone: Start Listening
User -> Microphone: Speaks Command
Microphone --> VoiceLoop: Audio Stream
VoiceLoop -> GUI: update_state("Listening")
VoiceLoop -> STT: transcribe(audio)
STT --> VoiceLoop: "Open Calculator"
VoiceLoop -> GUI: update_state("Transcribing")
VoiceLoop -> Assistant: process_input("Open Calculator")
Assistant -> GUI: update_state("Thinking")
Assistant -> Memory: add_message("User: Open Calculator")
Assistant -> IntentService: analyze(...)
IntentService --> Assistant: Intent(open_app)
Assistant -> Command: execute()
Command --> Assistant: "Success"
Assistant -> LLM: generate_response()
LLM --> Assistant: "Opening calculator now."
Assistant -> VoiceLoop: return response_text
VoiceLoop -> GUI: update_state("Speaking")
VoiceLoop -> TTS: speak("Opening calculator now.")
TTS -> Speaker: Play Audio
VoiceLoop -> GUI: update_state("Idle")
VoiceLoop -> Microphone: Start Listening (Loop continues)
