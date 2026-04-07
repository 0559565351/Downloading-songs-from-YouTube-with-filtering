import streamlit as st
from github import Github
import os

# כותרת האפליקציה
st.title("GitHub Repo Loader")

def load_github_repo():
    try:
        # שליבת הנתונים מתוך ה-Secrets של Streamlit
        # ודא שהגדרת אותם בלוח הבקרה של Streamlit Cloud תחת Settings -> Secrets
        github_token = st.secrets["GITHUB_TOKEN"]
        repo_name = st.secrets["REPO_NAME"]

        # התחברות ל-GitHub
        g = Github(github_token)
        
        # ניסיון גישה למאגר
        repo = g.get_repo(repo_name)
        
        st.success(f"התחברת בהצלחה למאגר: {repo.full_name}")
        return repo

    except KeyError:
        st.error("שגיאה: המפתחות GITHUB_TOKEN או REPO_NAME אינם מוגדרים ב-Secrets.")
    except Exception as e:
        st.error(f"אירעה שגיאת התחברות: {e}")
        st.info("טיפ: בדוק אם הטוקן פג תוקף או אם חסרות לו הרשאות מתאימות.")

# הרצת הפונקציה
repo_data = load_github_repo()

if repo_data:
    st.write(f"תיאור המאגר: {repo_data.description}")
