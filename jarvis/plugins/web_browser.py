import webbrowser
import os
import subprocess
import platform
from app.domain.interfaces import Command, ToolResult

class OpenWebsiteCommand(Command):
    """Opens websites in the default browser"""
    
    # Common website mappings
    WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com",
        "reddit": "https://www.reddit.com",
        "amazon": "https://www.amazon.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://www.spotify.com",
        "whatsapp": "https://web.whatsapp.com",
        "maps": "https://maps.google.com",
        "drive": "https://drive.google.com",
        "docs": "https://docs.google.com",
        "sheets": "https://sheets.google.com",
        "slides": "https://slides.google.com",
        "calendar": "https://calendar.google.com",
        "meet": "https://meet.google.com",
        "zoom": "https://zoom.us",
        "chatgpt": "https://chat.openai.com",
        "claude": "https://claude.ai",
        "gemini": "https://gemini.google.com",
    }
    
    @property
    def name(self) -> str:
        return "open_website"
    
    @property
    def description(self) -> str:
        return f"Opens a website in the default browser. Supported sites: {', '.join(self.WEBSITES.keys())}. Can also open custom URLs."
    
    def execute(self, **kwargs) -> ToolResult:
        site_name = kwargs.get("site_name", "").lower().strip()
        custom_url = kwargs.get("url", "").strip()
        
        if not site_name and not custom_url:
            return ToolResult(
                success=False,
                message="Please specify a website name or URL to open."
            )
        
        # Check if it's a known website
        if site_name in self.WEBSITES:
            url = self.WEBSITES[site_name]
            try:
                webbrowser.open(url)
                return ToolResult(
                    success=True,
                    data={"url": url, "site": site_name},
                    message=f"Opening {site_name.title()}..."
                )
            except Exception as e:
                return ToolResult(
                    success=False,
                    message=f"Failed to open {site_name}: {str(e)}"
                )
        
        # Try to open custom URL
        elif custom_url:
            # Add https:// if not present
            if not custom_url.startswith(("http://", "https://")):
                custom_url = "https://" + custom_url
            
            try:
                webbrowser.open(custom_url)
                return ToolResult(
                    success=True,
                    data={"url": custom_url},
                    message=f"Opening {custom_url}..."
                )
            except Exception as e:
                return ToolResult(
                    success=False,
                    message=f"Failed to open URL: {str(e)}"
                )
        
        else:
            return ToolResult(
                success=False,
                message=f"Unknown website: {site_name}. Try one of: {', '.join(list(self.WEBSITES.keys())[:10])}..."
            )


class OpenApplicationCommand(Command):
    """Opens common applications"""
    
    # Application mappings for Windows
    WINDOWS_APPS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "settings": "ms-settings:",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "vscode": "code",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
    }
    
    @property
    def name(self) -> str:
        return "open_application"
    
    @property
    def description(self) -> str:
        return f"Opens an application. Supported apps: {', '.join(self.WINDOWS_APPS.keys())}"
    
    def execute(self, **kwargs) -> ToolResult:
        app_name = kwargs.get("app_name", "").lower().strip()
        
        if not app_name:
            return ToolResult(
                success=False,
                message="Please specify an application name."
            )
        
        system = platform.system()
        
        if system == "Windows":
            if app_name in self.WINDOWS_APPS:
                app_path = self.WINDOWS_APPS[app_name]
                try:
                    if app_path.startswith("ms-"):
                        # For Windows settings and special URIs
                        os.startfile(app_path)
                    else:
                        subprocess.Popen(app_path, shell=True)
                    
                    return ToolResult(
                        success=True,
                        data={"app": app_name, "path": app_path},
                        message=f"Opening {app_name.title()}..."
                    )
                except Exception as e:
                    return ToolResult(
                        success=False,
                        message=f"Failed to open {app_name}: {str(e)}"
                    )
            else:
                # Try to open it anyway
                try:
                    subprocess.Popen(app_name, shell=True)
                    return ToolResult(
                        success=True,
                        data={"app": app_name},
                        message=f"Attempting to open {app_name}..."
                    )
                except Exception as e:
                    return ToolResult(
                        success=False,
                        message=f"Unknown application: {app_name}"
                    )
        else:
            return ToolResult(
                success=False,
                message=f"Application opening not yet supported on {system}"
            )


class SearchWebCommand(Command):
    """Performs a web search"""
    
    @property
    def name(self) -> str:
        return "search_web"
    
    @property
    def description(self) -> str:
        return "Searches the web using Google for a given query."
    
    def execute(self, **kwargs) -> ToolResult:
        query = kwargs.get("query", "").strip()
        
        if not query:
            return ToolResult(
                success=False,
                message="Please provide a search query."
            )
        
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return ToolResult(
                success=True,
                data={"query": query, "url": search_url},
                message=f"Searching for: {query}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                message=f"Failed to perform search: {str(e)}"
            )


def register(registry):
    """Register all web browser commands"""
    registry.register(OpenWebsiteCommand())
    registry.register(OpenApplicationCommand())
    registry.register(SearchWebCommand())
