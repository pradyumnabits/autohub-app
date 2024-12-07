-- Database : vehicles-db
-- Create vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id TEXT PRIMARY KEY NOT NULL,          -- Unique identifier for each vehicle (e.g., VIN or custom ID)
    make TEXT NOT NULL,                    -- Make of the vehicle (e.g., Ford, Toyota)
    model TEXT NOT NULL,                   -- Model of the vehicle (e.g., F-150, Camry)
    year INTEGER NOT NULL,                 -- Year of manufacture (e.g., 2020)
    price REAL NOT NULL,                   -- Price of the vehicle (as a real number)
    fuel_type TEXT NOT NULL,               -- Type of fuel used by the vehicle (e.g., Gasoline, Electric)
    transmission TEXT NOT NULL,            -- Transmission type (e.g., Automatic, Manual)
    body_type TEXT NOT NULL,               -- Body type (e.g., Sedan, SUV, Coupe)
    image_url TEXT                         -- URL to an image of the vehicle (optional)
)
