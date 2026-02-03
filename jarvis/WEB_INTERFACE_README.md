# J.A.R.V.I.S - Web Interface

A futuristic, Jarvis-inspired AI assistant with a stunning web-based UI featuring voice recognition, animated visualizations, and real-time command execution.

## Features

### 🎨 Premium UI Design
- **Futuristic Interface**: Inspired by Iron Man's Jarvis with cyan/blue/gold color scheme
- **Animated Voice Visualizer**: Real-time audio visualization using HTML5 Canvas
- **Glassmorphism Effects**: Modern translucent panels with backdrop blur
- **Pulsing Animations**: Dynamic visual feedback for system states
- **Particle Background**: Floating particles with grid animation
- **Responsive Design**: Works on desktop and tablet devices

### 🎤 Voice Capabilities
- **Voice Recognition**: Speak commands naturally
- **Text-to-Speech**: Jarvis responds with voice
- **Real-time Transcription**: See what Jarvis hears
- **Voice State Indicators**: Visual feedback for listening/speaking states

### 💬 Chat Interface
- **Real-time Messaging**: Instant communication with Jarvis
- **Command History**: Track recent commands
- **System Messages**: See internal thoughts and processes
- **Timestamped Messages**: All messages include timestamps

### 📊 System Monitoring
- **Live Status**: System, voice, and time displays
- **Performance Metrics**: CPU, memory, and network usage
- **Connection Status**: WebSocket connection monitoring

## Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up Environment Variables**:
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Application

### Web Interface (Recommended)
```bash
python main_web.py
```

Then open your browser to: **http://localhost:5000**

### Traditional GUI (Legacy)
```bash
python main.py
```

## Usage

### Text Commands
1. Type your command in the input field
2. Press Enter or click the Send button
3. Jarvis will process and respond

### Voice Commands
1. Click the microphone button (or press it in the UI)
2. Speak your command clearly
3. Wait for transcription
4. Jarvis will process and respond

### Example Commands
- "What time is it?"
- "Tell me a joke"
- "Search for Python tutorials"
- "Open calculator"
- "What's the weather like?"

## Architecture

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Advanced animations and effects
- **JavaScript**: Real-time WebSocket communication
- **Canvas API**: Voice visualization

### Backend
- **Flask**: Web server framework
- **Flask-SocketIO**: WebSocket support for real-time communication
- **Gemini AI**: Language model for intelligent responses
- **Speech Recognition**: Voice input processing
- **Edge TTS**: Text-to-speech output

### Communication Flow
```
User Input (Voice/Text)
    ↓
WebSocket → Flask Server
    ↓
Assistant Core → Gemini AI
    ↓
Response Processing
    ↓
WebSocket → Browser UI
    ↓
Display + Voice Output
```

## File Structure

```
jarvis/
├── app/
│   ├── application/        # Business logic
│   ├── domain/            # Core models
│   ├── infrastructure/    # External services
│   └── presentation/      # UI layer
│       ├── static/        # Web assets
│       │   ├── index.html # Main UI
│       │   ├── styles.css # Styling
│       │   └── app.js     # Frontend logic
│       ├── gui.py         # Legacy tkinter UI
│       └── web_server.py  # Flask server
├── plugins/               # Command plugins
├── main.py               # Legacy entry point
├── main_web.py           # Web interface entry point
└── requirements.txt      # Dependencies
```

## Customization

### Colors
Edit `styles.css` and modify the CSS variables:
```css
:root {
    --primary-cyan: #00d9ff;
    --primary-blue: #0066ff;
    --accent-gold: #ffd700;
    /* ... more colors */
}
```

### Voice Visualizer
Modify the `drawVisualizer()` function in `app.js` to change the animation style.

### System Metrics
Update the `updateMetrics()` function to show real system data instead of simulated values.

## Troubleshooting

### WebSocket Connection Failed
- Ensure Flask server is running
- Check firewall settings
- Verify port 5000 is not in use

### Voice Not Working
- Check microphone permissions
- Ensure PyAudio is installed correctly
- Verify internet connection (for online STT)

### UI Not Loading
- Clear browser cache
- Check browser console for errors
- Ensure all static files are present

## Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Internet Explorer (Not supported)

## Performance Tips

1. **Use Chrome/Edge**: Best performance for Canvas animations
2. **Close Unused Tabs**: Reduces CPU usage
3. **Disable Particles**: Comment out `createParticles()` for lower-end devices
4. **Reduce Visualizer Bars**: Lower the `bars` variable in `drawVisualizer()`

## Future Enhancements

- [ ] Real system metrics integration
- [ ] Voice activity detection visualization
- [ ] Command suggestions/autocomplete
- [ ] Dark/Light theme toggle
- [ ] Mobile app version
- [ ] Multi-user support
- [ ] Command macros/shortcuts
- [ ] Plugin management UI

## Credits

Inspired by the Jarvis AI assistant from Iron Man.

## License

MIT License - Feel free to use and modify!
