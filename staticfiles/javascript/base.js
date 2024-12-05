document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const menuClose = document.querySelector(".menu-close");
    const menuItems = document.querySelector(".menu-items");

    // Ensure all elements are correctly selected
    if (menuToggle && menuClose && menuItems) {
        // Open menu
        menuToggle.addEventListener("click", () => {
            menuItems.classList.add("active");
            menuToggle.style.display = "none"; // Hide toggle button
        });

        // Close menu
        menuClose.addEventListener("click", () => {
            menuItems.classList.remove("active");
            menuToggle.style.display = "block"; // Show toggle button
        });
    } else {
        console.error("Menu elements not found. Check your HTML structure.");
    }

    // Handle cookies
    const cookieConsentBanner = document.getElementById("cookie-consent");
    const acceptCookiesButton = document.getElementById("accept-cookies");
    const rejectCookiesButton = document.getElementById("reject-cookies");

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
    }

    function getCookie(name) {
        const cookies = document.cookie.split(";").map(cookie => cookie.trim());
        for (const cookie of cookies) {
            if (cookie.startsWith(name + "=")) {
                return cookie.split("=")[1];
            }
        }
        return null;
    }

    // Event listeners for cookie consent
    if (acceptCookiesButton) {
        acceptCookiesButton.addEventListener("click", () => {
            setCookie("cookiesAccepted", "true", 365);
            cookieConsentBanner.style.display = "none";
        });
    }

    if (rejectCookiesButton) {
        rejectCookiesButton.addEventListener("click", () => {
            setCookie("cookiesAccepted", "false", 365);
            cookieConsentBanner.style.display = "none";
        });
    }

    // Check cookies consent on load
    if (getCookie("cookiesAccepted") === "true") {
        cookieConsentBanner.style.display = "none";
    }
});

// CSRF Token Handling
function getCSRFToken() {
    var cookieValue = null;
    var name = "csrftoken";
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrfToken = getCSRFToken();

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrfToken
    }
});
