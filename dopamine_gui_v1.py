import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import csv
import os

# Persistent storage path - user Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "dopamine_log.csv")

# Ensure file and folder exist
if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Craving_Level", "Trigger", "Action_Taken", "Mood_After"])

# Save a log entry
def save_entry():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    craving_level = craving_var.get()
    trigger = trigger_var.get()
    action = action_var.get()
    mood = mood_var.get()

    if not (craving_level and trigger and action and mood):
        messagebox.showwarning("Missing Data", "Please select all fields.")
        return

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, craving_level, trigger, action, mood])

    messagebox.showinfo("Saved", "Log entry saved to Desktop!")
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("🧠 Dopamine Tracker")
root.geometry("400x300")
root.resizable(False, False)

ttk.Label(root, text="Craving Level (1-10):").pack(pady=(10, 0))
craving_var = tk.StringVar()
ttk.Combobox(root, textvariable=craving_var, values=[str(i) for i in range(1, 11)], state="readonly").pack()

ttk.Label(root, text="Trigger:").pack(pady=(10, 0))
trigger_var = tk.StringVar()
ttk.Combobox(root, textvariable=trigger_var, values=[
    "Insta", "YouTube", "Boredom", "Stress", "H-content", "Gaming Urge", "Loneliness"
], state="readonly").pack()

ttk.Label(root, text="Action Taken:").pack(pady=(10, 0))
action_var = tk.StringVar()
ttk.Combobox(root, textvariable=action_var, values=[
    "Scrolled", "Closed App", "Redirected to Coding", "Went for Walk", "Read Quran", "Watched Dev Video"
], state="readonly").pack()

ttk.Label(root, text="Mood After:").pack(pady=(10, 0))
mood_var = tk.StringVar()
ttk.Combobox(root, textvariable=mood_var, values=[
    "Clear", "Tired", "Focused", "Guilty", "Neutral", "Proud"
], state="readonly").pack()

ttk.Button(root, text="Save Log", command=save_entry).pack(pady=20)

root.mainloop()
