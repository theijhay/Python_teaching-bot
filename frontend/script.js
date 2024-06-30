const sidebar = document.querySelector("#sidebar");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");

hide_sidebar.addEventListener("click", function() {
    sidebar.classList.toggle("hidden");
});

const user_menu = document.querySelector(".user-menu ul");
const show_user_menu = document.querySelector(".user-menu button");

show_user_menu.addEventListener("click", function() {
    if (user_menu.classList.contains("show")) {
        user_menu.classList.toggle("show");
        setTimeout(function() {
            user_menu.classList.toggle("show-animate");
        }, 200);
    } else {
        user_menu.classList.toggle("show-animate");
        setTimeout(function() {
            user_menu.classList.toggle("show");
        }, 50);
    }
});

const models = document.querySelectorAll(".model-selector button");

for (const model of models) {
    model.addEventListener("click", function() {
        document.querySelector(".model-selector button.selected")?.classList.remove("selected");
        model.classList.add("selected");
    });
}

const message_box = document.querySelector("#message");

message_box.addEventListener("keyup", function() {
    message_box.style.height = "auto";
    let height = message_box.scrollHeight + 2;
    if (height > 200) {
        height = 200;
    }
    message_box.style.height = height + "px";
});

function show_view(view_selector) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

new_chat_button.addEventListener("click", function() {
    show_view(".new-chat-view");
});

document.querySelectorAll(".conversation-button").forEach(button => {
    button.addEventListener("click", function() {
        show_view(".conversation-view");
    });
});

function toggleDarkMode() {
    document.body.classList.remove("light-mode");
    document.body.classList.add("dark-mode");
}

function toggleLightMode() {
    document.body.classList.remove("dark-mode");
    document.body.classList.add("light-mode");
}

// Function to display the message in the chat with additional styling options
function displayMessage(message, type, fontColor = 'white', borderRadius = '16px', fontSize = '18px', maxWidth = '60%', boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)') {
    const responseWrapper = document.querySelector('.response-wrapper'); // Step 1
    const messageDiv = document.createElement('div'); // Step 2
    messageDiv.textContent = message; // Step 3
    messageDiv.style.color = fontColor; // Set font color
    messageDiv.style.borderRadius = borderRadius; // Set border radius for shape
    messageDiv.style.fontSize = fontSize; // Set font size
    messageDiv.style.maxWidth = maxWidth; // Set maximum width
    messageDiv.style.boxShadow = boxShadow; // Set box shadow for depth
    messageDiv.style.whiteSpace = 'pre-wrap'; // Preserve line breaks
    messageDiv.style.wordWrap = 'break-word';

    // Step 4: Apply different classes based on the message type
    if (type === 'user-message') {
        messageDiv.classList.add('user-message');
    } else if (type === 'bot-message') {
        messageDiv.classList.add('bot-message');
    }

    responseWrapper.appendChild(messageDiv); // Step 5
}
// Function to display the user input in the bot-answer class
// function displayUserInput(message) {
//     const queryWrapper = document.querySelector('.query-wrapper');
//     const botAnswer = queryWrapper.querySelector('.bot-answer');
//     botAnswer.innerText = message;
//     queryWrapper.style.display = 'block'; // Show the query-wrapper
// }

async function sendMessage() {
    const userInput = document.querySelector('#message');
    const message = userInput.value.trim();
    if (message === '') return;

    // Display user input in the bot-answer class
    displayMessage(message, 'user-message');


    // Clear the textarea and reset height
    userInput.value = '';
    userInput.style.height = 'auto';

    // Send message to server
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

document.querySelector('.send-button').addEventListener('click', sendMessage);

message_box.addEventListener("keyup", function(event) {
    message_box.style.height = "auto";
    let height = message_box.scrollHeight + 2;
    if (height > 200) {
        height = 200;
    }
    message_box.style.height = height + "px";

    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// Function to display welcome message
function displayWelcomeMessage() {
    displayMessage('Welcome to Python Teaching Bot, How can I help you today?', 'bot-message');
}

// Call displayWelcomeMessage when the page loads
document.addEventListener('DOMContentLoaded', displayWelcomeMessage);
