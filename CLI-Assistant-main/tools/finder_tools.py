import subprocess

def search_mac(query):
    try:
        # ניקוי השאילתה
        clean_query = query.replace('"', '').replace("'", "")
        
        # הרצה בלי -n (פשוט mdfind והשאילתה)
        # אנחנו נגביל את התוצאות בתוך הפייתון במקום בתוך הפקודה
        command = f'/usr/bin/mdfind "{clean_query}"'
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if not output:
            return f"No files found for '{clean_query}'."

        # לוקחים רק את 10 התוצאות הראשונות ידנית כדי לא להעמיס על ה-AI
        lines = output.splitlines()[:10]
        formatted_output = "\n".join(lines)
        
        return f"Found these paths:\n{formatted_output}"
    
    except Exception as e:
        return f"Search error: {str(e)}"