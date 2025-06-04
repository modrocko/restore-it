import os
import sys
import json

# Read query string
query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""

# Path to sessions.json in workflow data root
base_dir = os.environ["alfred_workflow_data"]
sessions_file = os.path.join(base_dir, "sessions.json")

# Load sessions
try:
    with open(sessions_file, "r") as f:
        sessions = json.load(f)
except FileNotFoundError:
    sessions = []

# Build Alfred Script Filter output
items = []
for session in sessions:
    name = session["session"]
    if query and query not in name.lower():
        continue

    uid = session.get("id")
    items.append({
        "title": name,
        "arg": uid,
        "subtitle": "↵ Restore session ∙ ⌘ Overwrite ∙ ⌥ Rename ∙ ⌃ Remove ∙ ⇧ View",
        "mods": {
            "cmd": {
                "arg": uid,
                "subtitle": "⌘ Overwrite this session with current windows & tabs"
            },
            "alt": {
                "arg": name,
                "subtitle": "⌥ Rename this session",
                "variables": {
                    "current_session_name": name,
                     "session_id": uid
                }
            },
            "ctrl": {
                "arg": uid,
                "subtitle": "⌃ Remove this session"
            },
            "shift": {
                "arg": uid,
                "subtitle": "⇧ View session windows & urls"
            }
        }
    })

    # Fallback if nothing matched
if not items:
    items = [{
        "title": "No matches found",
        "subtitle": "Try saving a session first",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({"items": items}))
