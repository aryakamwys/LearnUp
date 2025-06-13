FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers=2"] 