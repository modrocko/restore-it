import os
import sys
import json
import subprocess

def notify(message):
    title = os.environ["alfred_workflow_name"]
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ])

def get_browser_windows():
    browser = os.environ["browser"]

    script = f'''
    on join_json_items(the_list)
        if (count of the_list) is 0 then return "[]"
        set AppleScript's text item delimiters to ","
        set joined to the_list as text
        set AppleScript's text item delimiters to ""
        return "[" & joined & "]"
    end join_json_items

    if application "{browser}" is not running then
        return "[]"
    end if

    tell application "{browser}"
        set window_jsons to {{}}

        repeat with w in windows
            set b to bounds of w
            set x to item 1 of b
            set y to item 2 of b
            set width to (item 3 of b) - x
            set height to (item 4 of b) - y

            set tab_jsons to {{}}
            set tab_count to count of tabs of w

            repeat with i from 1 to tab_count
                set the_tab to tab i of w
                set the_title to title of the_tab
                set the_url to URL of the_tab

                set esc_title to do shell script "python3 -c \\"import json; print(json.dumps(" & quoted form of the_title & "))\\""
                set esc_url to do shell script "python3 -c \\"import json; print(json.dumps(" & quoted form of the_url & "))\\""

                set end of tab_jsons to "{{\\\"title\\\": " & esc_title & ", \\\"url\\\": " & esc_url & "}}"
            end repeat

            set tabs_str to my join_json_items(tab_jsons)
            set bounds_str to "{{\\\"x\\\": " & x & ", \\\"y\\\": " & y & ", \\\"width\\\": " & width & ", \\\"height\\\": " & height & "}}"
            set window_json to "{{\\\"bounds\\\": " & bounds_str & ", \\\"tabs\\\": " & tabs_str & "}}"
            set end of window_jsons to window_json
        end repeat

        return my join_json_items(window_jsons)
    end tell
    '''

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

    if result.returncode != 0:
        print("AppleScript error:", result.stderr)
        sys.exit(1)

    try:
        return json.loads(result.stdout.strip())
    except Exception as e:
        print("JSON parse error:", e)
        print("Raw output:", result.stdout)
        sys.exit(1)

def save_session(session_name, windows, file_path):
    try:
        with open(file_path, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = []

    sessions = [s for s in sessions if s["session"] != session_name]
    sessions.append({"session": session_name, "windows": windows})

    with open(file_path, "w") as f:
        json.dump(sessions, f, indent=2)

def main():
    if len(sys.argv) < 2:
        print("Usage: save_session.py <session_name>")
        sys.exit(1)

    session_name = sys.argv[1].strip()
    base_dir = os.environ["alfred_workflow_data"]
    os.makedirs(base_dir, exist_ok=True)
    sessions_path = os.path.join(base_dir, "sessions.json")
    title = os.environ["alfred_workflow_name"]

    windows = get_browser_windows()
    save_session(session_name, windows, sessions_path)

    notify(f"Saved session \"{session_name}\"")

if __name__ == "__main__":
    main()
