import sys
import os
import json
from ebooklib import epub
from bs4 import BeautifulSoup
from TTS.api import TTS
from pdfminer.high_level import extract_text


# -----------------------------
#   ESTRAZIONE EPUB
# -----------------------------
def extract_chapters_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items():
        if item.get_type() == 9:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text().strip()
            if len(text) > 50:
                chapters.append(text)

    return chapters


# -----------------------------
#   ESTRAZIONE PDF
# -----------------------------
def extract_chapters_pdf(pdf_path):
    text = extract_text(pdf_path)
    chunk_size = 3000
    chapters = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return [c.strip() for c in chapters if len(c.strip()) > 50]


# -----------------------------
#   AGGIORNA PROGRESSO
# -----------------------------
def update_progress(current, total):
    with open("progress.json", "w") as f:
        json.dump({"current": current, "total": total}, f)


# -----------------------------
#   MAIN
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python convert.py input.(epub|pdf) output_prefix lingua modello")
        sys.exit(1)

    input_file = sys.argv[1]
    out_prefix = sys.argv[2]
    language = sys.argv[3]
    model = sys.argv[4]

    ext = os.path.splitext(input_file)[1].lower()

    print("Estrazione contenuto...")

    if ext == ".epub":
        chapters = extract_chapters_epub(input_file)
    elif ext == ".pdf":
        chapters = extract_chapters_pdf(input_file)
    else:
        print("Formato non supportato.")
        sys.exit(1)

    total = len(chapters)
    update_progress(0, total)

    print(f"Caricamento modello TTS: {model}")
    tts = TTS(model)

    os.makedirs("audio", exist_ok=True)

    for i, chapter in enumerate(chapters, start=1):
        out_file = f"audio/{out_prefix}_capitolo_{i:02d}.wav"
        update_progress(i, total)
        tts.tts_to_file(text=chapter, file_path=out_file)

    update_progress(total, total)
    print("Conversione completata!")
