-- Smart Retail Weather Integration Database Setup
-- PostgreSQL Database and Table Creation Script

-- Create database (run as superuser)
-- CREATE DATABASE sales_weatherinfo_db;

-- Connect to the database and create tables
\c sales_weatherinfo_db;

-- Create weather data table
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    weather_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    temp_c DECIMAL(5,2),
    humidity INTEGER,
    description VARCHAR(255),
    pressure DECIMAL(7,2),
    wind_speed DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(weather_date, city)
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_weather_date_city ON weather(weather_date, city);
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather(city);
CREATE INDEX IF NOT EXISTS idx_weather_date ON weather(weather_date);

-- Create sample cities table (optional)
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL,
    country VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample cities
INSERT INTO cities (city_name, country, latitude, longitude) VALUES
    ('Patna', 'India', 25.5941, 85.1376),
    ('Delhi', 'India', 28.7041, 77.1025),
    ('Mumbai', 'India', 19.0760, 72.8777),
    ('Bangalore', 'India', 12.9716, 77.5946)
ON CONFLICT (city_name) DO NOTHING;

-- Create user roles (optional - for production)
-- CREATE ROLE weather_reader;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO weather_reader;

-- CREATE ROLE weather_writer;
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO weather_writer;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO weather_writer;

-- Display table structure
\d weather;

-- Sample queries for testing
-- SELECT * FROM weather ORDER BY weather_date DESC LIMIT 10;
-- SELECT city, COUNT(*) as record_count FROM weather GROUP BY city;
-- SELECT * FROM cities;

COMMIT;
