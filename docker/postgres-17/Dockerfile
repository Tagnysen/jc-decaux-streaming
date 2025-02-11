# Use PostgreSQL 17.2 as the base image
FROM postgres:17.2

# Copy the SQL initialization scripts (executed on first run)
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Set proper permissions for initialization scripts
RUN chmod -R 755 /docker-entrypoint-initdb.d/

# Expose PostgreSQL default port
EXPOSE 5432