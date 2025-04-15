FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure pip to disable bytecode compilation
RUN pip config set global.no-cache-dir true \
    && pip config set global.no-compile true

# Copy requirements file and install Python dependencies
COPY requirements.txt .

# Install Python dependencies with explicit no-compile flag
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for LightRAG
ENV LIGHTRAG_WORKING_DIR=/app/data
ENV AGE_GRAPH_NAME=embediq
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DATABASE=embediq

# Create necessary directories with proper permissions
RUN mkdir -p /app/data && \
    chmod -R 755 /app

# Expose port
EXPOSE 8000

# Create an entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set entrypoint script as the container's entrypoint
CMD ["./entrypoint.sh"]