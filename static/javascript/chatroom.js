function changeColor(element, color) {
    element.style.color = color;
}

// Show search container and change its color
document.getElementById('show-search-button').addEventListener('click', () => {
    const searchContainer = document.getElementById('search-container');
    searchContainer.style.display = 'flex';
    changeColor(searchContainer, 'blue');
});

// Handle search functionality
document.getElementById('submit-search').addEventListener('click', () => {
    const username = document.getElementById('search-username').value.trim();
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    if (!username) {
        resultsContainer.innerHTML = '<p>Please enter a username.</p>';
        return;
    }

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

                        openChat(username, userId);
                    });
                });
            } else {
                resultsContainer.innerHTML = '<p>No users found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching users:', error);
            resultsContainer.innerHTML = '<p>Error retrieving user data.</p>';
        });
});

// Initialize WebSocket
function initializeWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const chatSocket = new WebSocket(`${protocol}://${window.location.host}/`);

    chatSocket.onopen = () => console.log('WebSocket connection established');
    chatSocket.onmessage = event => {
        const data = JSON.parse(event.data);
        const messageContainer = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.textContent = data.message;
        changeColor(messageElement, 'white');
        messageContainer.appendChild(messageElement);

        if (isSavingEnabled()) saveChatHistory();
    };

    chatSocket.onclose = () => console.log('WebSocket connection closed');
    chatSocket.onerror = error => console.error('WebSocket error:', error);

    return chatSocket;
}

// Open a chat session
function openChat(username, userId) {
    const chatInterface = document.getElementById('chat-interface');
    chatInterface.style.display = 'flex';
    document.getElementById('chat-username').textContent = username;

    const chats = JSON.parse(localStorage.getItem('chats') || '[]');
    if (!chats.some(chat => chat.id === userId)) {
        chats.push({ id: userId, username });
        localStorage.setItem('chats', JSON.stringify(chats));
    }
    renderChatList();
    sendMessage(username);
}

// Send a message
function sendMessage(username) {
    const messageInput = document.querySelector('.input-section input');
    const sendButton = document.querySelector('.input-section button');
    const chatSocket = initializeWebSocket();

    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({ message, username }));
            messageInput.value = '';
        }
    });
}

// Chat saving toggle
function toggleChatSaving() {
    const chatSavingButton = document.getElementById('chat-saving-button');
    const isEnabled = isSavingEnabled();
    if (isEnabled) {
        localStorage.removeItem('chatHistory');
        localStorage.setItem('chatSavingEnabled', 'false');
        chatSavingButton.style.background = 'red';
    } else {
        localStorage.setItem('chatSavingEnabled', 'true');
        chatSavingButton.style.background = 'green';
    }
}

// Save chat history
function saveChatHistory() {
    const messages = Array.from(document.getElementById('messages').children).map(msg => msg.textContent);
    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

// Load chat history
function loadChatHistory() {
    if (isSavingEnabled()) {
        const savedMessages = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        const messageContainer = document.getElementById('messages');
        messageContainer.innerHTML = '';
        savedMessages.forEach(msgText => {
            const messageElement = document.createElement('div');
            messageElement.textContent = msgText;
            changeColor(messageElement, 'white');
            messageContainer.appendChild(messageElement);
        });
    }
}

// Check if saving is enabled
function isSavingEnabled() {
    return localStorage.getItem('chatSavingEnabled') === 'true';
}

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
            <button class="delete-chat-button" data-id="${chat.id}">Delete Chat</button>
        `;
        chatCard.querySelector('.switch-chat-button').addEventListener('click', () => {
            openChat(chat.username, chat.id);
        });
        chatCard.querySelector('.delete-chat-button').addEventListener('click', () => {
            deleteChat(chat.id);
        });
        chatList.appendChild(chatCard);
    });
}

// Delete a chat
function deleteChat(chatId) {
    let chats = JSON.parse(localStorage.getItem('chats') || '[]');
    chats = chats.filter(chat => chat.id !== chatId);
    localStorage.setItem('chats', JSON.stringify(chats));
    renderChatList();

    if (chats.length === 0) {
        document.querySelector('.message').style.display = 'block';
    }
}

// Close chat
document.getElementById('close-chat-button').addEventListener('click', () => {
    document.getElementById('chat-interface').style.display = 'none';
    document.getElementById('chat-username').textContent = 'User Name';
    if (JSON.parse(localStorage.getItem('chats') || '[]').length === 0) {
        document.querySelector('.message').style.display = 'block';
    }
});

// Initialize on page load
window.onload = () => {
    renderChatList();
    loadChatHistory();

    const chatSavingButton = document.getElementById('chat-saving-button');
    chatSavingButton.addEventListener('click', toggleChatSaving);

    const isEnabled = isSavingEnabled();
    chatSavingButton.style.background = isEnabled ? 'green' : 'red';
};
