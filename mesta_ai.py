import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #0a0b14 !important;
    color: #e2e8f0 !important;
}

#MainMenu, footer, header { visibility: hidden !important; display: none !important; }

.block-container {
    padding: 0 2rem 4rem !important;
    max-width: 860px !important;
}

/* ── HEADER ── */
.mesta-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.4rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.header-title { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; }
.header-sub { font-size: 0.68rem; color: #64748b; margin-top: 1px; }
.header-right { display: flex; align-items: center; gap: 10px; }
.online-dot {
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 6px #22c55e;
    display: inline-block;
}
.model-badge {
    font-size: 0.68rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 4px 12px;
    border-radius: 20px;
    color: #94a3b8;
}

/* ── HERO SECTION ── */
.hero {
    text-align: center;
    padding: 2.8rem 0 2rem 0;
    position: relative;
}
.hero-greeting {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    margin-bottom: 2rem;
}

/* ── MIC BUTTON AREA ── */
.mic-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    margin-bottom: 2rem;
}
.mic-ring {
    width: 90px; height: 90px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    box-shadow: 0 0 40px rgba(124,58,237,0.4), 0 0 80px rgba(124,58,237,0.15);
    cursor: pointer;
    transition: all 0.3s;
    border: 3px solid rgba(167,139,250,0.3);
}
.mic-label {
    font-size: 0.78rem;
    color: #64748b;
    letter-spacing: 0.5px;
}

/* ── WAVE SVG ── */
.wave-wrap {
    position: relative;
    width: 100%;
    height: 60px;
    margin: -1rem 0 1rem 0;
    opacity: 0.35;
    overflow: hidden;
}

/* ── MODE TOGGLE ── */
.mode-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 1.8rem;
}

/* ── INPUT BOX ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 50px !important;
    padding: 15px 24px !important;
    color: #f1f5f9 !important;
    font-size: 0.93rem !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: #a78bfa !important;
}
.stTextInput > div > div > input::placeholder {
    color: #334155 !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
    outline: none !important;
    background: rgba(255,255,255,0.07) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #94a3b8 !important;
    border-radius: 50px !important;
    padding: 9px 22px !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 30px rgba(124,58,237,0.55) !important;
}

/* ── QUICK QUESTION CARDS ── */
.qq-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}
.qq-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
}
.qq-card:hover {
    background: rgba(124,58,237,0.1);
    border-color: rgba(139,92,246,0.3);
}
.qq-icon { font-size: 1rem; margin-bottom: 6px; }
.qq-title { font-size: 0.82rem; font-weight: 600; color: #cbd5e1; margin-bottom: 2px; }
.qq-sub { font-size: 0.7rem; color: #475569; }

/* ── CHAT BUBBLES ── */
.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    padding: 13px 18px;
    border-radius: 20px 20px 4px 20px;
    margin: 10px 0;
    margin-left: auto;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.55;
    text-align: right;
    box-shadow: 0 4px 20px rgba(124,58,237,0.2);
}
.ai-bubble {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e2e8f0;
    padding: 13px 18px;
    border-radius: 20px 20px 20px 4px;
    margin: 10px 0;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.55;
}
.ai-name {
    font-size: 0.68rem;
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 6px;
    display: flex; align-items: center; gap: 5px;
}
.msg-time { font-size: 0.6rem; color: #334155; margin-top: 6px; }

/* ── LABELS ── */
.section-label {
    font-size: 0.63rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #334155;
    margin: 1.6rem 0 0.8rem 0;
}
.divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 1.2rem 0;
}

/* ── MODE INDICATOR ── */
.mode-indicator {
    font-size: 0.72rem;
    color: #475569;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    font-size: 0.6rem;
    color: #1e293b;
    padding: 2rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #7c3aed !important; }
</style>
""", unsafe_allow_html=True)

# ── CONFIG ──
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None
if "output_mode" not in st.session_state:
    st.session_state.output_mode = "text"

# ── HEADER ──
st.markdown("""
<div class="mesta-header">
    <div class="header-left">
        <div class="header-logo">✦</div>
        <div>
            <div class="header-title">Mesta AI &nbsp;<span style="font-size:0.7rem;color:#7c3aed;">✔</span></div>
            <div class="header-sub">Intelligent Assistant</div>
        </div>
    </div>
    <div class="header-right">
        <span style="display:flex;align-items:center;gap:6px;">
            <span class="online-dot"></span>
            <span style="font-size:0.68rem;color:#475569;">Online</span>
        </span>
        <span class="model-badge">Model: Mistral Small</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-greeting">Hello, Nirbhay! 👋</div>
    <div class="hero-sub">How can I help you today?</div>
    <svg width="100%" height="55" viewBox="0 0 800 55" xmlns="http://www.w3.org/2000/svg" style="opacity:0.3;margin-bottom:0.5rem;">
        <path d="M0,28 C80,5 160,50 240,28 C320,5 400,50 480,28 C560,5 640,50 720,28 C760,17 780,22 800,28" 
              fill="none" stroke="#7c3aed" stroke-width="2"/>
        <path d="M0,28 C100,10 200,46 300,28 C400,10 500,46 600,28 C700,10 760,38 800,28" 
              fill="none" stroke="#4f46e5" stroke-width="1.5" stroke-dasharray="4,4"/>
        <path d="M0,28 C60,18 120,38 200,28 C280,18 380,42 460,28 C540,14 660,40 800,28" 
              fill="none" stroke="#a78bfa" stroke-width="1"/>
    </svg>
</div>
""", unsafe_allow_html=True)

# ── TTS FUNCTION ──
def speak_text(text):
    safe = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')
    return f"""
    <script>
    (function() {{
        try {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{safe}');
            msg.lang = 'en-US'; msg.rate = 1.0; msg.pitch = 1.05; msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var preferred = voices.find(v => v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Daniel'));
            if (preferred) msg.voice = preferred;
            window.speechSynthesis.speak(msg);
        }} catch(e) {{ console.log('TTS:', e); }}
    }})();
    </script>
    """

# ── API ──
def ask_mistral(question):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are Mesta AI, a sleek and intelligent personal assistant created by Nirbhay. Answer clearly and concisely in 2-3 sentences."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 200
    }
    try:
        r = requests.post(MISTRAL_URL, json=data, headers=headers, timeout=15)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Connection issue: {str(e)}"

# ── PLAY PENDING AUDIO ──
if st.session_state.pending_audio:
    st.components.v1.html(st.session_state.pending_audio, height=0)
    st.session_state.pending_audio = None

# ── MODE TOGGLE ──
st.markdown('<div class="section-label">⚙ Response Mode</div>', unsafe_allow_html=True)
col_t, col_v, col_sp = st.columns([1, 1, 4])
with col_t:
    if st.button(
        "📝  Text" if st.session_state.output_mode != "text" else "✅  Text",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "text" else "secondary"
    ):
        st.session_state.output_mode = "text"
        st.rerun()
with col_v:
    if st.button(
        "🔊  Voice" if st.session_state.output_mode != "voice" else "✅  Voice",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "voice" else "secondary"
    ):
        st.session_state.output_mode = "voice"
        st.rerun()

if st.session_state.output_mode == "text":
    st.markdown('<div class="mode-indicator">📝 &nbsp;Text replies only</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="mode-indicator">🔊 &nbsp;Voice + Text replies active</div>', unsafe_allow_html=True)

# ── QUICK QUESTIONS (HTML cards for design, st.buttons hidden for logic) ──
st.markdown('<div class="section-label">⚡ Quick Questions</div>', unsafe_allow_html=True)

quick_qs = [
    ("🖥", "Explain Quantum Computing", "In simple terms"),
    ("💡", "Ideas for a startup", "Need creative ideas"),
    ("📝", "Improve my resume", "Make it more professional"),
    ("🐍", "Write Python code", "For data analysis"),
    ("🤖", "Latest AI trends", "What's new in AI?"),
    ("😄", "Tell me a joke", "Make me smile"),
]

cols = st.columns(3)
for i, (icon, title, sub) in enumerate(quick_qs):
    with cols[i % 3]:
        if st.button(f"{icon} {title}\n{sub}", use_container_width=True, key=f"qq_{i}"):
            with st.spinner("✦ Thinking..."):
                answer = ask_mistral(title)
                st.session_state.chat_history.append({
                    "q": title, "a": answer,
                    "t": datetime.now().strftime("%I:%M %p"),
                    "mode": st.session_state.output_mode
                })
                if st.session_state.output_mode == "voice":
                    st.session_state.pending_audio = speak_text(answer)
                st.rerun()

# ── INPUT ──
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

user_question = st.text_input(
    "", placeholder="Ask Mesta anything...",
    key="text_input", label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1.3, 1.3, 3])
with col1:
    ask_clicked = st.button("✦ Ask Mesta", use_container_width=True, type="primary")
with col2:
    clear_clicked = st.button("🗑 Clear Chat", use_container_width=True)

# ── PROCESS ──
if ask_clicked and user_question:
    with st.spinner("✦ Thinking..."):
        answer = ask_mistral(user_question)
        st.session_state.chat_history.append({
            "q": user_question, "a": answer,
            "t": datetime.now().strftime("%I:%M %p"),
            "mode": st.session_state.output_mode
        })
        if st.session_state.output_mode == "voice":
            st.session_state.pending_audio = speak_text(answer)
        st.rerun()

if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.pending_audio = None
    st.rerun()

# ── CONVERSATION ──
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 Conversation</div>', unsafe_allow_html=True)
    for chat in reversed(st.session_state.chat_history[-15:]):
        voice_tag = " 🔊" if chat.get("mode") == "voice" else ""
        st.markdown(
            f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'''<div class="ai-bubble">
                <div class="ai-name">✦ Mesta{voice_tag}</div>
                {chat["a"]}
                <div class="msg-time">{chat["t"]}</div>
            </div>''',
            unsafe_allow_html=True
        )

# ── FOOTER ──
st.markdown(
    '<div class="footer">✦ Mesta AI &nbsp;·&nbsp; Created by Nirbhay &nbsp;·&nbsp; Powered by Mistral AI</div>',
    unsafe_allow_html=True
)