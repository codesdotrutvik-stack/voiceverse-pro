import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✨", layout="wide")

# ============================================================
# LIGHT MODE CSS - CLEAN & PREMIUM
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #f5f7fb !important;
}

#MainMenu, footer, header {
    visibility: hidden !important;
    display: none !important;
}

.block-container {
    padding: 1.5rem 2rem 4rem !important;
    max-width: 1000px !important;
}

/* Header */
.mesta-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-logo {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: white;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.header-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
}

.header-sub {
    font-size: 0.7rem;
    color: #64748b;
    margin-top: 2px;
}

.header-badge {
    font-size: 0.7rem;
    background: #e0e7ff;
    padding: 5px 14px;
    border-radius: 20px;
    color: #7c3aed;
    font-weight: 600;
}

/* Mode Toggle */
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 50px !important;
    padding: 4px !important;
    width: fit-content !important;
    margin: 0 auto 1.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

div[data-testid="stRadio"] label {
    padding: 8px 28px !important;
    border-radius: 40px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    background: transparent !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
}

/* Status */
.status-pill {
    text-align: center;
    margin-bottom: 1.5rem;
}

.status-pill span {
    font-size: 0.8rem;
    padding: 6px 18px;
    border-radius: 30px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #64748b;
}

/* Mic Button */
.mic-area {
    text-align: center;
    margin: 2rem 0;
}

.mic-btn {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: white;
    border: 2px solid #e2e8f0;
    font-size: 2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #7c3aed;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.mic-btn:hover {
    transform: scale(1.02);
    border-color: #8b5cf6;
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.2);
}

.mic-btn-active {
    background: #fee2e2;
    border-color: #ef4444;
    animation: micPulse 1.5s infinite;
}

@keyframes micPulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.2); }
    50% { box-shadow: 0 0 0 16px rgba(239,68,68,0.08); }
}

.mic-hint {
    font-size: 0.7rem;
    color: #94a3b8;
    margin-top: 10px;
}

/* Text Input */
.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 50px !important;
    padding: 14px 20px !important;
    color: #1e293b !important;
    font-size: 0.9rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.stTextInput > div > div > input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #94a3b8 !important;
}

/* Buttons */
.stButton > button {
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
    border-radius: 50px !important;
    padding: 10px 24px !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #e2e8f0 !important;
    border-color: #cbd5e1 !important;
    color: #1e293b !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    border: none !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    transform: translateY(-1px);
}

/* Chat Bubbles */
.user-msg {
    margin: 1rem 0 0.5rem auto;
    max-width: 70%;
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    color: white;
    border-radius: 20px 20px 4px 20px;
    padding: 12px 18px;
    text-align: right;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.15);
}

.ai-msg {
    margin: 0.5rem 0 1rem;
    max-width: 70%;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px 20px 20px 4px;
    padding: 12px 18px;
    color: #1e293b;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.msg-label {
    font-size: 0.6rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    opacity: 0.7;
}

.ai-label {
    color: #8b5cf6;
}

.timestamp {
    font-size: 0.6rem;
    color: #94a3b8;
    margin-top: 6px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

[data-testid="stSidebar"] * {
    color: #475569 !important;
}

.sidebar-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b5cf6 !important;
    margin-bottom: 12px;
}

.sidebar-stat {
    font-size: 0.75rem;
    color: #64748b;
}

.sidebar-stat span {
    color: #8b5cf6;
    font-weight: 600;
}

/* Quick Questions */
.quick-section {
    margin: 2rem 0;
}

.quick-title {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    margin-bottom: 12px;
}

.quick-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.quick-btn {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 0.75rem;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s;
}

.quick-btn:hover {
    background: #f1f5f9;
    border-color: #8b5cf6;
    color: #8b5cf6;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 1.5rem 0;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.6rem;
    color: #94a3b8;
    padding: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid #e2e8f0;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}
</style>

<script>
let recognition = null;

function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        document.getElementById('statusMsg').innerHTML = '❌ Use Chrome browser';
        return;
    }
    
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        document.getElementById('statusMsg').innerHTML = '🎤 Listening... Speak now';
        document.getElementById('micBtn').style.background = '#fee2e2';
        document.getElementById('micBtn').style.borderColor = '#ef4444';
    };
    
    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById('statusMsg').innerHTML = '📝 Processing: ' + text;
        
        const input = document.querySelector('input[data-testid="stTextInput"]');
        if (input) {
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        setTimeout(() => {
            const btns = document.querySelectorAll('button');
            for (let btn of btns) {
                if (btn.innerText === '✨ Ask Mesta' || btn.innerText === 'Ask Mesta') {
                    btn.click();
                    break;
                }
            }
        }, 100);
        
        resetMic();
    };
    
    recognition.onerror = function() {
        resetMic();
    };
    
    recognition.start();
}

function resetMic() {
    document.getElementById('micBtn').style.background = 'white';
    document.getElementById('micBtn').style.borderColor = '#e2e8f0';
    document.getElementById('statusMsg').innerHTML = '● Ready';
}

function speakAnswer(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    utterance.onstart = () => document.getElementById('statusMsg').innerHTML = '🔊 Speaking...';
    utterance.onend = () => document.getElementById('statusMsg').innerHTML = '● Ready';
    window.speechSynthesis.speak(utterance);
}
</script>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="mesta-header">
    <div class="header-left">
        <div class="header-logo">✨</div>
        <div>
            <div class="header-title">Mesta AI</div>
            <div class="header-sub">Intelligent Assistant</div>
        </div>
    </div>
    <div class="header-badge">v1.0</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONFIG
# ============================================================
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

if "history" not in st.session_state:
    st.session_state.history = []
if "mode" not in st.session_state:
    st.session_state.mode = "text"

# ============================================================
# MODE TOGGLE
# ============================================================
mode = st.radio("", ["⌨️ Text Mode", "🎤 Voice Mode"], horizontal=True, label_visibility="collapsed")
st.session_state.mode = "text" if "Text" in mode else "voice"

# ============================================================
# STATUS
# ============================================================
st.markdown('<div class="status-pill"><span id="statusMsg">● Ready</span></div>', unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================
def ask_mesta(q):
    try:
        response = requests.post(
            MISTRAL_URL,
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
            json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": q}], "max_tokens": 200},
            timeout=15
        )
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Connection issue. Please try again."

def process(q):
    if not q.strip():
        return
    answer = ask_mesta(q)
    st.session_state.history.append({"q": q, "a": answer, "t": datetime.now().strftime("%I:%M %p")})
    safe = answer.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    st.markdown(f'<script>speakAnswer("{safe}");</script>', unsafe_allow_html=True)
    st.rerun()

# ============================================================
# TEXT MODE
# ============================================================
if st.session_state.mode == "text":
    user_input = st.text_input("", placeholder="Ask Mesta anything...", key="text_input", label_visibility="collapsed")
    if st.button("✨ Ask Mesta", use_container_width=False, type="primary"):
        if user_input:
            with st.spinner("Thinking..."):
                process(user_input)

# ============================================================
# VOICE MODE
# ============================================================
else:
    st.markdown("""
    <div class="mic-area">
        <button class="mic-btn" id="micBtn" onclick="startVoice()">🎤</button>
        <div class="mic-hint">Tap to speak</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# QUICK QUESTIONS
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="quick-title">🔥 QUICK QUESTIONS</div>', unsafe_allow_html=True)
st.markdown('<div class="quick-grid">', unsafe_allow_html=True)

quick_qs = ["Who are you?", "What can you do?", "Tell me something inspiring", "Future of AI", "What is machine learning?", "Tell me a joke"]

for q in quick_qs:
    st.markdown(f'<div class="quick-btn" onclick="document.querySelector(\'input[placeholder=\\\"Ask Mesta anything...\\\"]\').value = \'{q}\'; document.querySelector(\'button[kind=\\\"primary\\\"]\')?.click();">{q}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CONVERSATION HISTORY
# ============================================================
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="quick-title">💬 CONVERSATION</div>', unsafe_allow_html=True)
    
    for chat in reversed(st.session_state.history[-20:]):
        st.markdown(f'<div class="user-msg"><strong>You</strong><br>{chat["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-msg"><strong>✨ Mesta</strong><br>{chat["a"]}<br><span class="timestamp">{chat["t"]}</span></div>', unsafe_allow_html=True)

# ============================================================
# CLEAR BUTTON
# ============================================================
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer">✨ Mesta AI · Created by Nirbhay · Powered by Mistral AI</div>', unsafe_allow_html=True)