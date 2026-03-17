import streamlit as st
import yt_dlp
import os
import tempfile

st.title("YouTube Downloader (High Compatibility)")

YT_COOKIES = st.secrets.get("youtube_cookies")

url = st.text_input("הכנס קישור:")
format_choice = st.radio("בחר פורמט:", ("mp3", "mp4"))

if st.button("הפעל הורדה"):
    if url and YT_COOKIES:
        with st.spinner('מוריד...'):
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tfile:
                    tfile.write(YT_COOKIES)
                    cookie_path = tfile.name

                # תרגום ההגדרות מה-YAML לקוד פייתון
                ydl_opts = {
                    'cookiefile': cookie_path,
                    'outtmpl': '%(title)s.%(ext)s',
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0',
                }

                if format_choice == "mp3":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    ydl_opts.update({
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'merge_output_format': 'mp4',
                    })

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if format_choice == "mp3":
                        filename = filename.rsplit('.', 1)[0] + '.mp3'

                with open(filename, "rb") as f:
                    st.download_button("לחץ להורדה", f, file_name=filename)
                
                os.unlink(cookie_path)
            except Exception as e:
                st.error(f"שגיאה: {e}")
