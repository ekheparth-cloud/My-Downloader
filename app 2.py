import streamlit as st
import yt_dlp
import os
import re
from datetime import datetime

# --- CONFIGURATION & MULTI-LANGUAGE SUPPORT ---
LANGUAGES = {
    "English": {
        "title": "Universal Video Downloader",
        "input_label": "Paste your link here (Video or Playlist)",
        "btn_find": "Fetch Media",
        "btn_dl": "Download Now",
        "quality": "Select Quality",
        "high": "High Quality (Best)",
        "low": "Low Size (Fast)",
        "playlist_msg": "Playlist detected! This may take a moment for large lists...",
        "success": "Ready for download!",
    },
    "हिन्दी": {
        "title": "यूनिवर्सल वीडियो डाउनलोडर",
        "input_label": "अपना लिंक यहाँ पेस्ट करें (वीडियो या प्लेलिस्ट)",
        "btn_find": "मीडिया खोजें",
        "btn_dl": "अभी डाउनलोड करें",
        "quality": "गुणवत्ता चुनें",
        "high": "उच्च गुणवत्ता",
        "low": "छोटा आकार",
        "playlist_msg": "प्लेलिस्ट मिली! बड़ी लिस्ट में समय लग सकता है...",
        "success": "डाउनलोड के लिए तैयार!",
    }
}

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Downloader", page_icon="📥", layout="centered")

# --- CUSTOM CSS (SaveFrom Style) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00a651; color: white; border: none; }
    .stButton>button:hover { background-color: #008542; color: white; }
    .download-card { padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: white; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'lang' not in st.session_state:
    st.session_state.lang = "English"

# --- UI HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📥 Downloader Pro")
with col2:
    st.session_state.lang = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

L = LANGUAGES[st.session_state.lang]

# --- MAIN INPUT ---
url = st.text_input(L["input_label"], placeholder="https://www.youtube.com/watch?v=...")
format_type = st.radio("Format Type", ["Video (MP4)", "Audio (MP3)"], horizontal=True)
quality_pref = st.select_slider(L["quality"], options=[L["low"], L["high"]])

def get_info(url):
    """Fetches metadata using self-healing yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist', # Critical for 1000+ videos speed
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

if url:
    try:
        with st.spinner(L["btn_find"] + "..."):
            info = get_info(url)
            
        is_playlist = 'entries' in info
        title = info.get('title', 'Unknown Title')
        
        st.markdown(f"### {title}")
        if is_playlist:
            video_count = len(info['entries'])
            st.info(f"📁 {L['playlist_msg']} ({video_count} videos)")
        
        # --- DOWNLOAD LOGIC ---
        if st.button(L["btn_dl"]):
            # Setup download options
            save_path = "downloads"
            if not os.path.exists(save_path): os.makedirs(save_path)
            
            # Formatting Logic
            if format_type == "Audio (MP3)":
                ydl_format = 'bestaudio/best'
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                # High vs Low Size
                ydl_format = 'bestvideo+bestaudio/best' if quality_pref == L["high"] else 'worstvideo+worstaudio/worst'
                postprocessors = []

            final_opts = {
                'format': ydl_format,
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'postprocessors': postprocessors,
                'noplaylist': False if is_playlist else True,
                'ignoreerrors': True, # Keep going even if 1 video in 1000 fails
            }

            with st.spinner("Processing..."):
                with yt_dlp.YoutubeDL(final_opts) as ydl:
                    ydl.download([url])
                st.success(f"✅ {L['success']}")
                st.balloons()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Tip: Make sure the URL is public and yt-dlp is updated.")

# --- FOOTER ---
st.markdown("---")
st.caption("Supports: YouTube, Facebook, Instagram, TikTok & more.")