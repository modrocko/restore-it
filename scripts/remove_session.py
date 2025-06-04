import os
import sys
import json
import subprocess

if len(sys.argv) < 2:
    print("No session ID provided")
    sys.exit(1)

session_id = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(workflow_dir, "sessions.json")
title = os.environ["alfred_workflow_name"]

try:
    with open(sessions_path, "r") as f:
        sessions = json.load(f)
except FileNotFoundError:
    sessions = []

# Get session name before removal (for notification)
session = next((s for s in sessions if s.get("id") == session_id), None)
session_name = session.get("session") if session else "Unknown"

# Remove session by ID
updated_sessions = [s for s in sessions if s.get("id") != session_id]

with open(sessions_path, "w") as f:
    json.dump(updated_sessions, f, indent=2)

# Show macOS notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed session \\"{session_name}\\"" with title "{title}"'
])
