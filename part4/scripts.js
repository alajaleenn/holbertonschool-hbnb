
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await handleLogin(event);
        });
    }

    checkAuthentication();
});

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
            document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
            
            alert('Login successful!');
            
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

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginButton = document.querySelector('.login-button');
    
    if (token && loginButton) {
        loginButton.textContent = 'Logout';
        loginButton.href = '#';
        loginButton.addEventListener('click', handleLogout);
    }
}

function handleLogout(event) {
    event.preventDefault();
    document.cookie = 'token=; path=/; max-age=0';
    alert('Logged out successfully!');
    window.location.href = 'login.html';
}
