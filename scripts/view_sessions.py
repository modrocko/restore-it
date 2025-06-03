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
    items.append({
        "title": name,
        "arg": name,
        "subtitle": "↵ Restore session ∙ ⌘ Overwrite ∙ ⌥ Rename ∙ ⌃ Remove ∙ ⇧ View",
        "mods": {
            "cmd": {
                "arg": name,
                "subtitle": "⌘ Overwrite this session with current windows & tabs"
            },
            "alt": {
                "subtitle": "⌥ Rename this session",
                "variables": {
                    "session_name": name
                }
            },
            "ctrl": {
                "arg": name,
                "subtitle": "⌃ Remove this session"
            },
            "shift": {
                "arg": name,
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
