import streamlit as st
import requests

st.set_page_config(page_title="YouTube to GitHub", page_icon="🚀")
st.title("🚀 הורדה חזקה דרך GitHub Actions")

# שליפת נתונים מה-Secrets
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_USER = st.secrets.get("GITHUB_USER")
REPO_NAME = st.secrets.get("REPO_NAME")

url = st.text_input("הדבק קישור מיוטיוב:")
format_choice = st.selectbox("בחר פורמט:", ["mp3", "mp4"])

if st.button("הפעל הורדה בשרת"):
    if not url:
        st.error("נא להזין קישור.")
    elif not GITHUB_TOKEN:
        st.error("ה-Token לא מוגדר ב-Secrets.")
    else:
        with st.spinner('שולח פקודה ל-GitHub...'):
            # הכתובת להפעלת ה-YAML (download.yml)
            api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/actions/workflows/download.yml/dispatches"
            
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            data = {
                "ref": "main",
                "inputs": {
                    "yt_urls": url,
                    "format": format_choice
                }
            }
            
            response = requests.post(api_url, headers=headers, json=data)
            
            if response.status_code == 204:
                st.success("✅ הפקודה נשלחה! השרת של גיטהאב התחיל לעבוד.")
                st.balloons()
                st.info(f"תוכל לראות את ההתקדמות כאן: https://github.com/{GITHUB_USER}/{REPO_NAME}/actions")
            else:
                st.error(f"שגיאה: {response.status_code}")
                st.write(response.text)
