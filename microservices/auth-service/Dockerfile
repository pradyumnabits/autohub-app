# Use an official Python image as a base
#FROM python:3.10-slim
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_WARN_SCRIPT_LOCATION=0 \
    PIP_PROGRESS_BAR=off


# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 8001

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
