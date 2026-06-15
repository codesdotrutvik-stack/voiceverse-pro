import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✨", layout="wide")

# ============================================================
# CSS WITH VOICE SCRIPTS
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
    background: #f8fafc !important;
}

#MainMenu, footer, header {
    visibility: hidden !important;
    display: none !important;
}

.block-container {
    padding: 1.5rem 2rem 4rem !important;
    max-width: 1000px !important;
}

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
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    color: white;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.header-title {
    font-size: 1.4rem;
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
    padding: 4px 12px;
    border-radius: 20px;
    color: #7c3aed;
    font-weight: 600;
}

.status-box {
    text-align: center;
    margin-bottom: 1.5rem;
}

.status-box span {
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

.voice-btn {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    color: white;
    border: none;
    border-radius: 60px;
    padding: 14px 40px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    width: 100%;
}

.voice-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 50px !important;
    padding: 12px 20px !important;
    color: #1e293b !important;
    font-size: 0.9rem !important;
    outline: none !important;
}

.stTextInput > div > div > input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1) !important;
}

.stButton > button {
    background: #f1f5f9 !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
    border-radius: 50px !important;
    padding: 8px 20px !important;
    font-size: 0.85rem !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    border: none !important;
    color: white !important;
}

.user-bubble {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    color: white;
    padding: 12px 18px;
    border-radius: 20px;
    border-bottom-right-radius: 4px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 75%;
    text-align: right;
}

.ai-bubble {
    background: white;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    padding: 12px 18px;
    border-radius: 20px;
    border-bottom-left-radius: 4px;
    margin: 8px 0;
    max-width: 75%;
}

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    margin: 1.5rem 0 0.8rem 0;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 1.5rem 0;
}

.footer {
    text-align: center;
    font-size: 0.65rem;
    color: #94a3b8;
    padding: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid #e2e8f0;
}

/* Audio player hidden */
.audio-player {
    display: none;
}
</style>

<script>
function speakMessage(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        var utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 1;
        window.speechSynthesis.speak(utterance);
        return true;
    }
    return false;
}

function startVoiceRecognition() {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        document.getElementById('statusMsg').innerHTML = '❌ Speech not supported. Use Chrome.';
        return;
    }
    
    var recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
        document.getElementById('statusMsg').innerHTML = '🎤 Listening... Speak now';
        document.getElementById('statusMsg').style.background = '#fee2e2';
        document.getElementById('statusMsg').style.color = '#991b1b';
    };
    
    recognition.onresult = function(event) {
        var text = event.results[0][0].transcript;
        document.getElementById('statusMsg').innerHTML = '📝 You said: ' + text;
        document.getElementById('statusMsg').style.background = '#dbeafe';
        document.getElementById('statusMsg').style.color = '#1e40af';
        
        var input = document.querySelector('input[data-testid="stTextInput"]');
        if (input) {
            input.value = text;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        setTimeout(function() {
            var btns = document.querySelectorAll('button');
            for (var i = 0; i < btns.length; i++) {
                if (btns[i].innerText === '🔊 Ask') {
                    btns[i].click();
                    break;
                }
            }
        }, 500);
    };
    
    recognition.onerror = function() {
        document.getElementById('statusMsg').innerHTML = '❌ Try again';
        document.getElementById('statusMsg').style.background = '#ffffff';
        document.getElementById('statusMsg').style.color = '#64748b';
    };
    
    recognition.start();
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mode" not in st.session_state:
    st.session_state.mode = "text"

# ============================================================
# MODE TOGGLE
# ============================================================
col1, col2 = st.columns(2)
with col1:
    if st.button("⌨️ Text Mode", key="text_mode", use_container_width=True):
        st.session_state.mode = "text"
        st.rerun()
with col2:
    if st.button("🎤 Voice Mode", key="voice_mode", use_container_width=True):
        st.session_state.mode = "voice"
        st.rerun()

if st.session_state.mode == "text":
    st.info("✨ Text Mode Active - Type your question below")
else:
    st.info("🎤 Voice Mode Active - Click the microphone button and speak")

# ============================================================
# STATUS
# ============================================================
st.markdown('<div class="status-box"><span id="statusMsg">● Ready</span></div>', unsafe_allow_html=True)

# ============================================================
# VOICE MODE BUTTON
# ============================================================
if st.session_state.mode == "voice":
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <button class="voice-btn" onclick="startVoiceRecognition()">🎤 Click to Speak</button>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TEXT INPUT
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">💬 ASK MESTA</div>', unsafe_allow_html=True)

user_question = st.text_input("", placeholder="Ask Mesta anything...", key="text_input", label_visibility="collapsed")

col1, col2 = st.columns([1, 4])
with col1:
    ask_clicked = st.button("🔊 Ask", use_container_width=True, type="primary")
with col2:
    clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)

# ============================================================
# API FUNCTION
# ============================================================
def ask_mistral(question):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are Mesta AI, a helpful assistant. Answer clearly and concisely in 2-3 sentences."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 200
    }
    try:
        response = requests.post(MISTRAL_URL, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Connection issue. Please try again."

# ============================================================
# PROCESS QUESTION WITH VOICE
# ============================================================
if ask_clicked and user_question:
    with st.spinner("✨ Thinking..."):
        answer = ask_mistral(user_question)
        st.session_state.chat_history.append({
            "q": user_question,
            "a": answer,
            "t": datetime.now().strftime("%I:%M %p")
        })
        # Speak using JavaScript
        safe_answer = answer.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
        st.markdown(f'<script>speakMessage("{safe_answer}");</script>', unsafe_allow_html=True)
        st.rerun()

if clear_clicked:
    st.session_state.chat_history = []
    st.rerun()

# ============================================================
# QUICK QUESTIONS
# ============================================================
st.markdown('<div class="section-title">🔥 QUICK QUESTIONS</div>', unsafe_allow_html=True)

quick_qs = ["Who are you?", "What can you do?", "Tell me something inspiring", "Future of AI", "What is machine learning?", "Tell me a joke"]

cols = st.columns(3)
for i, q in enumerate(quick_qs):
    with cols[i % 3]:
        if st.button(q, use_container_width=True):
            with st.spinner("✨ Thinking..."):
                answer = ask_mistral(q)
                st.session_state.chat_history.append({
                    "q": q,
                    "a": answer,
                    "t": datetime.now().strftime("%I:%M %p")
                })
                safe_answer = answer.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
                st.markdown(f'<script>speakMessage("{safe_answer}");</script>', unsafe_allow_html=True)
                st.rerun()

# ============================================================
# CHAT HISTORY
# ============================================================
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 CONVERSATION</div>', unsafe_allow_html=True)
    
    for chat in reversed(st.session_state.chat_history[-15:]):
        st.markdown(f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-bubble"><strong>✨ Mesta</strong><br>{chat["a"]}<br><span style="font-size:0.6rem;color:#94a3b8;">{chat["t"]}</span></div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer">✨ Mesta AI · Created by Nirbhay · Powered by Mistral AI</div>', unsafe_allow_html=True)

# ============================================================
# AUTO SPEAK ON LOAD (for testing)
# ============================================================
st.markdown('<script>console.log("Mesta AI loaded - Voice ready");</script>', unsafe_allow_html=True)