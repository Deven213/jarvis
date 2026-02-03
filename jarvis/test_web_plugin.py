"""
Quick test script to verify the web browser plugin works
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.web_browser import OpenWebsiteCommand, OpenApplicationCommand, SearchWebCommand

def test_open_website():
    print("\n=== Testing Open Website Command ===")
    cmd = OpenWebsiteCommand()
    
    # Test opening Google
    result = cmd.execute(site_name="google")
    print(f"Open Google: {result.message} (Success: {result.success})")
    
    # Test opening YouTube
    result = cmd.execute(site_name="youtube")
    print(f"Open YouTube: {result.message} (Success: {result.success})")

def test_open_application():
    print("\n=== Testing Open Application Command ===")
    cmd = OpenApplicationCommand()
    
    # Test opening Calculator
    result = cmd.execute(app_name="calculator")
    print(f"Open Calculator: {result.message} (Success: {result.success})")
    
    # Test opening Notepad
    result = cmd.execute(app_name="notepad")
    print(f"Open Notepad: {result.message} (Success: {result.success})")

def test_search_web():
    print("\n=== Testing Web Search Command ===")
    cmd = SearchWebCommand()
    
    # Test web search
    result = cmd.execute(query="Python tutorials")
    print(f"Search Web: {result.message} (Success: {result.success})")

if __name__ == "__main__":
    print("Testing Web Browser Plugin Commands...")
    print("=" * 50)
    
    test_open_website()
    # Uncomment to test applications
    # test_open_application()
    # test_search_web()
    
    print("\n" + "=" * 50)
    print("Test completed! Check if websites opened in your browser.")
