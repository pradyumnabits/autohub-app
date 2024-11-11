import asyncio
import httpx
from datetime import date

BASE_URL = "http://localhost:8000"


# Create a customer
async def test_create_customer():
    customer_data = {
        "userName": "U001",  # Updated field name
        "firstName": "John",  # Updated field name
        "lastName": "Doe",    # Updated field name
        "email": "john.doe@example.com",
        "phoneNumber": "1234567890",  # Updated field name
        "address": "123 Main St",      # Optional field
        "profileStatus": "ACTIVE"       # Optional field with default value
    }


    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/customers", json=customer_data)
        print("Create Customer Response:", response.json())
        assert response.status_code == 201  # Assuming that 201 is the expected response status for a successful creation


# Create a test drive
async def test_create_test_drive():
    test_drive_data = {
        "vehicle_id": "V001",
        "user_name": "U001",  # Updated field name
        "date": str(date.today()),
        "time": "10:00",
        "status": "Confirmed"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/testdrives/book", json=test_drive_data)
        print("Create Test Drive Response:", response.json())
        assert response.status_code == 201


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


# Create a booking
async def test_create_booking():
    # Step 1: Create a customer
    customer_data = {
        "user_name": "U001",  # Updated field name
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890"
    }

    async with httpx.AsyncClient() as client:
        # Call to create customer
        customer_response = await client.post(f"{BASE_URL}/customers", json=customer_data)
        print("Create Customer Response:", customer_response.json())
        assert customer_response.status_code == 201  # Check for successful customer creation

    # Step 2: Create a booking
    booking_data = {
        "user_name": "U001",  # Updated field name
        "vehicle_id": "V001",
        "transaction_id": "TXN001"
    }

    async with httpx.AsyncClient() as client:
        # Call to create booking
        response = await client.post(f"{BASE_URL}/bookings", json=booking_data)
        print("Create Booking Response:", response.json())
        assert response.status_code == 201  # Check for successful booking creation


# Get all bookings for a user
async def test_get_user_bookings(user_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings?user_name={user_name}")  # Updated field name
        print("User Bookings:", response.json())
        assert response.status_code == 200


# Get booking by ID
async def test_get_booking_by_id(booking_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings/{booking_id}")
        print("Booking by ID:", response.json())
        assert response.status_code == 200


# Main function to run tests
async def main():
    await test_create_customer()  # Create the customer first
    await test_create_test_drive()
    await test_get_all_test_drives()
    await test_get_test_drive_by_id(1)  # Test with a valid ID (assumes ID 1 exists)
    await test_create_booking()  # Now that the customer exists, create a booking
    await test_get_user_bookings("U001")  # Test with the user name
    await test_get_booking_by_id(1)  # Test with a valid booking ID (assumes ID 1 exists)


# Run the tests
if __name__ == "__main__":
    asyncio.run(main())
