"""
Integrate reviews into the Library — remove the separate Reviews tab,
add review badges and intro access to review lessons in the Library.
"""
import re, json

# Load the current build_html.py
with open('build_html.py', 'r', encoding='utf-8') as f:
    src = f.read()

# ============================================================
# 1. Build the REVIEW_MAP JS object from the REVIEWS data
# ============================================================
with open('acim_companion.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const REVIEWS = (\[.*?\]);', html, re.DOTALL)
reviews = json.loads(m.group(1))

# Build a map: lesson_num -> { reviewName, reviewIdx, instructions, reviewedLessons }
review_map = {}
for idx, r in enumerate(reviews):
    roman = ['I', 'II', 'III', 'IV', 'V', 'VI'][idx]
    for entry in r.get('entries', []):
        day = entry['day']
        reviewed = [l['num'] for l in entry['lessons']]
        review_map[day] = {
            'name': f'Review {roman}',
            'subtitle': r['subtitle'],
            'instructions': r['instructions'],
            'reviewed': reviewed
        }

review_map_json = json.dumps(review_map, ensure_ascii=False)

# ============================================================
# 2. Remove the Reviews tab button
# ============================================================
# Change: <div class="tab" onclick="switchTab('reviews')">Reviews</div>
src = src.replace(
    """    <div class="tab" onclick="switchTab('reviews')">Reviews</div>""",
    ""  # Remove it
)

# ============================================================
# 3. Remove the Reviews panel HTML
# ============================================================
src = src.replace(
    """    <!-- REVIEWS PANEL -->
    <div id="panel-reviews" class="panel reviews-panel">
      <div id="reviews-list"></div>
    </div>""",
    ""
)

# ============================================================
# 4. Remove 'reviews' from the tab names array
# ============================================================
src = src.replace(
    "const names = ['cards','library','reviews','quotes','meditations','reference'];",
    "const names = ['cards','library','quotes','meditations','reference'];"
)

# ============================================================
# 5. Remove the renderReviews call from switchTab
# ============================================================
src = src.replace(
    "if (name === 'reviews') renderReviews();",
    ""
)

# ============================================================
# 6. Add REVIEW_MAP constant after REVIEWS constant
# ============================================================
# Replace the old REVIEWS constant with REVIEW_MAP
src = src.replace(
    f"const REVIEWS = {{reviews_raw}};",
    f"const REVIEW_MAP = {review_map_json};"
)

# ============================================================
# 7. Remove renderReviews, toggleReview, toggleReviewDay functions
# ============================================================
# Find and remove the renderReviews function block
src = re.sub(
    r'// REVIEWS\n// =+\nfunction renderReviews\(\).*?function toggleReview\(i\).*?\n.*?function toggleReviewDay\(id\).*?\n',
    '',
    src,
    flags=re.DOTALL
)

# ============================================================
# 8. Add CSS for review badges and intro blocks
# ============================================================
review_css = """
/* REVIEW INTEGRATION */
.review-badge {{
  display: inline-block;
  background: var(--gold);
  color: var(--bg);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 2px 6px;
  border-radius: 3px;
  margin-left: 6px;
  vertical-align: middle;
  text-transform: uppercase;
}}
.review-intro-btn {{
  display: inline-block;
  background: transparent;
  border: 1px solid var(--gold-dim);
  color: var(--gold);
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin: 8px 0;
}}
.review-intro-btn:hover {{ background: var(--bg3); }}
.review-intro-content {{
  display: none;
  background: var(--bg2);
  border-left: 3px solid var(--gold);
  padding: 12px 14px;
  margin: 8px 0;
  font-size: 12px;
  color: var(--text-dim);
  line-height: 1.6;
  white-space: pre-wrap;
  border-radius: 0 4px 4px 0;
}}
.review-intro-content.open {{ display: block; }}
.review-refs {{
  margin: 8px 0;
  padding: 8px 12px;
  background: var(--bg2);
  border-radius: 4px;
}}
.review-refs-title {{
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gold-dim);
  margin-bottom: 6px;
}}
.review-ref-link {{
  display: inline-block;
  background: var(--bg3);
  color: var(--gold);
  font-size: 11px;
  padding: 3px 8px;
  margin: 2px 4px 2px 0;
  border-radius: 3px;
  cursor: pointer;
  text-decoration: none;
  border: 1px solid var(--border);
}}
.review-ref-link:hover {{ background: var(--gold); color: var(--bg); }}
"""

# Insert review CSS before the quotes section CSS
src = src.replace(
    ".quotes-section-title",
    review_css + "\n.quotes-section-title"
)

# ============================================================
# 9. Modify renderLibrary to add review badges and intro
# ============================================================
# In the lesson-header, after the lesson-num-badge, add review badge
# Find the line that creates the lesson header
old_header = """<span class="lesson-num-badge">${{isSpecialLib ? '\\u2726' : l.num}}</span>
        <span class="lesson-title-text">${{hl(escHtml(l.title))}}</span>"""

new_header = """<span class="lesson-num-badge">${{isSpecialLib ? '\\u2726' : l.num}}</span>
        ${{REVIEW_MAP[l.num] ? '<span class="review-badge">' + REVIEW_MAP[l.num].name + '</span>' : ''}}
        <span class="lesson-title-text">${{hl(escHtml(l.title))}}</span>"""

src = src.replace(old_header, new_header)

# Add review intro block inside the lesson body, before the notes
old_body_start = """<div class="lesson-body">
        ${{notesHtml}}"""

new_body_start = """<div class="lesson-body">
        ${{REVIEW_MAP[l.num] ? `
          <button class="review-intro-btn" onclick="toggleReviewIntro(${{l.num}}, event)">
            ▶ ${{REVIEW_MAP[l.num].name}} Introduction
          </button>
          <div class="review-intro-content" id="rev-intro-${{l.num}}">${{escHtml(REVIEW_MAP[l.num].instructions)}}</div>
          <div class="review-refs">
            <div class="review-refs-title">Reviewing Lessons</div>
            ${{REVIEW_MAP[l.num].reviewed.map(n => {
              const rl = LESSONS.find(x => x.num === n);
              return rl ? '<span class="review-ref-link" onclick="jumpToLesson(' + n + ', event)">' + n + '. ' + escHtml(rl.title) + '</span>' : '';
            }).join('')}}
          </div>` : ''}}
        ${{notesHtml}}"""

src = src.replace(old_body_start, new_body_start)

# ============================================================
# 10. Add toggleReviewIntro and jumpToLesson functions
# ============================================================
# Add after the toggleSG function area
toggle_funcs = """
function toggleReviewIntro(num, e) {{
  e.stopPropagation();
  const el = document.getElementById('rev-intro-' + num);
  const btn = el.previousElementSibling;
  el.classList.toggle('open');
  btn.textContent = el.classList.contains('open')
    ? '▼ ' + REVIEW_MAP[num].name + ' Introduction'
    : '▶ ' + REVIEW_MAP[num].name + ' Introduction';
}}

function jumpToLesson(num, e) {{
  e.stopPropagation();
  // Scroll to the lesson in the library
  const el = document.getElementById('lib-' + num);
  if (el) {{
    el.classList.add('expanded');
    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
  }}
}}
"""

# Insert after toggleSG function
src = src.replace(
    "// ============================================================\n// QUOTES",
    toggle_funcs + "\n// ============================================================\n// QUOTES"
)

# ============================================================
# 11. Also remove the reviews_raw variable loading at the top
# ============================================================
src = src.replace(
    "reviews_match = re.search(r'const REVIEWS = (\\[.*?\\]);', orig, re.DOTALL)\n",
    ""
)
src = src.replace(
    "reviews_raw = reviews_match.group(1) if reviews_match else '[]'\n",
    ""
)

# ============================================================
# 12. Remove reviews CSS that's no longer needed
# ============================================================
# Remove the old reviews panel CSS block
src = re.sub(
    r'/\*.*?REVIEWS PANEL.*?\*/\n\.reviews-panel.*?\.review-lesson-link \{\{.*?\}\}\n',
    '',
    src,
    flags=re.DOTALL
)

# ============================================================
# 13. Also add review badge to the flashcard view
# ============================================================
# Find the card rendering for the front face
# We need to check renderCard function
# The card front shows lesson number and title

# ============================================================
# Save
# ============================================================
with open('build_html.py', 'w', encoding='utf-8') as f:
    f.write(src)

print("Done! Reviews integrated into Library.")
print(f"REVIEW_MAP has {len(review_map)} entries")
