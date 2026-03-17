import streamlit as st
import requests
import time

st.set_page_config(page_title="YouTube to PC", page_icon="🚀")
st.title("🚀 הורדה ישירה למחשב (דרך GitHub)")

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_USER = st.secrets.get("GITHUB_USER")
REPO_NAME = st.secrets.get("REPO_NAME")

url = st.text_input("הדבק קישור מיוטיוב:")
format_choice = st.selectbox("בחר פורמט:", ["mp3", "mp4"])

if st.button("הפעל הורדה"):
    if url and GITHUB_TOKEN:
        with st.spinner('מפעיל את השרת בגיטהאב...'):
            api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/actions/workflows/download.yml/dispatches"
            headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
            data = {"ref": "main", "inputs": {"yt_urls": url, "format": format_choice}}
            
            response = requests.post(api_url, headers=headers, json=data)
            
            if response.status_code == 204:
                st.success("✅ הפעולה הופעלה! המתן כדקה לסיום.")
                st.info("כעת תוכל להשתמש בקובץ ה-BAT על שולחן העבודה, או להוריד מהקישור שיופיע כאן בקרוב.")
                
                # בדיקה אוטומטית אם ה-Release מוכן (למשך 2 דקות)
                placeholder = st.empty()
                for i in range(12): 
                    time.sleep(10)
                    placeholder.text(f"בודק אם הקובץ מוכן... ({ (i+1)*10 } שניות)")
                    
                    # ניסיון למצוא את ה-Release האחרון
                    rel_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/releases/latest"
                    rel_res = requests.get(rel_url, headers=headers)
                    if rel_res.status_code == 200:
                        assets = rel_res.json().get("assets", [])
                        if assets:
                            download_url = assets[0]["browser_download_url"]
                            placeholder.empty()
                            st.balloons()
                            st.markdown(f"### 🎉 הקובץ מוכן!")
                            st.link_button("⬇️ לחץ כאן להורדה ישירה", download_url)
                            break
            else:
                st.error(f"שגיאה: {response.status_code}")
