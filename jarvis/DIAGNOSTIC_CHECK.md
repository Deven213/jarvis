# Jarvis Diagnostic & Fix Guide

If the command "Open Google" is still not working, follow these steps to reset the system.

## 1. Why it wasn't working
Previously, the interface said **"LISTENING"** but the brain wasn't actually turned on. We fixed a bug where the "Start" signal wasn't being sent.

## 2. Reset Instructions
Please follow these steps exactly:

1.  **Close all Jarvis browser tabs**.
2.  **Stop the server** in the terminal (Ctrl+C).
3.  **Start fresh**:
    ```bash
    python main.py
    ```
4.  **Wait** for the browser to open.

## 3. How to Verify It's Working
1.  Look at the **Terminal Output** (black box) on the web page.
2.  When it loads, you should see:
    ```
    [SYSTEM] Socket Link Established.
    ```
3.  **Say "Open Google"**.
4.  You MUST see this in the terminal log:
    ```
    [COMMAND] open google
    [EXECUTING] open_website
    ```
5.  If you see `[COMMAND]` appearing, the microphone works.
6.  If you see `[EXECUTING]`, the logic works.

## 4. Troubleshooting
If you say "Open Google" and the terminal log stays blank:
- **Check Microphone**: Make sure your browser has permission (click the lock icon in the address bar).
- **Check Terminal**: Look at the command prompt window where you ran `python main.py` for errors.
- **Type It**: Try typing "Open Google" in the input box at the bottom. If typing works but voice doesn't, it's a microphone issue.
