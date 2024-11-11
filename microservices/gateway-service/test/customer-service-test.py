import requests
import uuid
from faker import Faker

fake = Faker()

BASE_URL = "http://localhost:8000/customers"

# Function to generate a random alphanumeric userId
def generate_random_user_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric userId

# Function to generate random customer data
def generate_customer_data():
    return {
        "userName": generate_random_user_id(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.unique.email(),
        "phoneNumber": fake.phone_number(),
        "address": fake.address(),
        "profileStatus": fake.random_element(elements=["Active", "Inactive", "Suspended"])
    }

# Test Data
customer_data = generate_customer_data()

# Updated data for testing the update operation with new random data
updated_customer_data = generate_customer_data()

def test_create_customer():
    print("\n--- Testing Create Customer API ---")
    response = requests.post(BASE_URL, json=customer_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return customer_data['userName']  # Return the generated userId for further testing

def test_get_customers():
    print("\n--- Testing Get All Customers API ---")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_customer_by_id(user_id):
    print(f"\n--- Testing Get Customer by ID API for userId: {user_id} ---")
    response = requests.get(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Customer not found")

def test_update_customer(user_id):
    print(f"\n--- Testing Update Customer API for userId: {user_id} ---")
    response = requests.put(f"{BASE_URL}/{user_id}", json=updated_customer_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Customer update failed")

def test_delete_customer(user_id):
    print(f"\n--- Testing Delete Customer API for userId: {user_id} ---")
    response = requests.delete(f"{BASE_URL}/{user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Customer deleted successfully")
    else:
        print("Customer deletion failed")

if __name__ == "__main__":
    # Run the tests
    user_id = test_create_customer()  # Generate a random userId during customer creation
    test_get_customers()
    test_get_customer_by_id(user_id)
    test_update_customer(user_id)
    test_get_customer_by_id(user_id)  # Check updated customer details
    test_delete_customer(user_id)
    test_get_customers()  # Check remaining customers
