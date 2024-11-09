document.addEventListener("DOMContentLoaded", function() {
    const chatbotWebSocketUrl = window.chatbotConfig.websocket_url || 'ws://localhost:8000/ws/chat'; // Get WebSocket URL from settings

    const websocket = new WebSocket(chatbotWebSocketUrl);

    websocket.onopen = () => {
        console.log("WebSocket connection established.");
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // Process and display the chatbot's response
        displayMessage('bot', data.response);
    };

    websocket.onerror = (error) => {
        console.error("WebSocket error: ", error);
    };

    websocket.onclose = () => {
        console.log("WebSocket connection closed.");
    };

    // Function to send user message
    function sendMessage(message) {
        if (message.trim() !== '') {
            websocket.send(JSON.stringify({ message }));
            displayMessage('user', message);
        }
    }

    // Function to display message in the chat window
    function displayMessage(sender, text) {
        const chatWindow = document.getElementById("chatbot-app");
        const messageElement = document.createElement("div");
        messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
        messageElement.textContent = text;
        chatWindow.appendChild(messageElement);
    }

    // Handle user input
    const inputField = document.createElement('input');
    inputField.placeholder = 'Type a message...';
    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendMessage(inputField.value);
            inputField.value = '';
        }
    });
    document.getElementById("chatbot-app").appendChild(inputField);
});
