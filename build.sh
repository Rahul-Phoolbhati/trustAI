#!/usr/bin/env bash

apt-get update && apt-get install -y \
    libportaudio2 libportaudiocpp0 portaudio19-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*