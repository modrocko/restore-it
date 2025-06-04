import os
import sys
import json
import subprocess
import session_utils

def overwrite_session(session_id, file_path):
    try:
        with open(file_path, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = []

    # Find existing session
    existing = next((s for s in sessions if s["id"] == session_id), None)
    if not existing:
        session_utils.notify("Session not found")
        sys.exit(1)

    # Remove old one
    sessions = [s for s in sessions if s["id"] != session_id]

    # Add updated session
    sessions.append({
        "id": session_id,
        "session": existing["session"],
        "windows": session_utils.get_browser_windows()
    })

    with open(file_path, "w") as f:
        json.dump(sessions, f, indent=2)

    session_utils.notify(f"Overwrote session {existing['session']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: overwrite_session.py <session_id>")
        sys.exit(1)

    session_id = sys.argv[1].strip()
    base_dir = os.environ["alfred_workflow_data"]
    sessions_path = os.path.join(base_dir, "sessions.json")

    overwrite_session(session_id, sessions_path)

if __name__ == "__main__":
    main()
