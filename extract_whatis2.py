#!/usr/bin/env python3
"""Extract the 'Commentary on What Is...?' sections from the PDF, 
   separating them from the individual lesson commentaries."""

import re
import json
import os

# Read the full text
with open("/home/ubuntu/acim_flashcards/data/pdf_full_text.txt") as f:
    all_text = f.read()

# Find all Commentary on What Is headers (the actual ones, not TOC)
# The TOC ones are in the first ~400 lines, actual ones start later
lines = all_text.split('\n')

# Find the actual commentary sections and lesson headers
whatis_sections = []
lesson_headers = []

for i, line in enumerate(lines):
    # Match "Commentary on What Is/is/Am X?" 
    m = re.match(r'^Commentary on What [Ii]s (.+?)(\?)?$', line.strip())
    if m and i > 200:  # Skip TOC entries (first ~200 lines)
        whatis_sections.append({
            'topic': m.group(1).strip('?').strip(),
            'line': i,
            'full_title': line.strip()
        })
    
    m2 = re.match(r'^Commentary on What [Aa]m I\??$', line.strip())
    if m2 and i > 200:
        whatis_sections.append({
            'topic': 'What Am I',
            'line': i,
            'full_title': line.strip()
        })
    
    # Match LESSON headers
    m3 = re.match(r'^LESSON (\d+)$', line.strip())
    if m3:
        lesson_headers.append({
            'lesson_num': int(m3.group(1)),
            'line': i
        })

print(f"Found {len(whatis_sections)} What Is sections:")
for s in whatis_sections:
    print(f"  Line {s['line']}: {s['full_title']}")

print(f"\nFound {len(lesson_headers)} lesson headers")

# For each What Is section, extract text up to the first LESSON header after it
whatis_mapping = {
    'Forgiveness': {'lessons': range(221, 231)},
    'Salvation': {'lessons': range(231, 241)},
    'the World': {'lessons': range(241, 251)},
    'Sin': {'lessons': range(251, 261)},
    'the Body': {'lessons': range(261, 271)},
    'the Christ': {'lessons': range(271, 281)},
    'the Holy Spirit': {'lessons': range(281, 291)},
    'the Real World': {'lessons': range(291, 301)},
    'the Second Coming': {'lessons': range(301, 311)},
    'the Last Judgment': {'lessons': range(311, 321)},
    'Creation': {'lessons': range(321, 331)},
    'the Ego': {'lessons': range(331, 341)},
    'a Miracle': {'lessons': range(341, 351)},
    'What Am I': {'lessons': range(351, 361)},
}

os.makedirs("/home/ubuntu/acim_flashcards/data/whatis_commentaries", exist_ok=True)

results = []

for sec in whatis_sections:
    topic = sec['topic']
    start_line = sec['line']
    
    # Find the first LESSON header after this section
    end_line = len(lines)
    first_lesson = None
    for lh in lesson_headers:
        if lh['line'] > start_line:
            end_line = lh['line']
            first_lesson = lh['lesson_num']
            break
    
    # Extract the text
    section_text = '\n'.join(lines[start_line:end_line]).strip()
    
    # Clean up page markers
    section_text = re.sub(r'--- PAGE \d+ ---', '', section_text)
    section_text = re.sub(r'– \d+ –', '', section_text)
    section_text = re.sub(r'\n{3,}', '\n\n', section_text)
    
    word_count = len(section_text.split())
    
    print(f"\n{sec['full_title']}:")
    print(f"  Lines {start_line}-{end_line} ({word_count} words)")
    print(f"  Ends before Lesson {first_lesson}")
    print(f"  First 100 chars: {section_text[:100]}...")
    
    # Save to file
    filename = topic.lower().replace(' ', '_').replace('?', '')
    filepath = f"/home/ubuntu/acim_flashcards/data/whatis_commentaries/{filename}.txt"
    with open(filepath, 'w') as f:
        f.write(section_text)
    
    results.append({
        'topic': topic,
        'full_title': sec['full_title'],
        'word_count': word_count,
        'filename': f"{filename}.txt",
        'lessons': list(whatis_mapping.get(topic, {}).get('lessons', []))
    })

# Save index
with open("/home/ubuntu/acim_flashcards/data/whatis_commentaries/index.json", 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n\nSaved {len(results)} sections to data/whatis_commentaries/")

# Also extract the Part II practice instructions summary that appears in each lesson
# (the short bullet-point version)
print("\n\nLooking for the short practice instructions summary...")
for lh in lesson_headers:
    if lh['lesson_num'] == 221:
        # Get the practice instructions from lesson 221
        start = lh['line']
        end = start + 30
        print('\n'.join(lines[start:end]))
        break
