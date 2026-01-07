from app.services.facade import HBnBFacade

facade = HBnBFacade()

# Test 1: Create a user
print("Test 1: Creating user...")
user_data = {
    "first_name": "Test",
    "last_name": "User", 
    "email": "test@debug.com"
}
user = facade.create_user(user_data)
print(f"Created user with ID: {user.id}")

# Test 2: Try to get the user
print("\nTest 2: Getting user...")
retrieved_user = facade.get_user(user.id)
if retrieved_user:
    print(f"Success! Found user: {retrieved_user.first_name}")
else:
    print("FAILED! User not found")

# Test 3: Check what's in storage
print("\nTest 3: Checking repository storage...")
print(f"Storage keys: {list(facade.repository._storage.keys())}")
for key in facade.repository._storage:
    print(f"{key}: {len(facade.repository._storage[key])} objects")
