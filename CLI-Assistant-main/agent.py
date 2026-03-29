import os
import google.generativeai as genai
from rich.console import Console
from config import GEMINI_API_KEY, GENERATION_CONFIG, SAFETY_SETTINGS
from prompts import SYSTEM_INSTRUCTIONS
from tools.read_file import read_file
from tools.mac_tools import manage_note
from tools.speaker import say_text
from tools.write_file import write_file
from tools.finder_tools import search_mac
from tools.terminal_tools import run_command
from tools.web_search import search_web
from tools.reminders_tool import manage_reminder
import re

console = Console()

tools = {
    "read_file": read_file,
    "manage_note": manage_note,
    "say": say_text,
    "write_file": write_file,
    "search_mac": search_mac,
    "run_command": run_command,
    "search_web": search_web,
    "reminders": manage_reminder
}

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def setup_model():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite-preview",
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_INSTRUCTIONS
    )

def detect_tool_calls(text):
    # חיפוש תבנית הפתיחה של הכלי תוך שמירה על שמות המשתנים שלך
    match = re.search(r'\[(\w+)\]\(', text)
    
    if match:
        tool_name = match.group(1).lower() # שם הכלי
        start_index = match.end()          # תחילת הארגומנטים

        # תיקון קריטי: מוצא את הסוגר האחרון בטקסט (rfind) במקום הראשון (Regex)
        # זה מונע מצב שבו סוגריים בתוך content קוטעים את הקריאה
        end_index = text.rfind(')')
        
        if end_index != -1 and end_index > start_index:
            args_str = text[start_index:end_index] # כל מה שבתוך הסוגריים

            # פיצול לפי ||| כפי שהגדרת
            if "|||" in args_str:
                args = [arg.strip().strip('"').strip("'") for arg in args_str.split('|||')]
            else:
                args = [args_str.strip().strip('"').strip("'")]
                
            return tool_name, args
    
    return None, None

def main():
    model = setup_model()
    chat_session = model.start_chat(history=[])

    clear_screen()
    console.print("AI >> Welcome to the CLI Assistant!  Type 'exit' to quit.", style="bold cyan")

    while True:
        try:
            user_input = console.input("\n[bold_yellow]You >> [/bold_yellow]")

            if user_input.strip().lower() == "exit":
                console.print("\n[bold_cyan]AI >> Goodbye! Have a great day!", style="bold cyan")
                break

            console.print("[bold cyan]AI >> [/bold cyan]", end="")
            response = chat_session.send_message(user_input, stream=True)

            full_text = ""
            # לולאה ראשונה: רק אוספת ומדפיסה את הטקסט
            for chunk in response:
                if chunk.text:
                    console.print(chunk.text, style="bold cyan", end="")
                    full_text += chunk.text
            
            # --- כאן נגמרת הלולאה! הפעולות הבאות קורות רק פעם אחת בסוף התגובה ---
            
            response.resolve() # פותר את הבעיה שהתגובה לא מסתיימת

            tool_name, args = detect_tool_calls(full_text)

            # בדיקה אם נמצא כלי ואם הוא קיים במילון (באותיות קטנות)
            if tool_name and tool_name.lower() in tools:
                # הפעלה עם Unpacking (*) כדי לשלוח את כל הפרמטרים
                result = tools[tool_name.lower()](*args)
                
                console.print(f"\n[bold green]Tool Result >> {result}[/bold green]")

                # מעדכן את ה-AI בתוצאה כדי שיוכל להמשיך את השיחה
                chat_session.send_message(f"Tool result: {result}")

            console.print()

        except KeyboardInterrupt:
            console.print("\n[bold_red]AI >> Goodbye! Have a great day!", style="bold_red")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/bold red]")


          
if __name__ == "__main__":
      main()