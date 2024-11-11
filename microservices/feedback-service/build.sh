#!/bin/bash

# Define the image name and tag
IMAGE_NAME="feedback-svc"
IMAGE_TAG="latest"

# Build the Docker image
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Output the image name and tag
echo "Docker image built: $IMAGE_NAME:$IMAGE_TAG"
