# Use the official Python image from the Docker Hub
FROM python:3.8

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1-mesa-glx

# Add metadata to the image to describe that the container is listening on the specified port at runtime.
EXPOSE 8080

# Set the working directory in the Docker container
WORKDIR /app

# Set the environment variable to include the directory containing libGL.so.1
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/mesa

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory . in the host to /app in the container
COPY . /app

# Specify the command to run
CMD ["python", "main.py"]