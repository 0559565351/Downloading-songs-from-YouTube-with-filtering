import streamlit as st
import yt_dlp
import os
import tempfile

st.title("🎵 מוריד שירים - מצב עמידות גבוהה")

YT_COOKIES = st.secrets.get("youtube_cookies")

url = st.text_input("הכנס קישור:")
format_choice = st.radio("בחר פורמט:", ("MP3", "MP4"))

if st.button("הורד"):
    if url and YT_COOKIES:
        with st.spinner('מנסה פורמטים שונים...'):
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tfile:
                    tfile.write(YT_COOKIES)
                    cookie_path = tfile.name

                # הגדרת סדר עדיפויות: אם הכי טוב נכשל, תנסה את הבא בתור
                if format_choice == "MP3":
                    # מנסה להוריד אודיו איכותי, ואם לא - כל אודיו שזמין
                    format_str = 'bestaudio/best'
                else:
                    # מנסה וידאו משולב, ואם לא - כל פורמט יחיד שכולל וידאו
                    format_str = 'bestvideo+bestaudio/best'

                ydl_opts = {
                    'format': format_str,
                    'cookiefile': cookie_path,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'nocheckcertificate': True,
                    'ignoreerrors': True,  # דילוג על שגיאות בפורמטים מסוימים וניסיון של הבא בתור
                    'outtmpl': 'downloaded_file.%(ext)s',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # חילוץ המידע וניסיון הורדה
                    info = ydl.extract_info(url, download=True)
                    if info is None:
                        st.error("לא נמצא פורמט זמין להורדה. נסה קישור אחר.")
                    else:
                        filename = ydl.prepare_filename(info)
                        
                        with open(filename, "rb") as f:
                            st.download_button("הקובץ מוכן - לחץ כאן", f, file_name=filename)
                
                os.unlink(cookie_path)
                
            except Exception as e:
                st.error(f"שגיאה סופית: {e}")
    else:
        st.error("וודא שהזנת קישור ושהעוגיות מוגדרות ב-Secrets.")
