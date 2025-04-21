import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1_ggI55C66iNknQ6hM5XZInoEHK5bzceb-GArCNCcl_s").sheet1

# Streamlit App
st.title('Dopamine Tracker')
st.write("Track your dopamine activities and stay on top of your habits!")

# Dropdown for activity
activity = st.selectbox('What activity did you do?', ['Instagram', 'YouTube', 'Gaming', 'Work', 'Study'])

# Dropdown for mood/feeling
mood = st.selectbox('How do you feel?', ['Neutral', 'Good', 'Bad'])

# Submit form
if st.button('Log Activity'):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = [now, activity, mood]
    sheet.append_row(entry)
    st.success('✅ Activity logged successfully!')

# Display current log entries
st.subheader("Recent Entries")
entries = sheet.get_all_records()
st.write(entries)
