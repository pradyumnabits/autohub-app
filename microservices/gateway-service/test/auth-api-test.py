import requests
from faker import Faker

BASE_URL = "http://localhost:8000"

# Initialize Faker
fake = Faker()

# Function to test user registration with random data
def test_register_user():
    userName = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
    address = fake.address()

    url = f"{BASE_URL}/auth/register"
    payload = {
        "userName": userName,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    # Debugging output: print the request URL and payload
    print("Register Request URL:", url)
    print("Register Request Payload:", payload)

    response = requests.post(url, json=payload)

    # Debugging output: print the response
    print("Register Response Status Code:", response.status_code)
    print("Register Response Text:", response.text)

    if response.status_code == 200:
        print("Register Test Passed:", response.json())
    elif response.status_code == 400:
        print("Register Test Failed - UserName already exists:", response.json())
    else:
        print("Register Test Failed with unexpected status code:", response.status_code, response.text)


# Function to test user login with the same credentials as registration
def test_login_user():
    # Using the same data as the last registered user for login
    userName = fake.user_name()
    password = fake.password()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone_number = fake.phone_number()
    address = fake.address()

    # First register the user to be able to login
    register_payload = {
        "userName": userName,
        "password": password,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "address": address
    }

    # Register the user
    register_url = f"{BASE_URL}/auth/register"
    print("Register Request URL:", register_url)
    print("Register Request Payload:", register_payload)
    register_response = requests.post(register_url, json=register_payload)

    if register_response.status_code != 200:
        print("Registration failed:", register_response.json())
        return

    # Now attempt to log in with the same credentials
    login_payload = {
        "userName": userName,
        "password": password
    }

    login_url = f"{BASE_URL}/auth/login"
    print("Login Request URL:", login_url)
    print("Login Request Payload:", login_payload)

    response = requests.post(login_url, json=login_payload)

    # Debugging output: print the response
    print("Login Response Status Code:", response.status_code)
    print("Login Response Text:", response.text)

    if response.status_code == 200:
        print("Login Test Passed:", response.json())
        # Extract and print the token
        token = response.json().get("token")  # Adjust based on your actual response structure
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
