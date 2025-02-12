# Use official Python image
FROM python:3.11-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gnupg2 \
    wget \
    apt-transport-https \
    software-properties-common \
    unixodbc-dev \
    curl \
    && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_PORT=5001

# Expose port
EXPOSE 5001

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]