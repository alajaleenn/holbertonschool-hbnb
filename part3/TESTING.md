# HBnB API Testing Documentation

This document provides comprehensive testing instructions for all API endpoints in the HBnB application.

## Prerequisites

- Flask application running on `http://127.0.0.1:5003`
- `curl` installed for command-line testing
- `jq` (optional) for formatted JSON output

## Testing Overview

The API has 4 main entity endpoints:
1. Users
2. Amenities
3. Places
4. Reviews

---

## 1. User Endpoints

### Create a User (POST)
```bash
curl -X POST http://127.0.0.1:5003/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false
  }'
```

**Expected Response (201):**
```json
{
  "id": "uuid-here",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Validation Tests:**
```bash
# Test: Empty first name (400)
curl -X POST http://127.0.0.1:5003/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "",
    "last_name": "Doe",
    "email": "test@example.com"
  }'

# Test: Invalid email format (400)
curl -X POST http://127.0.0.1:5003/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "invalid-email"
  }'

# Test: Duplicate email (400)
curl -X POST http://127.0.0.1:5003/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "john.doe@example.com"
  }'
```

### Get All Users (GET)
```bash
curl http://127.0.0.1:5003/api/v1/users/
```

**Expected Response (200):**
```json
[
  {
    "id": "uuid-1",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Get User by ID (GET)
```bash
# Replace {user_id} with actual user ID
curl http://127.0.0.1:5003/api/v1/users/{user_id}
```

**Validation Tests:**
```bash
# Test: Non-existent user (404)
curl http://127.0.0.1:5003/api/v1/users/invalid-id
```

### Update User (PUT)
```bash
# Replace {user_id} with actual user ID
curl -X PUT http://127.0.0.1:5003/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
  }'
```

**Expected Response (200):**
```json
{
  "id": "uuid-here",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

## 2. Amenity Endpoints

### Create an Amenity (POST)
```bash
curl -X POST http://127.0.0.1:5003/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi"
  }'
```

**Expected Response (201):**
```json
{
  "id": "uuid-here",
  "name": "WiFi",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Validation Tests:**
```bash
# Test: Empty name (400)
curl -X POST http://127.0.0.1:5003/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'

# Test: Name too long (400)
curl -X POST http://127.0.0.1:5003/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "This is a very long amenity name that exceeds fifty characters limit"}'
```

### Get All Amenities (GET)
```bash
curl http://127.0.0.1:5003/api/v1/amenities/
```

### Get Amenity by ID (GET)
```bash
# Replace {amenity_id} with actual amenity ID
curl http://127.0.0.1:5003/api/v1/amenities/{amenity_id}
```

### Update Amenity (PUT)
```bash
# Replace {amenity_id} with actual amenity ID
curl -X PUT http://127.0.0.1:5003/api/v1/amenities/{amenity_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High-Speed WiFi"
  }'
```

---

## 3. Place Endpoints

### Create a Place (POST)
```bash
# Replace {user_id} with actual user ID
curl -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A lovely apartment in the city center",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "{user_id}"
  }'
```

**Expected Response (201):**
```json
{
  "id": "uuid-here",
  "title": "Cozy Apartment",
  "description": "A lovely apartment in the city center",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "user-uuid",
  "reviews": [],
  "amenities": [],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Validation Tests:**
```bash
# Test: Negative price (400)
curl -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "Test",
    "price": -50,
    "latitude": 0,
    "longitude": 0,
    "owner_id": "{user_id}"
  }'

# Test: Invalid latitude (400)
curl -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "Test",
    "price": 100,
    "latitude": 100,
    "longitude": 0,
    "owner_id": "{user_id}"
  }'

# Test: Invalid longitude (400)
curl -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "Test",
    "price": 100,
    "latitude": 0,
    "longitude": 200,
    "owner_id": "{user_id}"
  }'

# Test: Non-existent owner (404)
curl -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Place",
    "description": "Test",
    "price": 100,
    "latitude": 0,
    "longitude": 0,
    "owner_id": "invalid-id"
  }'
```

### Get All Places (GET)
```bash
curl http://127.0.0.1:5003/api/v1/places/
```

### Get Place by ID (GET)
```bash
# Replace {place_id} with actual place ID
curl http://127.0.0.1:5003/api/v1/places/{place_id}
```

### Update Place (PUT)
```bash
# Replace {place_id} with actual place ID
curl -X PUT http://127.0.0.1:5003/api/v1/places/{place_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Cozy Apartment",
    "description": "An updated description",
    "price": 120.0
  }'
```

---

## 4. Review Endpoints

### Create a Review (POST)
```bash
# Replace {place_id} and {user_id} with actual IDs
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place! Very comfortable and clean.",
    "rating": 5,
    "place_id": "{place_id}",
    "user_id": "{user_id}"
  }'
```

**Expected Response (201):**
```json
{
  "id": "uuid-here",
  "text": "Great place! Very comfortable and clean.",
  "rating": 5,
  "place_id": "place-uuid",
  "user_id": "user-uuid",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Validation Tests:**
```bash
# Test: Invalid rating - too low (400)
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test review",
    "rating": 0,
    "place_id": "{place_id}",
    "user_id": "{user_id}"
  }'

# Test: Invalid rating - too high (400)
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test review",
    "rating": 6,
    "place_id": "{place_id}",
    "user_id": "{user_id}"
  }'

# Test: Empty text (400)
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "",
    "rating": 5,
    "place_id": "{place_id}",
    "user_id": "{user_id}"
  }'

# Test: Non-existent place (404)
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test review",
    "rating": 5,
    "place_id": "invalid-id",
    "user_id": "{user_id}"
  }'

# Test: Non-existent user (404)
curl -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test review",
    "rating": 5,
    "place_id": "{place_id}",
    "user_id": "invalid-id"
  }'
```

### Get All Reviews (GET)
```bash
curl http://127.0.0.1:5003/api/v1/reviews/
```

### Get Review by ID (GET)
```bash
# Replace {review_id} with actual review ID
curl http://127.0.0.1:5003/api/v1/reviews/{review_id}
```

### Update Review (PUT)
```bash
# Replace {review_id} with actual review ID
curl -X PUT http://127.0.0.1:5003/api/v1/reviews/{review_id} \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated review text",
    "rating": 4
  }'
```

**Expected Response (200):**
```json
{
  "id": "uuid-here",
  "text": "Updated review text",
  "rating": 4,
  "place_id": "place-uuid",
  "user_id": "user-uuid",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### Delete Review (DELETE)
```bash
# Replace {review_id} with actual review ID
curl -X DELETE http://127.0.0.1:5003/api/v1/reviews/{review_id}
```

**Expected Response (204):**
No content (empty response body)

**Validation Tests:**
```bash
# Test: Delete non-existent review (404)
curl -X DELETE http://127.0.0.1:5003/api/v1/reviews/invalid-id
```

---

## Complete Testing Workflow

Here's a complete workflow to test all endpoints in sequence:
```bash
# 1. Create a user
USER_RESPONSE=$(curl -s -X POST http://127.0.0.1:5003/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com"
  }')

USER_ID=$(echo $USER_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created User ID: $USER_ID"

# 2. Create amenities
AMENITY1=$(curl -s -X POST http://127.0.0.1:5003/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')

AMENITY1_ID=$(echo $AMENITY1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created Amenity ID: $AMENITY1_ID"

# 3. Create a place
PLACE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5003/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"description\": \"A test place\",
    \"price\": 100.0,
    \"latitude\": 37.7749,
    \"longitude\": -122.4194,
    \"owner_id\": \"$USER_ID\"
  }")

PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created Place ID: $PLACE_ID"

# 4. Create a review
REVIEW_RESPONSE=$(curl -s -X POST http://127.0.0.1:5003/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Great place!\",
    \"rating\": 5,
    \"place_id\": \"$PLACE_ID\",
    \"user_id\": \"$USER_ID\"
  }")

REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created Review ID: $REVIEW_ID"

# 5. Get all entities
echo -e "\n=== All Users ==="
curl -s http://127.0.0.1:5003/api/v1/users/

echo -e "\n=== All Amenities ==="
curl -s http://127.0.0.1:5003/api/v1/amenities/

echo -e "\n=== All Places ==="
curl -s http://127.0.0.1:5003/api/v1/places/

echo -e "\n=== All Reviews ==="
curl -s http://127.0.0.1:5003/api/v1/reviews/

# 6. Update review
echo -e "\n=== Update Review ==="
curl -s -X PUT http://127.0.0.1:5003/api/v1/reviews/$REVIEW_ID \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated review!", "rating": 4}'

# 7. Delete review
echo -e "\n=== Delete Review ==="
curl -s -X DELETE http://127.0.0.1:5003/api/v1/reviews/$REVIEW_ID
```

---

## Validation Summary

### User Validation
- ✅ First name: Required, non-empty, max 50 chars
- ✅ Last name: Required, non-empty, max 50 chars
- ✅ Email: Required, valid format, unique
- ✅ Duplicate email check

### Amenity Validation
- ✅ Name: Required, non-empty, max 50 chars

### Place Validation
- ✅ Title: Required, non-empty, max 100 chars
- ✅ Description: Required, non-empty
- ✅ Price: Required, positive number
- ✅ Latitude: Required, -90 to 90
- ✅ Longitude: Required, -180 to 180
- ✅ Owner must exist

### Review Validation
- ✅ Text: Required, non-empty, max 500 chars
- ✅ Rating: Required, integer 1-5
- ✅ Place must exist
- ✅ User must exist

---

## Status Codes Reference

- **200 OK** - Successful GET, PUT
- **201 Created** - Successful POST
- **204 No Content** - Successful DELETE
- **400 Bad Request** - Validation error
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

---

## Notes

- All endpoints return JSON
- Timestamps are in ISO 8601 format
- IDs are UUID4 strings
- The DELETE operation is only available for reviews
- All data is stored in memory and will be lost when the app restarts
