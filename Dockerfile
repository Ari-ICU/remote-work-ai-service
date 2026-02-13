FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY . .

# Standard port for FastAPI in this project
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

