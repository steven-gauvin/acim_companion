#!/usr/bin/env python3
"""Add Big T / Little t chart to Reference tab and update dedication."""

import re

with open('/home/ubuntu/acim_flashcards/build_html.py', 'r') as f:
    content = f.read()

# 1. Add CSS for Big T / Little t chart
bigt_css = """/* Big T / Little t Chart */
.bigt-chart { padding: 8px 0; }
.bigt-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid rgba(201,168,76,0.08);
}
.bigt-row:last-child { border-bottom: none; }
.bigt-left {
  flex: 1; text-align: left; font-size: 14px; color: var(--text-dim);
  font-style: italic; letter-spacing: 0.5px;
}
.bigt-center {
  width: 40px; text-align: center; font-size: 16px; color: rgba(201,168,76,0.25);
}
.bigt-right {
  flex: 1; text-align: right; font-size: 14px; color: var(--gold);
  font-weight: 600; letter-spacing: 0.5px;
}
.bigt-header-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 0 8px; border-bottom: 2px solid var(--gold-dim);
  margin-bottom: 4px;
}
.bigt-header-left {
  flex: 1; text-align: left; font-size: 11px; color: var(--text-dim);
  letter-spacing: 2px; text-transform: uppercase;
}
.bigt-header-right {
  flex: 1; text-align: right; font-size: 11px; color: var(--gold);
  letter-spacing: 2px; text-transform: uppercase;
}
.bigt-quote {
  margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border);
  text-align: center;
}
.bigt-quote-text {
  font-size: 14px; color: var(--text); font-style: italic; line-height: 1.6;
  margin-bottom: 8px;
}
.bigt-quote-source {
  font-size: 11px; color: var(--gold-dim); letter-spacing: 1px;
}

"""

# Insert before /* Principles */
content = content.replace('/* Principles */\n.principle-item {{', bigt_css + '/* Principles */\n.principle-item {{')

# 2. Build the Big T / Little t chart HTML for the Reference tab
# The pairs: little t (left) vs Big T (right)
pairs = [
    ('death', 'Life'),
    ('darkness', 'Light'),
    ('perception', 'Knowledge'),
    ('false', 'True'),
    ('ego', 'Soul'),
    ('wrong mind', 'Right Mind'),
    ('ego / body', 'Holy Spirit'),
    ('fear', 'Love'),
    ('make', 'Create'),
    ('illusions', 'Reality'),
    ("man's self", "God's Self"),
    ('conflict', 'Peace'),
    ('imprisonment', 'Freedom'),
    ('time', 'Eternity'),
]

rows_html = ''
for left, right in pairs:
    rows_html += f'<div class="bigt-row"><div class="bigt-left">{left}</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">{right}</div></div>\n'

bigt_chart_html = f'''<div class="bigt-chart">
  <div class="bigt-header-row">
    <div class="bigt-header-left">little t</div>
    <div style="width:40px"></div>
    <div class="bigt-header-right">Big T</div>
  </div>
  {rows_html}
  <div class="bigt-quote">
    <div class="bigt-quote-text">&ldquo;I am that I am being present in all there is.&rdquo;</div>
    <div class="bigt-quote-source">Sandy Levey-Lund&eacute;n &middot; <em>I Just Want Peace</em></div>
  </div>
</div>'''

# 3. Insert the Big T chart as the FIRST section in the Reference tab
# Find the list.innerHTML = ` line and add our section before the first ref-section
old_ref_start = '''  list.innerHTML = `
    <div class="ref-section" id="ref-ce">'''

new_ref_start = f'''  list.innerHTML = `
    <div class="ref-section" id="ref-bigt">
      <div class="ref-header" onclick="toggleRef('ref-bigt')">
        <div>
          <div class="ref-title">Big T / Little t</div>
          <div class="ref-subtitle">Truth vs. perception &mdash; Sandy Levey-Lund&eacute;n, OnPurpose</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">{bigt_chart_html}</div>
    </div>
    <div class="ref-section" id="ref-ce">'''

content = content.replace(old_ref_start, new_ref_start)

# 4. Update the dedication
old_dedication = '''<div class="splash-dedication">
    <div class="splash-dedication-text">Dedicated to the One Self we share.<br>With love, light and laughter.</div>
    <div class="splash-dedication-names">To my friends at On Purpose and Clearmind</div>
  </div>'''

new_dedication = '''<div class="splash-dedication">
    <div class="splash-dedication-text">To the One Self we all share.<br>To each and every soul that I have met along my journey.<br>To those in every corner of the world who have touched my life.<br>And to those who have not yet crossed paths.</div>
    <div class="splash-dedication-names" style="margin-top:12px">To my brother JP, my grandparents, my friends at On Purpose<br>Sandy Levey-Lund&eacute;n, Clearmind, Duane O&rsquo;Kane, and also Sharon.</div>
    <div class="splash-dedication-names" style="margin-top:16px;font-style:italic;color:var(--gold)">To Him Who sent me.</div>
    <div class="splash-dedication-names" style="margin-top:12px">I say thank you.</div>
  </div>'''

content = content.replace(old_dedication, new_dedication)

with open('/home/ubuntu/acim_flashcards/build_html.py', 'w') as f:
    f.write(content)

print("Done! Added Big T / Little t chart and updated dedication.")
