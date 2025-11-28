FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend ./backend
COPY frontend ./frontend

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 8080

# Run the MongoDB version
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app_mongo:app"]
