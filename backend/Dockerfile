FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user and make scripts executable
RUN useradd --create-home --shell /bin/bash app && \
    chmod +x docker-entrypoint.sh init_db.py && \
    chown -R app:app /app

USER app

# Expose port
EXPOSE 8000

# Run the application with initialization
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]
