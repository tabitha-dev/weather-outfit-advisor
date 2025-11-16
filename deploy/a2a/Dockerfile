FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install A2A dependencies
RUN pip install --no-cache-dir uvicorn[standard]

# Copy the entire project
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Expose default port (will be overridden by docker-compose)
EXPOSE 8000

# Default command (will be overridden by docker-compose)
CMD ["python", "app.py"]
