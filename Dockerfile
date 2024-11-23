# Use the official Python image with a slim variant for smaller size
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "main.py"]