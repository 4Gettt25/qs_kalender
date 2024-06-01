const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

const passwordResetForm = document.getElementById('password-reset-form');
const emailInput = document.getElementById('email');

passwordResetForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = emailInput.value;
    // Make a POST request to your server with the email
    // The server should handle sending the password reset email
});