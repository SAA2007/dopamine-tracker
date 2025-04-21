import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# ==== AUTH ====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# ==== SHEET SETUP ====
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1_ggI55C66iNknQ6hM5XZInoEHK5bzceb-GArCNCcl_s/edit")

# ==== DEFAULT HEADERS & TAGS ====
log_headers = ["Timestamp", "Craving_Level", "Trigger", "Action_Taken", "Mood_After"]
tag_headers = ["Activity", "Trigger", "Action", "Mood"]
default_tags = {
    "Activity": ["YouTube", "Instagram", "Reddit", "Gaming"],
    "Trigger": ["Bored", "Lonely", "Stressed"],
    "Action": ["Scrolled", "Clicked", "Watched"],
    "Mood": ["Neutral", "Regret", "Happy"]
}

# ==== CHECK/CREATE Log SHEET ====
try:
    log_sheet = spreadsheet.worksheet("Log")
except gspread.exceptions.WorksheetNotFound:
    log_sheet = spreadsheet.add_worksheet(title="Log", rows="1000", cols="5")
    log_sheet.append_row(log_headers)

if log_sheet.row_values(1) != log_headers:
    log_sheet.update("A1:E1", [log_headers])

# ==== CHECK/CREATE Tags SHEET ====
try:
    tags_sheet = spreadsheet.worksheet("Tags")
except gspread.exceptions.WorksheetNotFound:
    tags_sheet = spreadsheet.add_worksheet(title="Tags", rows="1000", cols="4")
    tags_sheet.append_row(tag_headers)

current_headers = tags_sheet.row_values(1)
if current_headers != tag_headers:
    tags_sheet.update("A1:D1", [tag_headers])

# ==== Ensure each column has at least one value ====
for i, col in enumerate(tag_headers):
    col_vals = tags_sheet.col_values(i + 1)[1:]  # skip header
    if not col_vals:
        tags_sheet.update_cell(2, i + 1, default_tags[col][0])

print("✅ Sheet maintenance complete. Everything is tidy!")
