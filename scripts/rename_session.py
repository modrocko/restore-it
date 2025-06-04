import os
import sys
import json
import session_utils

def rename_session(session_id, new_name, file_path):
    try:
        with open(file_path, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        session_utils.notify("No sessions found")
        sys.exit(1)

    updated = False
    for session in sessions:
        if session.get("id") == session_id:
            session["session"] = new_name
            updated = True
            break

    if not updated:
        session_utils.notify("Session not found")
        sys.exit(1)

    with open(file_path, "w") as f:
        json.dump(sessions, f, indent=2)

    session_utils.notify(f"Renamed session to: {new_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: rename_session.py <new_name>")
        sys.exit(1)

    new_name = sys.argv[1].strip()
    session_id = os.environ.get("session_id")
    current_name = os.environ.get("current_session_name")

    if not session_id:
        session_utils.notify("Missing session ID")
        sys.exit(1)

    base_dir = os.environ["alfred_workflow_data"]
    sessions_path = os.path.join(base_dir, "sessions.json")

    rename_session(session_id, new_name, sessions_path)

if __name__ == "__main__":
    main()
