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


# Call the function to initialize the database
initialize_database()


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
