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
    first_name = fake.first_name()  # Generate a random first name
    last_name = fake.last_name()    # Generate a random last name
    phone_number = fake.phone_number()  # Generate a random phone number
    address = fake.address()         # Generate a random address

    url = f"{BASE_URL}/auth/register"
    payload = {
        "userName": username,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    response = requests.post(url, json=payload)

    print("HTTP Status Code:", response.status_code)
    if response.status_code == 201:
        print("Register Test Passed:", response.json())
    elif response.status_code == 400:
        print("Register Test Failed - Username already exists:", response.json())
    else:
        print("Register Test Failed with unexpected status code:", response.status_code, response.text)

    # Assert that the response status code is 201 (Created) for successful registration
    assert response.status_code == 201, "Expected status code 201 for successful registration."

# Function to test user login with the same credentials as registration
def test_login_user():
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
    address = fake.address()

    # First register the user to be able to login
    register_payload = {
        "userName": username,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    # Register the user
    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_payload)
    print("Registration HTTP Status Code:", register_response.status_code)

    if register_response.status_code != 201:  # Updated to check for 201 Created
        print("Registration failed:", register_response.json())
        return

    # Now attempt to log in with the same credentials
    login_payload = {
        "userName": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    print("Login HTTP Status Code:", response.status_code)

    # Check if the response is 200 and print relevant information
    if response.status_code == 200:
        print("Login Test Passed:", response.json())
        token = response.json().get("token")  # Ensure your login response includes a token
        print("Token:", token)
    elif response.status_code == 400:
        print("Login Test Failed - Invalid credentials:", response.json())
    else:
        print("Login Test Failed with unexpected status code:", response.status_code, response.text)

    # Assert that the login response status code is 200 (OK) for successful login
    assert response.status_code == 200, "Expected status code 200 for successful login."

# Function to test invalid login with incorrect credentials
def test_invalid_login_user():
    # Generate random credentials that are not registered
    login_payload = {
        "userName": "invalid_user",
        "password": "wrong_password"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    print("Invalid Login HTTP Status Code:", response.status_code)

    # Check if the response is 400 and print relevant information
    if response.status_code == 400:
        print("Invalid Login Test Passed - Correctly handled invalid credentials:", response.json())
    else:
        print("Invalid Login Test Failed with unexpected status code:", response.status_code, response.text)

    # Assert that the login response status code is 400 (Bad Request) for invalid login
    assert response.status_code == 400, "Expected status code 400 for invalid login attempt."


# Function to test user registration with invalid data
def test_register_user_invalid_request():
    # Creating a payload with missing fields
    payload = {
        "userName": fake.user_name(),
        # "password" field is intentionally left out to simulate invalid request
        "email": fake.email(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "phoneNumber": fake.phone_number(),
        "address": fake.address()
    }

    url = f"{BASE_URL}/auth/register"
    response = requests.post(url, json=payload)

    print("Invalid Registration HTTP Status Code:", response.status_code)
    if response.status_code == 422:
        print("Invalid Registration Test Passed - Correctly handled missing fields:", response.json())
    else:
        print("Invalid Registration Test Failed with unexpected status code:", response.status_code, response.text)

    # Assert that the response status code is 422 (Unprocessable Entity) for invalid registration
    assert response.status_code == 422, "Expected status code 422 for invalid registration attempt."

# Run the tests
if __name__ == "__main__":
    print("Testing User Registration API with Valid Data:")
    test_register_user()

    print("\nTesting User Registration API with Invalid Request:")
    test_register_user_invalid_request()

    print("\nTesting User Login API with Valid Data:")
    test_login_user()

    print("\nTesting Invalid Login API:")
    test_invalid_login_user()

