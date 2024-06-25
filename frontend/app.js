function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value;
    if (message.trim() === '') return;

    displayMessage(message, 'user-message');
    userInput.value = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (response.ok) {
            const data = await response.json();
            displayMessage(data.response, 'bot-message');
        } else {
            console.error('Error:', response.statusText);
            displayMessage('Error: Could not reach the server.', 'bot-message');
        }
    } catch (error) {
        console.error('Error:', error);
        displayMessage('Error: Could not reach the server.', 'bot-message');
    }
}

function displayMessage(message, className) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${className}`;
    messageElement.innerText = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
