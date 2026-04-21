#!/usr/bin/env python3
"""Fix the Big T CSS and HTML to use double braces for f-string escaping."""

with open('/home/ubuntu/acim_flashcards/build_html.py', 'r') as f:
    content = f.read()

# The CSS was inserted with single braces but needs double braces
# Find the Big T CSS block and fix it
# It starts with "/* Big T / Little t Chart */" and ends before "/* Principles */"

import re

# Extract the Big T CSS section
pattern = r'(/\* Big T / Little t Chart \*/.*?)(/\* Principles \*/)'
match = re.search(pattern, content, re.DOTALL)

if match:
    bigt_css = match.group(1)
    # Replace single { with {{ and single } with }}
    # But be careful not to double-escape already doubled ones
    fixed_css = bigt_css.replace('{', '{{').replace('}', '}}')
    content = content[:match.start()] + fixed_css + match.group(2) + content[match.end():]
    print("Fixed Big T CSS braces")
else:
    print("ERROR: Could not find Big T CSS section")

# Also fix the HTML in the ref-bigt section - find it and double-brace it
# The HTML was inserted with single braces too
# Find from ref-bigt to ref-ce
pattern2 = r'(<div class="ref-section" id="ref-bigt">.*?</div>\s*</div>\s*</div>)(\s*<div class="ref-section" id="ref-ce">)'
match2 = re.search(pattern2, content, re.DOTALL)

if match2:
    bigt_html = match2.group(1)
    # Check if it has single braces that need doubling
    # The bigt-* classes and inline styles use single braces
    # But we need to be careful - the HTML attributes use quotes not braces
    # Actually the issue is only CSS braces inside style attributes
    # Let's check what's there
    print(f"Found ref-bigt HTML block ({len(bigt_html)} chars)")
    # The HTML itself doesn't have CSS braces that need escaping
    # The issue was only in the CSS block above
else:
    print("WARNING: Could not find ref-bigt HTML section")

with open('/home/ubuntu/acim_flashcards/build_html.py', 'w') as f:
    f.write(content)

print("Done!")
