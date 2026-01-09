FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    espeak-ng \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    TTS \
    ebooklib \
    beautifulsoup4 \
    pdfminer.six \
    flask

WORKDIR /app

COPY convert.py /app/
COPY app.py /app/
COPY templates /app/templates

EXPOSE 8080

CMD ["python", "app.py"]
