#!/usr/bin/env python3
with open('/home/ubuntu/acim_flashcards/build_html.py', 'r') as f:
    content = f.read()

old = '''    <div class="splash-dedication-names" style="margin-top:12px">I say thank you.</div>
  </div>'''

new = '''    <div class="splash-dedication-names" style="margin-top:12px">I say thank you.</div>
    <div class="splash-dedication-names" style="margin-top:24px;font-size:10px;letter-spacing:1.5px;color:var(--text-dim)">Compiled with love by Steven Gauvin</div>
  </div>'''

content = content.replace(old, new)

with open('/home/ubuntu/acim_flashcards/build_html.py', 'w') as f:
    f.write(content)

print("Done!")
