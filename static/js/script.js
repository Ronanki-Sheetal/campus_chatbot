const messageList = document.querySelector("#messages");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const typing = document.querySelector("#typing");

function addMessage(text, sender) {
  const empty = messageList.querySelector(".empty-state");
  if (empty) empty.remove();
  const bubble = document.createElement("div");
  bubble.className = `message ${sender}`;
  bubble.textContent = text;
  messageList.appendChild(bubble);
  messageList.scrollTop = messageList.scrollHeight;
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const data = await response.json();
    data.messages.forEach((item) => {
      addMessage(item.user_message, "user");
      addMessage(item.bot_response, "bot");
    });
  } catch (error) {
    addMessage("I couldn’t load the conversation history. You can still send a new message.", "bot");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) {
    input.focus();
    input.setCustomValidity("Please type a message first.");
    input.reportValidity();
    input.setCustomValidity("");
    return;
  }
  addMessage(message, "user");
  input.value = "";
  input.disabled = true;
  typing.classList.remove("hidden");
  try {
    const response = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The message could not be sent.");
    addMessage(data.reply, "bot");
  } catch (error) {
    addMessage(error.message || "Sorry, something went wrong. Please try again.", "bot");
  } finally {
    typing.classList.add("hidden");
    input.disabled = false;
    input.focus();
  }
});

document.querySelector("#new-chat").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/new-chat", { method: "POST" });
    if (!response.ok) throw new Error("Could not start a new conversation.");
    messageList.innerHTML = '<div class="empty-state"><div class="sparkle">✦</div><h2>Ready for a GK question?</h2><p>Try “What is the capital of France?”</p></div>';
  } catch (error) {
    addMessage("Could not start a new conversation. Please refresh and try again.", "bot");
  }
});

loadHistory();
