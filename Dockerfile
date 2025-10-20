FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot/ ./bot/
COPY run.py .

# Create directories
RUN mkdir -p /app/data /app/logs

# Run the bot
CMD ["python", "run.py"]
