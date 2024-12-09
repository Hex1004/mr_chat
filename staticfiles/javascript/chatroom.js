// Show search container when the search button is clicked
document.getElementById('show-search-button').addEventListener('click', function () {
    document.getElementById('search-container').style.display = 'flex';
});

// Handle search functionality
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
                        const truncatedEmail = user.email.split('@')[0];
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

                            document.querySelector('.message').style.display = 'none';
                            document.getElementById('chat-interface').style.display = 'flex';
                            document.getElementById('chat-username').textContent = username;
                            document.getElementById('search-container').style.display = 'none';

                            const chats = JSON.parse(localStorage.getItem('chats') || '[]');
                            if (!chats.some(chat => chat.id === userId)) {
                                chats.push({ id: userId, username: username });
                                localStorage.setItem('chats', JSON.stringify(chats));
                            }

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

// WebSocket initialization
function initializeWebSocket(username) {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(`${protocol}://${window.location.host}/`);

    chatSocket.onopen = () => {
        console.log("WebSocket connection established");
    };

    chatSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageContainer = document.getElementById("messages");
        const messageElement = document.createElement("div");
        messageElement.textContent = `${data.message}`;
        messageElement.style.color = "white";
        messageContainer.appendChild(messageElement);

        if (isSavingEnabled()) {
            saveChatHistory();
        }
    };

    chatSocket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    chatSocket.onclose = () => {
        console.log("WebSocket connection closed");
    };

    return chatSocket;
}

// Send message functionality
function sendMessage(username) {
    const messageInput = document.querySelector('.input-section input');
    const sendButton = document.querySelector('.input-section button');

    const chatSocket = initializeWebSocket(username);

    sendButton.addEventListener('click', function () {
        const message = messageInput.value.trim();
        if (message && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({ message: message, username: username }));
            messageInput.value = "";
        }
    });
}

// Chat saving functionality
function isSavingEnabled() {
    return localStorage.getItem('chatSavingEnabled') === "true";
}

function saveChatHistory() {
    const messageContainer = document.getElementById("messages");
    const messages = Array.from(messageContainer.children).map(msg => msg.textContent);
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

function loadChatHistory() {
    if (isSavingEnabled()) {
        const savedMessages = JSON.parse(localStorage.getItem('chatHistory') || "[]");
        const messageContainer = document.getElementById("messages");
        messageContainer.innerHTML = '';
        savedMessages.forEach(msgText => {
            const messageElement = document.createElement("div");
            messageElement.textContent = msgText;
            messageElement.style.color = "white";
            messageContainer.appendChild(messageElement);
        });
    } else {
        localStorage.removeItem('chatHistory');
    }
}

loadChatHistory();

// Chat Saving Button
const chatSavingButton = document.getElementById("chatSavingButton");
chatSavingButton.addEventListener('click', function () {
    const isEnabled = isSavingEnabled();
    if (isEnabled) {
        localStorage.removeItem('chatHistory');
        localStorage.setItem('chatSavingEnabled', false);
        chatSavingButton.style.backgroundColor = "red";
    } else {
        localStorage.setItem('chatSavingEnabled', true);
        chatSavingButton.style.backgroundColor = "green";
    }
});

// Initialize Chat Saving Button
function initializeChatSavingButton() {
    const isEnabled = isSavingEnabled();
    chatSavingButton.style.backgroundColor = isEnabled ? "green" : "red";
}
initializeChatSavingButton();

// Render chat list
function renderChatList() {
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    const chatList = document.getElementById('results');
    chatList.innerHTML = '';
    chats.forEach(chat => {
        const chatCard = document.createElement('div');
        chatCard.classList.add('user-result');
        chatCard.innerHTML = `
            <div class="user-result-info">
                <p>${chat.username}</p>
            </div>
            <button class="switch-chat-button" data-username="${chat.username}" data-id="${chat.id}">Open Chat</button>
        `;
        chatCard.querySelector('.switch-chat-button').addEventListener('click', function () {
            openChat(chat.username, chat.id);
        });
        chatList.appendChild(chatCard);
    });
}

// Open a specific chat
function openChat(username, userId) {
    document.getElementById('chat-interface').style.display = 'flex';
    document.getElementById('chat-username').textContent = username;
}

// Close Chat
document.getElementById('close-chat-button').addEventListener('click', function () {
    document.getElementById('chat-interface').style.display = 'none';
    document.getElementById('chat-username').textContent = 'User Name';
    if (JSON.parse(localStorage.getItem('chats') || '[]').length === 0) {
        document.querySelector('.message').style.display = 'block';
    }
});

// Delete Chat
document.getElementById('delete-chat-button').addEventListener('click', function () {
    const chatUsername = document.getElementById('chat-username').textContent;
    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    const updatedChats = chats.filter(chat => chat.username !== chatUsername);
    localStorage.setItem('chats', JSON.stringify(updatedChats));
    document.getElementById('chat-interface').style.display = 'none';
    alert(`Chat with ${chatUsername} has been deleted.`);
    renderChatList();
});

// Render chat list on page load
window.onload = function () {
    renderChatList();
    loadChatHistory();
};
