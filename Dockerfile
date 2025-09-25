# Use official Python image as base
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and model
COPY . .

# Remove default nginx config and add our own
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80

# Start Nginx and Streamlit
CMD service nginx start && streamlit run app.py --server.port 8501 --server.address 0.0.0.0
