"""
Post-process acim_companion.html:
Find ALL CAPS words/phrases (2+ uppercase letters, possibly with spaces/punctuation)
that appear in text content (not inside HTML tag attributes or existing style tags)
and wrap them with <span style="font-variant:small-caps">Title Case</span>.

Strategy: work on text nodes only — i.e. content between > and <
that is NOT inside a <style> or <script> block.
"""

import re

with open('/home/ubuntu/acim_flashcards/acim_companion.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We'll process only the content OUTSIDE <script> and <style> blocks
# Split into segments: script/style blocks (leave alone) vs everything else (process)

# Pattern to match ALL CAPS sequences: 2+ uppercase letters, allowing spaces, /, &amp;, !, ?, .
# but NOT things like CSS property names or HTML attributes
ALLCAPS_RE = re.compile(
    r'\b([A-Z][A-Z][A-Z\s/!?&;\.]*[A-Z][!?]*)\b'
)

def title_case_caps(s):
    """Convert ALL CAPS string to Title Case for display inside small-caps span."""
    # Preserve punctuation at end
    stripped = s.rstrip('!?.')
    punct = s[len(stripped):]
    # Title case each word
    titled = ' '.join(w.capitalize() for w in stripped.split())
    return titled + punct

def process_text_segment(text):
    """Apply small-caps to ALL CAPS words in a text segment (between HTML tags)."""
    def replacer(m):
        caps = m.group(1)
        # Skip if it's just 2 chars that might be abbreviations like 'OR', 'OR' connector
        # Actually we DO want those too per Steven's request
        # Skip HTML entities like &amp; &lt; etc
        if caps.startswith('&') or caps.endswith(';'):
            return m.group(0)
        # Skip if already inside a small-caps span (won't happen here since we split)
        titled = title_case_caps(caps)
        return f'<span style="font-variant:small-caps;font-weight:inherit">{titled}</span>'
    return ALLCAPS_RE.sub(replacer, text)

# Split HTML into: script blocks, style blocks, and everything else
# We process "everything else" segments for text between tags

# Step 1: protect <script>...</script> and <style>...</style> blocks
protected = []
def protect(m):
    idx = len(protected)
    protected.append(m.group(0))
    return f'\x00PROTECTED{idx}\x00'

html_work = re.sub(r'<(script|style)[^>]*>.*?</\1>', protect, html, flags=re.DOTALL | re.IGNORECASE)

# Step 2: protect HTML tags themselves (< ... >)
tags = []
def protect_tag(m):
    idx = len(tags)
    tags.append(m.group(0))
    return f'\x01TAG{idx}\x01'

html_work = re.sub(r'<[^>]+>', protect_tag, html_work)

# Step 3: Now html_work contains only text nodes + our placeholders
# Apply small-caps to ALL CAPS in text nodes
html_work = process_text_segment(html_work)

# Step 4: Restore tags
def restore_tag(m):
    return tags[int(m.group(1))]
html_work = re.sub(r'\x01TAG(\d+)\x01', restore_tag, html_work)

# Step 5: Restore protected blocks
def restore_protected(m):
    return protected[int(m.group(1))]
html_work = re.sub(r'\x00PROTECTED(\d+)\x00', restore_protected, html_work)

with open('/home/ubuntu/acim_flashcards/acim_companion.html', 'w', encoding='utf-8') as f:
    f.write(html_work)

print(f"Done. File size: {len(html_work):,} bytes")

# Quick check: count how many small-caps spans we added
count = html_work.count('font-variant:small-caps')
print(f"Total small-caps spans: {count}")
