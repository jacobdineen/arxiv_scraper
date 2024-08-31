# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client for database connections
RUN apt-get update && apt-get install -y postgresql-client

# Run the main script when the container launches
CMD ["python", "main.py"]