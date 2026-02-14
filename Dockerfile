FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Cloud Run uses PORT env var)
ENV PORT=8080
EXPOSE 8080

# Run Streamlit
CMD streamlit run tools/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
