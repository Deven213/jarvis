# Jarvis Phase 3: Startup & Readiness Plan

## Goal
Implement a robust startup sequence that validates all subsystems (Mic, STT, TTS, LLM) before indicating "Online" and speaking a natural, context-aware greeting.

## Architecture
-   **Startup Layer**: `app/application/startup/` containing `startup_manager.py`.
-   **Interfaces**: All Providers (`LLM`, `STT`, `TTS`, `AudioSource`) gain a `check_health()` method.
-   **State Machine**: New states `BOOTING` and `GREETING`.

## Proposed Changes

### 1. Domain Layer (`app/domain`)
-   **Interfaces**: Add `check_health() -> bool` (or `HealthResult`) to all provider interfaces.
-   **Events**: Add `AssistantState.BOOTING`.

### 2. Infrastructure Layer (`app/infrastructure`)
-   Implement `check_health` in:
    -   `GeminiLLMProvider`: Simple generation call (e.g. "ping").
    -   `MicrophoneService`: Check `pyaudio` stream availability.
    -   `OnlineSTT`: Verify internet/service reachability (optional, or just logic check).
    -   `EdgeTTS`: No-op or import check.

### 3. Application Layer (`app/application`)
-   **[NEW]** `startup/startup_manager.py`:
    -   `run_checks()`: Iterates all providers.
    -   `generate_greeting()`: Time-based logic ("Good morning/evening").
    -   `boot()`: The main sequence.

### 4. Presentation Layer (`app/presentation`)
-   **GUI**: Handle `BOOTING` state (maybe a spinner or yellow status).
-   **Main**: Move `assistant.start_voice_loop()` to occur *after* `startup_manager.boot()` succeeds.

## Startup Sequence
1.  GUI Starts (Status: "OFFLINE" -> "BOOTING").
2.  `StartupManager` runs health checks in background.
3.  GUI updates (e.g., "Checking Mic... OK", "Checking Brain... OK").
4.  If all OK:
    -   Status -> "READY".
    -   `VoiceManager` speaks Greeting ("System Online. Good Evening.").
5.  `AssistantCore` Voice Loop starts.
6.  Status -> "LISTENING".

## Verification
-   Run `main.py`.
-   See "Booting..." in GUI.
-   Hear Greeting.
-   Talk to Jarvis.
