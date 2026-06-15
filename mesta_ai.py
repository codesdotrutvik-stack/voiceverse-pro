import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #0a0a12 !important;
    color: #e2e8f0 !important;
}
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 900px !important; }

/* Header */
.mesta-header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 1rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-logo {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.header-title { font-size: 1rem; font-weight: 600; color: #f1f5f9; }
.header-sub { font-size: 0.6rem; color: #475569; margin-top: 1px; }
.model-badge {
    font-size: 0.6rem; background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 4px 10px; border-radius: 20px; color: #64748b;
}

/* Input - NO WHITE BORDER */
.stTextInput > div > div > input {
    background: #12121e !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    color: #f1f5f9 !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #334155 !important;
}

/* Buttons */
.stButton > button {
    background: #12121e !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #9ca3af !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-size: 0.75rem !important;
}
.stButton > button:hover {
    background: #1a1a2a !important;
    color: #e2e8f0 !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    color: white !important;
}

/* Chat Bubbles - VISIBLE TEXT */
.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    padding: 10px 14px;
    border-radius: 16px 16px 4px 16px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 70%;
    font-size: 0.85rem;
}
.ai-bubble {
    background: #12121e;
    border: 1px solid rgba(255,255,255,0.06);
    color: #e2e8f0;
    padding: 10px 14px;
    border-radius: 16px 16px 16px 4px;
    margin: 8px 0;
    max-width: 70%;
    font-size: 0.85rem;
}
.ai-name {
    font-size: 0.6rem;
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.msg-time {
    font-size: 0.5rem;
    color: #334155;
    margin-top: 4px;
}

/* Section Labels - VISIBLE */
.section-label {
    font-size: 0.6rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #a78bfa;
    margin: 1rem 0 0.5rem 0;
}
.divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 1rem 0;
}
.mode-indicator {
    font-size: 0.65rem;
    color: #64748b;
    margin-bottom: 0.5rem;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.55rem;
    color: #1e293b;
    padding: 1.5rem;
    margin-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.03);
}
</style>

<script>
function speakAnswer(text, voiceType) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'en-US';
        
        var voices = window.speechSynthesis.getVoices();
        
        if (voiceType === 'man') {
            msg.pitch = 0.8;
            msg.rate = 0.9;
            var maleVoice = voices.find(v => v.name.toLowerCase().includes('david') || 
                                               v.name.toLowerCase().includes('google uk english male') ||
                                               (v.lang === 'en-US' && v.name.toLowerCase().indexOf('female') === -1));
            if (maleVoice) msg.voice = maleVoice;
        } else if (voiceType === 'woman') {
            msg.pitch = 1.2;
            msg.rate = 1.0;
            var femaleVoice = voices.find(v => v.name.toLowerCase().includes('samantha') || 
                                                 v.name.toLowerCase().includes('google uk english female') ||
                                                 v.name.toLowerCase().includes('female'));
            if (femaleVoice) msg.voice = femaleVoice;
        } else {
            msg.pitch = 1.0;
            msg.rate = 0.95;
            var naturalVoice = voices.find(v => v.name.toLowerCase().includes('google') || 
                                                  v.name.toLowerCase().includes('natural'));
            if (naturalVoice) msg.voice = naturalVoice;
        }
        
        window.speechSynthesis.speak(msg);
    }
}
</script>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="mesta-header">
    <div class="header-left">
        <div class="header-logo">✦</div>
        <div>
            <div class="header-title">Mesta AI</div>
            <div class="header-sub">Intelligent Assistant</div>
        </div>
    </div>
    <div class="model-badge">Mistral AI</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONFIG
# ============================================================
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "response_mode" not in st.session_state:
    st.session_state.response_mode = "voice"
if "voice_type" not in st.session_state:
    st.session_state.voice_type = "woman"

# ============================================================
# FUNCTIONS
# ============================================================
def ask_mistral(question):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 200
    }
    try:
        response = requests.post(MISTRAL_URL, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Connection issue. Please try again."

# ============================================================
# RESPONSE MODE
# ============================================================
st.markdown('<div class="section-label">⚡ RESPONSE MODE</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("📝 Text Only", use_container_width=True, 
                 type="primary" if st.session_state.response_mode == "text" else "secondary"):
        st.session_state.response_mode = "text"
        st.rerun()
with col2:
    if st.button("🔊 Voice Output", use_container_width=True,
                 type="primary" if st.session_state.response_mode == "voice" else "secondary"):
        st.session_state.response_mode = "voice"
        st.rerun()

# ============================================================
# VOICE TYPE (Only when voice mode is active)
# ============================================================
if st.session_state.response_mode == "voice":
    st.markdown('<div class="section-label">🎙 VOICE TYPE</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨 Man", use_container_width=True,
                     type="primary" if st.session_state.voice_type == "man" else "secondary"):
            st.session_state.voice_type = "man"
            st.rerun()
    with col2:
        if st.button("👩 Woman", use_container_width=True,
                     type="primary" if st.session_state.voice_type == "woman" else "secondary"):
            st.session_state.voice_type = "woman"
            st.rerun()
    with col3:
        if st.button("🎭 Realistic", use_container_width=True,
                     type="primary" if st.session_state.voice_type == "realistic" else "secondary"):
            st.session_state.voice_type = "realistic"
            st.rerun()

# ============================================================
# QUICK QUESTIONS
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">⚡ QUICK QUESTIONS</div>', unsafe_allow_html=True)

quick_qs = [
    "Explain Quantum Computing",
    "Write Python code for data analysis",
    "Ideas for a startup",
    "Latest AI trends",
    "Tell me a joke",
    "What is machine learning?"
]

cols = st.columns(3)
for i, q in enumerate(quick_qs):
    with cols[i % 3]:
        if st.button(q, use_container_width=True):
            with st.spinner("Thinking..."):
                answer = ask_mistral(q)
                st.session_state.chat_history.append({
                    "q": q,
                    "a": answer,
                    "t": datetime.now().strftime("%I:%M %p"),
                    "mode": st.session_state.response_mode,
                    "voice": st.session_state.voice_type
                })
                st.rerun()

# ============================================================
# INPUT
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">💬 ASK MESTA</div>', unsafe_allow_html=True)

user_question = st.text_input("", placeholder="Ask Mesta anything...", key="text_input", label_visibility="collapsed")

col1, col2 = st.columns([1, 4])
with col1:
    ask_clicked = st.button("✨ Ask Mesta", use_container_width=True, type="primary")
with col2:
    clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)

if ask_clicked and user_question:
    with st.spinner("Thinking..."):
        answer = ask_mistral(user_question)
        st.session_state.chat_history.append({
            "q": user_question,
            "a": answer,
            "t": datetime.now().strftime("%I:%M %p"),
            "mode": st.session_state.response_mode,
            "voice": st.session_state.voice_type
        })
        st.rerun()

if clear_clicked:
    st.session_state.chat_history = []
    st.rerun()

# ============================================================
# CONVERSATION HISTORY
# ============================================================
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 CONVERSATION</div>', unsafe_allow_html=True)
    
    for chat in reversed(st.session_state.chat_history[-15:]):
        voice_icon = ""
        if chat.get("mode") == "voice":
            voice_icon = {"man": "👨", "woman": "👩", "realistic": "🎭"}.get(chat.get("voice"), "")
        
        st.markdown(f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>', unsafe_allow_html=True)
        
        mode_text = "🔊 Voice" if chat.get("mode") == "voice" else "📝 Text"
        st.markdown(f'''
        <div class="ai-bubble">
            <div class="ai-name">✦ Mesta {voice_icon} <span style="color:#475569; font-size:0.5rem;">({mode_text})</span></div>
            {chat["a"]}
            <div class="msg-time">{chat["t"]}</div>
        </div>
        ''', unsafe_allow_html=True)

# ============================================================
# VOICE OUTPUT AFTER DISPLAY
# ============================================================
if st.session_state.chat_history and st.session_state.chat_history[-1].get("mode") == "voice":
    last_chat = st.session_state.chat_history[-1]
    answer_text = last_chat["a"]
    voice = last_chat.get("voice", "woman")
    safe_answer = answer_text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    st.markdown(f'<script>speakAnswer("{safe_answer}", "{voice}");</script>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer">✦ Mesta AI · Created by Nirbhay · Powered by Mistral AI</div>', unsafe_allow_html=True)