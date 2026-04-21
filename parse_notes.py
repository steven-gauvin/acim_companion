#!/usr/bin/env python3
"""Parse all Apple Notes HTML exports and extract clean text content."""

import os
import json
from bs4 import BeautifulSoup

NOTES_DIR = "/home/ubuntu/acim_flashcards/apple_notes"
OUTPUT_DIR = "/home/ubuntu/acim_flashcards/apple_notes_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

index = []

for fname in sorted(os.listdir(NOTES_DIR)):
    if not fname.endswith('.html'):
        continue
    
    filepath = os.path.join(NOTES_DIR, fname)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get title from h1 or filename
    h1 = soup.find('h1')
    title = h1.get_text(strip=True) if h1 else fname.replace('.html', '')
    
    # Get all text content
    text = soup.get_text(separator='\n', strip=True)
    
    # Get file size
    fsize = os.path.getsize(filepath)
    
    # Count lines and words
    lines = [l for l in text.split('\n') if l.strip()]
    word_count = len(text.split())
    
    # Save clean text
    clean_name = fname.replace('.html', '.txt')
    outpath = os.path.join(OUTPUT_DIR, clean_name)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # First 500 chars as preview
    preview = text[:500].replace('\n', ' ').strip()
    
    index.append({
        'title': title,
        'filename': fname,
        'file_size': fsize,
        'word_count': word_count,
        'line_count': len(lines),
        'preview': preview,
        'text_file': clean_name
    })
    
    print(f"✓ {title} — {word_count} words, {len(lines)} lines")

# Save index
with open(os.path.join(OUTPUT_DIR, '_index.json'), 'w') as f:
    json.dump(index, f, indent=2)

print(f"\n=== Done: {len(index)} notes processed ===")

# Print summary sorted by word count
print("\nBy size (largest first):")
for item in sorted(index, key=lambda x: x['word_count'], reverse=True):
    print(f"  {item['word_count']:>6} words — {item['title']}")
