# pip install ebooklib beautifulsoup4 gTTS

import os
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE
from bs4 import BeautifulSoup
from gtts import gTTS

def extract_text_from_epub(epub_path):
    print(f"[+] Lade EPUB: {epub_path}")
    book = epub.read_epub(epub_path)
    text_content = []

    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            if text.strip():
                text_content.append(text)

    return '\n'.join(text_content)

def convert_text_to_mp3(text, output_path, lang='de'):
    print(f"[+] Konvertiere Text in MP3: {output_path}")
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    print("[✓] MP3 gespeichert.")

def epub_to_mp3(epub_file, output_mp3, lang='de'):
    text = extract_text_from_epub(epub_file)
    if not text.strip():
        print("[-] Kein Text extrahiert!")
        return
    convert_text_to_mp3(text, output_mp3, lang=lang)

if __name__ == "__main__":
    # 1_Geschäftsfunktionen
    epub_path = "xxx.epub"     # Pfad zur EPUB-Datei
    mp3_path = "xxx.mp3"       # Pfad zur MP3-Ausgabe
    sprache = "de"

    if os.path.exists(epub_path):
        epub_to_mp3(epub_path, mp3_path, sprache)
    else:
        print(f"[-] Datei nicht gefunden: {epub_path}")
