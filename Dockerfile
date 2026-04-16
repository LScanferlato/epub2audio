# Dockerfile
FROM python:3.11-slim

# Imposta variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea utente non root
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Imposta il working directory
WORKDIR /app

# Copia solo requirements.txt prima
COPY requirements.txt .

# Installa dipendenze con cache disabilitata
RUN pip install --no-cache-dir -r requirements.txt

# Installa ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copia il codice sorgente
COPY . .

# Rendi app.py eseguibile (opzionale)
RUN chmod +x app.py

# Esegui il comando
CMD ["python", "app.py"]
