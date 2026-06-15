import streamlit as st
import json
from datetime import datetime, date
import uuid

st.set_page_config(page_title="TaskFlow", page_icon="📋", layout="wide")

st.markdown("""
<style>
    * { font-family: 'Inter', sans-serif; }
    .block-container { padding: 1rem 1.5rem !important; }
    
    .column {
        background: #f1f2f4;
        border-radius: 12px;
        padding: 12px;
        min-height: 500px;
    }
    
    .column-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
        margin-bottom: 10px;
        border-bottom: 2px solid;
        font-weight: 600;
    }
    
    .task-card {
        background: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        border: 1px solid #e2e4e6;
        cursor: pointer;
        transition: all 0.2s;
    }
    .task-card:hover {
        background: #f8f9fa;
        border-color: #4c9aff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .task-title { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
    .task-desc { font-size: 12px; color: #6b778c; margin-bottom: 8px; }
    .task-meta { display: flex; gap: 8px; font-size: 11px; }
    .priority-high { color: #bf2600; background: #ffebe6; padding: 2px 8px; border-radius: 4px; }
    .priority-medium { color: #974f0c; background: #fff0b3; padding: 2px 8px; border-radius: 4px; }
    .priority-low { color: #006644; background: #e3fcef; padding: 2px 8px; border-radius: 4px; }
    
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        background: white;
        border-radius: 12px;
        width: 500px;
        max-width: 90%;
        max-height: 80%;
        overflow-y: auto;
        padding: 20px;
    }
    
    .comment {
        background: #f4f5f7;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .comment-author { font-weight: 600; font-size: 12px; }
    .comment-time { font-size: 10px; color: #6b778c; }
    .comment-text { font-size: 12px; margin-top: 4px; }
    
    .stButton button { border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "taskflow_data.json"

if "tasks" not in st.session_state:
    try:
        with open(DATA_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
    except:
        st.session_state.tasks = []

if "selected_task" not in st.session_state:
    st.session_state.selected_task = None

if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.tasks, f, indent=2)

def add_task(title, desc, priority, due_date):
    task = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "desc": desc,
        "priority": priority,
        "due": due_date,
        "column": "upcoming",
        "comments": [],
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.tasks.append(task)
    save_tasks()
    st.rerun()

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    if st.session_state.selected_task == task_id:
        st.session_state.selected_task = None
    save_tasks()
    st.rerun()

def move_task(task_id, new_column):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["column"] = new_column
            break
    save_tasks()
    st.rerun()

def update_task(task_id, title, desc, priority, due):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["desc"] = desc
            task["priority"] = priority
            task["due"] = due
            break
    save_tasks()
    st.rerun()

def add_comment(task_id, comment_text, author):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["comments"].append({
                "id": str(uuid.uuid4())[:6],
                "text": comment_text,
                "author": author,
                "time": datetime.now().strftime("%d %b, %H:%M")
            })
            break
    save_tasks()
    st.rerun()

# Header
st.markdown("## 📋 TaskFlow")
st.markdown("---")

# Add Card Button
if st.button("➕ Add New Card", use_container_width=True):
    st.session_state.show_add_form = not st.session_state.show_add_form
    st.rerun()

# Add Card Form
if st.session_state.show_add_form:
    with st.container():
        st.markdown("### ➕ Create New Task")
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input("Title *", placeholder="What needs to be done?")
            new_desc = st.text_area("Description", placeholder="Add details...")
        with col2:
            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            new_due = st.date_input("Due Date", date.today())
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Create Task", use_container_width=True):
                if new_title.strip():
                    add_task(new_title.strip(), new_desc, new_priority, new_due.strftime("%Y-%m-%d"))
                    st.session_state.show_add_form = False
                    st.success("Task created!")
                    st.rerun()
                else:
                    st.warning("Title is required")
        with col_btn2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_add_form = False
                st.rerun()
    st.markdown("---")

# Statistics
total = len(st.session_state.tasks)
done = len([t for t in st.session_state.tasks if t["column"] == "done"])
progress = len([t for t in st.session_state.tasks if t["column"] == "progress"])
high = len([t for t in st.session_state.tasks if t["priority"] == "High"])

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
col_s1.metric("📊 Total Tasks", total)
col_s2.metric("✅ Completed", done)
col_s3.metric("⚙️ In Progress", progress)
col_s4.metric("🔴 High Priority", high)

st.markdown("---")

# Columns
COLUMNS = [
    {"name": "📋 Upcoming", "key": "upcoming", "color": "#97a0af"},
    {"name": "⚙️ In Progress", "key": "progress", "color": "#f8c844"},
    {"name": "📝 To Review", "key": "review", "color": "#4c9aff"},
    {"name": "✅ Done", "key": "done", "color": "#57d9a3"},
]

def render_column(column_name, column_key, color):
    tasks = [t for t in st.session_state.tasks if t["column"] == column_key]
    
    st.markdown(f"""
    <div class="column">
        <div class="column-header" style="border-color: {color}">
            <span>{column_name}</span>
            <span>{len(tasks)}</span>
        </div>
    """, unsafe_allow_html=True)
    
    for task in tasks:
        priority_class = f"priority-{task['priority'].lower()}"
        due_display = f"📅 {task['due']}" if task.get('due') else ""
        
        st.markdown(f"""
        <div class="task-card" onclick="location.href='?task={task['id']}'">
            <div class="task-title">{task['title']}</div>
            <div class="task-desc">{task['desc'][:60]}{'...' if len(task['desc']) > 60 else ''}</div>
            <div class="task-meta">
                <span class="{priority_class}">{task['priority']}</span>
                <span>{due_display}</span>
                <span>💬 {len(task.get('comments', []))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Move buttons
        col_move1, col_move2, col_move3, col_move4, col_del = st.columns([1,1,1,1,1])
        with col_move1:
            if column_key != "upcoming":
                if st.button("⬅️ Upcoming", key=f"mv_up_{task['id']}"):
                    move_task(task['id'], "upcoming")
        with col_move2:
            if column_key != "progress":
                if st.button("⚙️ Progress", key=f"mv_pr_{task['id']}"):
                    move_task(task['id'], "progress")
        with col_move3:
            if column_key != "review":
                if st.button("📝 Review", key=f"mv_re_{task['id']}"):
                    move_task(task['id'], "review")
        with col_move4:
            if column_key != "done":
                if st.button("✅ Done", key=f"mv_do_{task['id']}"):
                    move_task(task['id'], "done")
        with col_del:
            if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                delete_task(task['id'])
                st.rerun()
        
        # Edit button
        if st.button("✏️ Edit / Comments", key=f"edit_{task['id']}"):
            st.session_state.selected_task = task['id']
            st.rerun()
        
        st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        render_column(COLUMNS[i]["name"], COLUMNS[i]["key"], COLUMNS[i]["color"])

# Modal for task details
if st.session_state.selected_task:
    task = next((t for t in st.session_state.tasks if t["id"] == st.session_state.selected_task), None)
    if task:
        st.markdown("---")
        st.markdown(f"### ✏️ Editing: {task['title']}")
        
        tab1, tab2, tab3 = st.tabs(["📝 Details", "💬 Comments", "⚙️ Actions"])
        
        with tab1:
            edit_title = st.text_input("Title", task['title'], key="edit_title")
            edit_desc = st.text_area("Description", task.get('desc', ''), key="edit_desc", height=100)
            edit_priority = st.selectbox("Priority", ["High", "Medium", "Low"], 
                                        index=["High","Medium","Low"].index(task['priority']), 
                                        key="edit_priority")
            edit_due = st.date_input("Due Date", 
                                    datetime.strptime(task['due'], "%Y-%m-%d").date() if task.get('due') else date.today(),
                                    key="edit_due")
            
            if st.button("💾 Save Changes", key="save_edit"):
                update_task(task['id'], edit_title, edit_desc, edit_priority, edit_due.strftime("%Y-%m-%d"))
                st.success("Saved!")
                st.rerun()
        
        with tab2:
            st.markdown("**Comments**")
            for comment in task.get('comments', []):
                st.markdown(f"""
                <div class="comment">
                    <span class="comment-author">{comment['author']}</span>
                    <span class="comment-time">{comment['time']}</span>
                    <div class="comment-text">{comment['text']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            new_comment = st.text_area("Write a comment...", key="new_comment", height=60)
            comment_author = st.text_input("Your name", "You", key="comment_author")
            
            if st.button("💬 Post Comment", key="post_comment"):
                if new_comment.strip():
                    add_comment(task['id'], new_comment.strip(), comment_author.strip())
                    st.rerun()
        
        with tab3:
            st.markdown("**Move Task**")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                if st.button("📋 Upcoming", key="move_up"):
                    move_task(task['id'], "upcoming")
                    st.session_state.selected_task = None
                    st.rerun()
            with col_m2:
                if st.button("⚙️ In Progress", key="move_pr"):
                    move_task(task['id'], "progress")
                    st.session_state.selected_task = None
                    st.rerun()
            with col_m3:
                if st.button("📝 To Review", key="move_re"):
                    move_task(task['id'], "review")
                    st.session_state.selected_task = None
                    st.rerun()
            with col_m4:
                if st.button("✅ Done", key="move_do"):
                    move_task(task['id'], "done")
                    st.session_state.selected_task = None
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**⚠️ Danger Zone**")
            if st.button("🗑️ Delete This Task", key="delete_task_btn"):
                delete_task(task['id'])
                st.session_state.selected_task = None
                st.warning("Task deleted!")
                st.rerun()
        
        if st.button("❌ Close", key="close_modal"):
            st.session_state.selected_task = None
            st.rerun()

st.markdown("---")
st.caption("TaskFlow Pro | Click on card to edit | Use move buttons to change column")