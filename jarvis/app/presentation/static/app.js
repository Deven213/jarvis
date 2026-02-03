const termOutput = document.getElementById('terminalOutput');
const userInput = document.getElementById('userInput');
const orb = document.getElementById('orb');
const mainStatus = document.getElementById('mainStatus');

let socket;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initSocketIO();
    initEventListeners();
    logToTerminal('System Initialized. Accessing Neural Network...');
    logToTerminal('Waiting for Voice Input...');
});

// Socket.IO Connection
function initSocketIO() {
    socket = io();

    socket.on('connect', () => {
        logToTerminal('Socket Link Established.');
        updateSystemStatus('ONLINE');

        // Tells the server to actually start the voice loop
        socket.emit('message', { type: 'start_listening' });

        // Update UI
        updateVoiceState('listening');
    });

    socket.on('message', (data) => {
        handleSocketMessage(data);
    });

    socket.on('disconnect', () => {
        logToTerminal('WARNING: Link Severed. Reconnecting...');
        updateSystemStatus('OFFLINE');
    });
}

function handleSocketMessage(data) {
    switch (data.type) {
        case 'assistant_response':
            logToTerminal(`JARVIS: ${data.text}`);
            break;
        case 'voice_state':
            updateVoiceState(data.state);
            break;
        case 'transcription':
            logToTerminal(`COMMAND: ${data.text}`);
            break;
        case 'system_status':
            if (data.status === 'READY') {
                updateSystemStatus('ONLINE');
                logToTerminal('System Fully Operational.');
            }
            break;
        case 'thought':
            // Optional: Log thoughts if needed
            // logToTerminal(`THOUGHT: ${data.text}`);
            break;
        case 'command_executed':
            logToTerminal(`EXECUTING: ${data.command}`);
            updateVoiceState('executing');
            break;
    }
}

// Event Listeners
function initEventListeners() {
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const text = userInput.value.trim();
            if (text) {
                sendMessage(text);
                userInput.value = '';
            }
        }
    });

    // Focus input on any key press if not already focused
    document.addEventListener('keydown', (e) => {
        if (document.activeElement !== userInput) {
            userInput.focus();
        }
    });
}

// Send Message
function sendMessage(text) {
    logToTerminal(`USER: ${text}`);
    if (socket && socket.connected) {
        socket.emit('message', {
            type: 'user_input',
            text: text
        });
    }
}

// Update System Status Text
function updateSystemStatus(status) {
    const topStatus = document.querySelector('.top-statusbox');
    if (topStatus) topStatus.textContent = status;
}

// Update Voice State & UI Animations
function updateVoiceState(state) {
    if (!mainStatus || !orb) return;

    const cleanState = state.toLowerCase();
    mainStatus.textContent = cleanState.toUpperCase();

    // Reset classes
    orb.className = 'orb';
    mainStatus.className = 'main-status';

    if (cleanState === 'listening') {
        orb.style.background = 'radial-gradient(circle, #ccfffc 0%, #00ffea 60%, transparent 100%)';
        orb.style.boxShadow = '0 0 50px rgba(0, 255, 234, 0.6)';
        mainStatus.style.color = 'var(--primary-cyan)';
    }
    else if (cleanState === 'transcribing' || cleanState === 'thinking' || cleanState === 'processing') {
        orb.classList.add('active');
        orb.style.background = 'radial-gradient(circle, #fff 0%, #00aaff 60%, transparent 100%)';
        orb.style.boxShadow = '0 0 80px rgba(0, 170, 255, 0.8)';
        mainStatus.style.color = '#00aaff';
        mainStatus.textContent = 'PROCESSING';
    }
    else if (cleanState === 'speaking') {
        orb.classList.add('active');
        orb.style.background = 'radial-gradient(circle, #fff 0%, #00ff9d 60%, transparent 100%)';
        orb.style.boxShadow = '0 0 80px rgba(0, 255, 157, 0.8)';
        mainStatus.style.color = '#00ff9d';
    }
    else if (cleanState === 'executing') {
        orb.classList.add('active');
        orb.style.background = 'radial-gradient(circle, #fff 0%, #ff00ea 60%, transparent 100%)';
        orb.style.boxShadow = '0 0 80px rgba(255, 0, 234, 0.8)';
        mainStatus.style.color = '#ff00ea';
    }
    else {
        // Idle
        orb.style.background = 'radial-gradient(circle, #ccfffc 0%, #00ffea 60%, transparent 100%)';
        mainStatus.textContent = 'STANDBY';
        mainStatus.style.color = 'var(--text-dim)';
    }
}

// Log to Terminal
function logToTerminal(text) {
    if (!termOutput) return;

    // Check for max lines to prevent overflow lag
    while (termOutput.children.length > 50) {
        termOutput.removeChild(termOutput.firstChild);
    }

    const time = new Date().toLocaleTimeString();
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerHTML = `<span class="log-time">[${time}]</span> ${escapeHtml(text)}`;

    termOutput.appendChild(line);
    termOutput.scrollTop = termOutput.scrollHeight;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
