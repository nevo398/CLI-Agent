import os

def write_file(file_path, content):
    try:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: File '{file_path}' has been written."
    except Exception as e:
        return f"Error writing file {e}"