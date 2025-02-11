# Use the official Python 3.9 image
FROM python:3.11-alpine

# Install bash
RUN apk add --no-cache bash

# Set bash as default shell (optional)
SHELL ["/bin/bash", "-c"]

# Install required packages: bash, openjdk (Java), and other dependencies
RUN apk add --no-cache bash openjdk17

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set the working directory
WORKDIR /src

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory
COPY ./src/ /src

# Keep the container alive
CMD ["tail", "-f", "/dev/null"]
#CMD ["python", "main/python_producer.py"]