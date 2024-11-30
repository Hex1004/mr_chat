  function getCSRFToken() {
        // Retrieve the CSRF token from the cookie
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
            const [name, value] = cookies[i].split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }

    function showWelcomeMessage() {
        const welcomeBox = document.getElementById('welcomeBox');
        const buttonContainer = document.getElementById('buttonContainer');
        welcomeBox.style.display = 'block';

        setTimeout(() => {
            buttonContainer.style.display = 'flex';
        }, 1400);
    }

    window.addEventListener('load', () => {
        setTimeout(showWelcomeMessage, 500);
    });

    // Example of using CSRF Token in a fetch request
    function sendData() {
        const csrfToken = getCSRFToken();

        fetch('/api/endpoint/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Add CSRF token here
            },
            body: JSON.stringify({ key: 'value' }),
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    }