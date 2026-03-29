import subprocess

def manage_note(action, title, content=""):
    title = title.replace('"', '\\"')
    content = content.replace('"', '\\"')

    if action == "read":
        applescript = f'tell application "Notes" to get body of note "{title}"'

    elif action == "write":
        applescript = f'''
        tell application "Notes"
           tell account 1 -- זה יבחר את החשבון הראשי שלך
            make new note at folder "Notes" with properties {{name:"{title}", body:"{content}"}}
        end tell
        show note "{title}"
    end tell
        '''

    else:
        return "Action not supported. Use 'read' or 'write'."
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            check=True
        )

        if action == "read":
            return result.stdout.strip()
        else:
            return f"Success: Note '{title}' created."
        
    except subprocess.CalledProcessError as e:
        return f"Error: Make sure the note exists and permissions are granted. ({e.stderr.strip()})"

