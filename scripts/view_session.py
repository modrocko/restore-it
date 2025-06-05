import sys
import os
import json

query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""

uid = os.environ["session_id"]
workflow_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(workflow_dir, "sessions.json")

with open(sessions_path, "r") as f:
    sessions = json.load(f)

session = next((s for s in sessions if s.get("id") == uid), None)

items = []

if session:
    for window in session["windows"]:
        for tab in window.get("tabs", []):
            title = tab.get("title", "")
            url = tab.get("url", "")
            if query in title.lower() or query in url.lower():
                items.append({
                    "title": title,
                    "subtitle": url,
                    "arg": url
                })

if not items:
    items.append({
        "title": "No matching tabs found" if query else "No tabs found",
        "subtitle": "Try typing a keyword" if query else "This session has no windows or tabs",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
