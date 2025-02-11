DROP DATABASE IF EXISTS bike_sharing_db;
-- Step 1: Create the Database
CREATE DATABASE bike_sharing_db;

\c bike_sharing_db;

-- Step 2: Create the Table
CREATE TABLE bike_stations (
    id SERIAL PRIMARY KEY,  -- Unique auto-increment ID
    number INT NOT NULL,  
    contract_name VARCHAR(50) NOT NULL,  
    name VARCHAR(255) NOT NULL,  
    address VARCHAR(255) NOT NULL,  
    lat DOUBLE PRECISION NOT NULL,  -- Use DOUBLE PRECISION instead of FLOAT
    lng DOUBLE PRECISION NOT NULL,  
    banking BOOLEAN NOT NULL,  
    bonus BOOLEAN NOT NULL,  
    bike_stands INT NOT NULL,  
    available_bike_stands INT NOT NULL,  
    available_bikes INT NOT NULL,  
    status TEXT CHECK (status IN ('OPEN', 'CLOSED')) NOT NULL,  -- Use CHECK instead of ENUM
    last_update BIGINT NOT NULL  
);
