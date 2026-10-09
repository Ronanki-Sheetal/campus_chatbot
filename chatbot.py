"""Keyword-based answers to common general-knowledge questions."""
import json
import re
from pathlib import Path

INTENTS_FILE = Path(__file__).with_name("intents.json")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "did", "do", "does",
    "for", "from", "how", "i", "in", "is", "it", "me", "my", "of", "on",
    "please", "tell", "that", "the", "to", "was", "what", "when", "where",
    "which", "who", "why", "you",
}
FALLBACK_RESPONSE = (
    "I don’t know that one yet. Try a question about science, geography, "
    "history, or sports—for example, “What is the largest ocean?”"
)


def tokenize(text):
    """Lowercase and split text into useful words without NLTK data downloads."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def get_response(message):
    """Return the best unambiguous answer, or ask for a different question."""
    with INTENTS_FILE.open(encoding="utf-8") as file:
        intents = json.load(file)["intents"]
    user_words = set(tokenize(message))
    if not user_words:
        return FALLBACK_RESPONSE

    scores = {}
    for intent in intents:
        if intent["name"] == "fallback":
            continue
        best_intent_score = 0
        for example in intent["examples"]:
            example_words = set(tokenize(example))
            overlap = len(user_words & example_words)
            if overlap:
                score = overlap / len(user_words) + 0.25 * overlap / len(example_words)
                best_intent_score = max(best_intent_score, score)
        if best_intent_score:
            scores[intent["name"]] = (best_intent_score, intent["response"])

    if not scores:
        return FALLBACK_RESPONSE

    best_score = max(score for score, _ in scores.values())
    if best_score < 0.65:
        return FALLBACK_RESPONSE

    best_responses = {
        response
        for score, response in scores.values()
        if score == best_score
    }
    if len(best_responses) != 1:
        return FALLBACK_RESPONSE
    return best_responses.pop()
