# pip install ebooklib beautifulsoup4 gTTS

import os
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE
from bs4 import BeautifulSoup
from gtts import gTTS, gTTSError
import re

def sanitize_filename(name):
    # Entfernt ungültige Zeichen für Dateinamen
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def extract_chapters(epub_path):
    print(f"[+] Lade EPUB: {epub_path}")
    book = epub.read_epub(epub_path)
    chapters = []

    for idx, item in enumerate(book.get_items()):
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')

            title_tag = soup.find(['h1', 'h2', 'h3', 'title'])
            title = title_tag.get_text().strip() if title_tag else f"Kapitel_{idx+1}"

            text = soup.get_text().strip()
            if text:
                chapters.append((sanitize_filename(title), text))

    return chapters

def convert_chapters_to_mp3(chapters, output_folder, lang='de'):
    os.makedirs(output_folder, exist_ok=True)
    for i, (title, text) in enumerate(chapters):
        filename = f"{i+1:02d}_{title}.mp3"
        output_path = os.path.join(output_folder, filename)

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 0:
                print(f"[⏩] Überspringe vorhandene Datei: {filename}")
                continue
            else:
                print(f"[🧹] Lösche defekte/leere Datei: {filename}")
                try:
                    os.remove(output_path)
                except Exception as e:
                    print(f"[✗] Konnte Datei nicht löschen: {e}")
                    continue  # nicht neu erzeugen, wenn Löschung fehlschlägt

        print(f"[+] Erstelle: {output_path}")
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(output_path)
        except Exception as e:
            if "429" in str(e):
                print("\n[⛔] Fehler 429 – Zu viele Anfragen an die TTS-API.")
                print("[💡] Bitte warte einen Tag und starte das Skript erneut, um fortzufahren.\n")
                return  # sofortiger Abbruch
            else:
                print(f"[✗] Fehler bei Kapitel '{title}': {e}")
            continue  # nächste Datei verarbeiten
    print("[✓] Alle Kapitel wurden konvertiert.")

def epub_to_mp3_chapters(epub_file, output_folder, lang='de'):
    chapters = extract_chapters(epub_file)
    if not chapters:
        print("[-] Keine Kapitel gefunden.")
        return
    convert_chapters_to_mp3(chapters, output_folder, lang)

if __name__ == "__main__":
    epub_path = "xxx.epub"               # Pfad zur EPUB-Datei
    ausgabe_ordner = "xxx"               # Zielordner für MP3s
    sprache = "de"                       # z.B. "en", "de", "fr", etc.

    if os.path.exists(epub_path):
        epub_to_mp3_chapters(epub_path, ausgabe_ordner, sprache)
    else:
        print(f"[-] Datei nicht gefunden: {epub_path}")
