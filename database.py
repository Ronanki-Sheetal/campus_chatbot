"""SQLite helpers for conversation history."""
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATABASE_FILE = Path(__file__).with_name("chat_history.db")


def connect():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")


def create_session_id():
    return str(uuid.uuid4())


def save_message(session_id, user_message, bot_response):
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    with connect() as connection:
        connection.execute(
            "INSERT INTO messages (session_id, user_message, bot_response, created_at) VALUES (?, ?, ?, ?)",
            (session_id, user_message, bot_response, timestamp),
        )


def get_messages(session_id=None, limit=200):
    with connect() as connection:
        if session_id:
            rows = connection.execute(
                "SELECT user_message, bot_response, created_at FROM messages WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT session_id, user_message, bot_response, created_at FROM messages ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [dict(row) for row in rows]
