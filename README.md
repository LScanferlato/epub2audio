# 📚 epub2audio - Converti eBook EPUB in Audio Narrato

Un semplice strumento Python per convertire file `.epub` in file audio MP3 narrati.

## 🚀 Funzionalità
- Estrae testo da capitoli e sezioni
- Genera audio con sintesi vocale (TTS)
- Combina tutti i capitoli in un unico file MP3
- Supporta diversi motori TTS (configurabile)

## 📦 Requisiti
- Python 3.7+
- `ebooklib`, `pyttsx3`, `mutagen`, `click`

## 🛠 Installazione
```bash
git clone https://github.com/LScanferlato/epub2audio.git
cd epub2audio
pip install -r requirements.txt

# Installa le dipendenze
pip install ebooklib pyttsx3 mutagen click

# Esegui
python app.py -i "libro.epub" -o "narrato.mp3" -v it -r 140 -s 0.9
