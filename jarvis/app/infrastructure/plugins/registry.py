import importlib
import os
import sys
from typing import List, Optional, Dict
from ...domain.interfaces import CommandRegistry, Command

class SimpleCommandRegistry(CommandRegistry):
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        print(f"Registering command: {command.name}")
        self._commands[command.name] = command

    def get_command(self, name: str) -> Optional[Command]:
        return self._commands.get(name)

    def list_commands(self) -> List[Command]:
        return list(self._commands.values())

    def load_plugins_from_folder(self, folder_path: str):
        """Dynamically loads plugin modules from a folder."""
        if not os.path.isdir(folder_path):
            return

        # Add folder to sys.path to allow imports
        sys.path.append(folder_path)

        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "register"):
                         # Plugin convention: def register(registry):
                         module.register(self)
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")
