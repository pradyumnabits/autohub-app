-- Databse : bookings-db

-- Create test_drives table
CREATE TABLE IF NOT EXISTS test_drives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    status TEXT NOT NULL,
    transaction_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    transaction_price NUMBER NOT NULL,
    transaction_method TEXT NOT NULL
);
