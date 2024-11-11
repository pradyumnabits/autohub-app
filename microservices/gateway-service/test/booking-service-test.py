import asyncio
import httpx
from datetime import date
from faker import Faker
import random

fake = Faker()
BASE_URL = "http://localhost:8000"

CUSTOMER_BASE_URL = "http://localhost:8007"


# Generate a random customer
async def test_create_customer():
    customer_data = {
        "userName": f"U{random.randint(1000, 9999)}",
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phoneNumber": fake.phone_number(),
        "address": fake.address(),
        "profileStatus": random.choice(["ACTIVE", "INACTIVE"])
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CUSTOMER_BASE_URL}/customers", json=customer_data)
        print("Create Customer Response:", response.json())
        assert response.status_code == 201

    # Return generated username for further tests
    return customer_data["userName"]


# Generate a random test drive
async def test_create_test_drive(user_name):
    test_drive_data = {
        "vehicle_id": f"V{random.randint(100, 999)}",
        "user_name": user_name,
        "date": str(date.today()),
        "time": f"{random.randint(8, 18)}:00",
        "status": random.choice(["Confirmed", "Pending", "Canceled"])
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/testdrives/book", json=test_drive_data)
        print("Create Test Drive Response:", response.json())
        assert response.status_code == 201

    # Return generated vehicle_id for further tests
    return test_drive_data["vehicle_id"]


# Get all test drives
async def test_get_all_test_drives():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives")
        print("All Test Drives:", response.json())
        assert response.status_code == 200


# Get test drive by ID
async def test_get_test_drive_by_id(test_drive_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives/{test_drive_id}")
        print("Test Drive by ID:", response.json())
        assert response.status_code == 200


# Generate a random booking
async def test_create_booking(user_name, vehicle_id):
    booking_data = {
        "user_name": user_name,
        "vehicle_id": vehicle_id,
        "transaction_id": f"TXN{random.randint(1000, 9999)}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/bookings", json=booking_data)
        print("Create Booking Response:", response.json())
        assert response.status_code == 201

    # Return generated booking ID for further tests
    return response.json().get("id")  # Assuming the response contains an ID


# Get all bookings for a user
async def test_get_user_bookings(user_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings?user_name={user_name}")
        print("User Bookings:", response.json())
        assert response.status_code == 200


# Get booking by ID
async def test_get_booking_by_id(booking_id):
    async with httpx.AsyncClient() as client:
        print("Get Bookings for Id:", f"{BASE_URL}/bookings/{booking_id}")
        response = await client.get(f"{BASE_URL}/bookings/{booking_id}")
        print("Booking by ID:", response.json())
        assert response.status_code == 200


# Main function to run tests
async def main():
    # Create customer and get the username
    user_name = await test_create_customer()

    # Create a test drive with the generated customer username and get the vehicle ID
    vehicle_id = await test_create_test_drive(user_name)

    # Run other test functions
    await test_get_all_test_drives()
    await test_get_test_drive_by_id(1)  # Adjust with a valid test drive ID

    # Create a booking with the generated customer username and vehicle ID
    booking_id = await test_create_booking(user_name, vehicle_id)

    # Retrieve bookings by user and by booking ID
    await test_get_user_bookings(user_name)
    #await test_get_booking_by_id(booking_id)


# Run the tests
if __name__ == "__main__":
    asyncio.run(main())
