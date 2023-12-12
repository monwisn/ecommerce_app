// theme.js
function toggleMode() {
    var body = document.querySelector('body');
    var themeStyle = document.querySelector('#theme-style');

    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        themeStyle.href = "{% static 'main/css/light.css' %}";
        fetch('/set_mode/?mode=light');  // Send an AJAX request to update the mode in the session
    } else {
        body.classList.add('dark-mode');
        themeStyle.href = "{% static 'main/css/dark.css' %}";
        fetch('/set_mode/?mode=dark');  // Send an AJAX request to update the mode in the session
    }
}

var storedMode = localStorage.getItem('mode');
if (storedMode === 'dark') {
    toggleMode();
}