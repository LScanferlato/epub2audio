### ✅ `docker-compose.yml`

```yaml
version: '3.8'

services:
  epub2audio:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: epub2audio
    restart: unless-stopped
    user: "${USER_ID:-1000}:${GROUP_ID:-1000}"  # Usa ID utente host (opzionale)
    volumes:
      - ./input:/app/input:ro        # Cartella con file EPUB (solo lettura)
      - ./output:/app/output         # Cartella per salvare file MP3
    working_dir: /app
    command: >
      python app.py
      --input /app/input/libro.epub
      --output /app/output/narrato.mp3
      --voice it
      --rate 140
      --volume 0.9
    # Opzionale: aggiungi variabili d'ambiente
    environment:
      - PYTHONUNBUFFERED=1
    # Opzionale: log in console
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 📁 Struttura della Cartella Consigliata

```
epub2audio/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── app.py
├── input/                 # ← File EPUB qui (es. libro.epub)
│   └── libro.epub
├── output/                # ← File MP3 generati qui
│   └── (vuoto all'inizio)
└── README.md
```

> ✅ Il file `libro.epub` deve essere nella cartella `input/`.

---

## 🚀 Come Usarlo

1. **Assicurati che `input/libro.epub` esista**
2. **Esegui:**
   ```bash
   docker-compose up
   ```

3. **Dopo il completamento**, troverai:
   ```
   output/narrato.mp3
   ```

4. **Per usare un altro file o voce:**
   - Modifica `command` nel `docker-compose.yml`
   - Oppure usa `docker-compose run` per override:

   ```bash
   docker-compose run epub2audio \
     --input /app/input/altro-libro.epub \
     --output /app/output/altro-narrato.mp3 \
     --voice en \
     --rate 160
   ```

---

## 🔐 Sicurezza (Opzionale)

Se vuoi usare il tuo **ID utente reale** (per evitare problemi di permessi sui file):

```bash
# Su Linux/macOS, ottieni il tuo UID/GID:
echo $UID
echo $GID
```

Poi esegui:
```bash
docker-compose up --build
```

> ✅ I file creati avranno i tuoi permessi.

---

## 🎁 Extra: `Makefile` (opzionale ma utile)

```makefile
# Makefile
build:
	docker-compose build

up:
	docker-compose up

run:
	docker-compose run epub2audio --help

clean:
	docker-compose down --volumes

.PHONY: build up run clean
```

> Usa con: `make build`, `make up`, `make clean`

---

## ✅ Risultato

Con questo `docker-compose.yml`:

- ✅ Il container **funziona con `ffmpeg`**
- ✅ I file EPUB e MP3 sono **gestiti via volume**
- ✅ Il codice è **separato e sicuro**
- ✅ Puoi **modificare input/output facilmente**
- ✅ È **pronto per produzione o condivisione**

---

## 📬 Vuoi che ti generi:
- Un `GitHub Actions` per build automatica su push?
- Un `Docker Hub` push script?
- Un `README.md` completo con esempi?

Dimmi cosa ti serve e te lo preparo subito! 🚀
