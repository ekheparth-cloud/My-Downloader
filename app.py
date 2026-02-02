import os
import shutil
import streamlit as st
import yt_dlp

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="SaveFrom Pro Max", 
    page_icon="📥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for the "SaveFrom" Green Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #00d28a;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #00b377; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- APP INTERFACE ---
st.title("🎥 Ultimate Video & Playlist Downloader")
st.markdown("Download videos from 1000+ sites with merged Audio & Video.")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Download Settings")
    lang = st.selectbox("Preferred Audio Language", ["English/Original", "Hindi", "Marathi"])
    quality = st.select_slider("Max Quality", options=["480p", "720p", "1080p", "4K"], value="1080p")
    st.info("Files will be saved to your default system 'Downloads' folder.")

# Main URL Input
url = st.text_input("", placeholder="Paste your YouTube, Facebook, or Playlist link here...", label_visibility="collapsed")

# --- DOWNLOAD LOGIC ---
if st.button("🚀 START DOWNLOAD"):
    if not url:
        st.warning("⚠️ Please enter a URL first!")
    else:
        # Map quality and language
        res = quality.replace("p", "")
        lang_map = {"Hindi": "hi", "Marathi": "mr", "English/Original": "en"}
        lang_code = lang_map.get(lang, "en")
        
        # Path configuration (Cloud-safe)
        save_path = os.path.join(os.path.expanduser("~"), "Downloads")

        ydl_opts = {
            # Logic: Force high quality video + audio merging
            'format': f'bestvideo[height<={res}]+bestaudio/best',
            'outtmpl': f'{save_path}/%(playlist_title)s/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'ignoreerrors': True,
            'noplaylist': False,
            'quiet': False,
        }

        progress_container = st.empty()
        
        try:
            with st.status("📥 Processing... (Analyzing & Merging Audio/Video)", expanded=True) as status:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                status.update(label="✅ Download Complete!", state="complete")
            
            st.success(f"🎉 Success! Check your 'Downloads' folder.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Secure & Safe: No user data is stored. For personal use only.")