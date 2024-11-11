import requests
import uuid

BASE_URL = "http://localhost:8000/vehicles"


# Function to generate a random alphanumeric vehicle_id
def generate_random_vehicle_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric vehicle_id


# Test Data
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

updated_vehicle_data = {
    "id": vehicle_data["id"],
    "make": "Toyota",
    "model": "Camry",
    "year": 2021,
    "price": 25000.0,  # Updated price
    "fuel_type": "Gasoline",
    "transmission": "Automatic",
    "body_type": "Sedan",
    "image_url": "http://example.com/toyota_camry_updated.jpg"
}


def test_create_vehicle():
    print("\n--- Testing Create Vehicle API ---")
    response = requests.post(BASE_URL, json=vehicle_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Vehicle creation failed")


def test_get_vehicle(vehicle_id):
    print(f"\n--- Testing Get Vehicle by ID API for vehicle_id: {vehicle_id} ---")
    response = requests.get(f"{BASE_URL}/{vehicle_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Vehicle not found")


def test_get_vehicle_not_found():
    print("\n--- Testing Get Vehicle by ID API for non-existent vehicle_id ---")
    invalid_vehicle_id = "nonexistent123"
    response = requests.get(f"{BASE_URL}/{invalid_vehicle_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print(f"Response: {response.json()}")
    else:
        print("Unexpected response")


def test_update_vehicle(vehicle_id):
    print(f"\n--- Testing Update Vehicle API for vehicle_id: {vehicle_id} ---")
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=updated_vehicle_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Vehicle update failed")


def test_delete_vehicle(vehicle_id):
    print(f"\n--- Testing Delete Vehicle API for vehicle_id: {vehicle_id} ---")
    response = requests.delete(f"{BASE_URL}/{vehicle_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Vehicle successfully deleted")
    else:
        print("Vehicle deletion failed")


if __name__ == "__main__":
    # Run the tests
    print("\n--- Testing Vehicle API ---")
    print("--- Creating a new vehicle ---")
    test_create_vehicle()  # Create a new vehicle

    # Retrieve the vehicle_id from the test data
    vehicle_id = vehicle_data["id"]
    print("--- Retrieving vehicle ---")
    test_get_vehicle(vehicle_id)  # Get the created vehicle

    print("--- Retrieving non-existent vehicle ---")
    test_get_vehicle_not_found()  # Try to retrieve non-existent vehicle

    #print("--- Updating the vehicle ---")
    #test_update_vehicle(vehicle_id)  # Update the created vehicle

    #print("--- Deleting the vehicle ---")
    #test_delete_vehicle(vehicle_id)  # Delete the created vehicle
