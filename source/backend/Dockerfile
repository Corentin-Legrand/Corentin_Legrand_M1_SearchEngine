# Backend image: search API (default command) and data import script.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# The code lives in /app/source/backend so that EnvironmentManager resolves the project root to /app:
# the `.env` file is expected at /app/.env and the data directory at /app/<STORAGE_DIR>.
WORKDIR /app/source/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# The application factory builds the matrices once, before the server accepts requests.
CMD ["uvicorn", "api:build_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
