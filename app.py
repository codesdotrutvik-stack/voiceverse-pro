import streamlit as st
import requests

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Page config
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

# Custom CSS for better design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton button:hover {
        opacity: 0.9;
    }
    .user-msg {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
    }
    .ai-msg {
        background-color: #f0e6ff;
        padding: 10px;
        border-radius: 15px;
        margin: 5px 0;
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
    st.markdown("## ⚙️ Settings")
    mode = st.selectbox("Select Mode", ["Simple (Like I'm 5)", "Normal", "Detailed"])
    st.markdown("---")
    st.markdown("### 📚 Quick Topics")
    
    topics = ["🐍 Python", "🤖 AI", "🧮 Maths", "🔬 Science", "🌍 History", "💻 Coding"]
    for topic in topics:
        if st.button(topic, use_container_width=True):
            st.session_state.chat.append({"q": topic, "a": "🤔 Loading..."})
            st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask your question")
    user_input = st.text_area("", height=100, placeholder="Example: What is Python? Explain loops...")
    
    if st.button("🚀 Ask AI", use_container_width=True):
        if user_input:
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
<div style="text-align: center; color: gray; margin-top: 2rem;">
    Made with ❤️ using Mistral AI | AI Study Buddy Pro
</div>
""", unsafe_allow_html=True)