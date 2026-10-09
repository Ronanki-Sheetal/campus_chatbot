"""Flask routes for the college FAQ chatbot."""
from flask import Flask, jsonify, render_template, request, session

from chatbot import get_response
from database import create_session_id, get_messages, init_db, save_message

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-your-own-project"
init_db()


@app.get("/")
def home():
    if "session_id" not in session:
        session["session_id"] = create_session_id()
    return render_template("index.html", session_id=session["session_id"])


@app.get("/api/history")
def history():
    return jsonify({"messages": get_messages(session.get("session_id", ""))})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please type a message first."}), 400

    if "session_id" not in session:
        session["session_id"] = create_session_id()
    reply = get_response(message)
    save_message(session["session_id"], message, reply)
    return jsonify({"reply": reply})


@app.post("/api/new-chat")
def new_chat():
    session["session_id"] = create_session_id()
    return jsonify({"session_id": session["session_id"]})


@app.get("/admin")
def admin():
    return render_template("admin.html", messages=get_messages(limit=200))


if __name__ == "__main__":
    app.run(debug=True)
