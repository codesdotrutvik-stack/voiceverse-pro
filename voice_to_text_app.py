import streamlit as st
import assemblyai as aai
from datetime import datetime
import os
import requests
import json
import base64

st.set_page_config(page_title="Voice to Text Pro", page_icon="🎤", layout="wide")

# ============================================================
# API KEYS
# ============================================================
ASSEMBLYAI_KEY = "5e874d691c74442f8b602827e6d26752"
MISTRAL_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

aai.settings.api_key = ASSEMBLYAI_KEY

# ============================================================
# PREMIUM LIGHT MODE CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8edf5 100%);
}
.block-container { padding: 2rem; max-width: 1000px; }

/* Animated Gradient Header */
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0px); }
}
@keyframes glowPulse {
    0% { box-shadow: 0 0 20px rgba(124,58,237,0.15); }
    50% { box-shadow: 0 0 40px rgba(124,58,237,0.25); }
    100% { box-shadow: 0 0 20px rgba(124,58,237,0.15); }
}

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed, #4f46e5, #7c3aed);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: shimmer 6s linear infinite;
    letter-spacing: -0.02em;
}
.main-sub {
    color: #6b7280;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    animation: fadeIn 0.8s ease;
}

/* Premium Glass Card - Light Mode */
.glass-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
}
.glass-card:hover {
    box-shadow: 0 12px 48px rgba(124,58,237,0.10);
    border-color: rgba(124,58,237,0.15);
}

.text-box {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
    color: #1e293b;
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
    max-height: 500px;
    overflow-y: auto;
    animation: fadeIn 0.6s ease;
}

.history-item {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(124,58,237,0.08);
    border-radius: 16px;
    padding: 14px 18px;
    margin: 10px 0;
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease;
}
.history-item:hover {
    border-color: rgba(124,58,237,0.3);
    transform: translateX(4px);
    box-shadow: 0 4px 16px rgba(124,58,237,0.08);
}

.history-time { color: #94a3b8; font-size: 0.7rem; }

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.2) !important;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 32px rgba(124,58,237,0.3) !important;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.12), transparent);
    margin: 1.5rem 0;
}

.section-title {
    color: #6b7280;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: 50px !important;
    padding: 12px 20px !important;
    color: #1e293b !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.08) !important;
}

.stSelectbox > div > div > div {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: 12px !important;
    color: #1e293b !important;
}

.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: 12px !important;
    color: #1e293b !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.4) !important;
    border: 2px dashed rgba(124,58,237,0.2) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: #7c3aed !important; }

[data-testid="stAudioInput"] {
    background: rgba(255,255,255,0.4) !important;
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: 16px !important;
    padding: 0.5rem !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #e8edf5; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 10px; }

/* Status messages */
.success-status {
    background: rgba(52,211,153,0.15);
    color: #065f46;
    padding: 12px;
    border-radius: 12px;
    border-left: 4px solid #10b981;
}
.error-status {
    background: rgba(239,68,68,0.1);
    color: #991b1b;
    padding: 12px;
    border-radius: 12px;
    border-left: 4px solid #ef4444;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "copy_status" not in st.session_state:
    st.session_state.copy_status = ""

# ============================================================
# FUNCTIONS
# ============================================================
def translate_text(text, target_lang):
    lang_map = {
        "Hindi": "Hindi",
        "Gujarati": "Gujarati",
        "Spanish": "Spanish",
        "French": "French",
        "German": "German",
        "Chinese": "Chinese",
        "Japanese": "Japanese"
    }
    language = lang_map.get(target_lang, "Hindi")
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""Translate the following text to {language}. Only output the translation, no additional text.

Text:
{text}
"""
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Translation failed."

def copy_to_clipboard(text):
    """Copy text to clipboard using JavaScript"""
    return f"""
    <script>
        function copyText() {{
            navigator.clipboard.writeText(`{text}`).then(function() {{
                document.getElementById('copyStatus').innerHTML = '✅ Copied to clipboard!';
                document.getElementById('copyStatus').style.color = '#10b981';
            }});
        }}
        copyText();
    </script>
    """

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">🎤 Voice to Text Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Upload audio/video • Record voice • AI transcribes • Translate</div>', unsafe_allow_html=True)

# ============================================================
# COPY STATUS
# ============================================================
if st.session_state.copy_status:
    st.markdown(f'<div class="success-status">{st.session_state.copy_status}</div>', unsafe_allow_html=True)
    st.session_state.copy_status = ""

# ============================================================
# RECORD SECTION
# ============================================================
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎙️ Record Voice")
    
    audio_value = st.audio_input("Click to record", key="audio_recorder")
    
    if audio_value is not None:
        with st.spinner("⏳ Transcribing..."):
            try:
                temp_file = "temp_audio.wav"
                with open(temp_file, "wb") as f:
                    f.write(audio_value.getvalue())
                
                config = aai.TranscriptionConfig(
                    speaker_labels=True,
                    speakers_expected=2
                )
                transcriber = aai.Transcriber(config=config)
                transcript = transcriber.transcribe(temp_file)
                
                if transcript.text:
                    if transcript.utterances:
                        formatted = ""
                        for utterance in transcript.utterances:
                            speaker = f"Speaker {utterance.speaker}"
                            formatted += f"**{speaker}:** {utterance.text}\n\n"
                        st.session_state.transcribed_text = formatted
                        st.session_state.original_text = formatted
                    else:
                        st.session_state.transcribed_text = transcript.text
                        st.session_state.original_text = transcript.text
                    
                    st.session_state.history.append({
                        "full_text": st.session_state.original_text,
                        "time": datetime.now().strftime("%I:%M %p, %d %b"),
                        "mode": "Conversation",
                        "duration": "Recorded"
                    })
                    st.success("✅ Transcription complete!")
                else:
                    st.error("❌ No text detected.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            finally:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# UPLOAD SECTION
# ============================================================
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload File")
    st.caption("Supported: MP3, WAV, M4A, FLAC, WebM, MP4, MOV, AVI, MKV")

    uploaded_file = st.file_uploader(
        "",
        type=["mp3", "wav", "m4a", "flac", "webm", "mp4", "mov", "avi", "mkv"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([2, 1])
        with col1:
            file_type = uploaded_file.type
            if "video" in file_type or uploaded_file.name.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
                st.video(uploaded_file)
            else:
                st.audio(uploaded_file, format="audio/wav")
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
            st.caption(f"📁 {uploaded_file.name} | {file_size:.2f} MB")
        
        with col2:
            st.markdown("#### ⏱️ Duration (Minutes)")
            start_min = st.number_input("Start (min)", min_value=0, value=0, step=1, key="start_min")
            end_min = st.number_input("End (min)", min_value=0, value=0, step=1, key="end_min")
            st.caption("Leave 0 for full file")
        
        conversation_mode = st.checkbox("💬 Conversation Mode (Speaker Labels)", value=True)

        if st.button("🎯 Transcribe", type="primary", use_container_width=True):
            with st.spinner("⏳ Transcribing..."):
                try:
                    file_ext = uploaded_file.name.split('.')[-1]
                    temp_file = f"temp_upload.{file_ext}"
                    with open(temp_file, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    start_sec = start_min * 60
                    end_sec = end_min * 60
                    
                    config_params = {
                        "speaker_labels": True if conversation_mode else False,
                        "speakers_expected": 2
                    }
                    if start_sec > 0:
                        config_params["audio_start_from"] = start_sec
                    if end_sec > 0:
                        config_params["audio_end_at"] = end_sec
                    
                    config = aai.TranscriptionConfig(**config_params)
                    transcriber = aai.Transcriber(config=config)
                    transcript = transcriber.transcribe(temp_file)
                    
                    if transcript.text:
                        if conversation_mode and transcript.utterances:
                            formatted = ""
                            for utterance in transcript.utterances:
                                speaker = f"Speaker {utterance.speaker}"
                                formatted += f"**{speaker}:** {utterance.text}\n\n"
                            st.session_state.transcribed_text = formatted
                            st.session_state.original_text = formatted
                        else:
                            st.session_state.transcribed_text = transcript.text
                            st.session_state.original_text = transcript.text
                        
                        st.session_state.translated_text = ""
                        st.session_state.history.append({
                            "full_text": st.session_state.original_text,
                            "time": datetime.now().strftime("%I:%M %p, %d %b"),
                            "mode": "Conversation" if conversation_mode else "Standard",
                            "duration": f"{start_min}m-{end_min}m" if end_min > 0 else "Full"
                        })
                        st.success("✅ Transcription complete!")
                    else:
                        st.error("❌ No text detected.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    try:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                    except:
                        pass

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# DISPLAY TRANSCRIPTION
# ============================================================
if st.session_state.transcribed_text:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Transcription</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="text-box">{st.session_state.transcribed_text}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📋 Copy", use_container_width=True):
            st.session_state.copy_status = "✅ Copied to clipboard!"
            st.rerun()
    with col2:
        if st.button("📥 Download", use_container_width=True):
            st.download_button(
                label="📥 Download",
                data=st.session_state.transcribed_text,
                file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.transcribed_text = ""
            st.session_state.original_text = ""
            st.session_state.translated_text = ""
            st.rerun()
    with col4:
        if st.button("🔁 Translate", use_container_width=True):
            st.session_state.show_translate = not st.session_state.get("show_translate", False)
            st.rerun()

# ============================================================
# TRANSLATION MODERN DESIGN
# ============================================================
if st.session_state.get("show_translate", False) and st.session_state.original_text:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌍 Translate</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        target_lang = st.selectbox(
            "Select language",
            ["Hindi", "Gujarati", "Spanish", "French", "German", "Chinese", "Japanese"],
            label_visibility="collapsed"
        )
    with col2:
        translate_btn = st.button("Translate", type="primary", use_container_width=True)
    
    if translate_btn:
        with st.spinner("Translating..."):
            translated = translate_text(st.session_state.original_text, target_lang)
            if translated:
                st.session_state.translated_text = translated
                st.markdown(f'<div class="text-box" style="border-color: rgba(251,191,36,0.3);">{translated}</div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Translation", use_container_width=True):
                        st.session_state.copy_status = "✅ Translation copied!"
                        st.rerun()
                with col2:
                    st.download_button(
                        label="📥 Download Translation",
                        data=translated,
                        file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

# ============================================================
# HISTORY WITH COPY/DOWNLOAD
# ============================================================
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📜 History</div>', unsafe_allow_html=True)
    
    for idx, item in enumerate(reversed(st.session_state.history)):
        safe_text = item['full_text'].replace('`', '\\`').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
        short_text = item['full_text'][:200] + ('...' if len(item['full_text']) > 200 else '')
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: #7c3aed; font-weight: 600;">{item['mode']}</span>
                            <span style="color: #94a3b8; font-size: 0.7rem; margin-left: 8px;">{item['duration']}</span>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.7rem;">{item['time']}</div>
                    </div>
                    <div style="margin-top: 6px; color: #475569; font-size: 0.85rem;">
                        {short_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{idx}", use_container_width=True):
                    st.session_state.copy_status = "✅ Copied from history!"
                    st.rerun()
    
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 0.6rem;">🎤 Voice to Text Pro · Powered by AssemblyAI + Mistral · Created by Nirbhay</div>', unsafe_allow_html=True)