# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install system dependencies for OpenGL, gthread, and other potential dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Clean up to minimize image size

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy all the files from the current directory to the container
COPY . .

# Expose the port the app runs on
EXPOSE 6000

# Run the command to start the app
CMD ["flask", "run"]