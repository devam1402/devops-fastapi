FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

# Install system deps (psycopg2 needs this)
RUN apt-get update -o Acquire::ForceIPv4=true \
 && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic/ alembic/

COPY app/ app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
