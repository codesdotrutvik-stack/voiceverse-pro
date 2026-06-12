import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Job Finder AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .header p { color: rgba(255,255,255,0.85); margin: 0.3rem 0 0; font-size: 0.85rem; }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        width: 100%;
    }
    
    .api-success {
        background: #d1fae5;
        color: #065f46;
        padding: 0.6rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 500;
    }
    
    .stat-box {
        text-align: center;
        padding: 0.8rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }
    .stat-number { font-size: 1.3rem; font-weight: 700; color: #667eea; }
    .stat-label { font-size: 0.7rem; color: #64748b; }
    
    .point-item {
        padding: 0.25rem 0;
        margin: 0.15rem 0;
        border-left: 3px solid #667eea;
        padding-left: 0.7rem;
        font-size: 0.85rem;
    }
    
    .saved-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    /* WhatsApp Style Floating Chat Button */
    .floating-chat-btn {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
        z-index: 999;
        transition: all 0.3s;
        border: none;
    }
    .floating-chat-btn:hover {
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .floating-chat-btn img {
        width: 32px;
        height: 32px;
    }
    
    /* Chat Popup Window */
    .chat-popup {
        position: fixed;
        bottom: 100px;
        right: 25px;
        width: 380px;
        height: 500px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        z-index: 998;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        animation: slideUp 0.3s ease;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-popup-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .chat-popup-header h4 {
        margin: 0;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .close-chat {
        cursor: pointer;
        background: rgba(255,255,255,0.2);
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        transition: all 0.2s;
    }
    .close-chat:hover {
        background: rgba(255,255,255,0.3);
    }
    
    .chat-popup-messages {
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .message-bot {
        display: flex;
        gap: 8px;
        max-width: 85%;
    }
    .bot-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #00d4ff, #7b5ea7);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    .bot-text {
        background: white;
        padding: 10px 14px;
        border-radius: 18px;
        border-top-left-radius: 4px;
        font-size: 13px;
        color: #1e293b;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .message-user {
        display: flex;
        justify-content: flex-end;
        max-width: 85%;
        align-self: flex-end;
    }
    .user-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 14px;
        border-radius: 18px;
        border-top-right-radius: 4px;
        font-size: 13px;
        line-height: 1.4;
    }
    
    .message-time {
        font-size: 9px;
        color: #94a3b8;
        margin-top: 4px;
        text-align: right;
    }
    
    .chat-popup-input {
        padding: 12px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 8px;
    }
    .chat-popup-input input {
        flex: 1;
        padding: 10px 14px;
        border: 1px solid #e2e8f0;
        border-radius: 25px;
        outline: none;
        font-size: 13px;
    }
    .chat-popup-input input:focus {
        border-color: #667eea;
    }
    .chat-popup-input button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0 18px;
        cursor: pointer;
        font-weight: 500;
    }
    
    .typing {
        background: white;
        padding: 10px 14px;
        border-radius: 18px;
        border-top-left-radius: 4px;
        width: 50px;
        border: 1px solid #e2e8f0;
    }
    .typing span {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        margin: 0 2px;
        animation: typing 1.4s infinite;
    }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-6px); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>💼 Job Finder AI</h1>
    <p>Live jobs from Adzuna API • Save jobs permanently • Get company insights</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# API CONFIGURATION
# ============================================================
ADZUNA_APP_ID = "cab85cad"
ADZUNA_API_KEY = "9c920a8f1b37a639553a98541e0ba2e8"
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

CITIES = ["All", "Ahmedabad", "Surat", "Rajkot", "Vadodara", "Bangalore", "Mumbai", "Hyderabad"]

POPULAR_ROLES = [
    "Python Developer", "Shopify Developer", "Frontend Developer", 
    "WordPress Developer", "Full Stack Developer", "Data Scientist",
    "React Developer", "Java Developer", "DevOps Engineer"
]

DEFAULT_ROLE = "Python Developer"
DEFAULT_CITY = "Surat"

# ============================================================
# PERMANENT STORAGE
# ============================================================
SAVED_JOBS_FILE = "saved_jobs.json"

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
        response = requests.get(url, params=params, timeout=25)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for result in data.get("results", []):
                salary_min = result.get("salary_min", 0)
                salary_max = result.get("salary_max", 0)
                if salary_min and salary_max and salary_min > 0:
                    salary = f"₹{int(salary_min/100000)}-{int(salary_max/100000)} LPA"
                elif salary_min and salary_min > 0:
                    salary = f"₹{int(salary_min/100000)} LPA"
                else:
                    salary = "Not disclosed"
                
                company = result.get("company", {})
                company_name = company.get("display_name", "Private Limited") if isinstance(company, dict) else "Private Limited"
                
                jobs.append({
                    "id": result.get("id"),
                    "title": result.get("title", "N/A"),
                    "company": company_name,
                    "location": result.get("location", {}).get("display_name", location_name) if isinstance(result.get("location"), dict) else location_name,
                    "salary": salary,
                    "description": result.get("description", "")[:400] if result.get("description") else "No description available",
                    "url": result.get("redirect_url", "#"),
                    "created": result.get("created", "Recently")
                })
            return jobs, None
        else:
            return None, f"API Error: {response.status_code}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

def get_company_details(company_name, job_title):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Provide brief information about this company and job.

Company: {company_name}
Job Title: {job_title}

Return in this format:
- Industry:
- Required Experience:
- Key Skills:
- Interview Tips:"""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return f"- Industry: Technology\n- Company: {company_name}\n- Tip: Research the company before interview"

def chat_with_ai(user_message):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are JobBot, a helpful career assistant. Answer briefly.

User: {user_message}

Give friendly, helpful response in 2-3 sentences."""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Thanks for your message! How can I help with your job search?"

# ============================================================
# SESSION STATE
# ============================================================
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = load_saved_jobs()
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "searched" not in st.session_state:
    st.session_state.searched = False
if "company_details" not in st.session_state:
    st.session_state.company_details = {}
if "search_role" not in st.session_state:
    st.session_state.search_role = DEFAULT_ROLE
if "search_city" not in st.session_state:
    st.session_state.search_city = DEFAULT_CITY
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "bot", "content": "Hi! 👋 I'm JobBot. Ask me about jobs, companies, or career advice!", "time": datetime.now().strftime("%I:%M %p")}
    ]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🔍 Search Jobs")
    
    st.session_state.search_role = st.text_input(
        "Job Role", 
        value=st.session_state.search_role,
        placeholder="e.g., Python Developer, Shopify Expert"
    )
    
    st.session_state.search_city = st.selectbox(
        "City", 
        CITIES,
        index=CITIES.index(st.session_state.search_city) if st.session_state.search_city in CITIES else 0
    )
    
    search_clicked = st.button("🔍 Search Jobs", use_container_width=True, type="primary")
    
    st.markdown("---")
    
    st.markdown("### 📌 Quick Filters")
    
    for role in POPULAR_ROLES[:5]:
        if st.button(role, key=f"quick_{role}", use_container_width=True):
            st.session_state.search_role = role
            st.rerun()
    
    st.markdown("---")
    st.success("✅ API Active")
    
    st.markdown("---")
    st.markdown(f"### 📌 Saved Jobs")
    st.markdown(f"**{len(st.session_state.saved_jobs)}** jobs saved")
    
    if st.button("🗑️ Clear All Saved", use_container_width=True):
        st.session_state.saved_jobs = []
        save_saved_jobs([])
        st.rerun()

# ============================================================
# LOAD DEFAULT JOBS
# ============================================================
if not st.session_state.searched and not st.session_state.jobs:
    with st.spinner(f"Loading jobs..."):
        default_jobs, error = fetch_jobs(DEFAULT_ROLE, DEFAULT_CITY)
        if default_jobs:
            st.session_state.jobs = default_jobs
            st.session_state.searched = True

# ============================================================
# SEARCH LOGIC
# ============================================================
if search_clicked:
    with st.spinner(f"Searching..."):
        jobs, error = fetch_jobs(st.session_state.search_role, st.session_state.search_city)
        if jobs:
            st.session_state.jobs = jobs
            st.session_state.searched = True
            st.session_state.company_details = {}
            st.success(f"✅ Found {len(jobs)} jobs")
        else:
            st.session_state.jobs = []
            st.session_state.searched = True
            st.error(error)

# ============================================================
# RESULTS DISPLAY
# ============================================================
if st.session_state.searched:
    if st.session_state.jobs:
        st.markdown(f"""
        <div class="api-success">
            🎯 {len(st.session_state.jobs)} jobs found for '{st.session_state.search_role}' in {st.session_state.search_city}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-box"><div class="stat-number">{len(st.session_state.jobs)}</div><div class="stat-label">Jobs Found</div></div>', unsafe_allow_html=True)
        with col2:
            companies = len(set(j.get("company") for j in st.session_state.jobs))
            st.markdown(f'<div class="stat-box"><div class="stat-number">{companies}</div><div class="stat-label">Companies</div></div>', unsafe_allow_html=True)
        with col3:
            locations = len(set(j.get("location") for j in st.session_state.jobs))
            st.markdown(f'<div class="stat-box"><div class="stat-number">{locations}</div><div class="stat-label">Locations</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        for idx, job in enumerate(st.session_state.jobs):
            is_saved = any(j.get('id') == job.get('id') for j in st.session_state.saved_jobs)
            
            with st.expander(f"💼 {job['title']} - {job['company']} (📍 {job['location']})", expanded=False):
                st.markdown(f"""
                <div class="point-item"><b>Company:</b> {job['company']}</div>
                <div class="point-item"><b>Location:</b> {job['location']}</div>
                <div class="point-item"><b>Salary:</b> {job['salary']}</div>
                <div class="point-item"><b>Posted:</b> {job['created'][:10] if job['created'] != 'Recently' else 'Recently'}</div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📝 Description")
                desc_lines = job['description'][:350].split('.')[:4]
                for line in desc_lines:
                    if line.strip():
                        st.markdown(f'<div class="point-item">• {line.strip()}.</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if not is_saved:
                        if st.button(f"⭐ Save", key=f"save_{idx}"):
                            st.session_state.saved_jobs.append(job)
                            save_saved_jobs(st.session_state.saved_jobs)
                            st.success("Saved!")
                            st.rerun()
                    else:
                        st.markdown('<span class="saved-badge">✓ Saved</span>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"[📋 Apply]({job['url']})", unsafe_allow_html=True)
                
                with col3:
                    if st.button(f"🏢 Company Info", key=f"info_{idx}"):
                        with st.spinner("Fetching..."):
                            details = get_company_details(job['company'], job['title'])
                            st.session_state.company_details[idx] = details
                            st.rerun()
                
                if idx in st.session_state.company_details:
                    st.markdown("---")
                    st.markdown(f"#### 🏢 About {job['company']}")
                    st.info(st.session_state.company_details[idx])
                    
                    if st.button(f"✖️ Close", key=f"close_{idx}"):
                        del st.session_state.company_details[idx]
                        st.rerun()
    
    elif st.session_state.jobs == [] and st.session_state.searched:
        st.warning(f"No jobs found")
        st.info("💡 Try different job role or location")

# ============================================================
# SAVED JOBS DISPLAY
# ============================================================
if st.session_state.saved_jobs:
    st.markdown("---")
    st.markdown("## ⭐ Saved Jobs")
    
    for idx, job in enumerate(st.session_state.saved_jobs):
        with st.expander(f"💼 {job['title']} - {job['company']}", expanded=False):
            st.markdown(f"""
            **Location:** {job['location']}
            **Salary:** {job['salary']}
            """)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[📋 Apply]({job['url']})", unsafe_allow_html=True)
            with col2:
                if st.button(f"❌ Remove", key=f"remove_{idx}"):
                    st.session_state.saved_jobs.pop(idx)
                    save_saved_jobs(st.session_state.saved_jobs)
                    st.rerun()

# ============================================================
# WHATSAPP STYLE FLOATING CHAT BUTTON & POPUP
# ============================================================

# Floating Chat Button (HTML + JS)
floating_html = """
<div id="chat-container" style="position: fixed; bottom: 25px; right: 25px; z-index: 999;">
    <div id="chat-btn" class="floating-chat-btn" onclick="toggleChat()">
        <span style="font-size: 28px;">💬</span>
    </div>
</div>

<script>
    let isOpen = false;
    let chatWindow = null;
    
    function toggleChat() {
        isOpen = !isOpen;
        const btn = document.getElementById('chat-btn');
        if (isOpen) {
            // Create chat window
            const container = document.getElementById('chat-container');
            chatWindow = document.createElement('div');
            chatWindow.className = 'chat-popup';
            chatWindow.id = 'chat-popup';
            chatWindow.innerHTML = `
                <div class="chat-popup-header">
                    <h4><span>🤖</span> JobBot Assistant</h4>
                    <div class="close-chat" onclick="toggleChat()">✕</div>
                </div>
                <div class="chat-popup-messages" id="chat-popup-messages">
                    <!-- Messages will be loaded from Streamlit -->
                </div>
                <div class="chat-popup-input">
                    <input type="text" id="chat-input" placeholder="Type a message..." />
                    <button onclick="sendMessage()">Send</button>
                </div>
            `;
            container.appendChild(chatWindow);
            
            // Load messages from Streamlit
            loadMessages();
        } else {
            if (chatWindow) {
                chatWindow.remove();
                chatWindow = null;
            }
        }
    }
    
    function loadMessages() {
        const messagesDiv = document.getElementById('chat-popup-messages');
        if (messagesDiv) {
            // This will be populated by Streamlit's rerender
            messagesDiv.innerHTML = '<div style="text-align:center;padding:20px;">Loading...</div>';
        }
    }
    
    function sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value;
        if (message.trim()) {
            // Send to Streamlit backend
            const streamlitData = {message: message};
            // Streamlit will handle this
            input.value = '';
        }
    }
</script>
"""

# Alternative: Simple Streamlit-based Chat
if not st.session_state.chat_open:
    # Floating circle button
    st.markdown("""
    <style>
        .float-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 999;
            font-size: 28px;
            transition: all 0.3s;
            border: none;
        }
        .float-btn:hover {
            transform: scale(1.08);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
    </style>
    <div class="float-btn" onclick="document.querySelector('button[data-testid=\\'baseButton-secondary\\']')?.click()">
        💬
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("", key="hidden_chat_btn", help="Open Chat"):
        st.session_state.chat_open = True
        st.rerun()

if st.session_state.chat_open:
    # Chat popup
    with st.container():
        st.markdown("""
        <style>
            .chat-popup-container {
                position: fixed;
                bottom: 100px;
                right: 25px;
                width: 380px;
                height: 500px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.2);
                z-index: 998;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .chat-messages-area {
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                background: #f8fafc;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .chat-input-area {
                padding: 12px;
                background: white;
                border-top: 1px solid #e2e8f0;
                display: flex;
                gap: 8px;
            }
            .chat-input-area input {
                flex: 1;
                padding: 10px 14px;
                border: 1px solid #e2e8f0;
                border-radius: 25px;
                outline: none;
            }
            .chat-input-area button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 0 18px;
                cursor: pointer;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chat-popup-container">
            <div class="chat-header">
                <span>🤖 JobBot Assistant</span>
                <span style="cursor:pointer;" onclick="window.location.reload()">✕</span>
            </div>
            <div class="chat-messages-area" id="chatArea">
        """, unsafe_allow_html=True)
        
        # Display messages
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 14px; border-radius: 18px; border-top-right-radius: 4px; font-size: 13px; max-width: 85%;">
                        {msg['content']}
                    </div>
                </div>
                <div style="font-size: 9px; color: #94a3b8; text-align: right;">{msg.get('time', '')}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; gap: 8px;">
                    <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #00d4ff, #7b5ea7); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px;">🤖</div>
                    <div style="background: white; padding: 10px 14px; border-radius: 18px; border-top-left-radius: 4px; font-size: 13px; max-width: 85%; border: 1px solid #e2e8f0;">
                        {msg['content']}
                    </div>
                </div>
                <div style="font-size: 9px; color: #94a3b8; margin-left: 38px;">{msg.get('time', '')}</div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_msg = st.text_input("", key="popup_msg", placeholder="Type a message...", label_visibility="collapsed")
        with col2:
            if st.button("Send", key="popup_send"):
                if user_msg:
                    current_time = datetime.now().strftime("%I:%M %p")
                    st.session_state.chat_messages.append({"role": "user", "content": user_msg, "time": current_time})
                    with st.spinner(""):
                        response = chat_with_ai(user_msg)
                        st.session_state.chat_messages.append({"role": "bot", "content": response, "time": datetime.now().strftime("%I:%M %p")})
                    st.rerun()
        
        if st.button("✖️ Close", key="close_chat"):
            st.session_state.chat_open = False
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Job Finder AI | Powered by NB")