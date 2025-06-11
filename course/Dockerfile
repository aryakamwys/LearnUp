FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke container
COPY . .

# Expose port 5000
EXPOSE 5000

# Jalankan app Python
CMD ["python", "course/service/app.py"]
