from datetime import datetime
import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Create or open sheets
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1_ggI55C66iNknQ6hM5XZInoEHK5bzceb-GArCNCcl_s/edit")
log_sheet = sheet.worksheet("Log") if "Log" in [ws.title for ws in sheet.worksheets()] else sheet.add_worksheet(title="Log", rows="1000", cols="10")
tags_sheet = sheet.worksheet("Tags") if "Tags" in [ws.title for ws in sheet.worksheets()] else sheet.add_worksheet(title="Tags", rows="100", cols="5")

# --- Load Tags ---
def get_dropdown_tags():
    try:
        data = tags_sheet.get_all_records()
        activities = sorted(list(set([row["Activity"] for row in data if row["Activity"]])))
        triggers = sorted(list(set([row["Trigger"] for row in data if row["Trigger"]])))
        actions = sorted(list(set([row["Action"] for row in data if row["Action"]])))
        moods = sorted(list(set([row["Mood"] for row in data if row["Mood"]])))
        return activities, triggers, actions, moods
    except Exception as e:
        st.error("Error loading tags: " + str(e))
        return [], [], [], []

# --- Save Entry ---
def log_entry(activity, trigger, action, mood):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, activity, trigger, action, mood]
    log_sheet.append_row(row)

# --- Save New Tags ---
def add_new_tag(activity, trigger, action, mood):
    tags_sheet.append_row([activity, trigger, action, mood])

# --- UI Layout ---
st.set_page_config(page_title="Dopamine Tracker", layout="centered")
st.title("🧠 Dopamine Tracker")
tab1, tab2, tab3 = st.tabs(["Log Entry", "View Summary", "Add Tags"])

# --- Tab 1: Logging ---
with tab1:
    st.subheader("Track your dopamine activities and stay on top of your habits!")
    activities, triggers, actions, moods = get_dropdown_tags()

    activity = st.selectbox("What activity did you do?", activities)
    trigger = st.selectbox("How do you feel?", triggers)
    action = st.selectbox("What action did you take?", actions)
    mood = st.selectbox("How do you feel after?", moods)

    if st.button("✅ Log Activity"):
        log_entry(activity, trigger, action, mood)
        st.success("Activity logged successfully!")

# --- Tab 2: Summary ---
with tab2:
    st.subheader("📊 Summary Report")
    try:
        data = pd.DataFrame(log_sheet.get_all_records())
        if not data.empty:
            st.write("Recent Entries", data.tail(10))
            activity_counts = data["Activity"].value_counts().reset_index()
            activity_counts.columns = ["Activity", "Count"]
            st.bar_chart(activity_counts.set_index("Activity"))
        else:
            st.info("No data yet.")
    except Exception as e:
        st.error("Error loading summary: " + str(e))

# --- Tab 3: Add Tags ---
with tab3:
    st.subheader("➕ Add Custom Dropdown Tags")
    new_activity = st.text_input("New Activity")
    new_trigger = st.text_input("New Trigger")
    new_action = st.text_input("New Action")
    new_mood = st.text_input("New Mood")

    if st.button("💾 Save Tags"):
        add_new_tag(new_activity, new_trigger, new_action, new_mood)
        st.success("New tags saved! Refresh the page to see them in dropdowns.")

