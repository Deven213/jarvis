import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from typing import Callable

class JarvisGUI:
    def __init__(self, process_callback: Callable[[str], str]):
        self.root = tk.Tk()
        self.root.title("Jarvis AI Assistant")
        self.root.geometry("800x600")
        
        self.process_callback = process_callback # Function to call for processing input

        self._setup_ui()
        
    def _setup_ui(self):
        # Configure Styles
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))
        
        # 1. Main Container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 2. Chat History (Top)
        self.chat_display = scrolledtext.ScrolledText(main_frame, state='disabled', height=20, font=("Consolas", 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.tag_config("user", foreground="blue")
        self.chat_display.tag_config("assistant", foreground="green")
        self.chat_display.tag_config("system", foreground="gray", font=("Consolas", 9, "italic"))

        # 3. Brain Status (Middle)
        self.status_var = tk.StringVar(value="Status: Idle")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="purple")
        self.status_label.pack(anchor="w", pady=(0, 5))

        # 4. Input Area (Bottom)
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.input_field = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        # 5. Log Console (Bottom Panel - Optional, maybe just keep in status for now or separate window)
        # Keeping it simple as requested: "User input, Interpreted intent, AI response, Executed command"
        # These will show in chat for now with different styling.

    def append_chat(self, text: str, tag: str):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, text + "\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')

    def set_status(self, text: str):
        self.status_var.set(f"Status: {text}")

    def send_message(self):
        user_text = self.input_field.get().strip()
        if not user_text:
            return

        self.input_field.delete(0, tk.END)
        self.append_chat(f"You: {user_text}", "user")
        
        # Run processing in separate thread to keep UI responsive
        threading.Thread(target=self._process_in_thread, args=(user_text,), daemon=True).start()

    def _process_in_thread(self, text: str):
        self.root.after(0, lambda: self.set_status("Thinking..."))
        try:
            response = self.process_callback(text)
            self.root.after(0, lambda: self.append_chat(f"Jarvis: {response}", "assistant"))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.append_chat(f"Error: {error_msg}", "system"))
        finally:
            self.root.after(0, lambda: self.set_status("Idle"))

    def update_thought(self, thought_text: str):
        """Callback to update the UI with internal thoughts/logs."""
        # Use 'system' tag for thoughts
        self.root.after(0, lambda: self.append_chat(f"[Brain] {thought_text}", "system"))

    def start(self):
        self.root.mainloop()

    def update_voice_state(self, state_text: str):
        # Update status label with visual indicator
        icon = "🤖"
        if "listening" in state_text.lower():
            icon = "🎤"
        elif "speaking" in state_text.lower():
            icon = "🗣️"
        elif "transcribing" in state_text.lower():
            icon = "⏳"
        elif "thinking" in state_text.lower():
            icon = "🧠"
        elif "booting" in state_text.lower():
            icon = "🔌"
            
        self.root.after(0, lambda: self.set_status(f"{icon} {state_text.upper()}"))
