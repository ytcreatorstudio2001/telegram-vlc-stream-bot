FROM python:3.9-slim

# Cache bust to force fresh build with latest code
ENV CACHE_BUST=2025-11-25-08:07

WORKDIR /app

# Create directory for persistent session files
RUN mkdir -p /app/sessions

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
