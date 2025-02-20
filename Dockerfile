# Stage 1: Build stage (Install dependencies)
FROM python:3.10-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage (Run application)
FROM python:3.10-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

# Copy the entire application
COPY . .

# Expose Django port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]