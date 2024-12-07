-- Databse : customer-db
-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    userName TEXT PRIMARY KEY NOT NULL,      -- Unique username for each customer (e.g., a login name)
    firstName TEXT NOT NULL,                 -- First name of the customer
    lastName TEXT NOT NULL,                  -- Last name of the customer
    email TEXT UNIQUE NOT NULL,              -- Unique email address of the customer (must be unique in the table)
    phoneNumber TEXT,                        -- Optional phone number for the customer
    address TEXT,                            -- Optional address field for the customer
    profileStatus TEXT DEFAULT 'active'      -- Default status is 'active'; can be changed to 'inactive' or other values
)
