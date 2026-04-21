#!/usr/bin/env python3
"""Find the review intro lesson numbers and which lessons reference them."""
import json, re

with open('/tmp/app_data.json', 'r') as f:
    data = json.load(f)

with open('/tmp/review_map.json', 'r') as f:
    review_map = json.load(f)

# Show review map structure
print("=== REVIEW MAP KEYS (first 5) ===")
for i, (k, v) in enumerate(review_map.items()):
    if i >= 5: break
    print(f"  Lesson {k}: {v.get('name', '?')} — reviewed: {v.get('reviewed', [])[:3]}...")
    print(f"    instructions: {v.get('instructions', '')[:100]}...")

# Find all "See review X practice instructions on page Y" in sg_data
print("\n=== ALL 'SEE REVIEW' REFERENCES ===")
sg = data['sg_data']
review_page_map = {}  # review_name -> {page, lessons, intro_lesson}

for key, lesson in sg.items():
    try:
        num = int(key)
    except:
        continue
    for part in lesson.get('parts', []):
        text = part.get('text', '')
        m = re.match(r'^See (review \w+) practice instructions on page (\d+)', text, re.IGNORECASE)
        if m:
            rname = m.group(1)
            page = m.group(2)
            if rname not in review_page_map:
                review_page_map[rname] = {'page': page, 'lessons': [], 'full_text': text}
            review_page_map[rname]['lessons'].append(num)

# Also find "See complete instructions on page X"
complete_refs = {}
for key, lesson in sg.items():
    try:
        num = int(key)
    except:
        continue
    for part in lesson.get('parts', []):
        text = part.get('text', '')
        m = re.match(r'^See complete instructions on page (\d+)', text, re.IGNORECASE)
        if m:
            page = m.group(1)
            if page not in complete_refs:
                complete_refs[page] = {'lessons': [], 'full_text': text[:200]}
            complete_refs[page]['lessons'].append(num)

# Now figure out which lesson is the intro for each review
# Review I: Lessons 51-60 (intro = 51)
# Review II: Lessons 81-90 (intro = 81) -- but we saw lesson 82 has the ref?
# Review III: Lessons 111-120 (intro = 111)
# Review IV: Lessons 141-150 (intro = 141? or 131?)
# Review V: Lessons 171-180 (intro = 171)
# Review VI: Lessons 201-220 (intro = 201)

print("\nReview references found:")
for rname, info in sorted(review_page_map.items()):
    lessons = sorted(info['lessons'])
    print(f"  {rname}: page {info['page']}, lessons {lessons[0]}-{lessons[-1]}")
    print(f"    Full text: {info['full_text']}")

print("\n'See complete instructions' references:")
for page, info in sorted(complete_refs.items()):
    lessons = sorted(info['lessons'])
    print(f"  page {page}: lessons {lessons[0]}-{lessons[-1]} ({len(lessons)} lessons)")
    print(f"    Text: {info['full_text'][:150]}")

# Check which lessons have review_map entries (these are the review lessons with intros)
print("\n=== REVIEW MAP ENTRIES (intro lessons) ===")
for k, v in sorted(review_map.items(), key=lambda x: int(x[0])):
    print(f"  Lesson {k}: {v['name']}")

# Check what the intro lesson for each review section looks like in sg_data
print("\n=== SG_DATA FOR REVIEW INTRO LESSONS ===")
for intro_num in ['51', '81', '111', '141', '171', '201']:
    if intro_num in sg:
        parts = sg[intro_num].get('parts', [])
        first_text = parts[0].get('text', '')[:200] if parts else 'NO PARTS'
        print(f"\n  Lesson {intro_num}: {len(parts)} parts")
        print(f"    First part: {first_text}")
    else:
        print(f"\n  Lesson {intro_num}: NOT IN SG_DATA")
