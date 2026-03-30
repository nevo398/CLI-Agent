import os
import re
import google.generativeai as genai
from bidi.algorithm import get_display
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
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

console = Console()

# --- פונקציות עזר ---

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def contains_hebrew(text: str) -> bool:
    return any('\u0590' <= ch <= '\u05FF' for ch in text)

def wrap_rtl(text: str) -> str:
    if not contains_hebrew(text):
        return text
    wrapped_lines = []
    for line in text.splitlines():
        if line.strip():
            wrapped_lines.append(get_display(line))
        else:
            wrapped_lines.append(line)
    return "\n".join(wrapped_lines)

# --- ניהול כלים ---

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

def detect_tool_calls(text):
    match = re.search(r'\[(\w+)\]\(', text)
    if match:
        tool_name = match.group(1).lower()
        start_index = match.end()
        end_index = text.rfind(')')
        if end_index != -1 and end_index > start_index:
            args_str = text[start_index:end_index]
            if "|||" in args_str:
                args = [arg.strip().strip('"').strip("'") for arg in args_str.split('|||')]
            else:
                args = [args_str.strip().strip('"').strip("'")]
            return tool_name, args
    return None, None

# --- עיצוב ממשק ---

def get_tips_panel() -> Panel:
    tips = Table.grid(padding=(0, 3))
    tips.add_column(ratio=1, style="bold white")
    tips.add_column(ratio=1, style="bright_blue")
    tips.add_row("[bold yellow]Quick command[/bold yellow]", "[bold green][read_file](\"./README.md\")[/bold green]")
    tips.add_row("[bold yellow]Shell preview[/bold yellow]", "[bold green][run_command](\"ls -la\")[/bold green]")
    tips.add_row("[bold yellow]Search idea[/bold yellow]", "[bold green][search_web](\"macOS terminal tips\")[/bold green]")
    return Panel(Align.left(tips), title="[bold magenta]Power Prompts[/bold magenta]", border_style="bright_magenta", padding=(1, 2), width=82)

# --- ליבת הסוכן ---

def setup_model():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite-preview",
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_INSTRUCTIONS
    )

def handle_ai_response(chat_session, input_text, is_tool_result=False):
    full_text = ""
    status_msg = "[bold yellow]Agent is thinking..." if not is_tool_result else "[bold yellow]Processing step..."
    
    with console.status(status_msg, spinner="dots"):
        response = chat_session.send_message(input_text, stream=True)
        
        with Live(Panel(Text(""), title="[bold magenta]AI Reasoning[/bold magenta]", border_style="bright_magenta", width=82), 
                  console=console, refresh_per_second=10, transient=True) as live:
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    display_text = Text(wrap_rtl(full_text), style="bold cyan")
                    display_text.justify = "right" if contains_hebrew(full_text) else "left"
                    live.update(Panel(display_text, title="[bold magenta]Streaming Step Output[/bold magenta]", border_style="bright_magenta", width=82))
        response.resolve()

    console.rule("[bold magenta]AI Analysis[/bold magenta]", style="bright_blue")
    rendered = Markdown(wrap_rtl(full_text)) if contains_hebrew(full_text) else Markdown(full_text)
    alignment = Align.right(rendered) if contains_hebrew(full_text) else Align.left(rendered)
    console.print(Panel(alignment, title="CLI-Assistant", border_style="cyan", padding=(1, 2), width=82))
    
    return full_text

def main():
    model = setup_model()
    chat_session = model.start_chat(history=[])

    clear_screen()
    console.rule("[bold bright_magenta]CLI-Assistant v3.1 (Autonomous Mode)[/bold bright_magenta]", style="bright_blue")
    console.print(get_tips_panel())

    while True:
        try:
            user_input = console.input("\n[bold bright_white on dark_blue] You >> [/bold bright_white on dark_blue] ")

            if user_input.strip().lower() in ["exit", "quit"]:
                console.print(Panel("[bold cyan]Goodbye![/bold cyan]", border_style="bright_blue"))
                break

            current_prompt = user_input
            
            # לולאת האוטונומיה המטורפת - עד 5 צעדים ברצף
            for _ in range(5):
                ai_response = handle_ai_response(chat_session, current_prompt)
                tool_name, args = detect_tool_calls(ai_response)
                
                if tool_name and tool_name in tools:
                    # כאן השלב הקריטי לאבטחה:
                    # אם זה run_command, אנחנו לא שמים status כדי שהאישור [y/n] יעבוד!
                    if tool_name == "run_command":
                        try:
                            result = tools[tool_name](*args)
                        except Exception as e:
                            result = f"Error: {str(e)}"
                    else:
                        # לכל שאר הכלים (חיפוש, קריאה וכו') נשאיר את הספינר
                        with console.status(f"[bold green]Executing {tool_name}...", spinner="bouncingBar"):
                            try:
                                result = tools[tool_name](*args)
                            except Exception as e:
                                result = f"Error: {str(e)}"

                    # הצגת פלט הכלי ב-Panel
                    tool_display = Text(wrap_rtl(result) if contains_hebrew(result) else result, style="bright_white")
                    if contains_hebrew(result): tool_display.justify = "right"
                    console.print(Panel(tool_display, title=f"[bold green]Tool Result: {tool_name}[/bold green]", border_style="green", padding=(1, 2), width=82))
                    
                    # מעדכן את הפרומפט לתוצאת הכלי וממשיך בלולאה אוטומטית
                    current_prompt = f"Tool result: {result}"
                else:
                    # אין יותר כלים להריץ - עוצר ומחכה למשתמש
                    break

        except KeyboardInterrupt:
            console.print(Panel("[bold red]Stopped by user.[/bold red]", border_style="red"))
            break
        except Exception as e:
            console.print(f"\n[bold red]System Error: {e}[/bold red]")

if __name__ == "__main__":
    main()
