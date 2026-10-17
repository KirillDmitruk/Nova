const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const button = document.getElementById("send-button");

function addMessage(text, role) {
    const element = document.createElement("div");

    element.classList.add("message", role);
    element.textContent = text;

    messages.appendChild(element);
    messages.scrollTop = messages.scrollHeight;

    return element;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    input.value = "";

    button.disabled = true;

    const loading = addMessage(
        "NOVA is thinking...",
        "assistant"
    );

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status}`
            );
        }

        const data = await response.json();

        loading.textContent = data.answer;

    } catch (error) {
        console.error(error);

        loading.textContent =
            "Connection error. Please try again.";

    } finally {
        button.disabled = false;
        input.focus();
    }
});