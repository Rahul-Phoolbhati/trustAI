# FROM python:3.12-alpine
# RUN ./run.sh


# Base image
FROM python:3.10-slim

# Install system-level dependencies for PyAudio
RUN apt-get update && apt-get install -y portaudio19-dev python3-dev build-essential

# Set working directory inside container
WORKDIR /app

# Copy files into container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port (if it's a web app, e.g., Flask on 5000)
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
