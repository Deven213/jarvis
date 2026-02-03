# 🎤 Voice Commands Guide for J.A.R.V.I.S

## ✅ What's Been Added

I've added powerful voice commands to open websites and applications! Now you can say:

### 🌐 **Opening Websites**

Just say any of these:

- **"Open Google"** → Opens Google.com
- **"Open YouTube"** → Opens YouTube.com
- **"Open Gmail"** → Opens Gmail
- **"Go to Facebook"** → Opens Facebook
- **"Open Instagram"** → Opens Instagram
- **"Open LinkedIn"** → Opens LinkedIn
- **"Open GitHub"** → Opens GitHub
- **"Open Reddit"** → Opens Reddit
- **"Open Netflix"** → Opens Netflix
- **"Open Spotify"** → Opens Spotify
- **"Open WhatsApp"** → Opens WhatsApp Web
- **"Open Maps"** → Opens Google Maps
- **"Open Drive"** → Opens Google Drive
- **"Open ChatGPT"** → Opens ChatGPT
- **"Open Gemini"** → Opens Google Gemini

### 💻 **Opening Applications**

Say these to launch apps:

- **"Open Calculator"** → Launches Windows Calculator
- **"Open Notepad"** → Launches Notepad
- **"Launch Paint"** → Opens MS Paint
- **"Open Explorer"** → Opens File Explorer
- **"Start Chrome"** → Opens Google Chrome
- **"Open Edge"** → Opens Microsoft Edge
- **"Launch PowerShell"** → Opens PowerShell
- **"Open Task Manager"** → Opens Task Manager
- **"Open Settings"** → Opens Windows Settings

### 🔍 **Web Search**

- **"Search for Python tutorials"** → Searches Google
- **"Google artificial intelligence"** → Searches Google
- **"Search machine learning"** → Searches Google

### ⏰ **Other Commands**

- **"What time is it?"** → Tells you the current time
- **"System info"** → Shows system information

---

## 🚀 How to Use

### **Step 1: Restart Jarvis**

Since you already have Jarvis running, you need to restart it to load the new plugin:

1. **Stop the current instance:**
   - Press `Ctrl + C` in the terminal where Jarvis is running

2. **Restart Jarvis:**
   ```bash
   python main.py
   ```

### **Step 2: Wait for Boot**

You'll see:
```
System Check Passed. Starting Voice Loop...
[STT] Listening...
```

### **Step 3: Speak Your Command**

Just speak naturally! Examples:

- 🗣️ **"Open Google"**
- 🗣️ **"Open YouTube"**
- 🗣️ **"Launch Calculator"**
- 🗣️ **"Search for Python tutorials"**

### **Step 4: Watch It Happen!**

Jarvis will:
1. **Listen** to your voice
2. **Transcribe** what you said
3. **Understand** the intent (e.g., "open_website")
4. **Execute** the command (opens the website)
5. **Respond** with confirmation

---

## 📋 Complete List of Supported Websites

| Say This | Opens |
|----------|-------|
| "Open Google" | Google.com |
| "Open YouTube" | YouTube.com |
| "Open Gmail" | Gmail |
| "Open Facebook" | Facebook.com |
| "Open Twitter" | Twitter.com |
| "Open Instagram" | Instagram.com |
| "Open LinkedIn" | LinkedIn.com |
| "Open GitHub" | GitHub.com |
| "Open StackOverflow" | StackOverflow.com |
| "Open Reddit" | Reddit.com |
| "Open Amazon" | Amazon.com |
| "Open Netflix" | Netflix.com |
| "Open Spotify" | Spotify.com |
| "Open WhatsApp" | WhatsApp Web |
| "Open Maps" | Google Maps |
| "Open Drive" | Google Drive |
| "Open Docs" | Google Docs |
| "Open Sheets" | Google Sheets |
| "Open Slides" | Google Slides |
| "Open Calendar" | Google Calendar |
| "Open Meet" | Google Meet |
| "Open Zoom" | Zoom.us |
| "Open ChatGPT" | ChatGPT |
| "Open Claude" | Claude.ai |
| "Open Gemini" | Google Gemini |

---

## 🛠️ Technical Details

### Files Created/Modified:

1. **`plugins/web_browser.py`** ✅ NEW
   - `OpenWebsiteCommand` - Opens 25+ popular websites
   - `OpenApplicationCommand` - Launches Windows applications
   - `SearchWebCommand` - Performs Google searches

2. **`app/infrastructure/llm/gemini_provider.py`** ✅ UPDATED
   - Enhanced intent analysis with command descriptions
   - Better recognition of "open", "launch", "search" commands

### How It Works:

```
Your Voice → Speech Recognition → Intent Analysis → Command Execution → Browser Opens
```

1. **You speak:** "Open Google"
2. **STT transcribes:** "open google"
3. **LLM analyzes intent:**
   ```json
   {
     "action": "open_website",
     "confidence": 0.95,
     "parameters": {"site_name": "google"}
   }
   ```
4. **Command executes:** Opens https://www.google.com
5. **Jarvis responds:** "Opening Google..."

---

## 🧪 Testing

To test the plugin without voice:

```bash
python test_web_plugin.py
```

This will open Google and YouTube in your browser to verify it works.

---

## 🎯 Example Voice Conversations

### Example 1: Opening YouTube
```
You: "Open YouTube"
Jarvis: [Listens] → [Transcribes] → [Opens YouTube]
Jarvis: "Opening YouTube..."
```

### Example 2: Searching the Web
```
You: "Search for Python tutorials"
Jarvis: [Listens] → [Transcribes] → [Opens Google Search]
Jarvis: "Searching for: Python tutorials"
```

### Example 3: Opening Calculator
```
You: "Open Calculator"
Jarvis: [Listens] → [Transcribes] → [Launches Calculator]
Jarvis: "Opening Calculator..."
```

---

## 🔧 Troubleshooting

### Command Not Working?

1. **Restart Jarvis** - New plugins need a restart
2. **Speak Clearly** - Ensure good microphone quality
3. **Check Console** - Look for intent detection in terminal
4. **Try Text Input** - Type the command in the GUI to test

### Website Not Opening?

- Check your default browser is set
- Ensure you have internet connection
- Try the test script: `python test_web_plugin.py`

### Application Not Found?

- Some apps may not be installed on your system
- Try using the full app name (e.g., "calculator" not "calc")

---

## 🎨 Adding More Websites

Want to add more websites? Edit `plugins/web_browser.py`:

```python
WEBSITES = {
    # Add your custom websites here
    "twitter": "https://www.twitter.com",
    "mysite": "https://www.mywebsite.com",
}
```

Then restart Jarvis!

---

## 🚀 Next Steps

Now that you have voice commands working, you can:

1. ✅ **Try all the commands** listed above
2. ✅ **Add custom websites** to the plugin
3. ✅ **Use the web interface** (run `python main_web.py`)
4. ✅ **Create custom plugins** for more functionality

---

**Enjoy your enhanced Jarvis assistant! 🎉**
