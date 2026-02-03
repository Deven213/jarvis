# Jarvis Execution Sequence Diagram

User -> GUI: Type "Open Calculator" & Click Send
GUI -> GUI: Update Chat (User message)
GUI -> Assistant Thread: process_input("Open Calculator")
Assistant Thread -> Memory: add_message(UserMessage)
Assistant Thread -> GUI: update_thought("Analyzing intent...")
Assistant Thread -> IntentService: analyze("Open Calculator")
IntentService -> LLM: generate_intent_json()
LLM --> IntentService: JSON {action: "custom_command", args: ...}
IntentService --> Assistant Thread: Intent(action="custom_command")
Assistant Thread -> GUI: update_thought("Detected Intent: custom_command")
Assistant Thread -> CommandRegistry: get_command("custom_command")
CommandRegistry --> Assistant Thread: CommandObject
Assistant Thread -> CommandObject: execute()
CommandObject --> Assistant Thread: Result("Success")
Assistant Thread -> GUI: update_thought("Command Success")
Assistant Thread -> LLM: generate_response(History + ToolResult)
LLM --> Assistant Thread: "I have opened the calculator."
Assistant Thread -> Memory: add_message(AssistantMessage)
Assistant Thread -> GUI: update_thought("Idle")
Assistant Thread -> GUI: append_chat("I have opened the calculator.")
