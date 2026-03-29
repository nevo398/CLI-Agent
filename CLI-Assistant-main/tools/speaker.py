import os

def say_text(text):
    try:
        os.system(f'say "{text}"')
        return f"Successfully said: {text}"
    except Exception as e:
        return f"Error in speaking: {e}"