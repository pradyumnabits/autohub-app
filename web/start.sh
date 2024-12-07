#!/bin/bash

# Configuration
HOST="139.84.217.135"
PORT=5173  # Default port for npm dev servers (update if necessary)

# Logging
echo "Starting the server on $HOST:$PORT..."

# Run the server
npm run dev -- --host $HOST --port $PORT &

# Check if the server started successfully
if [ $? -eq 0 ]; then
  echo "Server started successfully on $HOST:$PORT"
else
  echo "Failed to start the server. Please check the logs for details."
  exit 1
fi