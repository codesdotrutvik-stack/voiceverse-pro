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
    
    /* Floating Chatbot - Bottom Center */
    .chat-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: auto;
        display: flex;
        justify-content: center;
    }
    
    .chat-toggle-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-weight: 600;
        font-size: 14px;
        border: none;
        transition: all 0.3s;
    }
    .chat-toggle-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    .chat-window {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        width: 400px;
        height: 500px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 999;
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
    .chat-header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
    }
    .close-btn {
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
    .close-btn:hover {
        background: rgba(255,255,255,0.3);
    }
    
    .chat-messages-area {
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .user-msg {
        background: #667eea;
        color: white;
        padding: 10px 14px;
        border-radius: 18px;
        border-bottom-right-radius: 4px;
        max-width: 85%;
        align-self: flex-end;
        font-size: 13px;
        word-wrap: break-word;
    }
    
    .bot-msg {
        background: white;
        color: #1e293b;
        padding: 10px 14px;
        border-radius: 18px;
        border-bottom-left-radius: 4px;
        max-width: 85%;
        align-self: flex-start;
        font-size: 13px;
        border: 1px solid #e2e8f0;
        word-wrap: break-word;
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
        font-size: 13px;
    }
    .chat-input-area input:focus {
        border-color: #667eea;
    }
    .chat-input-area button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0 20px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }
    .chat-input-area button:hover {
        opacity: 0.9;
    }
    
    .typing-indicator {
        background: white;
        padding: 10px 14px;
        border-radius: 18px;
        border-bottom-left-radius: 4px;
        max-width: 60px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .typing-indicator span {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        margin: 0 2px;
        animation: typing 1.4s infinite;
    }
    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
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
    """Chatbot function"""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are a helpful assistant for Job Finder AI. Answer the user's question.

User Question: {user_message}

Give a helpful, friendly response. If asked about jobs, companies, or careers, give practical advice.
Keep response short and friendly (2-3 sentences)."""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "I'm here to help! Ask me about jobs, companies, or careers."

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
        {"role": "assistant", "content": "👋 Hello! I'm your AI assistant. Ask me anything about jobs, companies, or career advice!"}
    ]
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

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
# LOAD DEFAULT JOBS ON STARTUP
# ============================================================
if not st.session_state.searched and not st.session_state.jobs:
    with st.spinner(f"Loading default jobs for {DEFAULT_ROLE} in {DEFAULT_CITY}..."):
        default_jobs, error = fetch_jobs(DEFAULT_ROLE, DEFAULT_CITY)
        if default_jobs:
            st.session_state.jobs = default_jobs
            st.session_state.searched = True
            st.session_state.search_role = DEFAULT_ROLE
            st.session_state.search_city = DEFAULT_CITY

# ============================================================
# SEARCH LOGIC
# ============================================================
if search_clicked:
    with st.spinner(f"Searching for '{st.session_state.search_role}'..."):
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
        st.warning(f"No jobs found for '{st.session_state.search_role}'")
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
# BOTTOM STICKY CHATBOT
# ============================================================
# Chat Toggle Button (Bottom Center)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if not st.session_state.chat_open:
        if st.button("💬 Need Help? Chat with AI", use_container_width=True):
            st.session_state.chat_open = True
            st.rerun()

# Chat Window
if st.session_state.chat_open:
    st.markdown("---")
    st.markdown("### 💬 AI Assistant")
    st.markdown("Ask me anything about jobs, companies, or career advice!")
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div style="text-align: right; margin: 8px 0;"><span style="background: #667eea; color: white; padding: 8px 14px; border-radius: 20px; display: inline-block; max-width: 80%; font-size: 13px;">🧑 {msg["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align: left; margin: 8px 0;"><span style="background: #f1f5f9; color: #1e293b; padding: 8px 14px; border-radius: 20px; display: inline-block; max-width: 80%; font-size: 13px;">🤖 {msg["content"]}</span></div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_message = st.text_input("", key="chat_user_msg", placeholder="Type your message...", label_visibility="collapsed")
    with col2:
        if st.button("Send", key="chat_send_btn"):
            if user_message:
                st.session_state.chat_messages.append({"role": "user", "content": user_message})
                with st.spinner("🤔 Thinking..."):
                    response = chat_with_ai(user_message)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Close chat button
    if st.button("✖️ Close Chat", use_container_width=True):
        st.session_state.chat_open = False
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Job Finder AI | Powered by Adzuna NB")