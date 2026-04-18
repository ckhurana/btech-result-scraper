FROM python:3.9-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy source code
COPY . .

EXPOSE 8000

# Using main:app because the Flask instance is in main.py
# and restored --workers 3 from backup configuration
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "main:app"]
