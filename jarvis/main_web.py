"""
J.A.R.V.I.S - Just A Rather Very Intelligent System
Main entry point for the web-based interface
"""
import os
import sys

# Ensure the root directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.presentation.web_server import main

if __name__ == "__main__":
    main()
