import streamlit as st
from github import Github
from github import Auth
import os

# כותרת האפליקציה
st.title("🎵 GitHub Repo Loader")

def load_github_repo():
    try:
        # שליפת הנתונים מתוך ה-Secrets של Streamlit
        # ודא שהגדרת אותם ב-Settings -> Secrets בלוח הבקרה
        if "GITHUB_TOKEN" not in st.secrets or "REPO_NAME" not in st.secrets:
            st.error("שגיאה: המפתחות GITHUB_TOKEN או REPO_NAME אינם מוגדרים ב-Secrets.")
            return None

        github_token = st.secrets["GITHUB_TOKEN"]
        repo_name = st.secrets["REPO_NAME"]

        # התחברות ל-GitHub בצורה המעודכנת (מונע את ה-DeprecationWarning)
        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        
        # ניסיון גישה למאגר
        repo = g.get_repo(repo_name)
        
        st.success(f"התחברת בהצלחה למאגר: {repo.full_name}")
        return repo

    except Exception as e:
        repo_name = st.secrets.get("REPO_NAME", "unknown")  # ✅ תיקון
        if "401" in str(e):
            st.error("שגיאת אימות (401): הטוקן של GitHub אינו תקין או פג תוקף.")
        elif "404" in str(e):
            st.error(f"שגיאה (404): המאגר '{repo_name}' לא נמצא.")
        else:
            st.error(f"אירעה שגיאת התחברות: {e}")
        st.info("בדוק את הגדרות ה-Secrets ואת תוקף הטוקן ב-GitHub.")
        return None

# הרצת הפונקציה
repo_data = load_github_repo()

if repo_data:
    st.write(f"**תיאור המאגר:** {repo_data.description}")
    # כאן תוכל להמשיך עם הלוגיקה של הורדת השירים
