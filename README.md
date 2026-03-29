# CLI-Agent Documentation

## Overview
CLI-Agent is a powerful, multi-functional AI assistant designed to streamline your development workflow, automate system tasks, and provide intelligent code assistance directly from your terminal.

## Features
* **Code Mastery:** Write, debug, and optimize code across multiple programming languages.
* **System Integration:** Execute shell commands, manage files, and interact with macOS system tools (Notes, Reminders).
* **AI-Powered Logic:** Advanced problem-solving, mathematical computations, and data analysis.
* **Tool Orchestration:** Seamless integration with web search and local file system operations.
* **Customizable Workflow:** Highly extensible and adaptable to individual developer needs.

## Setup
1. Clone the repository to your local machine.
2. Ensure you have Python 3.9+ installed.
3. Install the required dependencies

## Usage
To start the CLI-Agent, run the following command in your terminal:
```bash
python main.py
```
Follow the interactive prompts to begin your session.

---

## ⚠️ SECURITY WARNING: CRITICAL API KEY MANAGEMENT
**NEVER store your `GEMINI_API_KEY` directly in your source code.**

Hardcoding sensitive credentials poses a severe security risk, as it may lead to unauthorized access or accidental exposure if the code is pushed to a public repository.

**Required Steps:**
1. Create a file named `.env` in the root directory of this project.
2. Add your API key to the file as follows:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Ensure that `.env` is added to your `.gitignore` file to prevent it from being tracked by version control systems.
