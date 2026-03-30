# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client (for pg_isready) – optional, you can skip if using Python wait
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy app code
COPY . .

# Make wait script executable
RUN chmod +x wait-for-db.sh

# Command to start the app via wait-for-db.sh
CMD ["./wait-for-db.sh"]
