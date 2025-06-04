import os
import sys
import session_utils

if len(sys.argv) < 2:
    print("Usage: create_session.py <session_name>")
    sys.exit(1)

session_name = sys.argv[1].strip()
base_dir = os.environ["alfred_workflow_data"]
sessions_path = os.path.join(base_dir, "sessions.json")

windows = session_utils.get_browser_windows()
session_utils.save_session(session_name, windows, sessions_path)

session_utils.notify(f"Saved session {session_name}")
