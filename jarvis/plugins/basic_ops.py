import datetime
import platform
from app.domain.interfaces import Command, ToolResult

class GetTimeCommand(Command):
    @property
    def name(self) -> str:
        return "get_time"

    @property
    def description(self) -> str:
        return "Returns the current local time."

    def execute(self, **kwargs) -> ToolResult:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return ToolResult(success=True, data=now, message=f"Current time is {now}")

class SystemInfoCommand(Command):
    @property
    def name(self) -> str:
        return "system_info"

    @property
    def description(self) -> str:
        return "Returns basic system information (OS, python version)."

    def execute(self, **kwargs) -> ToolResult:
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "python": platform.python_version()
        }
        return ToolResult(success=True, data=info, message=f"System Info: {info}")

def register(registry):
    registry.register(GetTimeCommand())
    registry.register(SystemInfoCommand())
