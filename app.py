#!/usr/bin/env python3
"""
epub2audio - Converti file EPUB in audio narrato con sintesi vocale.
"""

import os
import sys
import click
import logging
import tempfile
from pathlib import Path

import ebooklib
from ebooklib import epub
import pyttsx3
from mutagen.mp3 import MP3
import subprocess

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Costanti
DEFAULT_RATE = 150
DEFAULT_VOLUME = 1.0
DEFAULT_LANG = 'en'

def extract_text(epub_path: str) -> str:
    """
    Estrai il testo da un file EPUB.
    Restituisce il testo completo, ordinato per capitoli.
    """
    try:
        book = epub.read_epub(epub_path)
        text_parts = []

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Rimuovi tag HTML e normalizza spazi
                html = item.get_content().decode('utf-8')
                # Sostituisci tag HTML con spazi
                clean_text = html.replace('<br>', ' ').replace('<p>', ' ').replace('</p>', ' ')
                clean_text = ' '.join(clean_text.split())
                text_parts.append(clean_text)

        return ' '.join(text_parts)
    except Exception as e:
        logger.error(f"Errore nell'estrazione del testo: {e}")
        return ""


def text_to_speech(text: str, output_file: str, voice: str = DEFAULT_LANG, rate: int = DEFAULT_RATE, volume: float = DEFAULT_VOLUME) -> bool:
    """
    Converti testo in audio MP3 usando pyttsx3.
    """
    if not text.strip():
        logger.warning("Testo vuoto: nessun audio generato.")
        return False

    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Imposta la voce (se disponibile)
    voices = engine.getProperty('voices')
    found_voice = False
    for v in voices:
        if voice.lower() in v.id.lower():
            engine.setProperty('voice', v.id)
            logger.info(f"Voce selezionata: {v.id}")
            found_voice = True
            break

    if not found_voice:
        logger.warning(f"Voce '{voice}' non trovata. Usa voce predefinita.")

    try:
        logger.info(f"Generazione audio: {output_file}")
        engine.say(text)
        engine.runAndWait()  # ← IMPORTANTE: aggiunto!
        logger.info(f"Audio generato con successo: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Errore nella sintesi vocale: {e}")
        return False


def merge_audio(temp_files: list, output_file: str) -> bool:
    """
    Unisci più file MP3 in un unico file usando ffmpeg.
    """
    if not temp_files:
        logger.warning("Nessun file da unire.")
        return False

    # Crea un file di lista per ffmpeg
    list_file = os.path.join(tempfile.gettempdir(), "filelist.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for file in temp_files:
            f.write(f"file '{file}'\n")

    try:
        # Comando ffmpeg per unire i file
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            "-y",  # Sovrascrivi senza chiedere
            output_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Errore in ffmpeg: {result.stderr}")
            return False

        logger.info(f"Audio unito con successo: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Errore nell'unione audio: {e}")
        return False
    finally:
        # Elimina il file di lista
        if os.path.exists(list_file):
            os.remove(list_file)


@click.command()
@click.option('--input', '-i', required=True, type=click.Path(exists=True, dir_okay=False), help='File EPUB di input')
@click.option('--output', '-o', default='output.mp3', type=click.Path(), help='File MP3 di output')
@click.option('--voice', '-v', default=DEFAULT_LANG, help='Lingua della voce (es. en, it, fr)')
@click.option('--rate', '-r', type=int, default=DEFAULT_RATE, help='Velocità della voce (100-300)')
@click.option('--volume', '-s', type=float, default=DEFAULT_VOLUME, help='Volume (0.0-1.0)')
def main(input_file: str, output_file: str, voice: str, rate: int, volume: float):
    """
    Converti un file EPUB in audio narrato.
    """
    logger.info(f"Avvio conversione: {input_file} → {output_file}")

    # Verifica che il file EPUB esista
    if not os.path.exists(input_file):
        logger.error(f"File EPUB non trovato: {input_file}")
        sys.exit(1)

    # Estrai testo
    text = extract_text(input_file)
    if not text:
        logger.error("Nessun testo estratto dal file EPUB.")
        sys.exit(1)

    # Usa un directory temporanea sicura
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_files = []
        chunk_size = 1000  # Caratteri per chunk

        # Dividi il testo in parti e genera audio per ogni parte
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            temp_file = os.path.join(tmpdir, f"chunk_{i // chunk_size}.mp3")
            success = text_to_speech(chunk, temp_file, voice=voice, rate=rate, volume=volume)
            if success:
                temp_files.append(temp_file)
            else:
                logger.warning(f"Fallito generare audio per il chunk {i // chunk_size}")

        # Unisci tutti i file MP3
        if temp_files:
            if merge_audio(temp_files, output_file):
                logger.info(f"Conversione completata: {output_file}")
            else:
                logger.error("Errore nell'unione dei file audio.")
                sys.exit(1)
        else:
            logger.error("Nessun file audio generato.")
            sys.exit(1)

    logger.info("Processo completato con successo!")


if __name__ == "__main__":
    main()
