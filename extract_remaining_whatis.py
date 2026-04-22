import re
import json
import os

text = open('/home/ubuntu/acim_flashcards/data/pdf_full_text.txt').read()

# Each section starts with the title and ends before the next section or lesson commentary
sections = [
    ('the_last_judgment', 'What is the Last Judgment?'),
    ('creation', 'What is Creation?'),
    ('the_ego', 'What is the Ego?'),
    ('a_miracle', 'What is a Miracle?'),
    ('what_am_i', 'What Am I?'),
]

# Find the second occurrence of each title (first is TOC)
def find_second(text, title):
    first = text.find(title)
    if first == -1:
        return -1
    second = text.find(title, first + 1)
    return second

results = {}

for key, title in sections:
    pos = find_second(text, title)
    if pos == -1:
        print(f"WARNING: Could not find second occurrence of '{title}'")
        continue
    
    # Extract from this position to the next section marker
    # The next section would be another "What is" or "Lesson" commentary header
    chunk = text[pos:pos+8000]
    
    # Clean up: remove "Paragraph N" markers, normalize whitespace
    # The PDF extraction has "Paragraph 1", "Paragraph 2" etc.
    chunk = re.sub(r'\nParagraph \d+\n', '\n\n', chunk)
    
    # Find where the actual content ends (before next "What is" or "Commentary on" or "Lesson 3")
    end_markers = [
        re.search(r'\nWhat is ', chunk[len(title)+10:]),
        re.search(r'\nCommentary on What', chunk[len(title)+10:]),
        re.search(r'\nLesson 3[2-9]\d', chunk[len(title)+10:]),
        re.search(r'\nLesson [4-9]\d\d', chunk[len(title)+10:]),
    ]
    
    end_pos = len(chunk)
    for m in end_markers:
        if m:
            candidate = len(title) + 10 + m.start()
            if candidate < end_pos:
                end_pos = candidate
    
    content = chunk[:end_pos].strip()
    
    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)
    
    results[key] = content
    print(f"{key}: {len(content)} chars")
    print(f"  First 150: {content[:150]!r}")
    print()

# Save individual files
os.makedirs('/home/ubuntu/acim_flashcards/data/whatis_workbook', exist_ok=True)
for key, content in results.items():
    filepath = f'/home/ubuntu/acim_flashcards/data/whatis_workbook/{key}.txt'
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Saved {filepath}")
