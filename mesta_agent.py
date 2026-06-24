# mesta_agent.py
import streamlit as st
import pyttsx3
import threading
from datetime import datetime
from agent_tools import detect_tool

st.set_page_config(page_title="Mesta Agent", page_icon="🤖", layout="wide")

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
.stApp { background: #0a0a12; }
.block-container { padding: 2rem; }

.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    padding: 10px 16px;
    border-radius: 18px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 75%;
    text-align: right;
}

.ai-bubble {
    background: #12121e;
    border: 1px solid rgba(255,255,255,0.06);
    color: #e2e8f0;
    padding: 10px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 75%;
}

.ai-name {
    color: #a78bfa;
    font-weight: 600;
    font-size: 0.75rem;
    margin-bottom: 4px;
}

.msg-time {
    color: #475569;
    font-size: 0.6rem;
    margin-top: 4px;
}

.stTextInput > div > div > input {
    background: #12121e !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 50px !important;
    padding: 12px 20px !important;
    color: white !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
}

.divider { height: 1px; background: rgba(255,255,255,0.05); margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION
# ============================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============================================================
# VOICE
# ============================================================
def speak_text(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 1)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except:
            pass
    thread = threading.Thread(target=_speak)
    thread.start()

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
    <div>
        <h1 style="color: #a78bfa;">🤖 Mesta Agent</h1>
        <p style="color: #475569;">AI with Tools — Calculator · Time · Weather · Search</p>
    </div>
    <div style="background: #12121e; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(139,92,246,0.2);">
        <span style="color: #22c55e; font-size: 0.7rem;">● Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TOOLS
# ============================================================
st.markdown("""
<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem;">
    <span style="background: #12121e; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; color: #9ca3af;">🧮 Calculator</span>
    <span style="background: #12121e; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; color: #9ca3af;">⏰ Country Time</span>
    <span style="background: #12121e; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; color: #9ca3af;">🌤️ Weather</span>
    <span style="background: #12121e; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; color: #9ca3af;">🔍 Search</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# QUICK EXAMPLES
# ============================================================
quick_examples = [
    "Calculate 25 * 4",
    "What time in India?",
    "Weather in Ahmedabad",
    "Search for AI"
]

cols = st.columns(4)
for i, example in enumerate(quick_examples):
    with cols[i]:
        if st.button(example, use_container_width=True):
            with st.spinner("Processing..."):
                answer = detect_tool(example)
                if answer is None:
                    answer = "🤖 I'm a specialized agent. Try: calculator, time, weather, or search."
                st.session_state.chat_history.append({
                    "q": example,
                    "a": answer,
                    "t": datetime.now().strftime("%I:%M %p")
                })
                speak_text(answer)
                st.rerun()

# ============================================================
# INPUT
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="Ask Mesta Agent anything...", key="user_input", label_visibility="collapsed")

col1, col2 = st.columns([1, 4])
with col1:
    ask_clicked = st.button("🔊 Ask", type="primary", use_container_width=True)
with col2:
    clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)

if ask_clicked and user_input:
    with st.spinner("Processing..."):
        answer = detect_tool(user_input)
        if answer is None:
            answer = "🤖 I'm a specialized agent. Try: calculator, time, weather, or search."
        st.session_state.chat_history.append({
            "q": user_input,
            "a": answer,
            "t": datetime.now().strftime("%I:%M %p")
        })
        speak_text(answer)
        st.rerun()

if clear_clicked:
    st.session_state.chat_history = []
    st.rerun()

# ============================================================
# CHAT HISTORY
# ============================================================
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #475569; font-size: 0.7rem; margin-bottom: 0.5rem;">💬 CONVERSATION</div>', unsafe_allow_html=True)
    
    for chat in reversed(st.session_state.chat_history[-15:]):
        st.markdown(f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-bubble"><div class="ai-name">🤖 Mesta Agent</div>{chat["a"]}<div class="msg-time">{chat["t"]}</div></div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #1e293b; font-size: 0.6rem;">🤖 Mesta Agent · Created by Nirbhay</div>', unsafe_allow_html=True)