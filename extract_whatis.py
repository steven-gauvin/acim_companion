#!/usr/bin/env python3
"""Extract the 'Commentary on What Is...?' sections from the Dee Doyle PDF."""

import pdfplumber
import re
import json

PDF_PATH = "/home/ubuntu/upload/_LessonandReadingGuide-2.pdf"

# Extract all text from the PDF
print("Extracting text from PDF...")
full_text = []
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"--- PAGE {i+1} ---\n{text}")

all_text = "\n".join(full_text)

# Save full text for reference
with open("/home/ubuntu/acim_flashcards/data/pdf_full_text.txt", "w") as f:
    f.write(all_text)
print(f"Full text saved ({len(all_text)} chars)")

# Find the "Commentary on What Is" sections
# Pattern: "Commentary on What Is [Topic]?"
sections = []
pattern = r'Commentary on What [Ii]s ([^\n?]+)\??'
matches = list(re.finditer(pattern, all_text))
print(f"\nFound {len(matches)} 'Commentary on What Is' sections:")
for m in matches:
    print(f"  - What Is {m.group(1).strip('?')}? at position {m.start()}")
    sections.append({
        'topic': m.group(1).strip('?').strip(),
        'start': m.start()
    })

# Also find "Commentary on What Am I?"
pattern2 = r'Commentary on What [Aa]m I\??'
matches2 = list(re.finditer(pattern2, all_text))
for m in matches2:
    print(f"  - What Am I? at position {m.start()}")
    sections.append({
        'topic': 'What Am I',
        'start': m.start()
    })

# Sort by position
sections.sort(key=lambda x: x['start'])

# Find where each section ends (at the next section or at lesson commentary)
# Also look for "Lesson 221" or similar as the end marker
lesson_pattern = r'(?:^|\n)Lesson 221'
lesson_match = re.search(lesson_pattern, all_text)
if lesson_match:
    print(f"\nLesson 221 starts at position {lesson_match.start()}")
    end_of_whatis = lesson_match.start()
else:
    end_of_whatis = len(all_text)

# Extract each section's text
for i, sec in enumerate(sections):
    if i + 1 < len(sections):
        sec['end'] = sections[i + 1]['start']
    else:
        sec['end'] = end_of_whatis
    sec['text'] = all_text[sec['start']:sec['end']].strip()
    # Count words
    sec['word_count'] = len(sec['text'].split())
    print(f"  {sec['topic']}: {sec['word_count']} words")

# Save each section to a separate file
import os
os.makedirs("/home/ubuntu/acim_flashcards/data/whatis_commentaries", exist_ok=True)

for sec in sections:
    filename = sec['topic'].lower().replace(' ', '_').replace('?', '')
    filepath = f"/home/ubuntu/acim_flashcards/data/whatis_commentaries/{filename}.txt"
    with open(filepath, 'w') as f:
        f.write(sec['text'])
    print(f"  Saved: {filepath}")

# Also save a summary JSON
summary = []
for sec in sections:
    summary.append({
        'topic': sec['topic'],
        'word_count': sec['word_count'],
        'first_100_chars': sec['text'][:100]
    })

with open("/home/ubuntu/acim_flashcards/data/whatis_commentaries/index.json", 'w') as f:
    json.dump(summary, f, indent=2)

print("\nDone!")
