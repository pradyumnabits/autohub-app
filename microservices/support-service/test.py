import requests
from faker import Faker
import uuid

# Base URLs for customer, vehicle, and service APIs
CUSTOMER_BASE_URL = "http://127.0.0.1:8007/customers"
VEHICLE_BASE_URL = "http://127.0.0.1:8002/vehicles"
BASE_URL = "http://127.0.0.1:8004"

fake = Faker()

# Function to generate a random alphanumeric ID
def generate_random_id():
    return str(uuid.uuid4())[:8]  # Short alphanumeric ID

# Generate random customer data
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

# Vehicle data
vehicle_data = {
    "id": generate_random_id(),
    "make": "Toyota",
    "model": "Camry",
    "year": 2021,
    "price": 24000.0,
    "fuel_type": "Gasoline",
    "transmission": "Automatic",
    "body_type": "Sedan",
    "image_url": "http://example.com/toyota_camry.jpg"
}

# Function to create customer
def create_customer():
    print("Creating Customer...")
    customer_data = generate_customer_data()
    response = requests.post(CUSTOMER_BASE_URL, json=customer_data)
    if response.status_code == 201:
        print(f"Customer created: {response.json()}")
        # Use 'userName' instead of 'id' if 'userName' is the unique identifier
        return response.json()['userName']
    else:
        print(f"Failed to create customer: {response.status_code}, {response.json()}")
        return None

# Function to create vehicle
def create_vehicle():
    print("Creating Vehicle...")
    response = requests.post(VEHICLE_BASE_URL, json=vehicle_data)
    if response.status_code == 201:
        print(f"Vehicle created: {response.json()}")
        return response.json()['id']  # Ensure 'id' is the key for vehicle ID
    else:
        print(f"Failed to create vehicle: {response.status_code}, {response.json()}")
        return None

# Test Service Appointment Scheduling
def test_schedule_service():
    print("\n--- Testing Service Appointment Scheduling ---")
    user_id = create_customer()
    vehicle_id = create_vehicle()

    if user_id and vehicle_id:
        payload = {
            "user_id": user_id,
            "vehicle_id": vehicle_id,
            "appointment_date": "2023-09-15",
            "service_type": "Oil Change"
        }
        response = requests.post(f"{BASE_URL}/service/schedule", json=payload)
        print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")
    else:
        print("Could not schedule service due to missing user or vehicle ID.\n")

# Test Service History Retrieval
def test_get_service_history():
    print("\n--- Testing Service History Retrieval ---")
    user_id = create_customer()  # Generate a new user for this test
    response = requests.get(f"{BASE_URL}/service/history?user_id={user_id}")
    print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")

# Test List Service Appointments
def test_list_service_appointments():
    print("\n--- Testing List Service Appointments ---")
    response = requests.get(f"{BASE_URL}/service/appointments")
    print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")

# Run tests
if __name__ == "__main__":
    test_schedule_service()
    test_list_service_appointments()
