# FROM python:3.12-alpine
# RUN ./run.sh


# Base image
# FROM python:3.10-alpine

# # Install system-level dependencies for PyAudio
# # RUN apt-get update && apt-get install -y portaudio19-dev python3-dev build-essential
# RUN apk add --no-cache portaudio-dev build-base


# # Set working directory inside container
# WORKDIR /app

# # Copy files into container
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Expose the port (if it's a web app, e.g., Flask on 5000)
# EXPOSE 5000

# # Start the app
# CMD ["python", "app.py"]

# apt-get update && apt-get install -y \
#         libportaudio2 libportaudiocpp0 portaudio19-dev \
#         python3-dev \
#         build-essential \
#         && rm -rf /var/lib/apt/lists/*


# FROM python:3.10-slim

# # RUN apt-get update && apt-get install -y \
# #     portaudio19-dev \
# #     python3-dev \
# #     build-essential \
# #     gfortran \
# #     libatlas-base-dev \
# #     libopenblas-dev \
# #     liblapack-dev \
# #     && apt-get clean

# RUN apt-get update && apt-get install -y \
#     libportaudio2 libportaudiocpp0 portaudio19-dev \
#     python3-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*


# WORKDIR /app

# # Install scipy separately first
# # RUN pip install --no-cache-dir scipy==1.11.4

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 5000
# CMD ["python", "app.py"]




FROM python:3.10-slim AS builder

# Install minimal build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    portaudio19-dev \
    python3-dev \
    gcc \
    libc6-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

# Build wheels for packages that need compilation
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Start fresh with a clean image
FROM python:3.10-slim

# Copy only the runtime library for PortAudio
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     libportaudio2 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /wheels /wheels

# Install from wheels (no compilation needed)
COPY requirements.txt .
RUN apt-get update && apt-get install --no-install-recommends -y \
    libportaudio2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY . .

EXPOSE 5001
CMD ["python", "app.py"]