import streamlit as st
import assemblyai as aai
from datetime import datetime
import os
import requests
import re

st.set_page_config(page_title="Voice to Text Pro", page_icon="📝", layout="wide")

# ============================================================
# API KEYS
# ============================================================
ASSEMBLYAI_KEY = "5e874d691c74442f8b602827e6d26752"
MISTRAL_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

aai.settings.api_key = ASSEMBLYAI_KEY

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }

.stApp { background: linear-gradient(135deg,#f5f7fa 0%,#e8ecf1 100%); }
.block-container { padding:2rem; max-width:1200px; }

@keyframes fadeIn {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}

.main-title {
  font-size:2.5rem; font-weight:700; color:#1e293b;
  text-align:center; letter-spacing:-0.02em;
}
.main-title span { color:#7c3aed; }
.main-sub {
  color:#64748b; text-align:center; font-size:.95rem;
  margin-bottom:1.5rem; animation:fadeIn .8s ease;
}

.glass-card {
  background:rgba(255,255,255,.7); backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,.5); border-radius:16px;
  padding:1.2rem; margin-bottom:1.5rem;
  box-shadow:0 2px 8px rgba(0,0,0,.04); transition:all .2s;
}
.glass-card:hover { box-shadow:0 4px 16px rgba(0,0,0,.06); }

[data-testid="stFileUploader"] {
  background:rgba(255,255,255,.3)!important;
  border:2px dashed #e2e8f0!important;
  border-radius:12px!important; padding:1.5rem!important;
}
[data-testid="stFileUploader"]:hover { border-color:#7c3aed!important; }

.text-box {
  background:rgba(255,255,255,.85); border:1px solid #e2e8f0;
  border-radius:12px; padding:18px; min-height:120px;
  color:#1e293b; font-size:.95rem; line-height:1.8;
  white-space:pre-wrap; max-height:500px; overflow-y:auto;
  animation:fadeIn .6s ease;
}

/* ── History card ── */
.h-card {
  background:#fff; border:1px solid #e2e8f0; border-radius:12px;
  padding:14px 16px; margin:8px 0; transition:all .2s;
}
.h-card:hover { border-color:#7c3aed; box-shadow:0 2px 8px rgba(124,58,237,.06); }
.h-meta { display:flex; justify-content:space-between; margin-bottom:6px; }
.h-mode { color:#7c3aed; font-weight:600; font-size:.85rem; }
.h-time { color:#94a3b8; font-size:.7rem; }
.h-text { color:#475569; font-size:.85rem; line-height:1.6; word-break:break-word; }

/* speaker label inside history */
.spk { color:#7c3aed; font-weight:600; }

.copy-mini {
  margin-top:8px; background:#f1f5f9; border:none; border-radius:6px;
  padding:4px 12px; font-size:.7rem; cursor:pointer; color:#475569;
  transition:background .2s;
}
.copy-mini:hover { background:#e2e8f0; }

.stButton > button {
  background:#7c3aed!important; color:white!important; border:none!important;
  border-radius:8px!important; font-weight:500!important;
  font-size:.85rem!important; padding:8px 18px!important;
  transition:all .2s!important;
}
.stButton > button:hover { background:#6d28d9!important; transform:translateY(-1px); }

.divider {
  height:1px;
  background:linear-gradient(90deg,transparent,#e2e8f0,transparent);
  margin:1.2rem 0;
}
.section-title {
  color:#94a3b8; font-size:.7rem; font-weight:600;
  text-transform:uppercase; letter-spacing:1px; margin-bottom:.6rem;
}
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:#7c3aed; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
for k, v in {
    "history": [],
    "transcribed_text": "",
    "original_text": "",
    "translated_text": "",
    "show_translate": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# HELPERS
# ============================================================
def translate_text(text, target_lang):
    lang_map = {"Hindi":"Hindi","Gujarati":"Gujarati","Spanish":"Spanish",
                "French":"French","German":"German","Chinese":"Chinese","Japanese":"Japanese"}
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type":"application/json"}
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role":"user",
                       "content": f"Translate to {lang_map.get(target_lang,'Hindi')}. Output translation only.\n\n{text}"}],
        "max_tokens": 2000
    }
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Translation failed."


def format_transcript_plain(transcript, conversation_mode):
    """Return PLAIN TEXT — no markdown, no HTML."""
    if conversation_mode and transcript.utterances:
        lines = []
        for u in transcript.utterances:
            lines.append(f"Speaker {u.speaker}: {u.text}")
        return "\n\n".join(lines)
    return transcript.text or ""


def render_history_text(text):
    """Convert 'Speaker X: ...' lines to HTML with coloured labels."""
    html_lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(Speaker [A-Z]):(.+)$", line)
        if m:
            html_lines.append(
                f'<span class="spk">{m.group(1)}:</span>{m.group(2)}'
            )
        else:
            html_lines.append(line)
    return "<br>".join(html_lines)


def copy_button(text, key):
    """Streamlit download-as-clipboard workaround — shows a JS copy button."""
    # escape backticks and backslashes for JS template literal
    safe = text.replace("\\", "\\\\").replace("`", "\\`")
    st.markdown(
        f"""<button class="copy-mini"
            onclick="navigator.clipboard.writeText(`{safe}`).then(()=>{{
                this.innerText='✅ Copied!';
                setTimeout(()=>this.innerText='📋 Copy',1500);
            }})">📋 Copy</button>""",
        unsafe_allow_html=True
    )

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-title">📝 Voice to Text <span>Pro</span></div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Upload audio/video • Record voice • AI transcribes • Translate</div>', unsafe_allow_html=True)

# ============================================================
# RECORD SECTION
# ============================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 🎙️ Record Voice")

audio_value = st.audio_input("Click to record", key="audio_recorder")

if audio_value is not None:
    with st.spinner("⏳ Transcribing..."):
        try:
            tmp = "temp_audio.wav"
            with open(tmp, "wb") as f:
                f.write(audio_value.getvalue())

            config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2)
            transcript = aai.Transcriber(config=config).transcribe(tmp)

            if transcript.text:
                plain = format_transcript_plain(transcript, True)
                st.session_state.transcribed_text = plain
                st.session_state.original_text    = plain
                st.session_state.history.append({
                    "text": plain,
                    "time": datetime.now().strftime("%I:%M %p, %d %b"),
                    "mode": "Conversation"
                })
                st.success("✅ Transcription complete!")
            else:
                st.error("❌ No text detected.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# UPLOAD SECTION
# ============================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 📤 Upload File")
st.caption("MP3, WAV, M4A, FLAC, WebM, MP4, MOV, AVI, MKV")

uploaded_file = st.file_uploader("", type=["mp3","wav","m4a","flac","webm","mp4","mov","avi","mkv"],
                                  label_visibility="collapsed")

if uploaded_file:
    if uploaded_file.type.startswith("video") or \
       uploaded_file.name.lower().endswith((".mp4",".mov",".avi",".mkv")):
        st.video(uploaded_file)
    else:
        st.audio(uploaded_file)
    st.caption(f"📁 {uploaded_file.name} | {len(uploaded_file.getvalue())/1e6:.2f} MB")

    conversation_mode = st.checkbox("💬 Conversation Mode (Speaker Labels)", value=True)

    if st.button("🎯 Transcribe", type="primary", use_container_width=True):
        with st.spinner("⏳ Transcribing..."):
            ext = uploaded_file.name.rsplit(".",1)[-1]
            tmp = f"temp_upload.{ext}"
            try:
                with open(tmp, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                config = aai.TranscriptionConfig(
                    speaker_labels=conversation_mode,
                    speakers_expected=2 if conversation_mode else None
                )
                transcript = aai.Transcriber(config=config).transcribe(tmp)

                if transcript.text:
                    plain = format_transcript_plain(transcript, conversation_mode)
                    st.session_state.transcribed_text = plain
                    st.session_state.original_text    = plain
                    st.session_state.translated_text  = ""
                    st.session_state.history.append({
                        "text": plain,
                        "time": datetime.now().strftime("%I:%M %p, %d %b"),
                        "mode": "Conversation" if conversation_mode else "Standard"
                    })
                    st.success("✅ Done!")
                else:
                    st.error("❌ No text detected.")
            except Exception as e:
                st.error(f"❌ {e}")
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TRANSCRIPTION OUTPUT
# ============================================================
if st.session_state.transcribed_text:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Transcription</div>', unsafe_allow_html=True)

    # Render with coloured speaker labels
    rendered = render_history_text(st.session_state.transcribed_text)
    st.markdown(f'<div class="text-box">{rendered}</div>', unsafe_allow_html=True)

    # Working copy button (JS clipboard)
    copy_button(st.session_state.transcribed_text, "main_copy")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.download_button("📥 Download", data=st.session_state.transcribed_text,
                           file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                           mime="text/plain", use_container_width=True)
    with c2:
        if st.button("🔁 Translate", use_container_width=True):
            st.session_state.show_translate = not st.session_state.show_translate
            st.rerun()
    with c3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.transcribed_text = ""
            st.session_state.original_text    = ""
            st.session_state.translated_text  = ""
            st.session_state.show_translate   = False
            st.rerun()
    with c4:
        wc = len(st.session_state.transcribed_text.split())
        st.markdown(f'<div style="text-align:center;color:#7c3aed;padding:8px;font-size:.8rem;font-weight:600;">{wc} words</div>',
                    unsafe_allow_html=True)

# ============================================================
# TRANSLATION
# ============================================================
if st.session_state.show_translate and st.session_state.original_text:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌍 Translate</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3,1])
    with c1:
        target_lang = st.selectbox("Language", ["Hindi","Gujarati","Spanish","French","German","Chinese","Japanese"],
                                   label_visibility="collapsed")
    with c2:
        do_translate = st.button("Translate ✨", type="primary", use_container_width=True)

    if do_translate:
        with st.spinner("Translating..."):
            t = translate_text(st.session_state.original_text, target_lang)
            st.session_state.translated_text = t

    if st.session_state.translated_text:
        st.markdown(f'<div class="text-box" style="border-color:#fbbf24;">{st.session_state.translated_text}</div>',
                    unsafe_allow_html=True)
        copy_button(st.session_state.translated_text, "trans_copy")
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("📥 Download Translation", data=st.session_state.translated_text,
                           file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                           mime="text/plain", use_container_width=True)

# ============================================================
# HISTORY  — pure HTML, no raw markdown leaking
# ============================================================
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📜 History ({len(st.session_state.history)} entries)</div>',
                unsafe_allow_html=True)

    for item in reversed(st.session_state.history[-15:]):
        # render speaker labels as coloured HTML
        preview_html = render_history_text(item["text"][:300])
        if len(item["text"]) > 300:
            preview_html += " <span style='color:#94a3b8'>…</span>"

        # safe JS string for clipboard
        safe_js = item["text"].replace("\\","\\\\").replace("`","\\`")

        st.markdown(f"""
        <div class="h-card">
            <div class="h-meta">
                <span class="h-mode">{item['mode']}</span>
                <span class="h-time">🕐 {item['time']}</span>
            </div>
            <div class="h-text">{preview_html}</div>
            <button class="copy-mini"
                onclick="navigator.clipboard.writeText(`{safe_js}`).then(()=>{{
                    this.innerText='✅ Copied!';
                    setTimeout(()=>this.innerText='📋 Copy',1500);
                }})">📋 Copy</button>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:.6rem;">📝 Voice to Text Pro · AssemblyAI + Mistral · Created by Nirbhay</div>',
            unsafe_allow_html=True)