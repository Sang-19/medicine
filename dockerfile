# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    libgstreamer1.0-dev \
    libsqlite3-dev \
    sqlite3 \
    libtool \
    pkg-config \
    openjdk-17-jdk \
    autoconf \
    automake \
    ccache \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install Cython==0.29.33
RUN pip install buildozer==1.5.0
RUN pip install kivy==2.1.0
RUN pip install kivymd==1.1.1
RUN pip install pillow
RUN pip install python-dateutil

# Set working directory
WORKDIR /app

# Copy the application files
COPY main.py .
COPY buildozer.spec .
COPY requirements.txt .

# Download Android SDK
RUN mkdir -p /app/android-sdk/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip && \
    unzip commandlinetools-linux-8512546_latest.zip && \
    mv cmdline-tools android-sdk/cmdline-tools/latest && \
    rm commandlinetools-linux-8512546_latest.zip

# Set Android SDK environment variables
ENV ANDROID_HOME=/app/android-sdk
ENV PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Accept licenses and install SDK components
RUN yes | /app/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/app/android-sdk \
    "platforms;android-30" \
    "build-tools;30.0.3" \
    "platform-tools" \
    "ndk;23.1.7779620" \
    "cmake;3.18.1"

RUN yes | /app/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/app/android-sdk --licenses

# Create data directory for the app
RUN mkdir -p /app/data

# Set volume for output APK
VOLUME ["/app/bin"]

# Command to build the APK
CMD ["buildozer", "android", "debug"]