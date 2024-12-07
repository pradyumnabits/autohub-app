-- Database : feedback-db
-- Create feedback table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    feedback_type TEXT NOT NULL,
    reference_id TEXT,
    details TEXT NOT NULL,
    rating INTEGER NOT NULL,
    submitted_at TEXT NOT NULL
);
