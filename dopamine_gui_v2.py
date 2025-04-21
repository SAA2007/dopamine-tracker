import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import csv
import os
import json
from collections import Counter

# 📁 Setup paths
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
csv_path = os.path.join(desktop, "dopamine_log.csv")
dropdown_path = os.path.join(desktop, "dropdown_data.json")
summary_path = os.path.join(desktop, "dopamine_summary.txt")

# 🔁 Load or create dropdown data
default_data = {
    "triggers": ["Instagram", "YouTube", "Boredom", "Stress", "H-content", "Gaming Urge", "Loneliness"],
    "actions": ["Scrolled", "Closed App", "Redirected to Coding", "Went for Walk", "Read Quran", "Watched Dev Video"],
    "moods": ["Clear", "Tired", "Focused", "Guilty", "Neutral", "Proud"]
}

if not os.path.exists(dropdown_path):
    with open(dropdown_path, 'w') as f:
        json.dump(default_data, f)

with open(dropdown_path, 'r') as f:
    dropdown_data = json.load(f)

# 🧾 Ensure CSV exists
if not os.path.exists(csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Craving_Level", "Trigger", "Action_Taken", "Mood_After"])

# 💾 Save entry to CSV
def save_entry():
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        craving = craving_var.get()
        trigger = trigger_var.get()
        action = action_var.get()
        mood = mood_var.get()

        if not (craving and trigger and action and mood):
            messagebox.showwarning("Missing Data", "Please fill out all fields.")
            return

        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, craving, trigger, action, mood])

        messagebox.showinfo("Saved", "Log entry saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save log:\n{e}")

# ➕ Add dropdown options and persist
def add_option(field_name, dropdown, label):
    new_value = simpledialog.askstring(f"Add {label}", f"Enter new {label}:")
    if new_value:
        if new_value not in dropdown_data[field_name]:
            dropdown_data[field_name].append(new_value)
            dropdown['values'] = dropdown_data[field_name]
            with open(dropdown_path, 'w') as f:
                json.dump(dropdown_data, f)
            messagebox.showinfo("Added", f"{label} '{new_value}' added!")
        else:
            messagebox.showinfo("Exists", f"{label} already exists.")

# 📊 Generate summary safely
def generate_summary():
    try:
        if not os.path.exists(csv_path):
            messagebox.showwarning("No Data", "No log file found.")
            return

        with open(csv_path, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            data = [row for row in reader if len(row) == 5]

        if not data:
            messagebox.showinfo("Empty", "No valid logs to summarize.")
            return

        cravings = [int(row[1]) for row in data if row[1].isdigit()]
        triggers = [row[2] for row in data]
        actions = [row[3] for row in data]
        moods = [row[4] for row in data]

        summary = f"""Dopamine Tracker Summary ({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

Total Logs: {len(data)}
Average Craving Level: {sum(cravings)/len(cravings):.2f}
Most Common Trigger: {Counter(triggers).most_common(1)[0][0]}
Most Common Action: {Counter(actions).most_common(1)[0][0]}
Most Common Mood: {Counter(moods).most_common(1)[0][0]}
"""

        with open(summary_path, "w") as f:
            f.write(summary)

        messagebox.showinfo("Summary Ready", f"Summary saved to:\n{summary_path}")
    except Exception as e:
        messagebox.showerror("Summary Error", f"Something went wrong:\n{e}")

# 🧠 GUI layout
root = tk.Tk()
root.title("🧠 Dopamine Tracker Deluxe")
root.geometry("470x450")
root.resizable(False, False)

craving_var = tk.StringVar()
trigger_var = tk.StringVar()
action_var = tk.StringVar()
mood_var = tk.StringVar()

# Craving
ttk.Label(root, text="Craving Level (1-10):").pack(pady=(10, 0))
ttk.Combobox(root, textvariable=craving_var, values=[str(i) for i in range(1, 11)], state="readonly").pack()

# Trigger
ttk.Label(root, text="Trigger:").pack(pady=(10, 0))
trigger_dd = ttk.Combobox(root, textvariable=trigger_var, values=dropdown_data["triggers"], state="readonly")
trigger_dd.pack()
ttk.Button(root, text="➕ Add Trigger", command=lambda: add_option("triggers", trigger_dd, "Trigger")).pack()

# Action
ttk.Label(root, text="Action Taken:").pack(pady=(10, 0))
action_dd = ttk.Combobox(root, textvariable=action_var, values=dropdown_data["actions"], state="readonly")
action_dd.pack()
ttk.Button(root, text="➕ Add Action", command=lambda: add_option("actions", action_dd, "Action")).pack()

# Mood
ttk.Label(root, text="Mood After:").pack(pady=(10, 0))
mood_dd = ttk.Combobox(root, textvariable=mood_var, values=dropdown_data["moods"], state="readonly")
mood_dd.pack()
ttk.Button(root, text="➕ Add Mood", command=lambda: add_option("moods", mood_dd, "Mood")).pack()

# Save & Summary buttons
ttk.Button(root, text="💾 Save Log", command=save_entry).pack(pady=(15, 5))
ttk.Button(root, text="📊 Generate Summary", command=generate_summary).pack()

root.mainloop()
