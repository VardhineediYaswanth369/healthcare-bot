document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender + "-message");
        messageDiv.innerText = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("user", "You: " + message);
        userInput.value = "";
        
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("bot", "Bot: " + data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("bot", "Something went wrong. Please try again.");
        });
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
