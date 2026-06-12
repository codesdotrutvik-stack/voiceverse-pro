import streamlit as st
import requests
from datetime import datetime
import base64
import random

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="✨", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        padding: 0rem 1rem;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
        padding: 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    .stButton button {
        width: auto !important;
        min-width: 100px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    
    .stTextArea textarea {
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        font-size: 0.9rem;
        background: white;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-right-radius: 4px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .ai-msg {
        background: #f1f5f9;
        color: #1e293b;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-left-radius: 4px;
        margin: 8px 0;
        max-width: 80%;
    }
    
    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .quiz-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .quiz-question {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 1rem;
        color: #1e293b;
    }
    
    .radio-label {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 10px;
        cursor: pointer;
    }
    
    .score-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
        padding: 1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>✨ AI Study Buddy</h1></div>', unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

def ask_ai(question, mode):
    if mode == "Simple":
        prompt = "Explain like the student is 5 years old. Very simple words."
    elif mode == "Detailed":
        prompt = "Explain in detail with examples."
    else:
        prompt = "Explain clearly and simply."
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def generate_quiz(topic, num_q=5):
    prompt = f"""Generate {num_q} multiple choice questions about {topic}.
    Format EXACTLY like this example:

Q1: What is Python?
A) A snake
B) A programming language
C) A game
D) A car
Answer: B

Q2: What is AI?
A) Artificial Intelligence
B) Apple Inc
C) Advanced Interface
D) Auto Input
Answer: A

Make questions clear and simple."""
    
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def parse_quiz(quiz_text):
    questions = []
    lines = quiz_text.split('\n')
    current_q = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('Q') and ':' in line:
            if current_q and 'question' in current_q:
                questions.append(current_q)
            current_q = {'question': line.split(':', 1)[1].strip(), 'options': [], 'answer': ''}
        
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            if current_q:
                current_q['options'].append(line)
        
        elif line.startswith('Answer:'):
            if current_q:
                current_q['answer'] = line.split(':')[1].strip()
    
    if current_q and 'question' in current_q:
        questions.append(current_q)
    
    return questions

with st.sidebar:
    st.markdown("### ⚡ Settings")
    mode = st.selectbox("Mode", ["Normal", "Simple", "Detailed"])
    
    st.markdown("---")
    st.markdown("### 📚 Quick Topics")
    
    topics = ["🐍 Python", "🤖 AI", "🧮 Math", "🔬 Science", "🌍 History", "💻 Code"]
    for topic in topics:
        if st.button(topic, key=f"side_{topic}", use_container_width=True):
            with st.spinner("✨"):
                answer = ask_ai(f"Explain {topic} simply", mode)
                st.session_state.chat.append({"q": f"Explain {topic}", "a": answer, "time": datetime.now().strftime("%H:%M")})
                st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask anything")
    user_input = st.text_area("", height=80, placeholder="e.g., What is machine learning?", label_visibility="collapsed")
    
    if st.button("✨ Ask", use_container_width=False) and user_input:
        with st.spinner(""):
            answer = ask_ai(user_input, mode)
            st.session_state.chat.append({"q": user_input, "a": answer, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

with col2:
    st.markdown("### 📝 Quiz")
    quiz_topic = st.text_input("", placeholder="Topic...", label_visibility="collapsed")
    num_q = st.slider("Questions", 3, 8, 5, label_visibility="collapsed")
    
    if st.button("🎯 Generate Quiz", use_container_width=False) and quiz_topic:
        with st.spinner("Creating quiz..."):
            quiz_raw = generate_quiz(quiz_topic, num_q)
            st.session_state.quiz_data = parse_quiz(quiz_raw)
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.rerun()

st.markdown("---")

# Display Chat
for item in reversed(st.session_state.chat[-15:]):
    st.markdown(f'<div class="user-msg"><strong>You</strong><br>{item["q"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-msg"><strong>AI</strong><br>{item["a"]}</div>', unsafe_allow_html=True)

# Display Quiz with Options
if st.session_state.quiz_data:
    st.markdown("---")
    st.markdown("### 📋 Quiz")
    
    # Show score if submitted
    if st.session_state.quiz_submitted:
        percentage = (st.session_state.quiz_score / len(st.session_state.quiz_data)) * 100
        st.markdown(f"""
        <div class="score-card">
            <h2>🎉 Your Score</h2>
            <h1>{st.session_state.quiz_score} / {len(st.session_state.quiz_data)}</h1>
            <p>{percentage:.0f}% Correct</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display each question
    for i, q in enumerate(st.session_state.quiz_data):
        with st.container():
            st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-question">{i+1}. {q["question"]}</div>', unsafe_allow_html=True)
            
            # Radio buttons for options
            if q.get('options'):
                selected = st.radio(
                    "",
                    q['options'],
                    key=f"quiz_q_{i}",
                    index=None,
                    label_visibility="collapsed",
                    horizontal=False
                )
                
                if selected and not st.session_state.quiz_submitted:
                    st.session_state.quiz_answers[f"q{i}"] = selected
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.quiz_submitted and st.session_state.quiz_data:
            if st.button("✅ Submit Quiz", use_container_width=False):
                score = 0
                for i, q in enumerate(st.session_state.quiz_data):
                    user_ans = st.session_state.quiz_answers.get(f"q{i}", "")
                    correct_ans = q.get('answer', '')
                    if user_ans and correct_ans and user_ans[0] == correct_ans:
                        score += 1
                st.session_state.quiz_score = score
                st.session_state.quiz_submitted = True
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Quiz", use_container_width=False):
            st.session_state.quiz_data = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
    
    # Show correct answers after submission
    if st.session_state.quiz_submitted:
        with st.expander("📖 Show Correct Answers"):
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.quiz_answers.get(f"q{i}", "Not answered")
                correct_ans = q.get('answer', 'N/A')
                is_correct = user_ans and correct_ans and user_ans[0] == correct_ans
                
                if is_correct:
                    st.success(f"Q{i+1}: ✅ Correct - {correct_ans}")
                else:
                    st.error(f"Q{i+1}: ❌ Your answer: {user_ans if user_ans else 'None'} | Correct: {correct_ans}")

# Export and Random
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Export Chat", use_container_width=False) and st.session_state.chat:
        chat_text = "\n\n".join([f"You: {c['q']}\nAI: {c['a']}" for c in st.session_state.chat])
        b64 = base64.b64encode(chat_text.encode()).decode()
        st.markdown(f'<a href="data:text/plain;base64,{b64}" download="chat.txt">📁 Download</a>', unsafe_allow_html=True)

with col2:
    if st.button("🎲 Random Topic", use_container_width=False):
        topics = ["Python", "AI", "Space", "Ocean", "Music", "Art", "Sports", "History"]
        rand_topic = random.choice(topics)
        with st.spinner("✨"):
            answer = ask_ai(f"Explain {rand_topic} simply", mode)
            st.session_state.chat.append({"q": f"Tell me about {rand_topic}", "a": answer, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

st.markdown('<div class="footer">✨ Made with Nirbhay </div>', unsafe_allow_html=True)