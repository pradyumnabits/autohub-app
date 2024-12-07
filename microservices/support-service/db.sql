-- Database : support-db
-- Create service_appointments table
CREATE TABLE IF NOT EXISTS service_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incremented ID for each appointment
    user_id TEXT NOT NULL,                 -- ID of the user who made the appointment
    vehicle_id TEXT NOT NULL,              -- ID of the vehicle for which the appointment is scheduled
    appointment_date TEXT NOT NULL,        -- Date of the service appointment (e.g., YYYY-MM-DD or timestamp)
    service_type TEXT NOT NULL,            -- Type of service being scheduled (e.g., Maintenance, Repair)
    status TEXT DEFAULT 'Scheduled'        -- Status of the appointment (default is 'Scheduled')
)
