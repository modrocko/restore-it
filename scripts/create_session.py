import os
import sys
import session_utils

# Require a session name
if len(sys.argv) < 2 or not sys.argv[1].strip():
    print("Usage: create_session.py <session_name>")
    sys.exit(1)

session_name = sys.argv[1].strip()

# Alfred data folder from env (no defaults)
base_dir = os.environ["alfred_workflow_data"]

# Ensure the folder exists before writing
os.makedirs(base_dir, exist_ok=True)

sessions_path = os.path.join(base_dir, "sessions.json")

# Capture windows & save
windows = session_utils.get_browser_windows()
session_utils.save_session(session_name, windows, sessions_path)

# Notify success
session_utils.notify(f'Saved session "{session_name}"')
