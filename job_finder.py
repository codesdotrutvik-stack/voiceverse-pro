import streamlit as st
import requests
import json
import os

st.set_page_config(
    page_title="Job Finder AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header h1 { color: white; margin: 0; font-size: 1.8rem; }

    /* Floating Chat Button */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        cursor: pointer;
        z-index: 10000;
        border: none;
        transition: all 0.3s;
    }
    .floating-btn:hover {
        transform: scale(1.1);
    }

    /* Chat Window */
    .chat-window {
        position: fixed;
        bottom: 110px;
        right: 30px;
        width: 380px;
        height: 520px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.25);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    .chat-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px 20px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        background: #f8fafc;
    }

    .chat-input-area {
        padding: 12px;
        background: white;
        border-top: 1px solid #e5e7eb;
    }

    .user-msg {
        background: #667eea;
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        align-self: flex-end;
        margin-left: auto;
    }

    .assistant-msg {
        background: #e2e8f0;
        color: #1e2937;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
    }

    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>💼 Job Finder AI</h1>
    <p>Live jobs from Adzuna API • Save jobs permanently • AI Career Assistant</p>
</div>
""", unsafe_allow_html=True)

# ====================== API KEYS ======================
ADZUNA_APP_ID = "cab85cad"
ADZUNA_API_KEY = "9c920a8f1b37a639553a98541e0ba2e8"
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

CITIES = ["All", "Ahmedabad", "Surat", "Rajkot", "Vadodara", "Bangalore", "Mumbai", "Hyderabad"]
POPULAR_ROLES = ["Python Developer", "Shopify Developer", "Frontend Developer", "WordPress Developer", "Full Stack Developer"]

SAVED_JOBS_FILE = "saved_jobs.json"

# ====================== FUNCTIONS ======================
def load_saved_jobs():
    try:
        if os.path.exists(SAVED_JOBS_FILE):
            with open(SAVED_JOBS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []

def save_saved_jobs(jobs):
    try:
        with open(SAVED_JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def fetch_jobs(role, location):
    # ... (same as before - keeping it short)
    location_name = location if location != "All" else "India"
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": 12,
        "what": role,
        "where": location_name,
        "sort_by": "date"
    }
    try:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            data = r.json()
            jobs = []
            for item in data.get("results", []):
                company = item.get("company", {}).get("display_name", "Unknown")
                jobs.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "company": company,
                    "location": item.get("location", {}).get("display_name", location_name),
                    "salary": "Not disclosed",
                    "description": item.get("description", "")[:350],
                    "url": item.get("redirect_url", "#"),
                    "created": item.get("created", "Recently")
                })
            return jobs
        return []
    except:
        return []

def chat_with_mistral(user_message, history):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    messages = [{"role": "system", "content": "You are a friendly and professional career assistant. Help with job search, resume, interview tips, and career guidance."}]
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    try:
        resp = requests.post(url, json={
            "model": "mistral-small-latest",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }, headers=headers, timeout=25)
        return resp.json()["choices"][0]["message"]["content"]
    except:
        return "Sorry, I couldn't process your request right now. Please try again."

# ====================== SESSION STATE ======================
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = load_saved_jobs()
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "searched" not in st.session_state:
    st.session_state.searched = False
if "search_role" not in st.session_state:
    st.session_state.search_role = "Python Developer"
if "search_city" not in st.session_state:
    st.session_state.search_city = "Surat"
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ====================== SIDEBAR & MAIN APP (Same as before) ======================
with st.sidebar:
    st.markdown("### 🔍 Search Jobs")
    st.session_state.search_role = st.text_input("Job Role", value=st.session_state.search_role)
    st.session_state.search_city = st.selectbox("City", CITIES, index=CITIES.index(st.session_state.search_city) if st.session_state.search_city in CITIES else 0)
    
    if st.button("🔍 Search Jobs", use_container_width=True, type="primary"):
        with st.spinner("Searching..."):
            jobs = fetch_jobs(st.session_state.search_role, st.session_state.search_city)
            st.session_state.jobs = jobs
            st.session_state.searched = True
            st.success(f"Found {len(jobs)} jobs")

    st.markdown("---")
    st.markdown("### Quick Filters")
    for role in POPULAR_ROLES:
        if st.button(role, key=f"q_{role}", use_container_width=True):
            st.session_state.search_role = role
            st.rerun()

    st.success("✅ API Active")

# Load default jobs
if not st.session_state.searched:
    st.session_state.jobs = fetch_jobs("Python Developer", "Surat")
    st.session_state.searched = True

# Main Content
if st.session_state.jobs:
    st.markdown(f"**{len(st.session_state.jobs)} jobs found for {st.session_state.search_role} in {st.session_state.search_city}**")
    for idx, job in enumerate(st.session_state.jobs):
        with st.expander(f"💼 {job['title']} - {job['company']}"):
            st.write(job['description'])
            cols = st.columns([1,1,1])
            with cols[0]:
                st.markdown(f"[Apply Now]({job['url']})")
            with cols[1]:
                if st.button("⭐ Save", key=f"save{idx}"):
                    if job not in st.session_state.saved_jobs:
                        st.session_state.saved_jobs.append(job)
                        save_saved_jobs(st.session_state.saved_jobs)
                        st.success("Saved!")

# ====================== FLOATING CHATBOT ======================
# Floating Button
if st.button("💬", key="open_chat", help="Chat with AI Career Assistant"):
    st.session_state.chat_open = True
    st.rerun()

# Chat Window
if st.session_state.chat_open:
    with st.container():
        st.markdown('<div class="chat-window">', unsafe_allow_html=True)
        
        # Header
        st.markdown("""
            <div class="chat-header">
                <span>💼 AI Career Assistant</span>
                <span style="cursor:pointer; font-size:20px;" onclick="window.parent.postMessage({type: 'close_chat'}, '*')">✕</span>
            </div>
        """, unsafe_allow_html=True)

        # Messages
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)

        # Input Area
        with st.container():
            user_input = st.text_input("Type your message...", key="chat_input_key", label_visibility="collapsed")
            col1, col2 = st.columns([4,1])
            with col1:
                if st.button("Send", use_container_width=True, key="send_btn"):
                    if user_input.strip():
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        with st.spinner("Thinking..."):
                            reply = chat_with_mistral(user_input, st.session_state.chat_history)
                            st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
            with col2:
                if st.button("Close", use_container_width=True):
                    st.session_state.chat_open = False
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.caption("💼 Job Finder AI | Powered by Adzuna + Mistral AI")