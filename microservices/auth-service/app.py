import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import os
import sqlite3
from sqlite3 import Error
import requests
import jwt

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

CUSTOMER_SERVICE_URL = "http://localhost:8007/customers"

# ===========================
# Database Setup
# ===========================
# Create a directory for the database if it doesn't exist
db_directory = os.path.join(
    os.getcwd(), "data"
)  # 'data' folder in the current directory
os.makedirs(db_directory, exist_ok=True)  # Create the directory if it doesn't exist
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(db_directory, 'test.db')}"


# Function to initialize the database
def initialize_database():
    try:
        with sqlite3.connect(os.path.join(db_directory, "test.db")) as conn:
            cursor = conn.cursor()
            # Create users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userName TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL
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
class User(BaseModel):
    userName: str  # Changed to userName
    email: str  # Use EmailStr for email validation
    password: str
    firstName: str  # New field for customer's first name
    lastName: str  # New field for customer's last name
    phoneNumber: str  # New field for customer's phone number
    address: str  # New field for customer's address


class AuthUser(BaseModel):
    userName: str  # Changed to userName
    password: str


# ===========================
# Business Logic (Password hashing)
# ===========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(os.path.join(db_directory, "test.db"))
    return conn


def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the userName already exists
    cursor.execute("SELECT * FROM users WHERE userName = ?", (user.userName,))
    db_user = cursor.fetchone()

    if db_user:
        conn.close()
        raise HTTPException(status_code=400, detail="User name already registered")

    # Hash the password and insert the new user
    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (userName, email, hashed_password) VALUES (?, ?, ?)",
        (user.userName, user.email, hashed_password),
    )
    conn.commit()
    # creating the customer -------------------------------------
    create_customer(user)
    conn.close()

    return {"userName": user.userName, "email": user.email}


def get_user_by_username(userName: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE userName = ?", (userName,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_token(user_id: int, user_name: str):
    """
    Creates a JWT token for the given user credentials
    """
    SECRET_KEY = "Autohub-api-secret-key"
    user = get_user_by_username(user_name)
    if not user:
        raise HTTPException(
            status_code=400, detail="User name or password is incorrect"
        )
    token = jwt.encode(
        {
            "user_id": user_id,
            "user_name": user_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    return token


def create_customer(user: User):
    # Prepare customer data from the User object
    customer_data = {
        "userName": user.userName,  # Use userName from the User model
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "phoneNumber": user.phoneNumber,
        "address": user.address,
        "profileStatus": "ACTIVE",  # Default profile status
    }

    # Print customer data for debugging
    print("Creating customer with the following data:", customer_data)

    try:
        response = requests.post(CUSTOMER_SERVICE_URL, json=customer_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to create customer") from e


# ===========================
# Routing and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-auth-svc"}


@app.post("/auth/register")
def register_user(user: User):
    print(
        "--------------------------------------user in auth service--------------------------------------"
    )
    print(user)
    user_data = create_user(user)
    # Step 2: Call the create_customer function to add a customer
    # customer_data = create_customer(user)
    return {"msg": "User registered successfully", "user": user_data}


@app.post("/auth/login")
def login_user(user: AuthUser):
    db_user = get_user_by_username(user.userName)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid user name or password")

    # Verify password
    if not verify_password(
        user.password, db_user[3]
    ):  # Assuming hashed_password is at index 3
        raise HTTPException(status_code=400, detail="Invalid user name or password")

    # Create and return a JWT token
    token = create_token(db_user[0], db_user[1])
    return {
        "msg": "Login successful",
        "user": {"userName": db_user[1], "email": db_user[2]},
        "token": token,
    }  # Assuming userName is at index 1 and email at index 2


# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8001)
