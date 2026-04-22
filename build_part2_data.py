#!/usr/bin/env python3
"""Build the Part II data JSON for embedding in the app."""

import json
import os
import re

# Part II mapping: What Is section -> lessons
WHATIS_MAPPING = [
    {'key': 'forgiveness',     'title': 'What Is Forgiveness?',      'lessons': list(range(221, 231))},
    {'key': 'salvation',       'title': 'What Is Salvation?',         'lessons': list(range(231, 241))},
    {'key': 'the_world',       'title': 'What Is the World?',         'lessons': list(range(241, 251))},
    {'key': 'sin',             'title': 'What Is Sin?',               'lessons': list(range(251, 261))},
    {'key': 'the_body',        'title': 'What Is the Body?',          'lessons': list(range(261, 271))},
    {'key': 'the_christ',      'title': 'What Is the Christ?',        'lessons': list(range(271, 281))},
    {'key': 'the_holy_spirit', 'title': 'What Is the Holy Spirit?',   'lessons': list(range(281, 291))},
    {'key': 'the_real_world',  'title': 'What Is the Real World?',    'lessons': list(range(291, 301))},
    {'key': 'the_second_coming','title': 'What Is the Second Coming?','lessons': list(range(301, 311))},
    {'key': 'the_last_judgment','title': 'What Is the Last Judgment?','lessons': list(range(311, 321))},
    {'key': 'creation',        'title': 'What Is Creation?',          'lessons': list(range(321, 331))},
    {'key': 'the_ego',         'title': 'What Is the Ego?',           'lessons': list(range(331, 341))},
    {'key': 'a_miracle',       'title': 'What Is a Miracle?',         'lessons': list(range(341, 351))},
    {'key': 'what_am_i',       'title': 'What Am I?',                 'lessons': list(range(351, 361))},
]

def clean_text(text):
    """Clean up extracted PDF text."""
    # Remove page markers
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    text = re.sub(r'– \d+ –', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text

# Read the intro and practice instructions
with open('/home/ubuntu/acim_flashcards/data/part2_intro_commentary.txt') as f:
    intro_text = f.read().strip()

with open('/home/ubuntu/acim_flashcards/data/part2_practice_instructions.txt') as f:
    practice_text = f.read().strip()

# Read all What Is commentaries
whatis_data = {}
for section in WHATIS_MAPPING:
    filepath = f"/home/ubuntu/acim_flashcards/data/whatis_commentaries/{section['key']}.txt"
    if os.path.exists(filepath):
        with open(filepath) as f:
            text = clean_text(f.read())
        whatis_data[section['key']] = {
            'title': section['title'],
            'text': text,
            'lessons': section['lessons'],
            'word_count': len(text.split())
        }
        print(f"  {section['title']}: {len(text.split())} words")
    else:
        print(f"  WARNING: Missing file for {section['key']}")

# Build the lesson -> What Is mapping
lesson_to_whatis = {}
for section in WHATIS_MAPPING:
    for lesson_num in section['lessons']:
        lesson_to_whatis[lesson_num] = section['key']

# Also handle lessons 361-365 (final lessons, no What Is section)
# They use "What Am I?" as their section
for n in range(361, 366):
    lesson_to_whatis[n] = 'what_am_i'

# Build the final Part II data structure
part2_data = {
    'intro': {
        'title': 'The Introduction to Part II',
        'text': intro_text
    },
    'practice_instructions': {
        'title': 'Practice Instructions Part II',
        'text': practice_text
    },
    'whatis_sections': whatis_data,
    'lesson_to_whatis': {str(k): v for k, v in lesson_to_whatis.items()}
}

# Save as JSON
output_path = '/tmp/part2_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(part2_data, f, ensure_ascii=False, indent=2)

print(f"\nPart II data saved to {output_path}")
print(f"  Intro: {len(intro_text.split())} words")
print(f"  Practice Instructions: {len(practice_text.split())} words")
print(f"  What Is sections: {len(whatis_data)}")
print(f"  Lesson mappings: {len(lesson_to_whatis)}")

# Verify
print("\nLesson mappings sample:")
for n in [221, 231, 241, 251, 261, 271, 281, 291, 301, 311, 321, 331, 341, 351, 361, 365]:
    print(f"  Lesson {n} -> {lesson_to_whatis.get(n, 'NOT FOUND')}")
