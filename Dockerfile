# Use Python 3.13 base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
