#!/usr/bin/env python3
"""Find all unique 'See review ... page X' references and other page refs in sg_data."""

import json
import re

with open('/tmp/app_data.json', 'r') as f:
    data = json.load(f)

sg = data.get('sg_data', {})

# Collect all unique "See review..." messages
review_refs = {}  # page -> {review_name, lesson_numbers}
other_page_refs = {}  # lesson_num -> page refs in longer notes

for key, lesson in sg.items():
    try:
        num = int(key)
    except:
        continue
    
    parts = lesson.get('parts', [])
    for part in parts:
        text = part.get('text', '')
        
        # Check for "See review X practice instructions on page Y"
        m = re.search(r'See (review \w+) practice instructions on page (\d+)', text, re.IGNORECASE)
        if m:
            review_name = m.group(1)
            page = m.group(2)
            if page not in review_refs:
                review_refs[page] = {'review': review_name, 'lessons': []}
            review_refs[page]['lessons'].append(num)
        else:
            # Check for other page references in longer notes
            page_matches = re.findall(r'page (\d+)', text, re.IGNORECASE)
            if page_matches:
                other_page_refs[num] = {
                    'pages': page_matches,
                    'text_preview': text[:200]
                }

print("=" * 60)
print("REVIEW PRACTICE INSTRUCTION REFERENCES")
print("=" * 60)
for page, info in sorted(review_refs.items(), key=lambda x: int(x[0])):
    lessons = sorted(info['lessons'])
    print(f"\n  {info['review'].upper()} — page {page}")
    print(f"  Lessons: {lessons[0]}–{lessons[-1]} ({len(lessons)} lessons)")

print("\n" + "=" * 60)
print("OTHER PAGE REFERENCES (in longer commentary notes)")
print("=" * 60)
for num, info in sorted(other_page_refs.items()):
    # Skip if it's just a review ref we already captured
    print(f"\n  Lesson {num}: pages {info['pages']}")
    print(f"  Preview: {info['text_preview'][:150]}...")

# Now show what the review intro lessons look like
print("\n" + "=" * 60)
print("REVIEW INTRO LESSONS (the ones that START each review)")
print("=" * 60)
review_intros = [51, 61, 81, 91, 111, 131, 151, 171, 181, 201, 221]
for num in review_intros:
    key = str(num)
    if key in sg:
        lesson = sg[key]
        parts = lesson.get('parts', [])
        text = parts[0].get('text', '') if parts else ''
        print(f"\n  Lesson {num}:")
        print(f"  {text[:300]}")
