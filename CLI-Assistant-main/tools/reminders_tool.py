import subprocess

def manage_reminder(action, title, description=""):
    """
    Manages Mac Reminders: creates or lists reminders.
    action: "create" or "list"
    """
    if action == "create":
        # AppleScript ליצירת תזכורת חדשה בתוך רשימת ברירת המחדל
        script = f'tell application "Reminders" to make new reminder at end of default list with properties {{name:"{title}", body:"{description}"}}'
        try:
            subprocess.run(["osascript", "-e", script], check=True)
            return f"✅ Reminder '{title}' created successfully!"
        except Exception as e:
            return f"❌ Error creating reminder: {str(e)}"
            
    elif action == "list":
        # AppleScript לקריאת שמות התזכורות שלא הושלמו
        script = 'tell application "Reminders" to get name of every reminder whose completed is false'
        try:
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            reminders_raw = result.stdout.strip()
            
            if not reminders_raw or reminders_raw == "":
                return "📭 No active reminders found."
            
            # הפיכת הפלט לרשימה קריאה
            reminders_list = reminders_raw.split(", ")
            formatted_reminders = "\n".join([f"- {r}" for r in reminders_list])
            
            return f"📝 Your active reminders:\n{formatted_reminders}"
        except Exception as e:
            return f"❌ Error listing reminders: {str(e)}"