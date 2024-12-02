   document.getElementById('show-search-button').addEventListener('click', function () {
    document.getElementById('search-container').style.display = 'flex';
});

document.getElementById('submit-search').addEventListener('click', () => {
    const username = document.getElementById('search-username').value.trim();
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    if (username) {
        fetch(`/home/login/chatroom/api/get-users/?username=${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(users => {
                if (users.length > 0) {
                    users.forEach(user => {
                        const truncatedEmail = user.email.split('@')[0]; // Shorten the email
                        const userElement = document.createElement('div');
                        userElement.classList.add('user-result');
                        userElement.innerHTML = `
                            <div class="user-result-info">
                                <p>${user.username} (${truncatedEmail}...)</p>
                            </div>
                            <button class="add-to-chat-button" data-username="${user.username}" data-id="${user.id}">Message</button>
                        `;
                        resultsContainer.appendChild(userElement);
                    });

                    document.querySelectorAll('.add-to-chat-button').forEach(button => {
                        button.addEventListener('click', function () {
                            const username = this.getAttribute('data-username');
                            const userId = this.getAttribute('data-id');

                            // Update chat interface
                            document.querySelector('.message').style.display = 'none';
                            document.getElementById('chat-interface').style.display = 'flex';
                            document.getElementById('chat-username').textContent = username;

                            document.getElementById('search-container').style.display = 'none';

                            // Save chat locally
                            const chats = JSON.parse(localStorage.getItem('chats') || '[]');
                            if (!chats.some(chat => chat.id === userId)) {
                                chats.push({ id: userId, username: username });
                                localStorage.setItem('chats', JSON.stringify(chats));
                            }

                            // Enable direct message sending
                            sendMessage(username);
                        });
                    });
                } else {
                    resultsContainer.innerHTML = '<p>No users found.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching users:', error);
                resultsContainer.innerHTML = '<p>There was an error retrieving user data.</p>';
            });
    } else {
        resultsContainer.innerHTML = '<p>Please enter a username.</p>';
    }
});

// Function to send a message
function sendMessage(username) {
    const messageInput = document.querySelector('.input-section input');
    const sendButton = document.querySelector('.input-section button');

    sendButton.addEventListener('click', function () {
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                message: message,
                username: username
            }));
            messageInput.value = "";
        }
    });
}

// WebSocket for chat
const chatSocket = new WebSocket("wss://" + window.location.host + "/");

chatSocket.onopen = function () {
    console.log("WebSocket connection established!");
};

chatSocket.onerror = function (error) {
    console.error("WebSocket error observed:", error);
};

chatSocket.onmessage = function (e) {
    console.log("Message received:", e.data);
    const data = JSON.parse(e.data);
    const messageContainer = document.getElementById("messages");

    const messageElement = document.createElement("div");
    messageElement.textContent = `${data.username}: ${data.message}`;
    messageElement.style.color = "white";
    messageContainer.appendChild(messageElement);
};

chatSocket.onclose = function () {
    console.log("WebSocket connection closed unexpectedly.");
};

document.querySelector('.input-section button').addEventListener('click', function () {
    const messageInput = document.querySelector('.input-section input');
    const message = messageInput.value.trim();

    if (message) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'email': '{{ user.email }}'
        }));
        messageInput.value = "";
    }
});

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const messageContainer = document.getElementById("messages");

    const messageElement = document.createElement("div");
    messageElement.textContent = `${data.message}`;
    messageElement.style.color = "white";
    messageContainer.appendChild(messageElement);

    // Save chat to localStorage if saving is enabled
    if (isSavingEnabled()) {
        saveChatHistory();
    }
};
   window.addEventListener('DOMContentLoaded', () => {
        const settings = JSON.parse(localStorage.getItem('themeSettings')) || {};

        if (settings.leftPanel) {
            document.querySelector('.left-panel').style.background =
                `linear-gradient(150deg, ${settings.leftPanel.color1}, ${settings.leftPanel.color2})`;
        }
        if (settings.button) {
            document.querySelectorAll('.icon-button').forEach(button => {
                button.style.background =
                    `linear-gradient(150deg, ${settings.button.color1}, ${settings.button.color2})`;
            });
        }
        if (settings.chatHeader) {
            document.querySelector('.chat-header').style.background =
                `linear-gradient(150deg, ${settings.chatHeader.color1}, ${settings.chatHeader.color2})`;
        }
        if (settings.sendButton) {
            document.querySelector('.input-section button').style.background =
                `linear-gradient(150deg, ${settings.sendButton.color1}, ${settings.sendButton.color2})`;
        }
    });

// Initialize the chat saving button and slider
const chatSavingButton = document.getElementById("chatSavingButton");

// Add event listener to toggle the button state
chatSavingButton.addEventListener('click', function () {
    const isSavingEnabled = chatSavingButton.style.backgroundColor === "green";

    if (isSavingEnabled) {
        localStorage.removeItem('chatHistory'); // Clear chat history if turning off
        localStorage.setItem('chatSavingEnabled', false); // Update saving state
        chatSavingButton.style.backgroundColor = "red"; // Change to red
    } else {
        localStorage.setItem('chatSavingEnabled', true); // Enable saving
        chatSavingButton.style.backgroundColor = "green"; // Change to green
    }
});

// On page load, initialize the button state
function initializeChatSavingButton() {
    const isSavingEnabled = localStorage.getItem('chatSavingEnabled') === "true";

    if (isSavingEnabled) {
        chatSavingButton.style.backgroundColor = "green"; // Set to green if enabled
    } else {
        chatSavingButton.style.backgroundColor = "red"; // Set to red if disabled
    }
}

initializeChatSavingButton();

function toggleChatSaving() {
    const isEnabled = isSavingEnabled();
    if (isEnabled) {
        localStorage.removeItem('chatHistory'); // Clear chat history if turning off
        chatSavingButton.style.background = "red";
    } else {

        chatSavingButton.style.background = "green";
    }
    localStorage.setItem('chatSavingEnabled', !isEnabled);
}

// Check if saving is enabled
function isSavingEnabled() {
    return localStorage.getItem('chatSavingEnabled') === "true";
}

// Save the chat history to localStorage
function saveChatHistory() {
    const messageContainer = document.getElementById("messages");
    const messages = Array.from(messageContainer.children).map(msg => msg.textContent);
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

// Load the chat history if saving is enabled
function loadChatHistory() {
    if (isSavingEnabled()) {
        const savedMessages = JSON.parse(localStorage.getItem('chatHistory') || "[]");
        const messageContainer = document.getElementById("messages");
        messageContainer.innerHTML = ""; // Clear existing messages
        savedMessages.forEach(msgText => {
            const messageElement = document.createElement("div");
            messageElement.textContent = msgText;
            messageElement.style.color = "white";
            messageContainer.appendChild(messageElement);
        });

        chatSavingButton.style.background = "green";
    } else {
        localStorage.removeItem('chatHistory'); // Ensure no old chats are loaded
        chatSavingButton.style.background = "red";
    }
}

// Load chat history on page load
loadChatHistory();

           

// WebSocket Consumer for receiving notifications and triggering showNotification
const socket = new WebSocket(`ws://${window.location.host}/`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    // Check if the data contains the notification
    if (data.notification) {
        const notification = data.notification;
        showNotification(notification.message, notification.username);
    }
};

window.onload = function () {
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');

    if (chats.length > 0) {
        // Hide the "No chats here" message
        document.querySelector('.message').style.display = 'none';

        const chatList = document.getElementById('results');
        chatList.innerHTML = ''; // Clear any previous content

        chats.forEach(chat => {
            // Create a card for each saved chat
            const chatCard = document.createElement('div');
            chatCard.classList.add('user-result'); // Apply card styles

            chatCard.innerHTML = `
                <div class="user-result-info">
                    <p>${chat.username}</p>
                </div>
                <button class="add-to-chat-button" data-username="${chat.username}" data-id="${chat.id}">Message</button>
            `;

            // Add event listener to the "Message" button
            chatCard.querySelector('.add-to-chat-button').addEventListener('click', function () {
                const username = this.getAttribute('data-username');
                const userId = this.getAttribute('data-id');

                // Hide the search container
                document.getElementById('search-container').style.display = 'none';

                // Show the chat interface
                document.getElementById('chat-interface').style.display = 'flex';

                // Update the chat header with the selected user's name
                document.getElementById('chat-username').textContent = username;

                // Optional: Handle backend chat loading logic or any other logic here
            });

            // Append the card to the results container
            chatList.appendChild(chatCard);
        });
    }
 document.getElementById('close-chat-button').addEventListener('click', function () {
    // Hide the chat interface
    document.getElementById('chat-interface').style.display = 'none';

    // Reset the chat username
    document.getElementById('chat-username').textContent = 'User Name';

    // Show the "No chats here" message if no chats are active
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    if (chats.length === 0) {
        document.querySelector('.message').style.display = 'block';
    }
});
    document.getElementById('close-chat-button').addEventListener('click', function () {
    // Hide the chat interface
    document.getElementById('chat-interface').style.display = 'none';

    // Reset the chat username
    document.getElementById('chat-username').textContent = 'User Name';

    // Show the "No chats here" message if no chats are active
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    if (chats.length === 0) {
        document.querySelector('.message').style.display = 'block';
    }
});
    function renderChatList() {
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    const chatList = document.getElementById('results');
    chatList.innerHTML = ''; // Clear existing list

    chats.forEach(chat => {
        const chatCard = document.createElement('div');
        chatCard.classList.add('user-result'); // Apply card styles

        chatCard.innerHTML = `
            <div class="user-result-info">
                <p>${chat.username}</p>
            </div>
            <button class="switch-chat-button" data-username="${chat.username}" data-id="${chat.id}">Open Chat</button>
        `;

        // Add event listener to the "Open Chat" button
        chatCard.querySelector('.switch-chat-button').addEventListener('click', function () {
            const username = this.getAttribute('data-username');
            const userId = this.getAttribute('data-id');

            // Hide any currently active chat
            document.getElementById('chat-interface').style.display = 'none';

            // Update chat interface with selected chat
            openChat(username, userId);
        });

        chatList.appendChild(chatCard);
    });
}

// Function to open a specific chat
function openChat(username, userId) {
    // Show the chat interface
    document.getElementById('chat-interface').style.display = 'flex';

    // Update the chat header with the selected user's name
    document.getElementById('chat-username').textContent = username;

    // Optional: Load messages for the selected chat user from the server or storage
    // You can fetch and display messages here
}
};
document.getElementById('delete-chat-button').addEventListener('click', function () {
    const chatUsername = document.getElementById('chat-username').textContent;

    // Get the list of chats from localStorage
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');

    // Filter out the chat with the current username (the one being deleted)
    const updatedChats = chats.filter(chat => chat.username !== chatUsername);

    // Save the updated chat list back to localStorage
    localStorage.setItem('chats', JSON.stringify(updatedChats));

    // Hide the chat interface after deleting the chat
    document.getElementById('chat-interface').style.display = 'none';

    // Show the "No chats here" message if no other chats exist
    if (updatedChats.length === 0) {
        document.querySelector('.message').style.display = 'block';
    }

    // Optional: You can add a confirmation message or alert here
    alert(`Your chat Chat with ${chatUsername} has been deleted.`);

    // Re-render the chat list to reflect the changes
    renderChatList();
});

