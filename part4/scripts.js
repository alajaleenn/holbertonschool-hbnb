// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    // Handle Login Form
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await handleLogin(event);
        });
    }

    // Check authentication on page load
    checkAuthentication();
});

// Function to handle login
async function handleLogin(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                email: email, 
                password: password 
            })
        });

        if (response.ok) {
            const data = await response.json();
            // Store token in cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
            
            // Show success message
            alert('Login successful!');
            
            // Redirect to index page
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert('Login failed: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
}

// Function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

// Function to check if user is authenticated
function checkAuthentication() {
    const token = getCookie('token');
    const loginButton = document.querySelector('.login-button');
    
    if (token && loginButton) {
        // User is logged in, change button to "Logout"
        loginButton.textContent = 'Logout';
        loginButton.href = '#';
        loginButton.addEventListener('click', handleLogout);
    }
}

// Function to handle logout
function handleLogout(event) {
    event.preventDefault();
    // Delete the token cookie
    document.cookie = 'token=; path=/; max-age=0';
    alert('Logged out successfully!');
    window.location.href = 'login.html';
}
