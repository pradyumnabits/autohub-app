#!/bin/bash

# Define the host and port where the server is running
HOST="139.84.217.135"
PORT=5173  # Replace with the actual port if different

echo "Stopping the server running on $HOST:$PORT..."

# Find the process running on the defined port
PID=$(lsof -t -i:$PORT)

if [ -n "$PID" ]; then
  echo "Found process with PID: $PID"
  echo "Stopping process..."
  kill -9 $PID
  echo "Server stopped successfully."
else
  echo "No server process found running on $PORT."
fi
