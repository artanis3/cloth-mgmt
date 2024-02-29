document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if(username == 'cloth' && password == '123@admin') {
        window.location.href = '/main_menu';
    } 
});




