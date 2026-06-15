import streamlit as st
import requests
import base64
import os
import tempfile
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✨", layout="wide")

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
MISTRAL_URL     = "https://api.mistral.ai/v1/chat/completions"

for k, v in [("history", []), ("mode", "text"), ("audio_html", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #050507 !important;
    color: #fafafa;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 5rem !important; max-width: 880px !important; }

/* ── ANIMATED BACKGROUND GRADIENT ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(168,85,247,0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(59,130,246,0.02) 0%, transparent 60%);
    animation: bgDrift 20s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes bgDrift {
    0%   { transform: translate(0,0) rotate(0deg); }
    100% { transform: translate(2%,2%) rotate(1deg); }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #080809 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: #71717a !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #71717a !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    box-shadow: none !important;
    transition: all .25s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: rgba(255,255,255,0.15) !important;
    color: #e4e4e7 !important;
    background: rgba(255,255,255,0.03) !important;
}
.sidebar-stat {
    font-size: 0.78rem;
    color: #3f3f46;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.02em;
}
.sidebar-stat span {
    color: #818cf8;
}

/* ── HEADER ── */
.mesta-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 2.2rem;
    position: relative;
}
.header-left { display: flex; align-items: center; gap: 16px; }
.header-logo {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #18181b 0%, #1c1c22 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 24px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: logoPulse 4s ease-in-out infinite;
}
@keyframes logoPulse {
    0%,100% { box-shadow: 0 4px 24px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.05); }
    50%      { box-shadow: 0 4px 32px rgba(99,102,241,0.2), inset 0 1px 0 rgba(255,255,255,0.08); }
}
.header-title {
    font-size: 1.3rem; font-weight: 700; color: #fafafa;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fafafa 0%, #a1a1aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.header-sub { font-size: 0.78rem; color: #52525b; margin-top: 3px; letter-spacing: 0.01em; }
.header-badge {
    font-size: 0.7rem; font-weight: 600; color: #818cf8;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    padding: 5px 14px; border-radius: 20px;
    letter-spacing: 0.04em;
    font-family: 'JetBrains Mono', monospace;
}

/* ── TOGGLE — Fixed: uses Streamlit radio styling ── */
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 2px !important;
    width: fit-content !important;
    margin: 0 auto 2rem !important;
}
div[data-testid="stRadio"] label {
    padding: 9px 32px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    color: #71717a !important;
    transition: all .2s ease !important;
    border: none !important;
    background: transparent !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: #fafafa !important;
    color: #09090b !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}
div[data-testid="stRadio"] label:hover:not(:has(input:checked)) {
    color: #d4d4d8 !important;
    background: rgba(255,255,255,0.04) !important;
}
div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
div[data-testid="stRadio"] > label { display: none !important; }

/* ── STATUS ── */
.status-pill {
    text-align: center;
    margin-bottom: 1.8rem;
}
.status-pill span {
    font-size: 0.8rem; font-weight: 500;
    padding: 7px 18px; border-radius: 20px;
    display: inline-flex; align-items: center; gap: 7px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.02em;
    transition: all .3s ease;
}
.s-ready    { background:rgba(255,255,255,0.03); color:#52525b; border:1px solid rgba(255,255,255,0.06); }
.s-listening{ background:rgba(239,68,68,0.07);  color:#f87171; border:1px solid rgba(239,68,68,0.2); animation: statusGlow 1s ease-in-out infinite; }
.s-thinking { background:rgba(99,102,241,0.07); color:#818cf8; border:1px solid rgba(99,102,241,0.2); animation: statusGlow 1s ease-in-out infinite; }
.s-speaking { background:rgba(52,211,153,0.07); color:#34d399; border:1px solid rgba(52,211,153,0.2); }
.s-error    { background:rgba(239,68,68,0.07);  color:#f87171; border:1px solid rgba(239,68,68,0.2); }
@keyframes statusGlow {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.7; }
}

/* ── MIC BUTTON ── */
.mic-area { text-align: center; margin: 2.5rem 0; }
#micBtn {
    width: 84px; height: 84px; border-radius: 50%;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    cursor: pointer;
    font-size: 2rem;
    color: white;
    transition: all .3s ease;
    display: inline-flex; align-items: center; justify-content: center;
    position: relative;
}
#micBtn::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(168,85,247,0.3));
    opacity: 0;
    transition: opacity .3s ease;
    z-index: -1;
}
#micBtn:hover::before { opacity: 1; }
#micBtn:hover { border-color: rgba(99,102,241,0.4); transform: scale(1.05); }
#micBtn.active {
    background: rgba(239,68,68,0.08);
    border-color: rgba(239,68,68,0.4);
    animation: micPulse 1.4s infinite;
}
@keyframes micPulse {
    0%,100% { box-shadow: 0 0 0 0px rgba(239,68,68,0.2); }
    50%      { box-shadow: 0 0 0 16px rgba(239,68,68,0.04); }
}
.mic-hint { font-size: 0.78rem; color: #3f3f46; margin-top: 12px; letter-spacing: 0.04em; font-family: 'JetBrains Mono', monospace; }

/* ── TEXT INPUT ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    color: #fafafa !important;
    padding: 14px 20px !important;
    font-size: 0.92rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.4) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #3f3f46 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #a1a1aa !important;
    border-radius: 12px !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    padding: 11px 22px !important;
    box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
    transition: all .2s ease !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: #fafafa !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.1) 100%) !important;
    border-color: rgba(99,102,241,0.3) !important;
    color: #818cf8 !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.25) 0%, rgba(168,85,247,0.18) 100%) !important;
    border-color: rgba(99,102,241,0.5) !important;
    color: #a5b4fc !important;
}

/* ── CHAT BUBBLES ── */
.bubble-wrap { animation: fadeSlideIn .35s ease forwards; opacity: 0; }
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.bubble-user {
    margin: 1.2rem 0 0.4rem auto;
    max-width: 70%;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px 18px 4px 18px;
    padding: 13px 17px;
    font-size: 0.9rem;
    color: #e4e4e7;
    line-height: 1.6;
    text-align: right;
}
.bubble-ai {
    margin: 0.4rem 0 1.2rem;
    max-width: 70%;
    background: linear-gradient(135deg, rgba(99,102,241,0.05) 0%, rgba(168,85,247,0.03) 100%);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 18px 18px 18px 4px;
    padding: 13px 17px;
    font-size: 0.9rem;
    color: #d4d4d8;
    line-height: 1.65;
}
.blabel {
    font-size: 0.67rem; font-weight: 600;
    color: #3f3f46; margin-bottom: 6px;
    text-transform: uppercase; letter-spacing: 0.09em;
    font-family: 'JetBrains Mono', monospace;
}
.blabel-ai { color: rgba(99,102,241,0.5); }
.btime { font-size: 0.64rem; color: #27272a; margin-top: 7px; font-family: 'JetBrains Mono', monospace; }

/* ── QUICK Qs ── */
.section-label {
    font-size: 0.68rem; font-weight: 600; color: #3f3f46;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin-bottom: 12px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    margin: 1.8rem 0;
}

/* ── FOOTER ── */
.mesta-footer {
    text-align: center; margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    font-size: 0.68rem; color: #27272a;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
}

/* ── THINKING DOTS ── */
.thinking-dot {
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #818cf8;
    animation: dotBounce 1.2s ease-in-out infinite;
    margin: 0 2px;
}
.thinking-dot:nth-child(2) { animation-delay: 0.15s; }
.thinking-dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes dotBounce {
    0%,80%,100% { transform: translateY(0); opacity: 0.4; }
    40%          { transform: translateY(-5px); opacity: 1; }
}

/* ── HIDE RADIO BUTTON CIRCLE ── */
div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { display: none !important; }
div[data-testid="stRadio"] [data-baseweb="radio"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# JAVASCRIPT
# ─────────────────────────────────────────────────────────────
st.markdown("""
<script>
var _rec  = null;
var _busy = false;

function setStatus(msg, cls) {
    var el = document.getElementById("statusInner");
    if (el) { el.textContent = msg; el.className = cls; }
}

function toggleMic() {
    if (_busy) { setStatus("⏳  Wait — AI is responding", "s-thinking"); return; }
    if (_rec)  { try { _rec.stop(); } catch(e){} _rec = null; resetMic(); return; }

    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { setStatus("❌  Use Chrome or Edge for mic", "s-error"); return; }

    if (window.speechSynthesis) window.speechSynthesis.cancel();

    _rec = new SR();
    _rec.lang = "en-US";
    _rec.continuous = false;
    _rec.interimResults = false;

    _rec.onstart = function() {
        var b = document.getElementById("micBtn");
        if (b) { b.classList.add("active"); b.innerHTML = "🔴"; }
        document.getElementById("micHint").textContent = "Listening…";
        setStatus("🎤  Listening… speak now", "s-listening");
    };

    _rec.onresult = function(e) {
        var txt = e.results[0][0].transcript;
        setStatus('📝  Processing…', "s-thinking");
        resetMic(); _rec = null; _busy = true;
        pushToStreamlit(txt);
    };

    _rec.onerror = function(e) {
        var m = "❌  Mic error — try again";
        if (e.error === "not-allowed") m = "❌  Allow mic in address bar";
        if (e.error === "no-speech")   m = "⏱  No speech detected";
        setStatus(m, "s-error");
        resetMic(); _rec = null;
    };

    _rec.onend = function() {
        resetMic(); _rec = null;
        if (!_busy) setStatus("●  Ready", "s-ready");
    };

    _rec.start();
}

function resetMic() {
    var b = document.getElementById("micBtn");
    var h = document.getElementById("micHint");
    if (b) { b.classList.remove("active"); b.innerHTML = "🎤"; }
    if (h) h.textContent = "Tap to speak";
}

function pushToStreamlit(text) {
    var inputs = window.parent.document.querySelectorAll('input[type="text"]');
    var target = null;
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].getAttribute("aria-label") === "__VOICE_BRIDGE__") {
            target = inputs[i]; break;
        }
    }
    if (!target && inputs.length) target = inputs[0];
    if (target) {
        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
        setter.set.call(target, text);
        target.dispatchEvent(new Event("input",  { bubbles: true }));
        target.dispatchEvent(new Event("change", { bubbles: true }));
    }
    setTimeout(function() {
        var btns = window.parent.document.querySelectorAll("button");
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].innerText.trim() === "__VOICE_SUBMIT__") {
                btns[i].click(); break;
            }
        }
    }, 350);
}

function browserSpeak(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US"; u.rate = 0.93; u.pitch = 1; u.volume = 1;
    var voices = window.speechSynthesis.getVoices();
    var v = voices.find(x => x.lang === "en-US" && x.name.includes("Google"))
          || voices.find(x => x.lang.startsWith("en"));
    if (v) u.voice = v;
    u.onstart = () => setStatus("🔊  Speaking…", "s-speaking");
    u.onend   = () => { setStatus("●  Ready", "s-ready"); _busy = false; };
    u.onerror = () => { setStatus("●  Ready", "s-ready"); _busy = false; };
    window.speechSynthesis.speak(u);
}

if (window.speechSynthesis) {
    window.speechSynthesis.getVoices();
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
}
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def ask_mesta(q: str) -> str:
    try:
        r = requests.post(
            MISTRAL_URL,
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}",
                     "Content-Type": "application/json"},
            json={
                "model": "mistral-small-latest",
                "messages": [
                    {"role": "system", "content":
                     "You are Mesta AI, a premium intelligent assistant. "
                     "Answer clearly and concisely in 2-3 sentences. Be warm and precise."},
                    {"role": "user", "content": q},
                ],
                "max_tokens": 250,
            },
            timeout=15,
        )
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Connection issue — please try again."

def process(question: str):
    answer = ask_mesta(question)
    st.session_state.history.append({
        "q": question, "a": answer,
        "t": datetime.now().strftime("%I:%M %p"),
    })
    safe = answer.replace("\\","\\\\").replace("'","\\'").replace("\n"," ")
    st.session_state.audio_html = f"<script>setTimeout(()=>browserSpeak('{safe}'),500);</script>"
    st.rerun()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✨ Mesta AI")
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:14px 0'></div>",
                unsafe_allow_html=True)
    st.markdown(
        f"<div class='sidebar-stat'>conversations &nbsp;<span>{len(st.session_state.history)}</span></div>",
        unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:14px 0'></div>",
                unsafe_allow_html=True)
    st.markdown("""
<div style='font-size:.78rem;color:#3f3f46;line-height:1.9;margin-top:8px'>
⌨️ &nbsp;<span style='color:#52525b'>Text</span> — Type &amp; ask<br>
🎤 &nbsp;<span style='color:#52525b'>Voice</span> — Speak naturally<br>
🔊 &nbsp;<span style='color:#52525b'>AI</span> replies with voice
</div>
""", unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:14px 0'></div>",
                unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()
    st.markdown("<div style='margin-top:auto;padding-top:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:.68rem;color:#27272a;font-family:monospace'>Mesta Core · v1.0</span>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────
# MODE TOGGLE
# ─────────────────────────────────────────────────────────────
mode_options = ["⌨️  Text", "🎤  Voice"]
selected = st.radio(
    "mode",
    mode_options,
    index=0 if st.session_state.mode == "text" else 1,
    horizontal=True,
    label_visibility="collapsed",
)
st.session_state.mode = "text" if selected == mode_options[0] else "voice"

# ─────────────────────────────────────────────────────────────
# STATUS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-pill">
  <span id="statusInner" class="s-ready">●  Ready</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# AUTOPLAY AUDIO
# ─────────────────────────────────────────────────────────────
if st.session_state.audio_html:
    st.markdown(st.session_state.audio_html, unsafe_allow_html=True)
    st.session_state.audio_html = ""

# ─────────────────────────────────────────────────────────────
# ── TEXT MODE ──
# ─────────────────────────────────────────────────────────────
if st.session_state.mode == "text":
    typed = st.text_input("", placeholder="Ask Mesta anything…",
                          key="typed", label_visibility="collapsed")
    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("Ask Mesta →", use_container_width=True, type="primary", key="ask_text"):
            if typed.strip():
                with st.spinner(""):
                    process(typed.strip())
    with c2:
        if st.button("Clear", use_container_width=True, key="clr_text"):
            st.session_state.history = []; st.rerun()

# ─────────────────────────────────────────────────────────────
# ── VOICE MODE ──
# ─────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="mic-area">
      <button id="micBtn" onclick="toggleMic()">🎤</button>
      <div class="mic-hint" id="micHint">Tap to speak</div>
    </div>
    """, unsafe_allow_html=True)

    bridge = st.text_input("__VOICE_BRIDGE__", key="vb",
                           label_visibility="collapsed")
    if st.button("__VOICE_SUBMIT__", key="vs"):
        if bridge and bridge.strip():
            with st.spinner(""):
                process(bridge.strip())

    c1, c2 = st.columns([3, 1])
    with c2:
        if st.button("Clear", use_container_width=True, key="clr_voice"):
            st.session_state.history = []; st.rerun()

# ─────────────────────────────────────────────────────────────
# QUICK QUESTIONS
# ─────────────────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>Quick questions</div>", unsafe_allow_html=True)

QUICK = ["Who are you?", "What can you do?",
         "Tell me something inspiring", "Future of AI",
         "What is machine learning?", "Tell me a joke"]

cols = st.columns(3)
for i, q in enumerate(QUICK):
    with cols[i % 3]:
        if st.button(q, key=f"qq{i}", use_container_width=True):
            with st.spinner(""):
                process(q)

# ─────────────────────────────────────────────────────────────
# CONVERSATION HISTORY
# ─────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Conversation</div>", unsafe_allow_html=True)

    for chat in reversed(st.session_state.history[-20:]):
        st.markdown(
            f'<div class="bubble-wrap">'
            f'<div class="bubble-user">'
            f'<div class="blabel">You</div>{chat["q"]}'
            f'</div></div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="bubble-wrap">'
            f'<div class="bubble-ai">'
            f'<div class="blabel blabel-ai">Mesta</div>{chat["a"]}'
            f'<div class="btime">{chat["t"]}</div>'
            f'</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="mesta-footer">
  Mesta AI &nbsp;·&nbsp; Intelligence v1.0
</div>
""", unsafe_allow_html=True)