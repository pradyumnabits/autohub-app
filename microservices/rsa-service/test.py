import requests
import uuid
from faker import Faker

fake = Faker()

# Base URLs for customer and vehicle APIs
CUSTOMER_BASE_URL = "http://localhost:8007/customers"
VEHICLE_BASE_URL = "http://localhost:8002/vehicles"
BASE_URL = "http://localhost:8005/rsa"


# Function to generate a random alphanumeric userId (simulating vehicle or user ID)
def generate_random_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric ID

def generate_random_vehicle_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric vehicle_id

# Test Data for Vehicle
vehicle_data = {
    "id": generate_random_vehicle_id(),
    "make": "Toyota",
    "model": "Camry",
    "year": 2021,
    "price": 24000.0,
    "fuel_type": "Gasoline",
    "transmission": "Automatic",
    "body_type": "Sedan",
    "image_url": "http://example.com/toyota_camry.jpg"
}

# Test Data for Request
request_data = {
    "user_id": "",  # Will be filled dynamically after creating customer
    "vehicle_id": "",  # Will be filled dynamically after creating vehicle
    "location": "123 Main St",
    "contact_number": "555-1234",  # Assuming these fields are required
    "assistance_type": "Towing"    # Assuming this field is required
}

updated_request_data = {
    "location": "456 Oak Avenue, Springfield, USA"  # Update location
}

# Function to generate random customer data
def generate_customer_data():
    return {
        "userName": generate_random_id(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.unique.email(),
        "phoneNumber": fake.phone_number(),
        "address": fake.address(),
        "profileStatus": fake.random_element(elements=["Active", "Inactive", "Suspended"])
    }

# Function to create customer
def test_create_customer():
    print("\n--- Testing Create Customer API ---")
    customer_data = generate_customer_data()
    response = requests.post(CUSTOMER_BASE_URL, json=customer_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 201:
        return customer_data['userName']  # Return the generated userName for further testing
    else:
        print("Customer creation failed")
        return None

# Function to create vehicle
def test_create_vehicle():
    print("\n--- Testing Create Vehicle API ---")
    response = requests.post(VEHICLE_BASE_URL, json=vehicle_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        print(f"Response: {response.json()}")
        return response.json()['id']  # Return the generated vehicle id
    else:
        print("Vehicle creation failed")
        return None

# Function to create request
def test_create_request(user_id, vehicle_id):
    request_data["user_id"] = user_id  # Fill user_id dynamically
    request_data["vehicle_id"] = vehicle_id  # Fill vehicle_id dynamically
    
    print("\n--- Testing Create Request API ---")
    response = requests.post(f"{BASE_URL}/requests", json=request_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:  # Assuming 201 is the status for successful creation
        print(f"Response: {response.json()}")
        return response.json().get('id')  # Get requestId (not userId) from the response
    else:
        print("Request creation failed:", response.text)
        return None  # Return None if creation failed

# Function to fetch all requests for a specific user
def test_get_all_requests(user_id):
    print("\n--- Testing Get All Requests API ---")
    response = requests.get(f"{BASE_URL}/requests", params={"userId": user_id})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Failed to retrieve requests:", response.text)

# Function to fetch request by ID
def test_get_request_by_id(request_id):
    print(f"\n--- Testing Get Request by ID API for requestId: {request_id} ---")
    response = requests.get(f"{BASE_URL}/requests/{request_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Request not found:", response.text)

# Function to update request by ID
def test_update_request(request_id):
    print(f"\n--- Testing Update Request API for requestId: {request_id} ---")
    response = requests.put(f"{BASE_URL}/requests/{request_id}", json=updated_request_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Request update failed:", response.text)

# Function to delete request by ID
def test_delete_request(request_id):
    print(f"\n--- Testing Delete Request API for requestId: {request_id} ---")
    response = requests.delete(f"{BASE_URL}/requests/{request_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Request deleted successfully")
    else:
        print("Request deletion failed:", response.text)

# Main flow
if __name__ == "__main__":
    user_id = test_create_customer()  # Create customer and get user_id
    if user_id:  # Only proceed if customer was created
        vehicle_id = test_create_vehicle()  # Create vehicle and get vehicle_id
        if vehicle_id:  # Only proceed if vehicle was created
            request_id = test_create_request(user_id, vehicle_id)  # Create request with customer and vehicle
            if request_id:  # Only proceed if request was created
                test_get_all_requests(user_id)  # Retrieve all requests for user
                test_get_request_by_id(request_id)  # Retrieve request by ID
                test_update_request(request_id)  # Update request by ID
                test_get_request_by_id(request_id)  # Check updated request details
                # Uncomment if delete route is implemented
                # test_delete_request(request_id)
                test_get_all_requests(user_id)  # Check remaining requests after deletion
