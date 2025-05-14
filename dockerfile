# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment (optional)
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "chatidfinder.py"]
