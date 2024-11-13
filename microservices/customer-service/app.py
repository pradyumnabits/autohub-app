import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sqlite3
from sqlite3 import Error
import requests

# FastAPI app initialization
app = FastAPI()

# Jaeger setup for tracing
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Jaeger tracing setup
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "customer-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

FastAPIInstrumentor.instrument_app(app)

# CORS middleware setup
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CUSTOMER_SERVICE_URL = "http://localhost:8007/customers"

# ===========================
# Database Setup
# ===========================
db_directory = os.path.join(os.getcwd(), "data")  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(db_directory, 'customer_db.db')}"

# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, "customer_db.db")) as conn:
            cursor = conn.cursor()
            # Create customers table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userName TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    phoneNumber TEXT NOT NULL,
                    address TEXT NOT NULL,
                    profileStatus TEXT NOT NULL
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
class Customer(BaseModel):
    userName: str
    email: str
    firstName: str
    lastName: str
    phoneNumber: str
    address: str
    profileStatus: str  # Active/Inactive

# ===========================
# Business Logic (Customer Creation)
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, "customer_db.db"))
    return conn

def create_customer_in_db(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the userName already exists
    cursor.execute("SELECT * FROM customers WHERE userName = ?", (customer.userName,))
    db_customer = cursor.fetchone()

    if db_customer:
        conn.close()
        raise HTTPException(status_code=400, detail="User name already registered")

    # Insert the new customer into the database
    cursor.execute(
        "INSERT INTO customers (userName, email, firstName, lastName, phoneNumber, address, profileStatus) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (customer.userName, customer.email, customer.firstName, customer.lastName, customer.phoneNumber, customer.address, customer.profileStatus),
    )
    conn.commit()
    conn.close()

    return {"userName": customer.userName, "email": customer.email, "profileStatus": customer.profileStatus}

# ===========================
# Routing and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-customer-svc"}

@app.post("/customers")
def register_customer(customer: Customer):
    print(f"Registering customer: {customer}")
    create_customer_in_db(customer)
    return {"msg": "Customer registered successfully", "customer": customer}

@app.get("/customers/{userName}")
def get_customer(userName: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE userName = ?", (userName,))
    customer = cursor.fetchone()
    conn.close()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "userName": customer[1],
        "email": customer[2],
        "firstName": customer[3],
        "lastName": customer[4],
        "phoneNumber": customer[5],
        "address": customer[6],
        "profileStatus": customer[7],
    }

@app.post("/customers/update/{userName}")
def update_customer(userName: str, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE userName = ?", (userName,))
    existing_customer = cursor.fetchone()

    if not existing_customer:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update the customer details in the database
    cursor.execute(
        """
        UPDATE customers SET email = ?, firstName = ?, lastName = ?, phoneNumber = ?, address = ?, profileStatus = ? 
        WHERE userName = ?
        """,
        (customer.email, customer.firstName, customer.lastName, customer.phoneNumber, customer.address, customer.profileStatus, userName),
    )
    conn.commit()
    conn.close()

    return {"msg": "Customer updated successfully"}

@app.post("/customers/deactivate/{userName}")
def deactivate_customer(userName: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE userName = ?", (userName,))
    customer = cursor.fetchone()

    if not customer:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update the customer status to 'Inactive'
    cursor.execute("UPDATE customers SET profileStatus = 'INACTIVE' WHERE userName = ?", (userName,))
    conn.commit()
    conn.close()

    return {"msg": "Customer deactivated successfully"}
