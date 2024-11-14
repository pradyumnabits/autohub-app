import requests
import uuid

BASE_URL = "http://localhost:8006/feedback"


# Function to generate a random alphanumeric feedback_id
def generate_random_feedback_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric feedback_id


# Test Data
feedback_data = {
    "user_id": generate_random_feedback_id(),  # Random alphanumeric userId
    "feedback_type": "vehicle",
    "reference_id": "101",
    "details": "The vehicle is excellent, but the service needs improvement.",
    "rating": 4,
}

updated_feedback_data = {
    "user_id": generate_random_feedback_id(),
    "feedback_type": "service",
    "reference_id": "102",
    "details": "The service was slow and unresponsive.",
    "rating": 2,
}


def test_submit_feedback():
    print("\n--- Testing Submit Feedback API ---")
    response = requests.post(f"{BASE_URL}/submit", json=feedback_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        print(f"Response: {response.json()}")
        return response.json()[
            "feedback_id"
        ]  # Return the generated feedback_id for further testing
    else:
        print("Feedback submission failed")
        return None


def test_get_feedback_by_id(feedback_id):
    print(f"\n--- Testing Get Feedback by ID API for feedback_id: {feedback_id} ---")
    response = requests.get(f"{BASE_URL}/{feedback_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print("Feedback not found")


def test_get_feedback_not_found():
    print("\n--- Testing Get Feedback by ID API for non-existent feedback_id ---")
    invalid_feedback_id = "nonexistent123"
    response = requests.get(f"{BASE_URL}/{invalid_feedback_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print(f"Response: {response.json()}")
    else:
        print("Unexpected response")


def test_submit_invalid_feedback():
    print("\n--- Testing Submit Invalid Feedback ---")
    invalid_feedback_data = {
        "user_id": "",  # Missing required fields like feedback_type, details, and rating
        "details": "",
    }
    response = requests.post(f"{BASE_URL}/submit", json=invalid_feedback_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 422:
        print(f"Success")
        #print(f"Response: {response.json()}")
    else:
        print("Unexpected response for invalid feedback")


# def test_submit_invalid_feedback():
#     print("\n--- Testing Submit Invalid Feedback ---")
#     invalid_feedback_data = {
#         "user_id": "",  # Missing required fields like feedback_type, details, and rating
#         "details": ""
#     }
#     response = requests.post(f"{BASE_URL}/submit", json=invalid_feedback_data)
#     print(f"Status Code: {response.status_code}")
#     if response.status_code == 422:  # Change expected status to 422
#         print(f"Response: {response.json()}")
#     else:
#         print("Unexpected response for invalid feedback")


if __name__ == "__main__":
    # Run the tests
    print("\n--- Testing Customer Feedback API ---")
    print("--- Submitting feedback ---")
    feedback_id = test_submit_feedback()  # Submit feedback and get feedback_id
    if feedback_id:
        print("--- Retrieving feedback ---")
        test_get_feedback_by_id(feedback_id)  # Retrieve the submitted feedback by ID
    print("--- Retrieving feedback by ID not found ---")
    test_get_feedback_not_found()  # Try to retrieve non-existent feedback
    print("--- Submitting invalid feedback ---")
    test_submit_invalid_feedback()  # Submit invalid feedback to test error handling
