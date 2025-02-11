-- 1️⃣ Create the user
CREATE USER developer WITH PASSWORD 'pythonlover';

-- 2️⃣ Grant all privileges on all databases
GRANT pg_read_all_data TO developer;
GRANT pg_write_all_data TO developer;

-- 3️⃣ Allow the user to create databases (equivalent to WITH GRANT OPTION in MySQL)
ALTER USER developer WITH CREATEDB CREATEROLE;

-- 4️⃣ Allow connections from any host (instead of localhost)
-- This is configured in `pg_hba.conf`, but you can also update the PostgreSQL system catalog:
ALTER ROLE developer SET client_encoding = 'utf8';
ALTER ROLE developer SET default_transaction_isolation = 'read committed';
ALTER ROLE developer SET timezone = 'UTC';