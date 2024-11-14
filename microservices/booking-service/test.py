import asyncio
import httpx
import random
import uuid  # Import uuid to generate random vehicle IDs
from datetime import date
from faker import Faker

# Initialize Faker to generate random data
fake = Faker()

# URLs for the services
BASE_URL = "http://localhost:8003"
CUSTOMER_SVC_URL = "http://localhost:8007"
VEHICLE_SVC_URL = "http://localhost:8002"

# Create a random customer
async def test_create_customer():
    print("Test Case: Create Customer")
    user_name = fake.user_name()  # Randomly generate a user_name

    customer_data = {
        "userName": user_name,  # Random username
        "firstName": fake.first_name(),  # Random first name
        "lastName": fake.last_name(),    # Random last name
        "email": fake.email(),          # Random email
        "phoneNumber": fake.phone_number(),  # Random phone number
        "address": fake.address(),      # Random address
        "profileStatus": "ACTIVE"       # Default to "ACTIVE"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CUSTOMER_SVC_URL}/customers", json=customer_data)
        
        print("Create Customer Status Code:", response.status_code)  # Print status code
        print("Create Customer Response Content:", response.text)    # Print raw content
        
        if response.status_code == 201:  # Assuming 201 is the expected response status for a successful creation
            customer = response.json()
            print("Create Customer Response:", customer)
            return customer["userName"]  # Return the random user_name to use it later for other operations
        else:
            print(f"Failed to create customer. Status code: {response.status_code}")
            return None  # Return None if creation fails

def generate_random_vehicle_id():
    return str(uuid.uuid4())[:8]  # Generate a short alphanumeric vehicle_id

# Create a random vehicle
async def test_create_vehicle():
    print("Test Case: Create Vehicle")
    # Test Data for Vehicle
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

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VEHICLE_SVC_URL}/vehicles", json=vehicle_data)
        print("Create Vehicle Status Code:", response.status_code)
        print("Create Vehicle Response Content:", response.text)
        if response.status_code == 201:
            vehicle = response.json()
            print("Vehicle Created:", vehicle)
            return vehicle["id"]  # Return the vehicle id for further use
        else:
            print("Failed to create vehicle.")
            return None  # Return None if creation fails

# Create a random booking with necessary dependencies
async def test_create_booking(user_name):
    print("Test Case: Create Booking")
    
    # Step 1: Ensure customer exists (via create_customer if not done already)
    print("Calling Create Customer API...")
    customer_response = await test_create_customer() if not user_name else user_name

    if not customer_response:
        print("Customer creation failed. Cannot proceed with booking.")
        return

    # Step 2: Ensure vehicle exists
    vehicle_id = await test_create_vehicle()  # Ensure vehicle is available before booking
    if not vehicle_id:
        print("Vehicle creation failed. Cannot proceed with booking.")
        return

    # Step 3: Create a booking
    booking_data = {
        "user_name": customer_response,  # Use the valid random user_name
        "vehicle_id": vehicle_id,  # Use the valid vehicle_id
        "transaction_id": f"TXN{random.randint(1000, 9999)}",  # Random transaction_id
        "transaction_date": str(date.today()),  # Add the transaction date
        "transaction_price": round(random.uniform(50, 500)),  # Random price
        "transaction_method": random.choice(["Credit Card", "Debit Card", "Cash"])  # Payment method
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/bookings", json=booking_data)
        print("Create Booking Status Code:", response.status_code)
        print("Create Booking Response Content:", response.text)
        if response.status_code == 201:
            booking = response.json()
            print("Booking Created:", booking)
            return booking["id"]  # Return the booking transaction_id for further use
        else:
            print(f"Failed to create booking. Status code: {response.status_code}")
            return None  # Return None if creation fails

# Get all bookings for a user
async def test_get_user_bookings(user_name):
    print("Test Case: Get User Bookings")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings", params={"user_name": user_name})
        if response.status_code == 200:
            print("User Bookings:", response.json())
        else:
            print(f"Failed to get bookings. Status code: {response.status_code}")

# Get booking by ID
async def test_get_booking_by_id(booking_id):
    print("Test Case: Get Booking by ID")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            print("Booking by ID:", response.json())
        else:
            print(f"Failed to get booking by ID. Status code: {response.status_code}")

# Get all test drives
async def test_get_all_testdrives():
    print("Test Case: Get All Test Drives")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives")
        if response.status_code == 200:
            print("All Test Drives:", response.json())
        else:
            print(f"Failed to get test drives. Status code: {response.status_code}")

# Get test drive by ID
async def test_get_testdrive_by_id(testdrive_id):
    print("Test Case: Get Test Drive by ID")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/testdrives/{testdrive_id}")
        if response.status_code == 200:
            print(f"Test Drive by ID {testdrive_id}:", response.json())
        else:
            print(f"Failed to get test drive by ID. Status code: {response.status_code}")

# Book a test drive
async def test_book_testdrive(user_name, vehicle_id):
    print("Test Case: Book Test Drive")

    # Ensure the customer and vehicle exist (use previously created data)
    if not user_name:
        print("Customer is required to book a test drive.")
        return
    
    if not vehicle_id:
        print("Vehicle is required to book a test drive.")
        return

    testdrive_data = {
        "user_name": user_name,
        "vehicle_id": vehicle_id,
        "date": str(date.today()),  # Test drive date
        "time": "10:00 AM",  # Example time slot
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/testdrives/book", json=testdrive_data)
        print("Book Test Drive Status Code:", response.status_code)
        print("Book Test Drive Response Content:", response.text)
        if response.status_code == 201:
            testdrive = response.json()
            print("Test Drive Booked:", testdrive)
            return testdrive["id"]  # Return the testdrive ID for further use
        else:
            print("Failed to book test drive.")
            return None  # Return None if booking fails


# Main function to run tests
async def main():
    print("Starting Test Cases...\n")

    # Step 1: Create customer (generate a random customer)
    user_name = await test_create_customer()
    
    if user_name:
        # Step 2: Create booking (with the created customer)
        booking_id = await test_create_booking(user_name)  # Create a booking for this customer

        if booking_id:
            # Step 3: Fetch bookings by user
            await test_get_user_bookings(user_name)  # Get bookings for this user

            # Step 4: Fetch booking by ID (use the created booking ID)
            await test_get_booking_by_id(booking_id)  # Fetch booking by the generated booking ID

        vehicle_id = await test_create_vehicle()
        
        if vehicle_id:
            # Step 5: Book a test drive (for the created customer and vehicle)
            testdrive_id = await test_book_testdrive(user_name, vehicle_id)
            
            if testdrive_id:
                # Step 6: Get all test drives
                await test_get_all_testdrives()
                
                # Step 7: Get test drive by ID
                await test_get_testdrive_by_id(testdrive_id)

# Run the test suite
if __name__ == "__main__":
    asyncio.run(main())
