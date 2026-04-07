import streamlit as st
from github import Github
from github import Auth
import time

st.set_page_config(page_title="YouTube Downloader via GitHub", page_icon="🎵")

st.title("🎵 YouTube Downloader (GitHub Actions)")

# פונקציית התחברות
def get_repo():
    try:
        if "GITHUB_TOKEN" not in st.secrets or "REPO_NAME" not in st.secrets:
            st.error("שגיאה: המפתחות GITHUB_TOKEN או REPO_NAME אינם מוגדרים ב-Secrets.")
            return None

        auth = Auth.Token(st.secrets["GITHUB_TOKEN"])
        g = Github(auth=auth)
        return g.get_repo(st.secrets["REPO_NAME"])
    except Exception as e:
        st.error(f"שגיאת התחברות: {e}")
        return None

repo = get_repo()

if repo:
    st.success(f"מחובר למאגר: {repo.full_name}")
    
    # ממשק המשתמש
    urls = st.text_area("הדבק קישורים מיוטיוב (מופרדים בפסיקים או בשורות חדשות):", placeholder="https://youtube.com/watch?v=..., https://youtube.com/watch?v=...")
    format_type = st.radio("בחר פורמט:", ("mp3", "mp4"))
    
    if st.button("🚀 התחל הורדה"):
        if not urls:
            st.warning("נא להזין לפחות קישור אחד.")
        else:
            try:
                # ניקוי הקישורים (הפיכת שורות חדשות לפסיקים)
                clean_urls = ",".join([url.strip() for url in urls.split("\n") if url.strip()])
                
                # מציאת ה-Workflow לפי שם הקובץ (ודא ששם הקובץ ב-GitHub הוא main.yml או שנה כאן)
                # אפשר גם לפי השם שכתוב בתוך ה-YAML: "Smart Download: Single MP3 or ZIP"
                workflow = repo.get_workflow("main.yml") # <--- שנה את זה לשם קובץ ה-YAML שלך ב-GitHub!
                
                # הפעלת ה-Workflow
                workflow.create_dispatch(
                    ref="main", # או ה-Branch שבו נמצא הקוד
                    inputs={
                        "yt_urls": clean_urls,
                        "format": format_type
                    }
                )
                
                st.balloons()
                st.success("✅ הפעולה נשלחה בהצלחה ל-GitHub Actions!")
                st.info("התהליך לוקח כ-1-3 דקות. בסיום, הקובץ יופיע בטאב ה-Releases במאגר שלך.")
                
                # קישור ישיר ל-Releases
                st.markdown(f"[לחץ כאן לצפייה בתוצאות במאגר](https://github.com/{st.secrets['REPO_NAME']}/releases)")
                
            except Exception as e:
                st.error(f"אירעה שגיאה בהפעלת ה-Workflow: {e}")
                st.info("טיפ: וודא ששם קובץ ה-YAML בקוד תואם לשם ב-GitHub (למשל main.yml).")
