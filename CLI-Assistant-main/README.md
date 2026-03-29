# CLI Assistant

A small interactive command-line AI assistant (Python) that uses Google Gemini via the `google-generativeai` client.

Overview
:
This repository contains a compact interactive CLI assistant implemented in `agent.py`. The assistant communicates with Google Gemini through the `google.generativeai` Python client and prints interactive responses to the terminal using `rich`.

What this project does
- Starts an interactive REPL-like loop (no CLI arguments) where you type messages and receive AI responses.
- Uses environment variable `GEMINI_API_KEY` (loaded from a `.env` file when present) to authenticate to the Gemini API.
- Prints outputs in Hebrew and English and preserves a short in-memory conversation history for the session.

Key files
- `agent.py`: main interactive script (entrypoint)
- `LICENSE`: project license (MIT)

Requirements
- Python 3.8 or newer
- A Google Gemini API key stored in the `GEMINI_API_KEY` environment variable or in a `.env` file

Python dependencies
- google-generativeai
- python-dotenv
- rich

Install
1. Clone the repository and change into it:

```bash
git clone https://github.com/raziel-star/CLI-Assistant
cd CLI-Assistant
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

3. Install the packages used by `agent.py`:

```bash
pip install google-generativeai python-dotenv rich
# If `print_arabic` is a separate package, install it too, or ensure the module is present locally
```

Authentication / configuration
- Create a `.env` file in the repository root (or export the variable in your shell) with your Gemini API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Usage
- Run the assistant:

```bash
python agent.py
```

The script starts an interactive loop; type a message and press Enter to get a response. There is no command-line interface implemented — the script is purely interactive.

Notes & implementation details
- The script configures `genai` with `gemini-3-flash-preview` and applies safety settings and generation config directly in code.
- Conversation history is stored in-memory for the running session and is not persisted.
- The script uses `python-dotenv` to load `.env` variables and `rich` for colored console output.

Security
- Never commit your `GEMINI_API_KEY` to source control. Store it in environment variables or an ignored `.env` file.

Contributing
- Contributions are welcome. Open issues for bugs and feature requests and submit pull requests for improvements.

License
- This project is licensed under the MIT License — see [LICENSE](LICENSE).

