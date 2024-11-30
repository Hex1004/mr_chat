document.addEventListener('DOMContentLoaded', () => {
    loadThemeSettings();
    loadChatHistory();
});

function loadThemeSettings() {
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
}

document.getElementById('save-settings').addEventListener('click', () => {
    const settings = {
        leftPanel: {
            color1: document.getElementById('left-panel-color1').value,
            color2: document.getElementById('left-panel-color2').value,
        },
        button: {
            color1: document.getElementById('button-color1').value,
            color2: document.getElementById('button-color2').value,
        },
        chatHeader: {
            color1: document.getElementById('chat-header-color1').value,
            color2: document.getElementById('chat-header-color2').value,
        },
        sendButton: {
            color1: document.getElementById('send-button-color1').value,
            color2: document.getElementById('send-button-color2').value,
        }
    };

    localStorage.setItem('themeSettings', JSON.stringify(settings));
    alert('Settings saved! Refresh the chat page to apply.');
});

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
                        const userElement = document.createElement('div');
                        userElement.classList.add('user-result');
                        userElement.innerHTML = `
                            <div class="user-result-info">
                                <p>${user.username} ${user.email}</p>
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

                            // Save chat locally
                            const chats = JSON.parse(localStorage.getItem('chats') || '[]');
                            chats.push({ id: userId, username: username });
                            localStorage.setItem('chats', JSON.stringify(chats));
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

// WebSocket Logic
const chatSocket = new WebSocket("ws://" + window.location.host + "/");
chatSocket.onopen = function () {
    console.log("WebSocket connection established!");
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const messageContainer = document.getElementById("messages");

    const messageElement = document.createElement("div");
    messageElement.textContent = `${data.username}: ${data.message}`;
    messageElement.style.color = "white";
    messageContainer.appendChild(messageElement);
};
