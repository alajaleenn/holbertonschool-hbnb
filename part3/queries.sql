-- HBnB Sample Queries
-- CREATE: Insert new user
INSERT INTO users (first_name, last_name, email, password) 
VALUES ('Jane', 'Smith', 'jane@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

-- READ: Get all places with owner info
SELECT p.*, u.first_name, u.last_name, u.email
FROM places p
JOIN users u ON p.owner_id = u.id;

-- READ: Get reviews for a place
SELECT r.*, u.first_name, u.last_name
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = '00000000-0000-0000-0000-000000000101';

-- READ: Get amenities for a place
SELECT a.name
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = '00000000-0000-0000-0000-000000000101';

-- UPDATE: Update place price
UPDATE places 
SET price = 275.00 
WHERE title = 'Beautiful Beach House';

-- DELETE: Remove a review
DELETE FROM reviews 
WHERE id = '00000000-0000-0000-0000-000000000203';

-- Advanced: Places with average rating
SELECT p.title, AVG(r.rating) as avg_rating
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title;

-- Advanced: Users with review count
SELECT u.first_name, u.last_name, COUNT(r.id) as review_count
FROM users u
LEFT JOIN reviews r ON u.id = r.user_id
GROUP BY u.id, u.first_name, u.last_name;
EOF
