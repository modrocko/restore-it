import sys
import os
import json

# Read session ID from modifier var
uid = os.environ.get("session_id", "").strip()
workflow_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(workflow_dir, "sessions.json")

# Load sessions
try:
    with open(sessions_path, "r") as f:
        sessions = json.load(f)
except:
    sessions = []

# Find session by id
session = next((s for s in sessions if s.get("id") == uid), None)

items = []

if session:
    for w_index, window in enumerate(session["windows"], 1):
        bounds = window["bounds"]
        tabs = window.get("tabs", [])
        for t_index, tab in enumerate(tabs, 1):
            url = tab.get("url")
            title = tab.get("title") or url
            subtitle = f"Window {w_index} • Tab {t_index} • {url}"
            items.append({
                "title": title,
                "subtitle": subtitle,
                "arg": tab.get("url"),
                "valid":False
            })

if not items:
    items.append({
        "title": "No tabs found",
        "subtitle": "This session has no windows or tabs",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
