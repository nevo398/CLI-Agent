import subprocess
import shlex

DUNGEROUS_COMMANDS = [
    "rm -rf", "sudo", "format", "mkfs", "dd",
    "chmod -R 777", "chown", "shutdown", "reboot"
]

def run_command(command):
    # הפיכת הפקודה לרשימת מילים לבדיקה מדויקת
    command_lower = command.lower()
    command_words = command_lower.split()
    
    for dangerous in DUNGEROUS_COMMANDS:
        # אם הפקודה האסורה היא מילה בודדת (כמו dd או sudo)
        if " " not in dangerous:
            if dangerous in command_words:
                return f"❌ SECURITY ALERT: The command '{command}' is blocked for safty reasons."
        # אם הפקודה האסורה מכילה רווחים (כמו rm -rf)
        else:
            if dangerous in command_lower:
                return f"❌ SECURITY ALERT: The command '{command}' is blocked for safty reasons."
        
    print(f"\n⚠️ AI wants to excute: {command}")
    confirm = input("Confirm execution? (y/n): ")

    if confirm.lower() != 'y':
        return "❌ Command execution cancelled by user."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return f"✅ Command executed successfully:\n{result.stdout}"
        else:
            return f"❌ Command failed (code {result.returncode}):\n{result.stderr}"
    
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"