from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import sqlite3
from datetime import datetime
from sqlite3 import Error
import uuid

# FastAPI app initialization
app = FastAPI(
    title="Customer Feedback Service API",
    version="1.0.0",
    description="API for collecting and managing customer feedback for vehicles and post-sale services.",
)

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
db_directory = os.path.join(os.getcwd(), "data")
os.makedirs(db_directory, exist_ok=True)
DATABASE_PATH = os.path.join(db_directory, "customer_feedback.db")


# Initialize the SQLite database
def initialize_database():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            # Create feedback table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    feedback_type TEXT NOT NULL,
                    reference_id TEXT,
                    details TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    submitted_at TEXT NOT NULL
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
class FeedbackRequest(BaseModel):
    user_id: str
    feedback_type: str
    reference_id: str
    details: str
    rating: int


class FeedbackResponse(BaseModel):
    feedback_id: str
    user_id: str
    feedback_type: str
    reference_id: str
    details: str
    rating: int
    submitted_at: str


class ErrorResponse(BaseModel):
    detail: str


# ===========================
# Database Access Functions
# ===========================
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def create_feedback(feedback: FeedbackRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    feedback_id = str(uuid.uuid4())  # Generate a unique feedback ID
    submitted_at = datetime.utcnow().isoformat()  # Get the current timestamp in UTC
    cursor.execute(
        "INSERT INTO feedback (feedback_id, user_id, feedback_type, reference_id, details, rating, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            feedback_id,
            feedback.user_id,
            feedback.feedback_type,
            feedback.reference_id,
            feedback.details,
            feedback.rating,
            submitted_at,
        ),
    )
    conn.commit()
    conn.close()
    return feedback_id, submitted_at


def get_feedback_by_id(feedback_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback WHERE feedback_id = ?", (feedback_id,))
    feedback = cursor.fetchone()
    conn.close()
    return feedback


# ===========================
# Routes and Business Logic
# ===========================
@app.get("/ping")
def ping():
    return {"msg": "pong-feedback-svc"}


@app.post(
    "/feedback/submit",
    status_code=201,
    response_model=FeedbackResponse,
    responses={400: {"model": ErrorResponse}},
)
def submit_feedback(feedback: FeedbackRequest):
    try:
        feedback_id, submitted_at = create_feedback(feedback)
        return FeedbackResponse(
            feedback_id=feedback_id,
            user_id=feedback.user_id,
            feedback_type=feedback.feedback_type,
            reference_id=feedback.reference_id,
            details=feedback.details,
            rating=feedback.rating,
            submitted_at=submitted_at,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Invalid feedback submission request"
        )


@app.get(
    "/feedback/{id}",
    response_model=FeedbackResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_feedback(id: str):
    feedback = get_feedback_by_id(id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return FeedbackResponse(
        feedback_id=feedback[0],
        user_id=feedback[1],
        feedback_type=feedback[2],
        reference_id=feedback[3],
        details=feedback[4],
        rating=feedback[5],
        submitted_at=feedback[6],
    )


@app.get("/feedback/history/{user_id}")
def get_user_feedback_history(user_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE user_id = ? ORDER BY submitted_at DESC", (user_id,))
        feedbacks = cursor.fetchall()
        conn.close()

        if not feedbacks:
            return []

        return [
            {
                "feedback_id": feedback[0],
                "user_id": feedback[1],
                "feedback_type": feedback[2],
                "reference_id": feedback[3],
                "details": feedback[4],
                "rating": feedback[5],
                "submitted_at": feedback[6]
            }
            for feedback in feedbacks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Error fetching feedback history"
        )


# ===========================
# Run the application (Optional - for testing)
# ===========================
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8006)
