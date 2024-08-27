FROM python:3.8-slim

# Install necessary packages
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the Python script and any other files
COPY backup.py /app/

# Install any Python dependencies (if required)
# RUN pip install -r requirements.txt

# Make the script executable
RUN chmod +x /app/backup.py

# Command to run the backup script via cron or directly
CMD ["python3", "/app/backup.py"]
