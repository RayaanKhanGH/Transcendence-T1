-- Transcendence T1 Database Schema
-- Run this in pgAdmin to create the intelligence table

CREATE TABLE IF NOT EXISTS intelligence (
    id SERIAL PRIMARY KEY,
    source_url TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster URL lookups
CREATE INDEX IF NOT EXISTS idx_intelligence_url ON intelligence(source_url);

-- Create index for timestamp queries
CREATE INDEX IF NOT EXISTS idx_intelligence_created ON intelligence(created_at DESC);
