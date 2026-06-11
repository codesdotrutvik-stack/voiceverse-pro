import streamlit as st
import requests
import pyttsx3
import threading

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

def speak_text(text):
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=_speak)
    thread.start()

# Custom CSS - Solid Colors (No Gradient)
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background-color: #1e3a8a;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #bfdbfe;
        margin: 0;
        font-size: 1.1rem;
    }
    .stButton button {
        background-color: #1e3a8a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #2563eb;
    }
    .user-msg {
        background-color: #dbeafe;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #1e3a8a;
    }
    .ai-msg {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #10b981;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .sidebar-box {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 AI Study Buddy</h1>
    <p>Your Personal AI Teacher – Learn Anything, Anytime!</p>
</div>
""", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mode = st.selectbox("Select Mode", ["Simple (Like I'm 5)", "Normal", "Detailed"])
    
    st.markdown("---")
    voice = st.checkbox("🔊 Voice Output")
    
    st.markdown("---")
    st.markdown("### 📚 Quick Topics")
    
    topics = ["🐍 Python", "🤖 AI", "🧮 Maths", "🔬 Science", "🌍 History", "💻 Coding", "🛒 Shopify", "🎨 CSS"]
    cols = st.columns(2)
    for i, topic in enumerate(topics):
        with cols[i % 2]:
            if st.button(topic, use_container_width=True):
                st.session_state.chat.append({"q": topic, "a": "🤔 Loading..."})
                st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# Main area
st.markdown("### 💬 Ask your question")
user_input = st.text_area("", height=100, placeholder="Example: What is Python? Explain loops...")

col1, col2 = st.columns([1, 4])
with col1:
    ask_clicked = st.button("🚀 Ask AI", use_container_width=True)

if ask_clicked and user_input:
    with st.spinner("🧠 AI is thinking..."):
        if mode == "Simple (Like I'm 5)":
            prompt = "Explain like the student is 5 years old. Very simple words. Short sentences."
        elif mode == "Detailed":
            prompt = "Explain in detail with examples."
        else:
            prompt = "Explain clearly and simply."
        
        data = {
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        answer = response.json()["choices"][0]["message"]["content"]
        st.session_state.chat.append({"q": user_input, "a": answer})
        if voice:
            speak_text(answer)
        st.rerun()

# Chat history
st.markdown("---")
st.markdown("### 💬 Conversation")

for item in reversed(st.session_state.chat):
    st.markdown(f'<div class="user-msg"><strong>🧑‍🎓 You:</strong><br>{item["q"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-msg"><strong>🤖 AI Teacher:</strong><br>{item["a"]}</div>', unsafe_allow_html=True)
    st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem;">
    Made with ❤️ using Mistral AI | AI Study Buddy
</div>
""", unsafe_allow_html=True)