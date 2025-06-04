import sys
import os
import json

query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
workflow_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(workflow_dir, "sessions.json")

if not query:
    items = [{
        "title": "Specify session",
        "subtitle": "Type or select a session",
        "valid": False,
        "icon": { "path": "info.png" }
    }]
else:
    items = []


# Load existing session names
session_names = []
if os.path.exists(sessions_path):
    with open(sessions_path, "r") as f:
        try:
            data = json.load(f)
            session_names = sorted(set(s["session"] for s in data if s.get("session")))
        except:
            pass

# Suggest new session name
if query and query not in session_names:
    items.append({
        "title": f"'{query}'",
        "subtitle": "↵ Save new session",
        "arg": query,
        "variables": {
            "operation": "create_session"
        }
    })

# Show existing matches
for name in session_names:
    if query and query not in name.lower():
        continue
    items.append({
        "title": name,
        "subtitle": "↵ Overwrite existing session",
        "arg": name,
        "variables": {
            "operation": "overwrite_session"
        }
    })

# Default fallback
if not items:
    items = [{
        "title": "Specify session name",
        "subtitle": "Type a session name to save",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({ "items": items }))
