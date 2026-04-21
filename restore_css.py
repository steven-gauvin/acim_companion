"""
Restore the missing base CSS that was accidentally removed by the review integration regex.
The regex that removed old reviews CSS also ate the :root variables and all base styling.
"""
import re

# Read the backup to get the base CSS (everything from <style> to QUOTES PANEL)
with open('/tmp/backup_extract/build_html.py') as f:
    backup = f.read()

# Extract base CSS from backup (up to but not including QUOTES PANEL)
m = re.search(r'(<style>\n.*?)(\/\* =+\n   QUOTES PANEL)', backup, re.DOTALL)
base_css_with_old_reviews = m.group(1)

# We need the base CSS but WITHOUT the old reviews panel CSS
# The old reviews CSS starts with "/* REVIEWS PANEL */" or similar
# Let's find where the reviews CSS starts and cut it
reviews_start = re.search(r'/\*.*?REVIEWS PANEL.*?\*/', base_css_with_old_reviews)
if reviews_start:
    base_css = base_css_with_old_reviews[:reviews_start.start()]
    print(f"Found old reviews CSS at position {reviews_start.start()}, cutting it")
else:
    base_css = base_css_with_old_reviews
    print("No old reviews CSS found in base, using as-is")

print(f"Base CSS length: {len(base_css)} chars")

# Now read the current build_html.py
with open('build_html.py') as f:
    current = f.read()

# The current file starts with <style> followed immediately by QUOTES PANEL
# We need to replace <style>\n\n/* QUOTES PANEL with the full base CSS + /* QUOTES PANEL
current = current.replace(
    '<style>\n\n/* ============================================================\n   QUOTES PANEL',
    base_css + '\n/* ============================================================\n   QUOTES PANEL'
)

with open('build_html.py', 'w') as f:
    f.write(current)

print("Base CSS restored!")

# Verify
with open('build_html.py') as f:
    check = f.read()
has_root = ':root' in check
has_base = 'BASE & RESET' in check
print(f":root present: {has_root}")
print(f"BASE & RESET present: {has_base}")
