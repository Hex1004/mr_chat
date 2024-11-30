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
  });
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