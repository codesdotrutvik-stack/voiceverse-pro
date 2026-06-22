import streamlit as st
import assemblyai as aai
from datetime import datetime
import os
import requests
import json

st.set_page_config(page_title="Voice to Text Pro", page_icon="🎤", layout="wide")

# ============================================================
# API KEYS
# ============================================================
ASSEMBLYAI_KEY = "5e874d691c74442f8b602827e6d26752"
MISTRAL_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

aai.settings.api_key = ASSEMBLYAI_KEY

# ============================================================
# PREMIUM DARK CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
.stApp { background: #0a0a12; }
.block-container { padding: 2rem; max-width: 1000px; }

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0px); }
}
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #7c3aed, #4f46e5, #a78bfa);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: shimmer 6s linear infinite;
    letter-spacing: -0.02em;
}
.main-sub { color: #94a3b8; text-align: center; font-size: 1rem; margin-bottom: 1.5rem; animation: fadeIn 0.8s ease; }

.glass-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}
.glass-card:hover { border-color: rgba(139,92,246,0.2); }

.text-box {
    background: #12121e;
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
    color: #e2e8f0;
    font-size: 0.95rem;
    line-height: 1.8;
    white-space: pre-wrap;
    max-height: 500px;
    overflow-y: auto;
    animation: fadeIn 0.6s ease;
}

.history-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 10px 0;
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease;
}
.history-item:hover { border-color: rgba(139,92,246,0.3); transform: translateX(4px); }
.history-time { color: #475569; font-size: 0.7rem; }

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(124,58,237,0.25);
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.15), transparent);
    margin: 1.5rem 0;
}

.section-title {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}

.stTextInput > div > div > input {
    background: #12121e !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 50px !important;
    padding: 12px 20px !important;
    color: #e2e8f0 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}

.stSelectbox > div > div > div {
    background: #12121e !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

.stNumberInput > div > div > input {
    background: #12121e !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(139,92,246,0.2) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: #7c3aed !important; }

[data-testid="stAudioInput"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 16px !important;
    padding: 0.5rem !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #12121e; }
::-webkit-scrollbar-thumb { background: #7c3aed; border-radius: 10px; }
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

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">🎤 Voice to Text Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Upload audio/video • Record voice • AI transcribes • Translate</div>', unsafe_allow_html=True)

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
                    
                    # Convert minutes to seconds
                    start_sec = start_min * 60
                    end_sec = end_min * 60
                    
                    # Build config with correct parameters
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
            st.success("✅ Copied!")
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
# TRANSLATION
# ============================================================
if st.session_state.get("show_translate", False) and st.session_state.original_text:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌍 Translate</div>', unsafe_allow_html=True)
    
    target_lang = st.selectbox("Select language", ["Hindi", "Gujarati", "Spanish", "French", "German", "Chinese", "Japanese"])
    
    if st.button("Translate", type="primary"):
        with st.spinner("Translating..."):
            translated = translate_text(st.session_state.original_text, target_lang)
            if translated:
                st.session_state.translated_text = translated
                st.markdown(f'<div class="text-box" style="border-color: rgba(251,191,36,0.3);">{translated}</div>', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Translation",
                    data=translated,
                    file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

# ============================================================
# HISTORY WITH FIXED COPY/DOWNLOAD
# ============================================================
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📜 History</div>', unsafe_allow_html=True)
    
    for idx, item in enumerate(reversed(st.session_state.history)):
        safe_text = item['full_text'].replace('`', '\\`').replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
        
        st.markdown(f"""
        <div class="history-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #a78bfa; font-weight: 600;">{item['mode']}</span>
                    <span style="color: #475569; font-size: 0.7rem; margin-left: 8px;">{item['duration']}</span>
                </div>
                <div style="color: #475569; font-size: 0.7rem;">{item['time']}</div>
            </div>
            <div style="margin-top: 6px; color: #94a3b8; font-size: 0.85rem; max-height: 80px; overflow: hidden; text-overflow: ellipsis;">
                {item['full_text'][:200]}{'...' if len(item['full_text']) > 200 else ''}
            </div>
            <div style="display: flex; gap: 10px; margin-top: 8px; flex-wrap: wrap;">
                <button onclick="navigator.clipboard.writeText(`{safe_text}`)" style="background: none; border: 1px solid rgba(139,92,246,0.3); color: #a78bfa; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; cursor: pointer;">📋 Copy</button>
                <a href="data:text/plain;charset=utf-8,{item['full_text'].replace('\n', '%0A').replace(' ', '%20')}" download="transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt" style="background: none; border: 1px solid rgba(139,92,246,0.3); color: #a78bfa; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; text-decoration: none;">📥 Download</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #475569; font-size: 0.6rem;">🎤 Voice to Text Pro · Powered by AssemblyAI + Mistral · Created by Nirbhay</div>', unsafe_allow_html=True)