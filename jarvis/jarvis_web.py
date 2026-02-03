"""
J.A.R.V.I.S - Web GUI Version
Launches the futuristic web-based interface
"""
import os
import sys
import webbrowser
import time
import threading

# Ensure the root directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.presentation.web_server import main as start_web_server

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5001')

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🤖 J.A.R.V.I.S - Just A Rather Very Intelligent System")
    print("="*70)
    print("\n  Starting futuristic web interface...")
    print("  Your browser will open automatically in 2 seconds...")
    print("\n  Server will be running at: http://localhost:5001")
    print("\n  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start web server
    start_web_server()
