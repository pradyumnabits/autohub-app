import requests
from faker import Faker

BASE_URL = "http://localhost:8001"

# Initialize Faker
fake = Faker()


# Function to test user registration with random data
def test_register_user():
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()   # Generate a random first name
    last_name = fake.last_name()     # Generate a random last name
    phone_number = fake.phone_number()  # Generate a random phone number
    address = fake.address()          # Generate a random address

    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": username,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Register Test Passed:", response.json())
    elif response.status_code == 400:
        print("Register Test Failed - Username already exists:", response.json())
    else:
        print("Register Test Failed with unexpected status code:", response.status_code, response.text)


# Function to test user login with the same credentials as registration
def test_login_user():
    # Using the same data as the last registered user for login
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
    address = fake.address()

    # First register the user to be able to login
    register_payload = {
        "username": username,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    # Register the user
    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_payload)

    if register_response.status_code != 200:
        print("Registration failed:", register_response.json())
        return

    # Now attempt to log in with the same credentials
    login_payload = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)

    if response.status_code == 200:
        print("Login Test Passed:", response.json())
        # Adjust based on your actual response structure
        token = response.json().get("token")  # Ensure your login response includes a token
        print("Token:", token)
    elif response.status_code == 400:
        print("Login Test Failed - Invalid credentials:", response.json())
    else:
        print("Login Test Failed with unexpected status code:", response.status_code, response.text)


# Run the tests
if __name__ == "__main__":
    print("Testing User Registration API:")
    test_register_user()

    print("\nTesting User Login API:")
    test_login_user()
