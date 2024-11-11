import requests
import uuid

BASE_URL = "http://localhost:8000/rsa/requests"

# Function to generate a random alphanumeric userId (simulating vehicle or user ID)
def generate_random_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric ID

# Test Data
request_data = {
    "user_id": generate_random_id(),  # Random alphanumeric userId
    "vehicle_id": generate_random_id(),  # Random vehicleId
    "location": "123 Main St"
}

updated_request_data = {
    "location": "456 Oak Avenue, Springfield, USA"  # Update location
}

def test_create_request():
    print("\n--- Testing Create Request API ---")
    response = requests.post(BASE_URL, json=request_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:  # Assuming 201 is the status for successful creation
        print(f"Response: {response.json()}")
        return response.json().get('user_id')  # Get userId from the response
    else:
        print("Request creation failed:", response.text)
        return None  # Return None if creation failed

def test_get_all_requests():
    print("\n--- Testing Get All Requests API ---")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Failed to retrieve requests:", response.text)

def test_get_request_by_id(user_id):
    print(f"\n--- Testing Get Request by ID API for userId: {user_id} ---")
    response = requests.get(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Request not found:", response.text)

def test_update_request(user_id):
    print(f"\n--- Testing Update Request API for userId: {user_id} ---")
    response = requests.put(f"{BASE_URL}/{user_id}", json=updated_request_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Request update failed:", response.text)

def test_delete_request(user_id):
    print(f"\n--- Testing Delete Request API for userId: {user_id} ---")
    response = requests.delete(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Request deleted successfully")
    else:
        print("Request deletion failed:", response.text)

if __name__ == "__main__":
    # Run the tests
    user_id = test_create_request()  # Generate a random userId during request creation
    if user_id:  # Only proceed if creation was successful
        test_get_all_requests()
        test_get_request_by_id(user_id)
        test_update_request(user_id)
        test_get_request_by_id(user_id)  # Check updated request details
        #test_delete_request(user_id)
        test_get_all_requests()  # Check remaining requests
