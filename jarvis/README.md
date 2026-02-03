# Jarvis AI Assistant v1

A production-ready, clean-architecture AI assistant built in Python.

## Architecture
This project follows **Clean Architecture** principles:
- **Domain Layer** (`app/domain`): Core logic, Interfaces, and Data Models. No external dependencies.
- **Application Layer** (`app/application`): Orchestration logic (Use Cases). Connects Domain to Infrastructure.
- **Infrastructure Layer** (`app/infrastructure`): Implementations of interfaces (LLM APIs, Database, Plugins).
- **Presentation Layer** (`app/presentation`): User Interface (GUI).

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your API keys.
3. Run `python main.py`

## Features
- Modular Plugin System
- Abstracted LLM Provider (Switch between Gemini/OpenAI)
- GUI with internal thought process visibility
