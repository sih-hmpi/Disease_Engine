# syntax=docker/dockerfile:1.4

# -------- Build Stage --------
FROM ubuntu:rolling AS builder
LABEL AUTHOR="HEMANT KUMAR"
LABEL VERSION="1.0"

RUN apt-get update && apt-get install -y git openssh-client

WORKDIR /usr/src/app

# Copy the local project files into the image
COPY . DISEASE_ENGINE/

# -------- Runtime Stage --------
FROM python:3.13.5-alpine3.21

# Set workdir to project root
WORKDIR /usr/src/app/service

# Copy code from builder stage
COPY --from=builder /usr/src/app/DISEASE_ENGINE ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start FastAPI app from the service directory where app.py is located
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]