import requests

BASE_URL = "http://127.0.0.1:8004"  # Change if your FastAPI server is running on a different host/port

def test_schedule_service():
    print("Testing Service Appointment Scheduling...")
    payload = {
        "user_id": "5001",
        "vehicle_id": "101",
        "appointment_date": "2023-09-15",
        "service_type": "Oil Change"
    }
    response = requests.post(f"{BASE_URL}/service/schedule", json=payload)
    print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")

def test_get_service_history():
    print("Testing Service History Retrieval...")
    user_id = "5001"
    response = requests.get(f"{BASE_URL}/service/history?user_id={user_id}")
    print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")

def test_list_service_appointments():
    print("Testing List Service Appointments...")
    response = requests.get(f"{BASE_URL}/service/appointments")
    print(f"Response Code: {response.status_code}, Response Body: {response.json()}\n")

if __name__ == "__main__":
    test_schedule_service()
    test_get_service_history()
    test_list_service_appointments()
