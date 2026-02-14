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

    // Task 3: Initialize place details page
    if (window.location.pathname.includes('place.html')) {
        const placeId = getPlaceIdFromURL();
        
        if (!placeId) {
            alert('Invalid place ID');
            window.location.href = 'index.html';
            return;
        }

        const token = getCookie('token');
        fetchPlaceDetails(token, placeId);
    }

    // Task 4: Initialize add review page
    if (window.location.pathname.includes('add_review.html')) {
        const token = checkAuthenticationForReview();
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            alert('Invalid place ID');
            window.location.href = 'index.html';
            return;
        }

        const reviewForm = document.querySelector('.add-review');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                await submitReview(token, placeId);
            });
        }
    }
});

// ============ TASK 1: LOGIN ============
async function handleLogin(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5003/api/v1/auth/login', {
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
            alert('Login failed: ' + (errorData.error || response.statusText));
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

function handleLogout(event) {
    event.preventDefault();
    document.cookie = 'token=; path=/; max-age=0';
    alert('Logged out successfully!');
    window.location.href = 'login.html';
}

// ============ TASK 2: INDEX PAGE ============
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
        
        // Fetch places even if not authenticated (public endpoint)
        const placesContainer = document.getElementById('places-list');
        if (placesContainer) {
            fetchPlaces(null);
        }
    }
}

async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Places endpoint is public, but we can still send token if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://127.0.0.1:5003/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else if (response.status === 401 && token) {
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
        placeCard.setAttribute('data-price', place.price || 0);
        
        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
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

// ============ TASK 3: PLACE DETAILS ============
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://127.0.0.1:5003/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place, token);
            await fetchPlaceReviews(placeId, token);
        } else {
            alert('Failed to fetch place details.');
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('An error occurred while fetching place details.');
    }
}

function displayPlaceDetails(place, token) {
    const placeDetails = document.querySelector('.place-details');
    
    if (!placeDetails) return;

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-info">
            <p><strong>Host:</strong> Owner ID: ${place.owner_id}</p>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Location:</strong> Latitude: ${place.latitude}, Longitude: ${place.longitude}</p>
            <p><strong>Amenities:</strong> ${place.amenities && place.amenities.length > 0 ? place.amenities.join(', ') : 'None listed'}</p>
        </div>
    `;

    // Show/hide add review button based on authentication
    const addReviewButton = document.querySelector('a[href*="add_review.html"]');
    if (addReviewButton) {
        if (token) {
            addReviewButton.href = `add_review.html?place_id=${place.id}`;
            addReviewButton.style.display = 'inline-block';
        } else {
            addReviewButton.style.display = 'none';
        }
    }
}

async function fetchPlaceReviews(placeId, token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://127.0.0.1:5003/api/v1/places/${placeId}/reviews`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to fetch reviews');
            displayReviews([]);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);
    }
}

function displayReviews(reviews) {
    const reviewsSection = document.querySelector('section h2');
    
    if (!reviewsSection || reviewsSection.textContent !== 'Reviews') return;

    const reviewsContainer = reviewsSection.parentElement;
    
    // Remove existing review cards
    const existingReviews = reviewsContainer.querySelectorAll('.review-card');
    existingReviews.forEach(card => card.remove());

    if (reviews.length === 0) {
        const noReviews = document.createElement('p');
        noReviews.textContent = 'No reviews yet. Be the first to review!';
        reviewsSection.after(noReviews);
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('article');
        reviewCard.className = 'review-card';
        
        reviewCard.innerHTML = `
            <p>"${review.text}"</p>
            <p><strong>User:</strong> ${review.user_id}</p>
            <p><strong>Rating:</strong> ${review.rating}/5</p>
        `;
        
        reviewsContainer.appendChild(reviewCard);
    });
}

// ============ TASK 4: ADD REVIEW ============
function checkAuthenticationForReview() {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review.');
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

async function submitReview(token, placeId) {
    const reviewText = document.getElementById('comment').value;
    const rating = document.getElementById('rating').value;

    if (!reviewText || !rating) {
        alert('Please fill in all fields.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5003/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            // Clear the form
            document.getElementById('comment').value = '';
            document.getElementById('rating').value = '';
            // Redirect to place details page
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert('Failed to submit review: ' + (errorData.error || response.statusText));
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting the review.');
    }
}