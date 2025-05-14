FROM python:3.13-slim

WORKDIR /app

# Salin requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi
COPY . .

# Jalankan Flask dengan Python (bukan uvicorn)
CMD ["python", "main.py"]
