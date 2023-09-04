# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy all the files from the current directory to the container
COPY . .

# Expose the port the app runs on
EXPOSE 6000

# Run the command to start the app
CMD ["flask", "run"]
