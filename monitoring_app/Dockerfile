FROM python:3.12.11-slim

WORKDIR /app

# Installera beroenden
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera hela appen
COPY . .

# Startkommando
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
