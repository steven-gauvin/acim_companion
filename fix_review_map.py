"""
Fix the REVIEW_MAP injection — it was put directly into the f-string,
but needs to be a Python variable like lessons_json.
"""
import re, json

with open('build_html.py', 'r', encoding='utf-8') as f:
    src = f.read()

# 1. Extract the inline REVIEW_MAP JSON from the JS section
# It's on a line like: const REVIEW_MAP = {...};
m = re.search(r'const REVIEW_MAP = (\{.*?\});', src, re.DOTALL)
if m:
    review_map_json_raw = m.group(1)
    print(f"Found inline REVIEW_MAP ({len(review_map_json_raw)} chars)")
    
    # Save it to a separate file for loading
    with open('/tmp/review_map.json', 'w', encoding='utf-8') as f:
        f.write(review_map_json_raw)
    
    # Replace the inline JSON with a Python variable reference
    old_line = f'const REVIEW_MAP = {review_map_json_raw};'
    new_line = 'const REVIEW_MAP = {review_map_json};'
    src = src.replace(old_line, new_line)
    
    # Add the Python variable at the top, after the other json variables
    src = src.replace(
        "cause_effect_json = json.dumps(data['cause_effect'], ensure_ascii=False)\n",
        "cause_effect_json = json.dumps(data['cause_effect'], ensure_ascii=False)\n\n# Review map: lesson_num -> review info\nwith open('/tmp/review_map.json', 'r', encoding='utf-8') as _rf:\n    review_map_json = _rf.read()\n"
    )
    
    with open('build_html.py', 'w', encoding='utf-8') as f:
        f.write(src)
    
    print("Fixed! REVIEW_MAP now loaded as Python variable.")
else:
    print("ERROR: Could not find inline REVIEW_MAP")
