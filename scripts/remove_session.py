import os
import sys
import json
import subprocess

if len(sys.argv) < 2:
    print("No session name provided")
    sys.exit(1)

session_to_remove = sys.argv[1].strip().lower()
workflow_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(workflow_dir, "sessions.json")
title = os.environ.get("alfred_workflow_name", "Session Refresh")

try:
    with open(sessions_path, "r") as f:
        sessions = json.load(f)
except FileNotFoundError:
    sessions = []

# Filter out the session to remove
updated_sessions = [s for s in sessions if s.get("session", "").lower() != session_to_remove]

with open(sessions_path, "w") as f:
    json.dump(updated_sessions, f, indent=2)

# Show macOS notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed session \\"{session_to_remove}\\"" with title "{title}"'
])
