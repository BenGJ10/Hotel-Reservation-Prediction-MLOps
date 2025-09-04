# This Dockerfile is for the whole project

# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install the package in editable mode, elimination caches
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install --no-cache-dir -e .

# Add a build ARG for credentials
ARG GCP_CREDS_FILE
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_key.json

# Copy credentials into the image during build
COPY ${GCP_CREDS_FILE} /app/gcp_key.json

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
