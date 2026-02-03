// WebSocket connection
let ws = null;
let isListening = false;
let audioContext = null;
let analyser = null;
let dataArray = null;
let animationId = null;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const voiceIcon = document.getElementById('voiceIcon');
const voiceText = document.getElementById('voiceText');
const commandList = document.getElementById('commandList');
const systemStatus = document.getElementById('systemStatus');
const voiceStatus = document.getElementById('voiceStatus');
const currentTime = document.getElementById('currentTime');
const voiceVisualizer = document.getElementById('voiceVisualizer');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
    initVoiceVisualizer();
    initEventListeners();
    updateTime();
    createParticles();
    
    // Update time every second
    setInterval(updateTime, 1000);
    
    // Update metrics periodically
    setInterval(updateMetrics, 2000);
});

// WebSocket Connection
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        updateSystemStatus('ONLINE', 'success');
        addSystemMessage('WebSocket connection established');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateSystemStatus('ERROR', 'error');
    };
    
    ws.onclose = () => {
        console.log('WebSocket disconnected');
        updateSystemStatus('OFFLINE', 'error');
        addSystemMessage('Connection lost. Attempting to reconnect...');
        
        // Attempt to reconnect after 3 seconds
        setTimeout(initWebSocket, 3000);
    };
}

// Handle WebSocket Messages
function handleWebSocketMessage(data) {
    switch(data.type) {
        case 'assistant_response':
            addAssistantMessage(data.text);
            break;
        case 'voice_state':
            updateVoiceState(data.state);
            break;
        case 'command_executed':
            addCommandToHistory(data.command);
            break;
        case 'transcription':
            addUserMessage(data.text);
            break;
        case 'thought':
            addSystemMessage(data.text);
            break;
        case 'system_status':
            updateSystemStatus(data.status, data.level);
            break;
        default:
            console.log('Unknown message type:', data.type);
    }
}

// Event Listeners
function initEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    voiceBtn.addEventListener('click', toggleVoiceListening);
}

// Send Message
function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    
    addUserMessage(text);
    userInput.value = '';
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'user_input',
            text: text
        }));
    }
}

// Toggle Voice Listening
function toggleVoiceListening() {
    isListening = !isListening;
    
    if (isListening) {
        voiceBtn.classList.add('active');
        voiceIcon.classList.add('active');
        voiceText.textContent = 'Listening...';
        
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'start_listening'
            }));
        }
    } else {
        voiceBtn.classList.remove('active');
        voiceIcon.classList.remove('active');
        voiceText.textContent = 'Click to speak';
        
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'stop_listening'
            }));
        }
    }
}

// Update Voice State
function updateVoiceState(state) {
    voiceStatus.textContent = state.toUpperCase();
    voiceText.textContent = state;
    
    const statusColors = {
        'idle': 'var(--text-secondary)',
        'listening': 'var(--primary-cyan)',
        'transcribing': 'var(--warning)',
        'thinking': 'var(--primary-blue)',
        'speaking': 'var(--success)',
        'booting': 'var(--accent-gold)'
    };
    
    voiceStatus.style.color = statusColors[state.toLowerCase()] || 'var(--text-secondary)';
    
    if (state.toLowerCase() === 'listening') {
        voiceIcon.classList.add('active');
    } else {
        voiceIcon.classList.remove('active');
    }
}

// Add Messages
function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <span class="timestamp">[${getCurrentTimestamp()}]</span>
        <p>${escapeHtml(text)}</p>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addAssistantMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message';
    messageDiv.innerHTML = `
        <span class="timestamp">[${getCurrentTimestamp()}] JARVIS</span>
        <p>${escapeHtml(text)}</p>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system-message';
    messageDiv.innerHTML = `
        <span class="timestamp">[${getCurrentTimestamp()}] SYSTEM</span>
        <p>${escapeHtml(text)}</p>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add Command to History
function addCommandToHistory(command) {
    const commandDiv = document.createElement('div');
    commandDiv.className = 'command-item';
    commandDiv.innerHTML = `
        <div class="cmd-time">${getCurrentTimestamp()}</div>
        <div class="cmd-text">${escapeHtml(command)}</div>
    `;
    commandList.insertBefore(commandDiv, commandList.firstChild);
    
    // Keep only last 10 commands
    while (commandList.children.length > 10) {
        commandList.removeChild(commandList.lastChild);
    }
}

// Voice Visualizer
function initVoiceVisualizer() {
    const canvas = voiceVisualizer;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Animation variables
    let time = 0;
    const bars = 64;
    
    function drawVisualizer() {
        const width = canvas.width;
        const height = canvas.height;
        
        ctx.clearRect(0, 0, width, height);
        
        const barWidth = width / bars;
        const centerY = height / 2;
        
        for (let i = 0; i < bars; i++) {
            const x = i * barWidth;
            
            // Create wave effect
            const wave1 = Math.sin(time * 0.05 + i * 0.2) * 30;
            const wave2 = Math.sin(time * 0.03 + i * 0.15) * 20;
            const barHeight = Math.abs(wave1 + wave2) + 10;
            
            // Gradient
            const gradient = ctx.createLinearGradient(x, centerY - barHeight, x, centerY + barHeight);
            gradient.addColorStop(0, 'rgba(0, 217, 255, 0.8)');
            gradient.addColorStop(0.5, 'rgba(0, 102, 255, 0.6)');
            gradient.addColorStop(1, 'rgba(0, 217, 255, 0.8)');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(x, centerY - barHeight / 2, barWidth - 2, barHeight);
            
            // Glow effect
            ctx.shadowBlur = 15;
            ctx.shadowColor = 'rgba(0, 217, 255, 0.5)';
        }
        
        time++;
        animationId = requestAnimationFrame(drawVisualizer);
    }
    
    drawVisualizer();
}

// Update System Status
function updateSystemStatus(status, level) {
    systemStatus.textContent = status;
    
    const colors = {
        'success': 'var(--success)',
        'warning': 'var(--warning)',
        'error': 'var(--error)',
        'info': 'var(--primary-cyan)'
    };
    
    systemStatus.style.color = colors[level] || 'var(--success)';
    systemStatus.style.textShadow = `0 0 10px ${colors[level] || 'var(--success)'}`;
}

// Update Time
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    currentTime.textContent = `${hours}:${minutes}:${seconds}`;
}

// Update Metrics (Simulated)
function updateMetrics() {
    const cpuMetric = document.getElementById('cpuMetric');
    const memMetric = document.getElementById('memMetric');
    const netMetric = document.getElementById('netMetric');
    
    // Simulate random metrics
    const cpu = Math.floor(Math.random() * 40) + 30;
    const mem = Math.floor(Math.random() * 30) + 50;
    const net = Math.floor(Math.random() * 50) + 10;
    
    cpuMetric.style.width = `${cpu}%`;
    cpuMetric.nextElementSibling.nextElementSibling.textContent = `${cpu}%`;
    
    memMetric.style.width = `${mem}%`;
    memMetric.nextElementSibling.nextElementSibling.textContent = `${mem}%`;
    
    netMetric.style.width = `${net}%`;
    netMetric.nextElementSibling.nextElementSibling.textContent = `${net}%`;
}

// Create Particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = '2px';
        particle.style.height = '2px';
        particle.style.background = 'var(--primary-cyan)';
        particle.style.borderRadius = '50%';
        particle.style.boxShadow = '0 0 5px var(--primary-cyan)';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        particle.style.animation = `float ${Math.random() * 10 + 10}s linear infinite`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        
        particlesContainer.appendChild(particle);
    }
    
    // Add float animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% { transform: translateY(0) translateX(0); }
            50% { transform: translateY(-20px) translateX(10px); }
            100% { transform: translateY(0) translateX(0); }
        }
    `;
    document.head.appendChild(style);
}

// Utility Functions
function getCurrentTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { hour12: false });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
