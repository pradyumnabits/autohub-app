from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sqlite3
from sqlite3 import Error

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

# ===========================
# Database Setup
# ===========================
db_directory = os.path.join(os.getcwd(), "data")
os.makedirs(db_directory, exist_ok=True)
db_file = os.path.join(db_directory, "customers.db")


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    userName TEXT PRIMARY KEY NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phoneNumber TEXT,
                    address TEXT,
                    profileStatus TEXT DEFAULT 'active'  -- Add default status 'active'
                )
            """
            )
            conn.commit()
            print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")


initialize_database()


# ===========================
# Pydantic Schemas
# ===========================
class Customer(BaseModel):
    userName: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str = None
    address: str = None
    profileStatus: str = "ACTIVE"  # New field with a default value


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(db_file)
    return conn


def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return customers


def get_customer_by_id(userName: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE userName = ?", (userName,))
    customer = cursor.fetchone()
    conn.close()
    return customer


def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (userName, firstName, lastName, email, phoneNumber, address, profileStatus) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            customer.userName,
            customer.firstName,
            customer.lastName,
            customer.email,
            customer.phoneNumber,
            customer.address,
            customer.profileStatus,
        ),
    )
    conn.commit()
    conn.close()


def update_customer(userName: str, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET firstName = ?, lastName = ?, email = ?, phoneNumber = ?, address = ?, profileStatus = ? WHERE userName = ?",
        (
            customer.firstName,
            customer.lastName,
            customer.email,
            customer.phoneNumber,
            customer.address,
            customer.profileStatus,
            userName,
        ),
    )
    conn.commit()
    conn.close()


def delete_customer(userName: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET profileStatus = 'inactive' WHERE userName = ?",
        (userName,),
    )
    conn.commit()
    conn.close()


def update_customer_status(userName: str, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET profileStatus = ? WHERE userName = ?", (status, userName)
    )
    conn.commit()
    conn.close()


# ===========================
# Routing and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-customer-svc"}


@app.get("/customers")
def list_customers():
    customers = get_all_customers()
    return [
        {
            "userName": c[0],
            "firstName": c[1],
            "lastName": c[2],
            "email": c[3],
            "phoneNumber": c[4],
            "address": c[5],
            "profileStatus": c[6],
        }
        for c in customers
    ]


@app.post("/customers", status_code=201)
def create_new_customer(customer: Customer):
    create_customer(customer)
    return customer


@app.get("/customers/{userName}")
def get_customer(userName: str):
    customer = get_customer_by_id(userName)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "userName": customer[0],
        "firstName": customer[1],
        "lastName": customer[2],
        "email": customer[3],
        "phoneNumber": customer[4],
        "address": customer[5],
        "profileStatus": customer[6],
    }


@app.put("/customers/{userName}")
def update_existing_customer(userName: str, customer: Customer):
    existing_customer = get_customer_by_id(userName)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_customer(userName, customer)
    return customer


@app.delete("/customers/{userName}", status_code=204)
def remove_customer(userName: str):
    existing_customer = get_customer_by_id(userName)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(userName)


@app.put("/customers/{userName}/status", response_model=dict)
def update_customer_profile_status(userName: str, status: str = "ACTIVE"):
    existing_customer = get_customer_by_id(userName)
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    update_customer_status(userName, status)
    return {"userName": userName, "profileStatus": status}
