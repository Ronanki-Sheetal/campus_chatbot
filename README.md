# Aspire Bot: General Knowledge Chatbot

Aspire Bot is a small Flask web app for asking common general-knowledge questions. It answers from a local set of editable facts about science, geography, history, and sports. The chatbot uses keyword matching; it is not a trained AI model and does not search the internet.

## Features
- Responsive chat page with conversation history and a new-chat button.
- Built-in answers for common GK questions, greetings, and help.
- SQLite storage for chat messages and an optional `/admin` page for recent logs.
- No NLP data downloads or external API keys required.

## Run on Windows
1. Open this project folder in VS Code.
2. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.
3. Install Flask:
   ```powershell
   py -m pip install -r requirements.txt
   ```
4. Start the app:
   ```powershell
   py app.py
   ```
5. Open `http://127.0.0.1:5000`. The recent-message log is at `http://127.0.0.1:5000/admin`.

## Example questions
- What is the capital of France?
- Which planet is known as the Red Planet?
- What is the chemical formula for water?
- Who wrote Hamlet?
- When did India gain independence?

The supported fact questions and their example phrases are in `intents.json`. Add new entries there to teach the bot more answers. An unknown or ambiguous question gets a fallback response rather than an unrelated fact.

## Project structure
```text
app.py                 Flask routes and JSON endpoints
chatbot.py             Tokenization and intent matching
database.py            SQLite message history
intents.json           Built-in questions and answers
templates/index.html   Chat page
templates/admin.html   Recent chat log
static/css/style.css   Responsive styling
static/js/script.js    Browser chat behavior
tests/test_chatbot.py  Focused chatbot tests
```

## Notes
- Messages are stored in `chat_history.db` beside the application.
- `/admin` is not authenticated; keep this demonstration app local and do not expose the log page publicly.
- Responses come from a small fixed knowledge base. The bot may not recognize reworded questions or questions outside its included facts.
- Flask debug mode is enabled for local development in `app.py`; disable it before deploying.

## Test
Run the unit tests from the project directory:
```powershell
py -m unittest discover -s tests
```
