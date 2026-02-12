document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await handleLogin(event);
        });
    }

    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterByPrice);
    }
});

async function handleLogin(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5003/api/v1/login', {
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
    const loginLink = document.getElementById('login-link');
    
    if (token) {
        if (loginLink) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', handleLogout);
        }
        
        const placesContainer = document.getElementById('places-list');
        if (placesContainer) {
            fetchPlaces(token);
        }
    } else {
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    }
}

function handleLogout(event) {
    event.preventDefault();
    document.cookie = 'token=; path=/; max-age=0';
    alert('Logged out successfully!');
    window.location.href = 'login.html';
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5003/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else if (response.status === 401) {
            alert('Session expired. Please login again.');
            document.cookie = 'token=; path=/; max-age=0';
            window.location.href = 'login.html';
        } else {
            alert('Failed to fetch places.');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('An error occurred while fetching places.');
    }
}

function displayPlaces(places) {
    const placesContainer = document.getElementById('places-list');
    placesContainer.innerHTML = '';

    if (places.length === 0) {
        placesContainer.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('article');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price_per_night || 0);
        
        placeCard.innerHTML = `
            <h2>${place.name}</h2>
            <p>Price per night: $${place.price_per_night}</p>
            <p class="location">${place.city || ''}, ${place.country || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        placesContainer.appendChild(placeCard);
    });
}

function filterByPrice() {
    const selectedPrice = document.getElementById('price-filter').value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const cardPrice = parseFloat(card.getAttribute('data-price'));
        
        if (selectedPrice === 'all') {
            card.style.display = 'block';
        } else {
            const maxPrice = parseFloat(selectedPrice);
            if (cardPrice <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}
