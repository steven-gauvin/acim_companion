#!/usr/bin/env python3
"""Find all page number references in app data and study notes."""

import json
import re

# Load app data
with open('/tmp/app_data.json', 'r') as f:
    data = json.load(f)

# Broader regex for page references
page_re = re.compile(r'(page\s*\d+|p\.\s*\d+|pg\.?\s*\d+|p\s+\d{2,3}\b|\bp\d{2,3}\b)', re.IGNORECASE)
# Also catch standalone 3-digit numbers that might be page refs
num_re = re.compile(r'\b(\d{3})\b')

print("=" * 60)
print("SEARCHING ALL LESSON NOTES FOR PAGE REFERENCES")
print("=" * 60)

found = 0
for lesson in data.get('lessons', []):
    num = lesson.get('number', '?')
    notes = lesson.get('notes', '')
    title = lesson.get('title', '')
    
    matches = page_re.findall(notes)
    if matches:
        found += 1
        print(f"\nLesson {num}: {title}")
        print(f"  Notes: {notes[:200]}...")
        print(f"  Page refs: {matches}")

if not found:
    print("\nNo explicit 'page' references found in lesson notes.")

# Search more broadly - look at all string fields
print("\n" + "=" * 60)
print("SEARCHING ALL STRING VALUES IN APP DATA")
print("=" * 60)

def search_dict(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            search_dict(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            search_dict(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        matches = page_re.findall(obj)
        if matches:
            print(f"\n{path}:")
            print(f"  Value: {obj[:300]}")
            print(f"  Matches: {matches}")

search_dict(data)

# Also search Steven's study notes
print("\n" + "=" * 60)
print("SEARCHING STEVEN'S STUDY NOTES")
print("=" * 60)

try:
    with open('/home/ubuntu/acim_flashcards/steven_acim_study_notes.md', 'r') as f:
        notes_text = f.read()
    
    for i, line in enumerate(notes_text.split('\n'), 1):
        matches = page_re.findall(line)
        if matches:
            print(f"\n  Line {i}: {line.strip()}")
            print(f"  Matches: {matches}")
except FileNotFoundError:
    print("  Study notes file not found")

# Search the apple notes too
print("\n" + "=" * 60)
print("SEARCHING APPLE NOTES TEXT FILES")
print("=" * 60)

import os
notes_dir = '/home/ubuntu/acim_flashcards/apple_notes_text'
for fname in sorted(os.listdir(notes_dir)):
    if not fname.endswith('.txt'):
        continue
    with open(os.path.join(notes_dir, fname), 'r') as f:
        text = f.read()
    
    matches_found = False
    for i, line in enumerate(text.split('\n'), 1):
        matches = page_re.findall(line)
        if matches:
            if not matches_found:
                print(f"\n--- {fname} ---")
                matches_found = True
            print(f"  Line {i}: {line.strip()[:150]}")

# Now let's look specifically at what lesson 111 (Review III) says
print("\n" + "=" * 60)
print("REVIEW LESSONS AND THEIR NOTES")
print("=" * 60)

for lesson in data.get('lessons', []):
    num = lesson.get('number', 0)
    notes = lesson.get('notes', '')
    title = lesson.get('title', '')
    
    # Show all review lessons
    if 'review' in title.lower() or 'review' in notes.lower():
        print(f"\nLesson {num}: {title}")
        print(f"  Notes: {notes[:500]}")

# Show lesson 111 specifically
print("\n" + "=" * 60)
print("LESSON 111 SPECIFICALLY")
print("=" * 60)
for lesson in data.get('lessons', []):
    if lesson.get('number') == 111:
        print(json.dumps(lesson, indent=2))

# Show all lessons with "practice" or "instruction" in notes
print("\n" + "=" * 60)
print("LESSONS WITH 'PRACTICE' OR 'INSTRUCTION' IN NOTES")
print("=" * 60)
for lesson in data.get('lessons', []):
    num = lesson.get('number', 0)
    notes = lesson.get('notes', '')
    title = lesson.get('title', '')
    if 'practice' in notes.lower() or 'instruction' in notes.lower() or 'p 237' in notes.lower() or '237' in notes:
        print(f"\nLesson {num}: {title}")
        print(f"  Notes: {notes[:500]}")
