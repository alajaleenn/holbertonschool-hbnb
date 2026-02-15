
   const API_BASE_URL = 'http://127.0.0.1:5003/api/v1';

   // ==================== AUTHENTICATION ====================
   
   function getCookie(name) {
       const value = `; ${document.cookie}`;
       const parts = value.split(`; ${name}=`);
       if (parts.length === 2) {
           return parts.pop().split(';').shift();
       }
       return null;
   }
   
   function checkAdminAuth() {
       const token = getCookie('token');
       
       // If on login page, allow access
       if (window.location.pathname.includes('login.html')) {
           if (token) {
               // Already logged in, redirect to dashboard
               window.location.href = 'index.html';
           }
           return null;
       }
       
       // For all other admin pages, require token
       if (!token) {
           alert('Please login as admin to access this page.');
           window.location.href = 'login.html';
           return null;
       }
       
       return token;
   }
   
   async function handleAdminLogin(event) {
       event.preventDefault();
       
       const email = document.getElementById('email').value;
       const password = document.getElementById('password').value;
   
       try {
           const response = await fetch(`${API_BASE_URL}/auth/login`, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({ email, password })
           });
   
           if (response.ok) {
               const data = await response.json();
               
               // Store token
               document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
               
               // Verify user is admin (check JWT claims)
               const tokenPayload = JSON.parse(atob(data.access_token.split('.')[1]));
               
               if (!tokenPayload.is_admin) {
                   alert('Access denied. Admin privileges required.');
                   document.cookie = 'token=; path=/; max-age=0';
                   return;
               }
               
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
   
   function logout() {
       document.cookie = 'token=; path=/; max-age=0';
       alert('Logged out successfully!');
       window.location.href = 'login.html';
   }
   
   // ==================== DASHBOARD ====================
   
   async function loadDashboardStats(token) {
       try {
           const response = await fetch(`${API_BASE_URL}/admin/stats`, {
               method: 'GET',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               const stats = await response.json();
               
               document.getElementById('total-users').textContent = stats.total_users || 0;
               document.getElementById('total-places').textContent = stats.total_places || 0;
               document.getElementById('total-reviews').textContent = stats.total_reviews || 0;
               document.getElementById('total-amenities').textContent = stats.total_amenities || 0;
           } else {
               console.error('Failed to load stats');
           }
       } catch (error) {
           console.error('Error loading stats:', error);
       }
   }
   
   // ==================== USERS MANAGEMENT ====================
   
   async function loadUsers(token) {
       try {
           const response = await fetch(`${API_BASE_URL}/users/`, {
               method: 'GET',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               const users = await response.json();
               displayUsers(users);
           } else {
               document.getElementById('users-table-body').innerHTML = 
                   '<tr><td colspan="6" class="error">Failed to load users</td></tr>';
           }
       } catch (error) {
           console.error('Error loading users:', error);
           document.getElementById('users-table-body').innerHTML = 
               '<tr><td colspan="6" class="error">Error loading users</td></tr>';
       }
   }
   
   function displayUsers(users) {
       const tbody = document.getElementById('users-table-body');
       
       if (users.length === 0) {
           tbody.innerHTML = '<tr><td colspan="6">No users found</td></tr>';
           return;
       }
       
       tbody.innerHTML = users.map(user => `
           <tr>
               <td>${user.id.substring(0, 8)}...</td>
               <td>${user.first_name} ${user.last_name}</td>
               <td>${user.email}</td>
               <td>${user.is_admin ? '✅ Yes' : '❌ No'}</td>
               <td>${new Date(user.created_at).toLocaleDateString()}</td>
               <td>
                   <button class="btn-small btn-danger" onclick="deleteUser('${user.id}')">Delete</button>
               </td>
           </tr>
       `).join('');
   }
   
   function showCreateUserModal() {
       document.getElementById('create-user-modal').style.display = 'block';
   }
   
   function closeCreateUserModal() {
       document.getElementById('create-user-modal').style.display = 'none';
       document.getElementById('create-user-form').reset();
   }
   
   async function handleCreateUser(event) {
       event.preventDefault();
       
       const token = getCookie('token');
       const userData = {
           first_name: document.getElementById('first_name').value,
           last_name: document.getElementById('last_name').value,
           email: document.getElementById('email').value,
           password: document.getElementById('password').value,
           is_admin: document.getElementById('is_admin').checked
       };
   
       try {
           const response = await fetch(`${API_BASE_URL}/users/`, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify(userData)
           });
   
           if (response.ok) {
               alert('User created successfully!');
               closeCreateUserModal();
               loadUsers(token);
           } else {
               const errorData = await response.json();
               alert('Failed to create user: ' + (errorData.error || response.statusText));
           }
       } catch (error) {
           console.error('Error creating user:', error);
           alert('An error occurred while creating the user.');
       }
   }
   
   async function deleteUser(userId) {
       if (!confirm('Are you sure you want to delete this user?')) {
           return;
       }
       
       const token = getCookie('token');
       
       try {
           const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
               method: 'DELETE',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               alert('User deleted successfully!');
               loadUsers(token);
           } else {
               alert('Failed to delete user');
           }
       } catch (error) {
           console.error('Error deleting user:', error);
           alert('An error occurred while deleting the user.');
       }
   }
   
   // ==================== PLACES MANAGEMENT ====================
   
   async function loadPlaces(token) {
       try {
           const response = await fetch(`${API_BASE_URL}/places/`, {
               method: 'GET',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               const places = await response.json();
               displayPlaces(places);
           } else {
               document.getElementById('places-table-body').innerHTML = 
                   '<tr><td colspan="6" class="error">Failed to load places</td></tr>';
           }
       } catch (error) {
           console.error('Error loading places:', error);
           document.getElementById('places-table-body').innerHTML = 
               '<tr><td colspan="6" class="error">Error loading places</td></tr>';
       }
   }
   
   function displayPlaces(places) {
       const tbody = document.getElementById('places-table-body');
       
       if (places.length === 0) {
           tbody.innerHTML = '<tr><td colspan="6">No places found</td></tr>';
           return;
       }
       
       tbody.innerHTML = places.map(place => `
           <tr>
               <td>${place.id.substring(0, 8)}...</td>
               <td>${place.title}</td>
               <td>$${place.price}</td>
               <td>${place.owner_id.substring(0, 8)}...</td>
               <td>${new Date(place.created_at).toLocaleDateString()}</td>
               <td>
                   <button class="btn-small btn-info" onclick="window.open('../place.html?id=${place.id}', '_blank')">View</button>
               </td>
           </tr>
       `).join('');
   }
   
   // ==================== REVIEWS MANAGEMENT ====================
   
   async function loadReviews(token) {
       try {
           const response = await fetch(`${API_BASE_URL}/reviews/`, {
               method: 'GET',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               const reviews = await response.json();
               displayReviews(reviews);
           } else {
               document.getElementById('reviews-table-body').innerHTML = 
                   '<tr><td colspan="7" class="error">Failed to load reviews</td></tr>';
           }
       } catch (error) {
           console.error('Error loading reviews:', error);
           document.getElementById('reviews-table-body').innerHTML = 
               '<tr><td colspan="7" class="error">Error loading reviews</td></tr>';
       }
   }
   
   function displayReviews(reviews) {
       const tbody = document.getElementById('reviews-table-body');
       
       if (reviews.length === 0) {
           tbody.innerHTML = '<tr><td colspan="7">No reviews found</td></tr>';
           return;
       }
       
       tbody.innerHTML = reviews.map(review => `
           <tr>
               <td>${review.id.substring(0, 8)}...</td>
               <td>${review.text.substring(0, 50)}...</td>
               <td>${review.rating}/5 ⭐</td>
               <td>${review.user_id.substring(0, 8)}...</td>
               <td>${review.place_id.substring(0, 8)}...</td>
               <td>${new Date(review.created_at).toLocaleDateString()}</td>
               <td>
                   <button class="btn-small btn-danger" onclick="deleteReview('${review.id}')">Delete</button>
               </td>
           </tr>
       `).join('');
   }
   
   async function deleteReview(reviewId) {
       if (!confirm('Are you sure you want to delete this review?')) {
           return;
       }
       
       const token = getCookie('token');
       
       try {
           const response = await fetch(`${API_BASE_URL}/reviews/${reviewId}`, {
               method: 'DELETE',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               alert('Review deleted successfully!');
               loadReviews(token);
           } else {
               alert('Failed to delete review');
           }
       } catch (error) {
           console.error('Error deleting review:', error);
           alert('An error occurred while deleting the review.');
       }
   }
   
   // ==================== AMENITIES MANAGEMENT ====================
   
   async function loadAmenities(token) {
       try {
           const response = await fetch(`${API_BASE_URL}/amenities/`, {
               method: 'GET',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               const amenities = await response.json();
               displayAmenities(amenities);
           } else {
               document.getElementById('amenities-table-body').innerHTML = 
                   '<tr><td colspan="4" class="error">Failed to load amenities</td></tr>';
           }
       } catch (error) {
           console.error('Error loading amenities:', error);
           document.getElementById('amenities-table-body').innerHTML = 
               '<tr><td colspan="4" class="error">Error loading amenities</td></tr>';
       }
   }
   
   function displayAmenities(amenities) {
       const tbody = document.getElementById('amenities-table-body');
       
       if (amenities.length === 0) {
           tbody.innerHTML = '<tr><td colspan="4">No amenities found</td></tr>';
           return;
       }
       
       tbody.innerHTML = amenities.map(amenity => `
           <tr>
               <td>${amenity.id.substring(0, 8)}...</td>
               <td>${amenity.name}</td>
               <td>${new Date(amenity.created_at).toLocaleDateString()}</td>
               <td>
                   <button class="btn-small btn-danger" onclick="deleteAmenity('${amenity.id}')">Delete</button>
               </td>
           </tr>
       `).join('');
   }
   
   function showCreateAmenityModal() {
       document.getElementById('create-amenity-modal').style.display = 'block';
   }
   
   function closeCreateAmenityModal() {
       document.getElementById('create-amenity-modal').style.display = 'none';
       document.getElementById('create-amenity-form').reset();
   }
   
   async function handleCreateAmenity(event) {
       event.preventDefault();
       
       const token = getCookie('token');
       const amenityData = {
           name: document.getElementById('amenity_name').value
       };
   
       try {
           const response = await fetch(`${API_BASE_URL}/amenities/`, {
               method: 'POST',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify(amenityData)
           });
   
           if (response.ok) {
               alert('Amenity created successfully!');
               closeCreateAmenityModal();
               loadAmenities(token);
           } else {
               const errorData = await response.json();
               alert('Failed to create amenity: ' + (errorData.error || response.statusText));
           }
       } catch (error) {
           console.error('Error creating amenity:', error);
           alert('An error occurred while creating the amenity.');
       }
   }
   
   async function deleteAmenity(amenityId) {
       if (!confirm('Are you sure you want to delete this amenity?')) {
           return;
       }
       
       const token = getCookie('token');
       
       try {
           const response = await fetch(`${API_BASE_URL}/amenities/${amenityId}`, {
               method: 'DELETE',
               headers: {
                   'Authorization': `Bearer ${token}`,
                   'Content-Type': 'application/json'
               }
           });
   
           if (response.ok) {
               alert('Amenity deleted successfully!');
               loadAmenities(token);
           } else {
               alert('Failed to delete amenity');
           }
       } catch (error) {
           console.error('Error deleting amenity:', error);
           alert('An error occurred while deleting the amenity.');
       }
   }
   
   // ==================== PAGE INITIALIZATION ====================
   
   document.addEventListener('DOMContentLoaded', () => {
       const token = checkAdminAuth();
       
       // Login page
       const loginForm = document.getElementById('admin-login-form');
       if (loginForm) {
           loginForm.addEventListener('submit', handleAdminLogin);
           return;
       }
       
       if (!token) return;
       
       // Setup logout button
       const logoutBtn = document.getElementById('logout-btn');
       if (logoutBtn) {
           logoutBtn.addEventListener('click', (e) => {
               e.preventDefault();
               logout();
           });
       }
       
       // Dashboard
       if (window.location.pathname.includes('admin/index.html')) {
           loadDashboardStats(token);
       }
       
       // Users page
       if (window.location.pathname.includes('users.html')) {
           loadUsers(token);
           
           const createUserForm = document.getElementById('create-user-form');
           if (createUserForm) {
               createUserForm.addEventListener('submit', handleCreateUser);
           }
       }
       
       // Places page
       if (window.location.pathname.includes('places.html')) {
           loadPlaces(token);
       }
       
       // Reviews page
       if (window.location.pathname.includes('reviews.html')) {
           loadReviews(token);
       }
       
       // Amenities page
       if (window.location.pathname.includes('amenities.html')) {
           loadAmenities(token);
           
           const createAmenityForm = document.getElementById('create-amenity-form');
           if (createAmenityForm) {
               createAmenityForm.addEventListener('submit', handleCreateAmenity);
           }
       }
   });