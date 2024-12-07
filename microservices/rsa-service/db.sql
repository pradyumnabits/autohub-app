-- dabase : rsa-db
-- Create requests table
CREATE TABLE IF NOT EXISTS requests (
    id TEXT PRIMARY KEY NOT NULL,
    user_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    provider TEXT,
    contact_number TEXT NOT NULL,
    assistance_type TEXT NOT NULL
);
