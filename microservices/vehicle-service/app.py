from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import sqlite3
from sqlite3 import Error

# FastAPI app initialization
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Database Setup
# ===========================
# Create a directory for the database if it doesn't exist
db_directory = os.path.join(
    os.getcwd(), "data"
)  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(db_directory, 'vehicles.db')}"


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, "vehicles.db")) as conn:
            cursor = conn.cursor()
            # Create vehicles table with id as the primary key
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS vehicles (
                    id TEXT PRIMARY KEY NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    price REAL NOT NULL,
                    fuel_type TEXT NOT NULL,
                    transmission TEXT NOT NULL,
                    body_type TEXT NOT NULL,
                    image_url TEXT
                )
                """
            )
            conn.commit()
            print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")

# Function to seed data into the database
def seed_data():
    try:
        with sqlite3.connect(os.path.join(db_directory, "vehicles.db")) as conn:
            cursor = conn.cursor()
            # Check if the table is empty
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            count = cursor.fetchone()[0]
            if count == 0:
                # Insert seed data
                seed_data = [
                    # Hatchbacks
                    ("1", "Maruti Suzuki", "Swift", 2024, 800000, "Petrol", "Manual", "Hatchback", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("2", "Hyundai", "i20", 2024, 950000, "Petrol", "Manual", "Hatchback", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("3", "Tata", "Altroz", 2024, 850000, "Diesel", "Manual", "Hatchback", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    # Sedans
                    ("4", "Honda", "City", 2024, 1500000, "Petrol", "Automatic", "Sedan", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("5", "Hyundai", "Verna", 2024, 1400000, "Diesel", "Automatic", "Sedan", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("6", "Skoda", "Octavia", 2024, 2600000, "Petrol", "Automatic", "Sedan", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    # SUVs
                    ("7", "Hyundai", "Creta", 2024, 1500000, "Diesel", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("8", "Tata", "Nexon", 2024, 1400000, "Electric", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("9", "Mahindra", "XUV700", 2024, 2000000, "Diesel", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("10", "Toyota", "Fortuner", 2024, 4000000, "Diesel", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("11", "Kia", "Seltos", 2024, 1700000, "Petrol", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    # MPVs
                    ("12", "Toyota", "Innova Crysta", 2024, 2500000, "Diesel", "Manual", "MPV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("13", "Maruti Suzuki", "Ertiga", 2024, 1200000, "Petrol", "Manual", "MPV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("14", "Mahindra", "Marazzo", 2023, 1500000, "Diesel", "Manual", "MPV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    # Electric
                    ("15", "MG", "ZS EV", 2024, 2300000, "Electric", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("16", "Hyundai", "Ioniq 5", 2024, 4500000, "Electric", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("17", "Tata", "Tiago EV", 2024, 850000, "Electric", "Automatic", "Hatchback", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    # Luxury
                    ("18", "Mercedes-Benz", "E-Class", 2024, 8500000, "Diesel", "Automatic", "Sedan", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("19", "BMW", "X5", 2024, 9500000, "Diesel", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                    ("20", "Audi", "Q7", 2024, 8000000, "Petrol", "Automatic", "SUV", "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg"),
                ]
                cursor.executemany(
                    "INSERT INTO vehicles (id, make, model, year, price, fuel_type, transmission, body_type, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    seed_data,
                )
                conn.commit()
                print("Seed data loaded successfully with updated image URLs.")
    except Error as e:
        print(f"Error seeding data: {e}")



# Call the function to initialize the database
initialize_database()
seed_data()

# ===========================
# Pydantic Schemas
# ===========================
class Vehicle(BaseModel):
    id: str
    make: str
    model: str
    year: int
    price: float
    fuel_type: str
    transmission: str
    body_type: str
    image_url: str = None


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, "vehicles.db"))
    return conn


def get_all_vehicles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles


def get_vehicle_by_id(vehicle_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()
    return vehicle


def create_vehicle(vehicle: Vehicle):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vehicles (id, make, model, year, price, fuel_type, transmission, body_type, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            vehicle.id,
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.price,
            vehicle.fuel_type,
            vehicle.transmission,
            vehicle.body_type,
            vehicle.image_url,
        ),
    )
    conn.commit()
    conn.close()


def update_vehicle(vehicle_id: str, vehicle: Vehicle):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE vehicles SET make = ?, model = ?, year = ?, price = ?, fuel_type = ?, transmission = ?, body_type = ?, image_url = ? WHERE id = ?",
        (
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.price,
            vehicle.fuel_type,
            vehicle.transmission,
            vehicle.body_type,
            vehicle.image_url,
            vehicle_id,
        ),
    )
    conn.commit()
    conn.close()


def delete_vehicle(vehicle_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
    conn.commit()
    conn.close()


# ===========================
# Routing and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-vehicle-svc"}


@app.get("/vehicles")
def list_vehicles():
    vehicles = get_all_vehicles()
    return [
        {
            "id": v[0],
            "make": v[1],
            "model": v[2],
            "year": v[3],
            "price": v[4],
            "fuel_type": v[5],
            "transmission": v[6],
            "body_type": v[7],
            "image_url": v[8],
        }
        for v in vehicles
    ]


@app.post("/vehicles", status_code=201)
def create_new_vehicle(vehicle: Vehicle):
    create_vehicle(vehicle)
    return vehicle


@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: str):
    vehicle = get_vehicle_by_id(vehicle_id)

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {
        "id": vehicle[0],
        "make": vehicle[1],
        "model": vehicle[2],
        "year": vehicle[3],
        "price": vehicle[4],
        "fuel_type": vehicle[5],
        "transmission": vehicle[6],
        "body_type": vehicle[7],
        "image_url": vehicle[8],
    }


@app.put("/vehicles/{vehicle_id}")
def update_existing_vehicle(vehicle_id: str, vehicle: Vehicle):
    existing_vehicle = get_vehicle_by_id(vehicle_id)
    if existing_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    update_vehicle(vehicle_id, vehicle)
    return vehicle


@app.delete("/vehicles/{vehicle_id}", status_code=204)
def remove_vehicle(vehicle_id: str):
    existing_vehicle = get_vehicle_by_id(vehicle_id)
    if existing_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    delete_vehicle(vehicle_id)


# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8002)
