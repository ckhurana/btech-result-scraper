FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the entire source code (since src/ might not exist in all repos)
COPY . /app/

# Adjust the wsgi entrypoint based on the actual app structure
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "wsgi:app"]
