import os
import sys
import json
import subprocess

def get_session_by_id(uid, path):
    try:
        with open(path, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        return None
    return next((s for s in sessions if s.get("id") == uid), None)


def open_window_in_browser(bounds, urls, browser):
    if not urls:
        return

    if browser.lower() == "safari":
        script = f'''
        tell application "Safari"
            activate
            set newDoc to make new document
            set bounds of front window to {{{bounds["x"]}, {bounds["y"]}, {bounds["x"] + bounds["width"]}, {bounds["y"] + bounds["height"]}}}
            set URL of front document to "{urls[0]}"
        '''

        if len(urls) > 1:
            script += '\ntell front window'
            for url in urls[1:]:
                script += f'\nset newTab to make new tab at end of tabs'
                script += f'\nset URL of newTab to "{url}"'
            script += '\nend tell'

        script += '\nend tell'

    else:
        first_url = json.dumps(urls[0])
        script = f'''
        tell application "{browser}"
            activate
            set newWindow to make new window
            set bounds of newWindow to {{{bounds["x"]}, {bounds["y"]}, {bounds["x"] + bounds["width"]}, {bounds["y"] + bounds["height"]}}}
            tell newWindow
                set URL of active tab to {first_url}
        '''
        for url in urls[1:]:
            script += f'\nmake new tab with properties {{URL: {json.dumps(url)}}}'

        script += '\nend tell\nend tell'

    subprocess.run(["osascript", "-e", script])


def main():
    if len(sys.argv) < 2:
        print("No session id provided")
        sys.exit(1)

    session_id = sys.argv[1].strip()
    base_dir = os.environ["alfred_workflow_data"]
    browser = os.environ["browser"]
    session_path = os.path.join(base_dir, "sessions.json")

    session = get_session_by_id(session_id, session_path)
    if not session:
        print(f"No session found with id '{session_id}'")
        sys.exit(1)

    for i, window in enumerate(session["windows"], 1):
        bounds = window["bounds"]
        urls = [tab["url"] for tab in window["tabs"]]
        print(f"Opening window {i} with {len(urls)} tabs")
        open_window_in_browser(bounds, urls, browser)

    print("Session restore complete.")


if __name__ == "__main__":
    main()
