#!/usr/bin/env python3
"""
ACIM Lesson Study Guide & Recommended Text Reading
by Dee Doyle & Allen Watson (Circle of Atonement)
HTML Builder — Personal Use Only
"""

import re
import json
import html as html_module

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Read both source files
# ─────────────────────────────────────────────────────────────────────────────

with open('/home/ubuntu/upload/_LessonandReadingGuide-1.txt', 'r', encoding='utf-8') as f:
    part1_text = f.read()

with open('/home/ubuntu/upload/_LessonandReadingGuide-2.txt', 'r', encoding='utf-8') as f:
    part2_text = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Spelling corrections (only typos, never content changes)
# ─────────────────────────────────────────────────────────────────────────────

SPELLING_FIXES = [
    ('attonment', 'Atonement'),
    ('attonment', 'atonement'),
    ('Attonment', 'Atonement'),
    ('teh ', 'the '),
    ('recieve', 'receive'),
    ('beleive', 'believe'),
    ('seperate', 'separate'),
    ('occured', 'occurred'),
    ('untill', 'until'),
    ('wich', 'which'),
    ('wihch', 'which'),
    ('practise instructions', 'practice instructions'),
    ('Practise instructions', 'Practice instructions'),
]

def apply_spelling_fixes(text):
    for wrong, right in SPELLING_FIXES:
        text = text.replace(wrong, right)
    return text

part1_text = apply_spelling_fixes(part1_text)
part2_text = apply_spelling_fixes(part2_text)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Parse lessons from text
# ─────────────────────────────────────────────────────────────────────────────

def parse_lessons(text, part_label):
    """Parse lessons from text, returning list of lesson dicts."""
    lessons = []
    
    # Split on lesson headers: "Lesson N" at start of line
    # Also handle Review sections
    lesson_pattern = re.compile(
        r'^(Lesson\s+(\d+))\s*\n(.*?)(?=^Lesson\s+\d+|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    matches = list(lesson_pattern.finditer(text))
    
    for match in matches:
        lesson_num = int(match.group(2))
        content = match.group(3).strip()
        
        # Extract lesson title (first quoted line or first non-empty line)
        title = ''
        title_match = re.match(r'^"([^"]+)"', content)
        if title_match:
            title = title_match.group(1)
            content = content[title_match.end():].strip()
        else:
            # Try first line
            first_line = content.split('\n')[0].strip()
            if first_line and not first_line.lower().startswith('practice'):
                title = first_line
                content = '\n'.join(content.split('\n')[1:]).strip()
        
        # Split into sections
        sections = parse_lesson_sections(content)
        
        lessons.append({
            'num': lesson_num,
            'title': title,
            'sections': sections,
            'part': part_label
        })
    
    return lessons

def parse_lesson_sections(content):
    """Parse a lesson's content into named sections."""
    sections = {}
    
    # Define section markers
    section_markers = [
        ('practice_instructions', r'Practice instructions?\s*\n'),
        ('commentary', r'Commentary\s*\n'),
        ('reading', r'(?:Recommended\s+)?A Course in Miracles reading\s*\n'),
        ('practice_suggestions', r'Practice (?:suggestions?|comments?|suggestion)\s*\n'),
    ]
    
    # Find positions of each section
    positions = []
    for section_name, pattern in section_markers:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            positions.append((m.start(), m.end(), section_name))
    
    positions.sort(key=lambda x: x[0])
    
    if not positions:
        # No sections found, treat all as commentary
        sections['commentary'] = content.strip()
        return sections
    
    # Extract text before first section
    if positions[0][0] > 0:
        pre_text = content[:positions[0][0]].strip()
        if pre_text:
            sections['intro'] = pre_text
    
    # Extract each section
    for i, (start, end, name) in enumerate(positions):
        if i + 1 < len(positions):
            section_text = content[end:positions[i+1][0]].strip()
        else:
            section_text = content[end:].strip()
        
        # Merge duplicate sections (e.g. multiple practice sections)
        if name in sections:
            sections[name] += '\n\n' + section_text
        else:
            sections[name] = section_text
    
    return sections

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Parse Reviews
# ─────────────────────────────────────────────────────────────────────────────

def parse_reviews(text):
    """Parse review sections from Part I text."""
    reviews = []
    
    # Note: source text has 'Review I\t\n' (tab after header) so we use [\t ]* to match
    review_pattern = re.compile(
        r'^(Review\s+([IVX]+))[\t ]*\n(.*?)(?=^Review\s+[IVX]+[\t ]*\n|\Z)',
        re.MULTILINE | re.DOTALL
    )
    
    for match in review_pattern.finditer(text):
        review_name = match.group(1).strip()
        review_num = match.group(2).strip()
        content = match.group(3).strip()
        
        reviews.append({
            'name': review_name,
            'num': review_num,
            'content': content
        })
    
    return reviews

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: Parse What Is sections from Part II
# ─────────────────────────────────────────────────────────────────────────────

# What Is section BLA URL slugs (from betterlifeawareness.com sitemap)
WHAT_IS_BLA_SLUGS = {
    'What Is Forgiveness?': 'acim-book-workbook-1-what-is-forgiveness',
    'What Is Salvation?': 'acim-book-workbook-2-what-is-salvation',
    'What is the World?': 'acim-book-workbook-3-what-is-the-world',
    'What is Sin?': 'acim-book-workbook-4-what-is-sin',
    'What is the Body?': 'acim-book-workbook-5-what-is-the-body',
    'What is the Christ?': 'acim-book-workbook-6-what-is-the-christ',
    'What is the Holy Spirit?': 'acim-book-workbook-7-what-is-the-holy-spirit',
    'What is the Real World?': 'acim-book-workbook-8-what-is-the-real-world',
    'What is the Second Coming?': 'acim-book-workbook-9-what-is-the-second-coming',
    'What is the Last Judgment?': 'acim-book-workbook-10-what-is-the-last-judgement',
    'What is Creation?': 'acim-book-workbook-11-what-is-creation',
    'What is the Ego?': 'acim-book-workbook-12-what-is-the-ego',
    'What is a Miracle?': 'acim-book-workbook-13-what-is-a-miracle',
    'What Am I?': 'acim-book-workbook-14-what-am-i',
}

def parse_what_is_sections(text):
    """Parse 'What Is...' commentary sections from Part II."""
    what_is = []
    
    # Also handles 'What Am I?' (the 14th section)
    pattern = re.compile(
        r'Commentary on (What (?:Is|Am) [^?\n]+\??)\s*\n(.*?)(?=Commentary on What|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    
    for match in pattern.finditer(text):
        title = match.group(1).strip()
        content = match.group(2).strip()
        # Build BLA URL: match case-insensitively
        bla_url = ''
        for key, slug in WHAT_IS_BLA_SLUGS.items():
            if key.lower() == title.lower():
                bla_url = f'https://www.betterlifeawareness.com/{slug}'
                break
        what_is.append({
            'title': title,
            'content': content,
            'bla_url': bla_url,
        })
    
    return what_is

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6: Parse front matter (Preface, When Should You...)
# ─────────────────────────────────────────────────────────────────────────────

def extract_front_matter(text):
    """Extract preface and morning quiet time sections."""
    sections = {}
    
    # Preface
    preface_match = re.search(r'Preface\s*\n(.*?)(?=When Should You|Part I|\Z)', text, re.DOTALL)
    if preface_match:
        sections['preface'] = preface_match.group(1).strip()
    
    # When Should You Take Your Morning Quiet Time
    morning_match = re.search(r'When Should You Take Your Morning Quiet Time\?\s*\n(.*?)(?=Part I|\Z)', text, re.DOTALL)
    if morning_match:
        sections['morning_quiet_time'] = morning_match.group(1).strip()
    
    return sections

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7: Parse Appendix sections
# ─────────────────────────────────────────────────────────────────────────────

def parse_appendix(text):
    """Parse appendix sections."""
    appendix = []
    
    # Find appendix start
    appendix_match = re.search(r'^Appendix\s*\n(.*)', text, re.MULTILINE | re.DOTALL)
    if not appendix_match:
        return appendix
    
    appendix_text = appendix_match.group(1)
    
    # Known appendix section titles
    titles = [
        'Name of God Meditation',
        'Think Not You Made The World',
        'Open Mind Meditation',
        'Let Us Pray',
        'Practice Instructions Part II',
    ]
    
    # Build pattern
    title_pattern = '|'.join(re.escape(t) for t in titles)
    parts = re.split(r'(' + title_pattern + r')', appendix_text)
    
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if part in titles:
            content = parts[i+1].strip() if i+1 < len(parts) else ''
            appendix.append({'title': part, 'content': content})
            i += 2
        else:
            i += 1
    
    return appendix

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8: Run all parsers
# ─────────────────────────────────────────────────────────────────────────────

print("Parsing Part I lessons...")
part1_lessons = parse_lessons(part1_text, 'I')
print(f"  Found {len(part1_lessons)} lessons")

print("Parsing Part II lessons...")
part2_lessons = parse_lessons(part2_text, 'II')
print(f"  Found {len(part2_lessons)} lessons")

print("Parsing Reviews...")
reviews = parse_reviews(part1_text)
print(f"  Found {len(reviews)} reviews")

print("Parsing What Is sections...")
what_is_sections = parse_what_is_sections(part2_text)
print(f"  Found {len(what_is_sections)} What Is sections")

print("Parsing front matter...")
front_matter_1 = extract_front_matter(part1_text)
front_matter_2 = extract_front_matter(part2_text)

print("Parsing appendix...")
appendix_1 = parse_appendix(part1_text)
appendix_2 = parse_appendix(part2_text)

# Combine all lessons
all_lessons = sorted(part1_lessons + part2_lessons, key=lambda x: x['num'])

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9: Helper functions for HTML rendering
# ─────────────────────────────────────────────────────────────────────────────

def esc(text):
    """Escape HTML special characters."""
    return html_module.escape(str(text)) if text else ''

def format_text_block(text):
    """Format a block of text into HTML paragraphs, preserving structure."""
    if not text:
        return ''
    
    lines = text.split('\n')
    result = []
    current_para = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Detect bullet points
        if stripped.startswith('•') or stripped.startswith('·') or re.match(r'^\d+\.\s', stripped):
            if current_para:
                result.append('<p>' + esc(' '.join(current_para)) + '</p>')
                current_para = []
            if not in_list:
                result.append('<ul class="sg-list">')
                in_list = True
            item_text = re.sub(r'^[•·]\s*', '', stripped)
            item_text = re.sub(r'^\d+\.\s*', '', item_text)
            result.append('<li>' + esc(item_text) + '</li>')
        elif stripped.startswith('\t') or (line.startswith('    ') and stripped):
            # Indented content - treat as list item or indented block
            if current_para:
                result.append('<p>' + esc(' '.join(current_para)) + '</p>')
                current_para = []
            if in_list:
                result.append('<li class="indented">' + esc(stripped) + '</li>')
            else:
                result.append('<p class="indented">' + esc(stripped) + '</p>')
        elif stripped == '':
            if in_list:
                result.append('</ul>')
                in_list = False
            if current_para:
                result.append('<p>' + esc(' '.join(current_para)) + '</p>')
                current_para = []
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            current_para.append(stripped)
    
    if in_list:
        result.append('</ul>')
    if current_para:
        result.append('<p>' + esc(' '.join(current_para)) + '</p>')
    
    return '\n'.join(result)

def format_practice_instructions(text):
    """Format practice instructions with special styling for Purpose/Exercise/Remarks."""
    if not text:
        return ''
    
    lines = text.split('\n')
    result = ['<div class="practice-block">']
    current_label = None
    current_content = []
    
    label_pattern = re.compile(r'^(Purpose|Exercise|Remarks?|Response to temptation|Reading the|Morning/evening|Hourly|Frequent|Practice suggestions?|Practice comments?)\s*:?\s*(.*)', re.IGNORECASE)
    
    def flush():
        if current_label and current_content:
            content_html = format_text_block('\n'.join(current_content))
            result.append(f'<div class="practice-item"><span class="practice-label">{esc(current_label)}:</span><div class="practice-content">{content_html}</div></div>')
        elif current_content:
            result.append(format_text_block('\n'.join(current_content)))
    
    for line in lines:
        stripped = line.strip()
        m = label_pattern.match(stripped)
        if m:
            flush()
            current_label = m.group(1)
            current_content = [m.group(2)] if m.group(2) else []
        elif stripped:
            current_content.append(stripped)
        else:
            if current_content:
                current_content.append('')
    
    flush()
    result.append('</div>')
    return '\n'.join(result)

def format_what_is_content(text):
    """Format What Is section content with proper structure:
    - 'Paragraph N' headers styled as section markers
    - ACIM quoted text in a styled blockquote with citation
    - Watson's commentary in clean readable paragraphs
    """
    if not text:
        return ''
    
    # Split content into paragraphs by 'Paragraph N' markers
    # Pattern: 'Paragraph N\n{ACIM quote block}\t\n({citation})\n{commentary}'
    # OR:      'Paragraph N\n{ACIM quote block} ({citation})\n{commentary}'
    
    # Split by paragraph markers
    para_split = re.split(r'(?=^Paragraph \d+$)', text, flags=re.MULTILINE)
    
    result = []
    
    for chunk in para_split:
        if not chunk.strip():
            continue
        
        # Check if this chunk starts with a Paragraph marker
        para_match = re.match(r'^Paragraph (\d+)\n(.*)', chunk, re.DOTALL)
        if para_match:
            para_num = para_match.group(1)
            rest = para_match.group(2)
            
            # Emit paragraph header
            result.append(f'<h5 class="what-is-para-header">Paragraph {para_num}</h5>')
            
            # Now parse the rest: ACIM quote block + citation + commentary
            # The ACIM quote ends with either:
            #   a) '\t\n({citation})\n' (tab before newline, then citation on its own line)
            #   b) ' ({citation})\n'    (citation inline at end of last sentence)
            
            # Try pattern a: quote ends with \t\n, citation on next line
            quote_a = re.match(
                r'(.*?)\t\n\(([^)]+)\)\n(.*)',
                rest, re.DOTALL
            )
            # Try pattern b: citation inline at end of quote
            quote_b = re.match(
                r'(.*?) \(([^)]+)\)\n(.*)',
                rest, re.DOTALL
            )
            
            if quote_a:
                quote_text = quote_a.group(1).strip()
                citation = quote_a.group(2).strip()
                commentary = quote_a.group(3).strip()
            elif quote_b:
                quote_text = quote_b.group(1).strip()
                citation = quote_b.group(2).strip()
                commentary = quote_b.group(3).strip()
            else:
                # No citation found, treat entire rest as commentary
                quote_text = ''
                citation = ''
                commentary = rest.strip()
            
            # Render ACIM quote block
            if quote_text:
                # Build citation link if it's a workbook citation
                cit_html = ''
                if citation:
                    # Try to extract lesson number for a link
                    # W-pII.1.1:1-7 -> lesson 1 of What Is Forgiveness
                    # The 'What Is' sections are numbered 1-14 in Part II
                    cit_w_match = re.match(r'W-pII\.(\d+)\.', citation)
                    if cit_w_match:
                        # This is a What Is section citation - link to the section
                        cit_html = f'<cite class="what-is-citation">({esc(citation)})</cite>'
                    else:
                        cit_html = f'<cite class="what-is-citation">({esc(citation)})</cite>'
                
                result.append(f'''<blockquote class="acim-quote">
  <p class="acim-quote-text">{esc(quote_text)}</p>
  {cit_html}
</blockquote>''')
            
            # Render commentary
            if commentary:
                result.append('<div class="what-is-commentary">')
                result.append(format_text_block(commentary))
                result.append('</div>')
        else:
            # Content before first paragraph marker (shouldn't normally happen)
            if chunk.strip():
                result.append(format_text_block(chunk))
    
    return '\n'.join(result)


def format_reading_ref(text):
    """Format a reading reference with a link to betterlifeawareness.com."""
    if not text:
        return ''
    
    text = text.strip()
    if text.lower() in ['no text reading today.', 'no text reading for today.', 'none.', '']:
        return '<p class="reading-ref no-reading">No text reading today.</p>'
    
    # Try to build a link from the reference
    # Pattern: T-27.VII.1 or W-pI.121 or M-4.I.A
    ref_match = re.match(r'^([TtWwMm]-[^\s—]+)', text)
    if ref_match:
        ref = ref_match.group(1)
        url = build_bla_url(ref)
        rest = text[ref_match.end():].strip()
        rest_html = f'<span class="reading-desc">—{esc(rest)}</span>' if rest else ''
        if url:
            return f'<p class="reading-ref"><a href="{url}" target="_blank" class="reading-link">📖 {esc(ref)}</a>{rest_html}</p>'
    
    return f'<p class="reading-ref">📖 {esc(text)}</p>'

# ── Text URL lookup (built from betterlifeawareness.com sitemap) ──
# Maps 'T-{chap}.{ROMAN}' -> slug for betterlifeawareness.com
TEXT_URL_LOOKUP = {
  "T-1.I": "acim-book-text-1i-principles-of-miracles",
  "T-1.II": "acim-book-text-1ii-revelation-time-and-miracles",
  "T-1.III": "acim-book-text-1iii-atonement-and-miracles",
  "T-1.IV": "acim-book-text-1iv-the-escape-from-darkness",
  "T-1.V": "acim-book-text-1v-wholeness-and-spirit",
  "T-1.VI": "acim-book-text-1vi-the-illusion-of-needs",
  "T-1.VII": "acim-book-text-1vii-distortions-of-miracle-impulses",
  "T-2.I": "acim-book-text-2i-the-origins-of-separation",
  "T-2.II": "acim-book-text-2ii-the-atonement-as-defense",
  "T-2.III": "acim-book-text-2iii-fear-as-lack-of-love",
  "T-2.IV": "acim-book-text-2iv-the-correction-for-lack-of-love",
  "T-2.V": "acim-book-text-2v-the-meaning-of-the-last-judgment",
  "T-2.VI": "acim-book-text-2vi-fear-and-conflict",
  "T-2.VII": "acim-book-text-2vii-cause-and-effect",
  "T-2.VIII": "acim-book-text-2viii-the-meaning-of-the-last-judgment",
  "T-3.I": "acim-book-text-3i-special-principles-for-miracle-workers",
  "T-3.II": "acim-book-text-3ii-miracles-as-true-perception",
  "T-3.III": "acim-book-text-3iii-perception-versus-knowledge",
  "T-3.IV": "acim-book-text-3iv-error-and-the-ego",
  "T-3.V": "acim-book-text-3v-conflict-and-the-ego",
  "T-3.VI": "acim-book-text-3vi-judgment-and-the-authority-problem",
  "T-3.VII": "acim-book-text-3vii-creating-versus-the-self-image",
  "T-4.I": "acim-book-text-4i-right-teaching-and-right-learning",
  "T-4.II": "acim-book-text-4ii-the-ego-and-false-autonomy",
  "T-4.III": "acim-book-text-4iii-love-without-conflict",
  "T-4.IV": "acim-book-text-4iv-this-need-not-be",
  "T-4.V": "acim-book-text-4v-the-ego-body-illusion",
  "T-4.VI": "acim-book-text-4vi-the-rewards-of-god",
  "T-4.VII": "acim-book-text-4vii-creation-and-communication",
  "T-5.I": "acim-book-text-5i-the-invitation-to-the-holy-spirit",
  "T-5.II": "acim-book-text-5ii-the-voice-for-god",
  "T-5.III": "acim-book-text-5iii-the-guide-to-salvation",
  "T-5.IV": "acim-book-text-5iv-teaching-and-healing",
  "T-5.V": "acim-book-text-5v-the-function-of-the-ego",
  "T-5.VI": "acim-book-text-5vi-time-and-eternity",
  "T-5.VII": "acim-book-text-5vii-the-decision-for-god",
  "T-6.I": "acim-book-text-6i-the-message-of-the-crucifixion",
  "T-6.II": "acim-book-text-6ii-the-alternative-to-projection",
  "T-6.III": "acim-book-text-6iii-the-relinquishment-of-attack",
  "T-6.IV": "acim-book-text-6iv-the-only-answer",
  "T-6.V": "acim-book-text-6v-the-lessons-of-the-holy-spirit",
  "T-7.I": "acim-book-text-7i-the-last-step",
  "T-7.II": "acim-book-text-7ii-the-law-of-the-kingdom",
  "T-7.III": "acim-book-text-7iii-the-reality-of-the-kingdom",
  "T-7.IV": "acim-book-text-7iv-healing-as-the-recognition-of-truth",
  "T-7.V": "acim-book-text-7v-healing-and-the-changelessness-of-mind",
  "T-7.VI": "acim-book-text-7vi-from-vigilance-to-peace",
  "T-7.VII": "acim-book-text-7vii-the-totality-of-the-kingdom",
  "T-7.VIII": "acim-book-text-7viii-the-defense-of-conflict",
  "T-7.IX": "acim-book-text-7ix-the-extension-of-the-kingdom",
  "T-7.X": "acim-book-text-7x-the-confusion-of-pain-and-joy",
  "T-7.XI": "acim-book-text-7xi-the-state-of-grace",
  "T-8.I": "acim-book-text-8i-the-direction-of-the-curriculum",
  "T-8.II": "acim-book-text-8ii-the-difference-between-imprisonment-and-freedom",
  "T-8.III": "acim-book-text-8iii-the-holy-encounter",
  "T-8.IV": "acim-book-text-8iv-the-gift-of-freedom",
  "T-8.V": "acim-book-text-8v-the-undivided-will",
  "T-8.VI": "acim-book-text-8vi-the-treasure-of-god",
  "T-8.VII": "acim-book-text-8vii-the-body-as-means-or-end",
  "T-8.VIII": "acim-book-text-8viii-the-body-as-means-or-end",
  "T-8.IX": "acim-book-text-8ix-healing-as-corrected-perception",
  "T-9.I": "acim-book-text-9i-the-acceptance-of-reality",
  "T-9.II": "acim-book-text-9ii-the-answer-to-prayer",
  "T-9.III": "acim-book-text-9iii-the-correction-of-error",
  "T-9.IV": "acim-book-text-9iv-the-holy-spirit-s-plan-of-forgiveness",
  "T-9.V": "acim-book-text-9v-the-unhealed-healer",
  "T-9.VI": "acim-book-text-9vi-the-saints-of-god",
  "T-9.VII": "acim-book-text-9vii-the-two-evaluations",
  "T-9.VIII": "acim-book-text-9viii-grandeur-versus-grandiosity",
  "T-10.I": "acim-book-text-10i-at-home-in-god",
  "T-10.II": "acim-book-text-10ii-the-decision-to-forget",
  "T-10.III": "acim-book-text-10iii-the-god-of-sickness",
  "T-10.IV": "acim-book-text-10iv-the-end-of-sickness",
  "T-10.V": "acim-book-text-10v-the-denial-of-god",
  "T-11.I": "acim-book-text-11i-the-gifts-of-fatherhood",
  "T-11.II": "acim-book-text-11ii-the-invitation-to-healing",
  "T-11.III": "acim-book-text-11iii-from-darkness-to-light",
  "T-11.IV": "acim-book-text-11iv-the-inheritance-of-gods-son",
  "T-11.V": "acim-book-text-11v-the-dynamics-of-the-ego",
  "T-11.VI": "acim-book-text-11vi-walking-to-redemption",
  "T-11.VII": "acim-book-text-11vii-the-condition-of-reality",
  "T-11.VIII": "acim-book-text-11viii-the-problem-and-the-answer",
  "T-12.I": "acim-book-text-12i-the-judgement-of-the-holy-spirit",
  "T-12.II": "acim-book-text-12ii-the-way-to-remember-god",
  "T-12.III": "acim-book-text-12iii-the-investment-in-reality",
  "T-12.IV": "acim-book-text-12iv-seeking-and-finding",
  "T-12.V": "acim-book-text-12v-the-sane-curriculum",
  "T-12.VI": "acim-book-text-12vi-the-vision-of-christ",
  "T-12.VII": "acim-book-text-12vii-looking-within",
  "T-12.VIII": "acim-book-text-12viii-the-attraction-of-love-for-love",
  "T-13.I": "acim-book-text-13i-the-role-of-healing",
  "T-13.II": "acim-book-text-13ii-the-guiltless-son",
  "T-13.III": "acim-book-text-13iii-the-fear-of-redemption",
  "T-13.IV": "acim-book-text-13-iv-the-function-of-time",
  "T-13.V": "acim-book-text-13v-the-two-emotions",
  "T-13.VI": "acim-book-text-13-vi-finding-the-present",
  "T-13.VII": "acim-book-text-13-vii-attainment-of-the-real-world",
  "T-13.VIII": "acim-book-text-13-viii-from-perception-to-knowledge",
  "T-13.IX": "acim-book-text-13-ix-the-cloud-of-guilt",
  "T-13.X": "acim-book-text-13x-release-from-guilt",
  "T-13.XI": "acim-book-text-13xi-the-peace-of-heaven",
  "T-14.I": "acim-book-text-14i-the-conditions-of-learning",
  "T-14.II": "acim-book-text-14ii-the-happy-learner",
  "T-14.III": "acim-book-text-14iii-the-decision-for-guiltlessness",
  "T-14.IV": "acim-book-text-14iv-your-function-in-the-atonement",
  "T-14.V": "acim-book-text-14v-the-circle-of-atonement",
  "T-14.VI": "acim-book-text-14vi-the-light-of-communication",
  "T-14.VII": "acim-book-text-14vii-the-recognition-of-truth",
  "T-14.VIII": "acim-book-text-14viii-the-holy-meeting-place",
  "T-14.IX": "acim-book-text-14ix-the-reflection-of-holiness",
  "T-14.X": "acim-book-text-14x-the-equality-of-miracles",
  "T-14.XI": "acim-book-text-14xi-the-test-of-truth",
  "T-15.I": "acim-book-text-15i-the-two-uses-of-time",
  "T-15.II": "acim-book-text-15ii-the-end-of-doubt",
  "T-15.III": "acim-book-text-15iii-slipping-into-the-present",
  "T-15.IV": "acim-book-text-15iv-practicing-the-holy-instant",
  "T-15.V": "acim-book-text-15v-the-holy-instant-and-special-relationships",
  "T-15.VI": "acim-book-text-15vi-the-holy-instant-and-the-laws-of-god",
  "T-15.VII": "acim-book-text-15vii-the-holy-instant-and-communication",
  "T-15.VIII": "acim-book-text-15viii-the-holy-instant-and-real-relationships",
  "T-15.IX": "acim-book-text-15ix-the-holy-instant-and-the-attraction-of-god",
  "T-15.X": "acim-book-text-15x-the-time-of-rebirth",
  "T-15.XI": "acim-book-text-15xi-christmas-as-the-end-of-sacrifice",
  "T-16.I": "acim-book-text-16i-true-empathy",
  "T-16.II": "acim-book-text-16ii-the-magnitude-of-holiness",
  "T-16.III": "acim-book-text-16iii-the-reward-of-teaching",
  "T-16.IV": "acim-book-text-16iv-illusion-and-reality-of-love",
  "T-16.V": "acim-book-text-16v-the-choice-for-completion",
  "T-16.VI": "acim-book-text-16vi-the-bridge-to-the-real-world",
  "T-16.VII": "acim-book-text-16vii-the-end-of-illusions",
  "T-17.I": "acim-book-text-17i-bringing-fantasy-to-truth",
  "T-17.II": "acim-book-text-17ii-the-forgiven-world",
  "T-17.III": "acim-book-text-17iii-shadows-of-the-past",
  "T-17.IV": "acim-book-text-17iv-the-two-pictures",
  "T-17.V": "acim-book-text-17v-the-healed-relationship",
  "T-17.VI": "acim-book-text-17vi-setting-the-goal",
  "T-17.VII": "acim-book-text-17vii-the-call-for-faith",
  "T-17.VIII": "acim-book-text-17viii-the-conditions-of-peace",
  "T-18.I": "acim-book-text-18i-the-substitute-reality",
  "T-18.II": "acim-book-text-18ii-the-basis-of-the-dream",
  "T-18.III": "acim-book-text-18iii-light-in-the-dream",
  "T-18.IV": "acim-book-text-18iv-the-little-willingness",
  "T-18.V": "acim-book-text-18v-the-happy-dream",
  "T-18.VI": "acim-book-text-18vi-beyond-the-body",
  "T-18.VII": "acim-book-text-18vii-i-need-do-nothing",
  "T-18.VIII": "acim-book-text-18viii-the-little-garden",
  "T-18.IX": "acim-book-text-18ix-the-two-worlds",
  "T-19.I": "acim-book-text-19i-the-unreality-of-sin",
  "T-19.II": "acim-book-text-19ii-sin-versus-error",
  "T-19.III": "acim-book-text-19iii-the-unreality-of-sin",
  "T-19.IV": "acim-book-text-19iv-the-obstacles-to-peace",
  "T-20.I": "acim-book-text-20i-the-holy-week",
  "T-20.II": "acim-book-text-20ii-the-gift-of-lilies",
  "T-20.III": "acim-book-text-20iii-sin-as-adjustment",
  "T-20.IV": "acim-book-text-20iv-entering-the-ark",
  "T-20.V": "acim-book-text-20v-the-function-of-the-holy-relationship",
  "T-20.VI": "acim-book-text-20vi-the-temple-of-the-holy-spirit",
  "T-20.VII": "acim-book-text-20vii-the-consistency-of-means-and-end",
  "T-20.VIII": "acim-book-text-20viii-the-vision-of-sinlessness",
  "T-21.I": "acim-book-text-21i-the-forgotten-song",
  "T-21.II": "acim-book-text-21ii-the-responsibility-for-sight",
  "T-21.III": "acim-book-text-21iii-faith-belief-and-vision",
  "T-21.IV": "acim-book-text-21iv-the-fear-to-look-within",
  "T-21.V": "acim-book-text-21v-the-function-of-reason",
  "T-21.VI": "acim-book-text-21vi-reason-versus-madness",
  "T-21.VII": "acim-book-text-21vii-the-inner-shift",
  "T-21.VIII": "acim-book-text-21viii-the-inner-shift",
  "T-22.I": "acim-book-text-22i-the-end-of-vision",
  "T-22.II": "acim-book-text-22ii-your-brothers-sinlessness",
  "T-22.III": "acim-book-text-22iii-reason-and-the-forms-of-error",
  "T-22.IV": "acim-book-text-22iv-the-branching-of-the-road",
  "T-22.V": "acim-book-text-22v-the-branching-of-the-road",
  "T-22.VI": "acim-book-text-22vi-the-light-of-the-holy-relationship",
  "T-23.I": "acim-book-text-23i-the-contradiction-in-the-ego",
  "T-23.II": "acim-book-text-23ii-the-laws-of-chaos",
  "T-23.III": "acim-book-text-23iii-salvation-without-compromise",
  "T-23.IV": "acim-book-text-23iv-above-the-battleground",
  "T-24.I": "acim-book-text-24i-specialness-as-a-substitute-for-love",
  "T-24.II": "acim-book-text-24ii-the-treachery-of-specialness",
  "T-24.III": "acim-book-text-24iii-the-forgiveness-of-specialness",
  "T-24.IV": "acim-book-text-24iv-specialness-and-salvation",
  "T-24.V": "acim-book-text-24v-the-resolution-of-the-dream",
  "T-24.VI": "acim-book-text-24vi-the-special-function",
  "T-24.VII": "acim-book-text-24vii-the-meeting-place",
  "T-25.I": "acim-book-text-25i-the-link-to-truth",
  "T-25.II": "acim-book-text-25ii-the-savior-from-the-dark",
  "T-25.III": "acim-book-text-25iii-salvation-and-the-holy-instant",
  "T-25.IV": "acim-book-text-25iv-the-light-you-bring",
  "T-25.V": "acim-book-text-25v-the-justice-of-god",
  "T-25.VI": "acim-book-text-25vi-the-special-function",
  "T-25.VII": "acim-book-text-25vii-the-rock-of-salvation",
  "T-25.VIII": "acim-book-text-25viii-justice-returned-to-love",
  "T-25.IX": "acim-book-text-25ix-the-justice-of-heaven",
  "T-26.I": "acim-book-text-26i-the-borderland",
  "T-26.II": "acim-book-text-26ii-many-forms-one-correction",
  "T-26.III": "acim-book-text-26iii-the-forgiving-dream",
  "T-26.IV": "acim-book-text-26iv-where-sin-has-left",
  "T-26.V": "acim-book-text-26v-the-little-hindrance",
  "T-26.VI": "acim-book-text-26vi-the-appointed-friend",
  "T-26.VII": "acim-book-text-26vii-the-laws-of-healing",
  "T-26.VIII": "acim-book-text-26viii-the-immediacy-of-salvation",
  "T-26.IX": "acim-book-text-26ix-for-they-have-come",
  "T-26.X": "acim-book-text-26x-the-end-of-injustice",
  "T-27.I": "acim-book-text-27i-the-picture-of-crucifixion",
  "T-27.II": "acim-book-text-27ii-the-fear-of-healing",
  "T-27.III": "acim-book-text-27iii-beyond-all-symbols",
  "T-27.IV": "acim-book-text-27iv-the-quiet-answer",
  "T-27.V": "acim-book-text-27v-the-healing-example",
  "T-27.VI": "acim-book-text-27vi-the-witnesses-to-sin",
  "T-27.VII": "acim-book-text-27vii-the-dreamer-of-the-dream",
  "T-27.VIII": "acim-book-text-27viii-the-hero-of-the-dream",
  "T-28.I": "acim-book-text-28i-the-present-memory",
  "T-28.II": "acim-book-text-28ii-reversing-effect-and-cause",
  "T-28.III": "acim-book-text-28iii-the-agreement-to-join",
  "T-28.IV": "acim-book-text-28iv-the-greater-joining",
  "T-28.V": "acim-book-text-28v-the-body-as-dream-figure",
  "T-28.VI": "acim-book-text-28vi-the-secret-vows",
  "T-28.VII": "acim-book-text-28vii-the-ark-of-safety",
  "T-29.I": "acim-book-text-29i-the-closing-of-the-gap",
  "T-29.II": "acim-book-text-29ii-the-invitation-to-healing",
  "T-29.III": "acim-book-text-29iii-god-s-witnesses",
  "T-29.IV": "acim-book-text-29iv-dream-roles",
  "T-29.V": "acim-book-text-29v-the-changeless-dwelling-place",
  "T-29.VI": "acim-book-text-29vi-forgiveness-and-the-end-of-time",
  "T-29.VII": "acim-book-text-29vii-the-puzzle-of-perception",
  "T-29.VIII": "acim-book-text-29viii-the-anti-christ",
  "T-29.IX": "acim-book-text-29ix-the-forgiving-dream",
  "T-30.I": "acim-book-text-30i-the-rules-for-decision",
  "T-30.II": "acim-book-text-30ii-freedom-of-will",
  "T-30.III": "acim-book-text-30iii-beyond-all-idols",
  "T-30.IV": "acim-book-text-30iv-the-truth-behind-illusions",
  "T-30.V": "acim-book-text-30v-the-only-purpose",
  "T-30.VI": "acim-book-text-30vi-the-justification-for-forgiveness",
  "T-30.VII": "acim-book-text-30vii-the-new-interpretation",
  "T-30.VIII": "acim-book-text-30viii-changeless-reality",
  "T-31.I": "acim-book-text-31i-the-simplicity-of-salvation",
  "T-31.II": "acim-book-text-31ii-the-selfishness-of-the-ego",
  "T-31.III": "acim-book-text-31iii-the-self-concept-versus-the-self",
  "T-31.IV": "acim-book-text-31iv-self-concept-versus-self",
  "T-31.V": "acim-book-text-31v-the-real-alternative",
  "T-31.VI": "acim-book-text-31vi-recognizing-the-spirit",
  "T-31.VII": "acim-book-text-31vii-the-savior-s-vision",
  "T-31.VIII": "acim-book-text-31viii-choose-once-again",
}

def build_bla_url(ref):
    """Build a betterlifeawareness.com URL from an ACIM reference."""
    # Normalize
    ref = ref.strip().rstrip('.')
    
    # Text references: T-27.VII -> look up in table
    t_match = re.match(r'(T-\d+\.[IVXivx]+)', ref)
    if t_match:
        key = t_match.group(1).upper()
        # Normalize roman numerals to uppercase
        key = re.sub(r'T-(\d+)\.([ivx]+)', lambda m: f'T-{m.group(1)}.{m.group(2).upper()}', key)
        slug = TEXT_URL_LOOKUP.get(key)
        if slug:
            return f'https://www.betterlifeawareness.com/{slug}'
        # Fallback: try chapter-only
        chap_match = re.match(r'T-(\d+)\.([IVX]+)', key)
        if chap_match:
            chap = chap_match.group(1)
            roman = chap_match.group(2).lower()
            return f'https://www.betterlifeawareness.com/acim-book-text-{chap}{roman}'
    
    # Workbook references: W-pI.121 or W-pII.307
    # Correct URL pattern: /acim-book-workbook-lesson-{N}
    w_match = re.match(r'W-p[Ii]+\.(\d+)', ref)
    if w_match:
        lesson = w_match.group(1)
        return f'https://www.betterlifeawareness.com/acim-book-workbook-lesson-{int(lesson)}'
    
    # Manual references: M-4 or M-4.I — use slug-based URLs
    m_match = re.match(r'M-(\d+)', ref)
    if m_match:
        return f'https://www.betterlifeawareness.com/acim-book-manual-for-teachers'
    
    return ''

def render_lesson_html(lesson):
    """Render a single lesson as an HTML card."""
    num = lesson['num']
    title = lesson['title']
    sections = lesson['sections']
    
    # Build christmind.info link
    cm_url = f'https://www.christmind.info/t/acimoe/workbook/l{str(num).zfill(3)}/'
    bla_url = f'https://www.betterlifeawareness.com/acim-book-workbook-lesson-{num}'
    
    html_parts = [f'<div class="lesson-card" id="lesson-{num}">']
    
    # Header
    html_parts.append(f'''
    <div class="lesson-header" onclick="toggleLesson({num})">
      <div class="lesson-num-badge">{num}</div>
      <div class="lesson-title-text">{esc(title)}</div>
      <div class="lesson-toggle-icon" id="toggle-{num}">▶</div>
    </div>''')
    
    # Body (collapsed by default)
    html_parts.append(f'<div class="lesson-body" id="body-{num}" style="display:none;">')
    
    # Links row
    html_parts.append(f'''
    <div class="lesson-links">
      <a href="{cm_url}" target="_blank" class="lesson-link cm-link">Read on christmind.info (OE) ↗</a>
      <a href="{bla_url}" target="_blank" class="lesson-link bla-link">Read on betterlifeawareness.com (FIP) ↗</a>
    </div>''')
    
    # Practice Instructions
    if 'practice_instructions' in sections:
        html_parts.append('<div class="section-block practice-section">')
        html_parts.append('<h4 class="section-heading practice-heading">✦ Practice Instructions</h4>')
        html_parts.append(format_practice_instructions(sections['practice_instructions']))
        html_parts.append('</div>')
    
    # Practice Suggestions (if separate)
    if 'practice_suggestions' in sections:
        html_parts.append('<div class="section-block suggestions-section">')
        html_parts.append('<h4 class="section-heading suggestions-heading">✦ Practice Suggestions</h4>')
        html_parts.append(format_text_block(sections['practice_suggestions']))
        html_parts.append('</div>')
    
    # Commentary
    if 'commentary' in sections:
        html_parts.append('<div class="section-block commentary-section">')
        html_parts.append('<h4 class="section-heading commentary-heading">✦ Commentary</h4>')
        html_parts.append(format_text_block(sections['commentary']))
        html_parts.append('</div>')
    
    # Reading
    if 'reading' in sections:
        html_parts.append('<div class="section-block reading-section">')
        html_parts.append('<h4 class="section-heading reading-heading">✦ Recommended Reading</h4>')
        html_parts.append(format_reading_ref(sections['reading']))
        html_parts.append('</div>')
    
    html_parts.append('</div>')  # lesson-body
    html_parts.append('</div>')  # lesson-card
    
    return '\n'.join(html_parts)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 10: Build the complete HTML
# ─────────────────────────────────────────────────────────────────────────────

# Build all lesson cards
all_lesson_cards = []
for lesson in all_lessons:
    all_lesson_cards.append(render_lesson_html(lesson))

lessons_html = '\n'.join(all_lesson_cards)

# Build review cards
review_cards = []
for review in reviews:
    rnum = review['num']
    rname = review['name']
    rcontent = format_text_block(review['content'])
    review_cards.append(f'''
<div class="review-card" id="review-{rnum}">
  <div class="review-header" onclick="toggleReview('{rnum}')">
    <div class="review-badge">R{rnum}</div>
    <div class="review-title">{esc(rname)}</div>
    <div class="review-toggle" id="rtoggle-{rnum}">▶</div>
  </div>
  <div class="review-body" id="rbody-{rnum}" style="display:none;">
    {rcontent}
  </div>
</div>''')

reviews_html = '\n'.join(review_cards)

# Build What Is cards
what_is_cards = []
for i, wi in enumerate(what_is_sections):
    wi_id = f'wi-{i}'
    wi_content = format_what_is_content(wi['content'])
    bla_url = wi.get('bla_url', '')
    bla_link_html = ''
    if bla_url:
        bla_link_html = f'<div class="what-is-links"><a href="{bla_url}" target="_blank" class="lesson-link bla-link">Read on betterlifeawareness.com (FIP) ↗</a></div>'
    what_is_cards.append(f'''
<div class="what-is-card" id="{wi_id}">
  <div class="what-is-header" onclick="toggleWhatIs('{wi_id}')">
    <div class="what-is-icon">✦</div>
    <div class="what-is-title">{esc(wi["title"])}</div>
    <div class="what-is-toggle" id="toggle-{wi_id}">▶</div>
  </div>
  <div class="what-is-body" id="body-{wi_id}" style="display:none;">
    {bla_link_html}
    {wi_content}
  </div>
</div>''')

what_is_html = '\n'.join(what_is_cards)

# Build front matter
preface1_html = format_text_block(front_matter_1.get('preface', ''))
morning_html = format_text_block(front_matter_1.get('morning_quiet_time', ''))
preface2_html = format_text_block(front_matter_2.get('preface', ''))

# Build appendix
appendix_html_parts = []
for section in appendix_1 + appendix_2:
    sec_id = re.sub(r'[^a-z0-9]', '-', section['title'].lower())
    sec_content = format_text_block(section['content'])
    appendix_html_parts.append(f'''
<div class="appendix-card" id="appendix-{sec_id}">
  <div class="appendix-header" onclick="toggleAppendix('{sec_id}')">
    <div class="appendix-title">{esc(section["title"])}</div>
    <div class="appendix-toggle" id="atoggle-{sec_id}">▶</div>
  </div>
  <div class="appendix-body" id="abody-{sec_id}" style="display:none;">
    {sec_content}
  </div>
</div>''')

appendix_html = '\n'.join(appendix_html_parts)

# Build lesson index for search (lightweight JSON)
lesson_index = []
for lesson in all_lessons:
    lesson_index.append({
        'num': lesson['num'],
        'title': lesson['title'],
        'part': lesson['part']
    })

lesson_index_js = json.dumps(lesson_index)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 11: Write the HTML file
# ─────────────────────────────────────────────────────────────────────────────

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>ACIM Lesson Study Guide — Dee Doyle &amp; Allen Watson</title>
<style>
/* ── Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg:          #f5f0e8;
  --bg-card:     #fffdf8;
  --bg-alt:      #f0ebe0;
  --border:      #d4c9b0;
  --border-light:#e8e0d0;
  --text:        #2c2416;
  --text-muted:  #7a6a50;
  --text-light:  #a09070;
  --gold:        #8b6914;
  --gold-light:  #c4a44a;
  --teal:        #2a6b6b;
  --teal-light:  #4a9b9b;
  --blue:        #2a4a7a;
  --blue-light:  #4a7ab0;
  --green:       #2a5a2a;
  --green-light: #4a8a4a;
  --red:         #7a2a2a;
  --red-light:   #b04a4a;
  --purple:      #5a2a7a;
  --purple-light:#8a5ab0;
  --shadow:      0 2px 12px rgba(44,36,22,0.08);
  --shadow-hover:0 4px 20px rgba(44,36,22,0.14);
  --radius:      12px;
  --radius-sm:   8px;
  --font-serif:  'Georgia', 'Times New Roman', serif;
  --font-sans:   -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

html {{ font-size: 16px; scroll-behavior: smooth; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  line-height: 1.7;
  min-height: 100vh;
}}

/* ── Header ── */
.site-header {{
  background: linear-gradient(135deg, #2c2416 0%, #4a3820 100%);
  color: #f5f0e8;
  padding: 24px 20px 20px;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 16px rgba(0,0,0,0.3);
}}
.site-header h1 {{
  font-family: var(--font-serif);
  font-size: clamp(1.1rem, 4vw, 1.6rem);
  font-weight: normal;
  letter-spacing: 0.04em;
  color: #e8d8a0;
  margin-bottom: 4px;
}}
.site-header .subtitle {{
  font-size: 0.8rem;
  color: #b0a080;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}
.diamonds {{
  color: #c4a44a;
  font-size: 0.9rem;
  margin: 6px 0 0;
  letter-spacing: 0.3em;
}}

/* ── Tab Bar ── */
.tab-bar {{
  display: flex;
  background: #3a2e1e;
  border-bottom: 2px solid #c4a44a;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}}
.tab-bar::-webkit-scrollbar {{ display: none; }}
.tab-btn {{
  flex: 1;
  min-width: 80px;
  padding: 12px 8px;
  background: none;
  border: none;
  color: #9a8a6a;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}}
.tab-btn.active {{
  color: #e8d8a0;
  border-bottom-color: #c4a44a;
  background: rgba(196,164,74,0.08);
}}
.tab-btn:hover:not(.active) {{
  color: #c4a44a;
  background: rgba(196,164,74,0.05);
}}

/* ── Panels ── */
.panel {{ display: none; }}
.panel.active {{ display: block; }}

/* ── Search Bar ── */
.search-bar {{
  padding: 16px;
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
}}
.search-input {{
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--border);
  border-radius: 24px;
  background: var(--bg-card);
  color: var(--text);
  font-size: 1rem;
  font-family: var(--font-sans);
  outline: none;
  transition: border-color 0.2s;
}}
.search-input:focus {{ border-color: var(--gold-light); }}
.search-input::placeholder {{ color: var(--text-light); }}

/* ── Filter Chips ── */
.filter-bar {{
  padding: 10px 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border);
}}
.filter-chip {{
  padding: 5px 14px;
  border: 1.5px solid var(--border);
  border-radius: 20px;
  background: var(--bg-card);
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}}
.filter-chip.active {{
  background: var(--gold);
  border-color: var(--gold);
  color: #fff;
}}
.filter-chip:hover:not(.active) {{
  border-color: var(--gold-light);
  color: var(--gold);
}}

/* ── Results Count ── */
.results-count {{
  padding: 8px 16px;
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border-light);
}}

/* ── Lesson Cards ── */
.lessons-container {{
  padding: 12px;
  max-width: 900px;
  margin: 0 auto;
}}

.lesson-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: box-shadow 0.2s;
}}
.lesson-card:hover {{ box-shadow: var(--shadow-hover); }}
.lesson-card.hidden {{ display: none; }}

.lesson-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s;
}}
.lesson-header:hover {{ background: var(--bg-alt); }}

.lesson-num-badge {{
  min-width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #3a2e1e, #5a4a2e);
  color: #e8d8a0;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}}

.lesson-title-text {{
  flex: 1;
  font-family: var(--font-serif);
  font-style: italic;
  font-size: clamp(0.9rem, 2.5vw, 1.05rem);
  color: var(--text);
  line-height: 1.4;
}}

.lesson-toggle-icon {{
  color: var(--text-light);
  font-size: 0.75rem;
  transition: transform 0.2s;
  flex-shrink: 0;
}}
.lesson-toggle-icon.open {{ transform: rotate(90deg); }}

/* ── Lesson Body ── */
.lesson-body {{
  border-top: 1px solid var(--border-light);
  padding: 0;
}}

.lesson-links {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding: 12px 16px;
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border-light);
}}
.lesson-link {{
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}}
.cm-link {{
  background: rgba(42,75,122,0.1);
  color: var(--blue);
  border: 1.5px solid rgba(42,75,122,0.3);
}}
.cm-link:hover {{ background: var(--blue); color: #fff; }}
.bla-link {{
  background: rgba(42,107,107,0.1);
  color: var(--teal);
  border: 1.5px solid rgba(42,107,107,0.3);
}}
.bla-link:hover {{ background: var(--teal); color: #fff; }}

/* ── Section Blocks ── */
.section-block {{
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
}}
.section-block:last-child {{ border-bottom: none; }}

.section-heading {{
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border-light);
}}
.practice-heading {{ color: var(--teal); }}
.suggestions-heading {{ color: var(--blue); }}
.commentary-heading {{ color: var(--gold); }}
.reading-heading {{ color: var(--green); }}

/* ── Practice Block ── */
.practice-block {{
  display: flex;
  flex-direction: column;
  gap: 10px;
}}
.practice-item {{
  display: flex;
  gap: 12px;
  align-items: flex-start;
}}
.practice-label {{
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--teal);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  min-width: 90px;
  padding-top: 3px;
  flex-shrink: 0;
}}
.practice-content {{
  flex: 1;
  font-size: 0.9rem;
  color: var(--text);
}}
.practice-content p {{ margin-bottom: 6px; }}
.practice-content p:last-child {{ margin-bottom: 0; }}

/* ── Commentary ── */
.commentary-section p {{
  font-size: 0.95rem;
  line-height: 1.75;
  color: var(--text);
  margin-bottom: 12px;
}}
.commentary-section p:last-child {{ margin-bottom: 0; }}

/* ── Reading Reference ── */
.reading-ref {{
  font-size: 0.9rem;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  background: rgba(42,90,42,0.06);
  border-left: 3px solid var(--green);
}}
.reading-link {{
  color: var(--green);
  text-decoration: none;
  font-weight: 600;
}}
.reading-link:hover {{ text-decoration: underline; }}
.reading-desc {{ color: var(--text-muted); font-size: 0.85rem; }}
.no-reading {{ color: var(--text-light); font-style: italic; background: none; border: none; }}

/* ── Lists ── */
.sg-list {{
  padding-left: 20px;
  margin: 8px 0;
}}
.sg-list li {{
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 4px;
  color: var(--text);
}}
.indented {{
  padding-left: 20px;
  color: var(--text-muted);
  font-size: 0.9rem;
}}

/* ── Review Cards ── */
.reviews-container {{
  padding: 12px;
  max-width: 900px;
  margin: 0 auto;
}}
.review-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.review-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.15s;
}}
.review-header:hover {{ background: var(--bg-alt); }}
.review-badge {{
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, var(--purple), var(--purple-light));
  color: #fff;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}}
.review-title {{
  flex: 1;
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: var(--text);
}}
.review-toggle {{
  color: var(--text-light);
  font-size: 0.75rem;
  transition: transform 0.2s;
}}
.review-toggle.open {{ transform: rotate(90deg); }}
.review-body {{
  padding: 20px;
  border-top: 1px solid var(--border-light);
}}
.review-body p {{
  font-size: 0.95rem;
  line-height: 1.75;
  margin-bottom: 12px;
  color: var(--text);
}}

/* ── What Is Cards ── */
.what-is-container {{
  padding: 12px;
  max-width: 900px;
  margin: 0 auto;
}}
.what-is-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--gold);
  border-radius: var(--radius);
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.what-is-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.15s;
}}
.what-is-header:hover {{ background: var(--bg-alt); }}
.what-is-icon {{
  color: var(--gold);
  font-size: 1.1rem;
  flex-shrink: 0;
}}
.what-is-title {{
  flex: 1;
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: var(--text);
  font-style: italic;
}}
.what-is-toggle {{
  color: var(--text-light);
  font-size: 0.75rem;
  transition: transform 0.2s;
}}
.what-is-toggle.open {{ transform: rotate(90deg); }}
.what-is-body {{
  padding: 20px;
  border-top: 1px solid var(--border-light);
}}
.what-is-body p {{
  font-size: 0.95rem;
  line-height: 1.75;
  margin-bottom: 12px;
  color: var(--text);
}}

/* ── What Is Links ── */
.what-is-links {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding: 12px 16px;
  background: var(--bg-alt);
  border-bottom: 1px solid var(--border-light);
}}

/* ── What Is Paragraph Headers ── */
.what-is-para-header {{
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--gold);
  margin: 20px 0 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(196,164,74,0.25);
}}
.what-is-para-header:first-child {{
  margin-top: 0;
}}

/* ── ACIM Quote Block ── */
.acim-quote {{
  margin: 0 0 14px;
  padding: 14px 18px;
  background: rgba(196,164,74,0.06);
  border-left: 3px solid var(--gold);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}}
.acim-quote-text {{
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 0.95rem;
  line-height: 1.75;
  color: var(--text);
  margin-bottom: 6px;
}}
.what-is-citation {{
  font-size: 0.78rem;
  color: var(--gold);
  font-style: normal;
  font-weight: 600;
  letter-spacing: 0.02em;
}}

/* ── What Is Commentary ── */
.what-is-commentary p {{
  font-size: 0.95rem;
  line-height: 1.75;
  color: var(--text);
  margin-bottom: 12px;
}}
.what-is-commentary p:last-child {{
  margin-bottom: 0;
}}

/* ── Front Matter / Appendix ── */
.front-matter-container,
.appendix-container {{
  padding: 12px;
  max-width: 900px;
  margin: 0 auto;
}}
.front-matter-card,
.appendix-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.front-matter-header,
.appendix-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.15s;
}}
.front-matter-header:hover,
.appendix-header:hover {{ background: var(--bg-alt); }}
.front-matter-title,
.appendix-title {{
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: var(--text);
}}
.front-matter-toggle,
.appendix-toggle {{
  color: var(--text-light);
  font-size: 0.75rem;
  transition: transform 0.2s;
}}
.front-matter-toggle.open,
.appendix-toggle.open {{ transform: rotate(90deg); }}
.front-matter-body,
.appendix-body {{
  padding: 20px;
  border-top: 1px solid var(--border-light);
}}
.front-matter-body p,
.appendix-body p {{
  font-size: 0.95rem;
  line-height: 1.75;
  margin-bottom: 12px;
  color: var(--text);
}}

/* ── Part Dividers ── */
.part-divider {{
  padding: 16px 20px 8px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gold);
  border-bottom: 1px solid var(--border-light);
  margin: 8px 0 4px;
}}

/* ── Attribution ── */
.attribution {{
  padding: 24px 20px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.8rem;
  line-height: 1.8;
  border-top: 1px solid var(--border);
  margin-top: 20px;
}}
.attribution strong {{ color: var(--text); }}

/* ── Highlight ── */
mark {{
  background: rgba(196,164,74,0.3);
  color: inherit;
  border-radius: 2px;
  padding: 0 1px;
}}

/* ── Responsive ── */
@media (max-width: 480px) {{
  .practice-item {{ flex-direction: column; gap: 4px; }}
  .practice-label {{ min-width: unset; }}
  .lesson-links {{ flex-direction: column; }}
}}
</style>
</head>
<body>

<header class="site-header">
  <h1>ACIM Lesson Study Guide &amp; Recommended Text Reading</h1>
  <div class="subtitle">Commentaries by Dee Doyle &amp; Allen Watson · Circle of Atonement</div>
  <div class="diamonds">✦ ✦ ✦</div>
</header>

<nav class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('lessons')">Lessons</button>
  <button class="tab-btn" onclick="switchTab('reviews')">Reviews</button>
  <button class="tab-btn" onclick="switchTab('whatis')">What Is…</button>
  <button class="tab-btn" onclick="switchTab('frontmatter')">Preface</button>
  <button class="tab-btn" onclick="switchTab('appendix')">Appendix</button>
</nav>

<!-- ── LESSONS PANEL ── -->
<div id="panel-lessons" class="panel active">
  <div class="search-bar">
    <input type="search" class="search-input" id="lesson-search" placeholder="🔍  Search lessons, themes, or phrases…" oninput="filterLessons()">
  </div>
  <div class="filter-bar">
    <button class="filter-chip active" onclick="setFilter('all', this)">All</button>
    <button class="filter-chip" onclick="setFilter('1-50', this)">1–50</button>
    <button class="filter-chip" onclick="setFilter('51-100', this)">51–100</button>
    <button class="filter-chip" onclick="setFilter('101-150', this)">101–150</button>
    <button class="filter-chip" onclick="setFilter('151-200', this)">151–200</button>
    <button class="filter-chip" onclick="setFilter('201-220', this)">201–220</button>
    <button class="filter-chip" onclick="setFilter('221-365', this)">Part II</button>
  </div>
  <div class="results-count" id="results-count">All 365 lessons</div>
  <div class="lessons-container" id="lessons-container">
    {lessons_html}
  </div>
  <div class="attribution">
    <strong>A Course in Miracles Lesson Study Guide &amp; Recommended Text Reading</strong><br>
    Commentaries by Dee Doyle &amp; Allen Watson<br>
    © Circle of Atonement · Personal use only · All rights reserved<br>
    <em>A Course in Miracles</em> © Foundation for Inner Peace
  </div>
</div>

<!-- ── REVIEWS PANEL ── -->
<div id="panel-reviews" class="panel">
  <div class="reviews-container">
    <div class="part-divider">Part I · Review Periods</div>
    {reviews_html}
    <div class="attribution">
      <strong>A Course in Miracles Lesson Study Guide</strong><br>
      Commentaries by Dee Doyle &amp; Allen Watson · Circle of Atonement<br>
      Personal use only
    </div>
  </div>
</div>

<!-- ── WHAT IS PANEL ── -->
<div id="panel-whatis" class="panel">
  <div class="what-is-container">
    <div class="part-divider">Part II · "What Is…" Commentary Sections</div>
    {what_is_html}
    <div class="attribution">
      <strong>A Course in Miracles Lesson Study Guide</strong><br>
      Commentaries by Dee Doyle &amp; Allen Watson · Circle of Atonement<br>
      Personal use only
    </div>
  </div>
</div>

<!-- ── FRONT MATTER PANEL ── -->
<div id="panel-frontmatter" class="panel">
  <div class="front-matter-container">
    <div class="part-divider">Preface &amp; Introductory Material</div>
    <div class="front-matter-card">
      <div class="front-matter-header" onclick="toggleFM('preface1')">
        <div class="front-matter-title">Preface — Part I</div>
        <div class="front-matter-toggle" id="fmtoggle-preface1">▶</div>
      </div>
      <div class="front-matter-body" id="fmbody-preface1" style="display:none;">
        {preface1_html}
      </div>
    </div>
    <div class="front-matter-card">
      <div class="front-matter-header" onclick="toggleFM('morning')">
        <div class="front-matter-title">When Should You Take Your Morning Quiet Time?</div>
        <div class="front-matter-toggle" id="fmtoggle-morning">▶</div>
      </div>
      <div class="front-matter-body" id="fmbody-morning" style="display:none;">
        {morning_html}
      </div>
    </div>
    <div class="front-matter-card">
      <div class="front-matter-header" onclick="toggleFM('preface2')">
        <div class="front-matter-title">Preface — Part II</div>
        <div class="front-matter-toggle" id="fmtoggle-preface2">▶</div>
      </div>
      <div class="front-matter-body" id="fmbody-preface2" style="display:none;">
        {preface2_html}
      </div>
    </div>
    <div class="attribution">
      <strong>A Course in Miracles Lesson Study Guide</strong><br>
      Commentaries by Dee Doyle &amp; Allen Watson · Circle of Atonement<br>
      Personal use only
    </div>
  </div>
</div>

<!-- ── APPENDIX PANEL ── -->
<div id="panel-appendix" class="panel">
  <div class="appendix-container">
    <div class="part-divider">Appendix</div>
    {appendix_html}
    <div class="attribution">
      <strong>A Course in Miracles Lesson Study Guide</strong><br>
      Commentaries by Dee Doyle &amp; Allen Watson · Circle of Atonement<br>
      Personal use only
    </div>
  </div>
</div>

<script>
// ── Data ──
const LESSON_INDEX = {lesson_index_js};

// ── State ──
let currentFilter = 'all';
let currentSearch = '';

// ── Tab Switching ──
function switchTab(tab) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + tab).classList.add('active');
  event.currentTarget.classList.add('active');
}}

// ── Lesson Toggle ──
function toggleLesson(num) {{
  const body = document.getElementById('body-' + num);
  const icon = document.getElementById('toggle-' + num);
  const isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  icon.classList.toggle('open', !isOpen);
}}

// ── Review Toggle ──
function toggleReview(num) {{
  const body = document.getElementById('rbody-' + num);
  const icon = document.getElementById('rtoggle-' + num);
  const isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  icon.classList.toggle('open', !isOpen);
}}

// ── What Is Toggle ──
function toggleWhatIs(id) {{
  const body = document.getElementById('body-' + id);
  const icon = document.getElementById('toggle-' + id);
  const isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  icon.classList.toggle('open', !isOpen);
}}

// ── Front Matter Toggle ──
function toggleFM(id) {{
  const body = document.getElementById('fmbody-' + id);
  const icon = document.getElementById('fmtoggle-' + id);
  const isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  icon.classList.toggle('open', !isOpen);
}}

// ── Appendix Toggle ──
function toggleAppendix(id) {{
  const body = document.getElementById('abody-' + id);
  const icon = document.getElementById('atoggle-' + id);
  const isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  icon.classList.toggle('open', !isOpen);
}}

// ── Filter ──
function setFilter(filter, btn) {{
  currentFilter = filter;
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  filterLessons();
}}

function lessonInFilter(num) {{
  if (currentFilter === 'all') return true;
  const [a, b] = currentFilter.split('-').map(Number);
  return num >= a && num <= b;
}}

// ── Search & Filter ──
function filterLessons() {{
  currentSearch = document.getElementById('lesson-search').value.toLowerCase().trim();
  let visible = 0;
  
  LESSON_INDEX.forEach(lesson => {{
    const card = document.getElementById('lesson-' + lesson.num);
    if (!card) return;
    
    const inFilter = lessonInFilter(lesson.num);
    const inSearch = !currentSearch || 
      lesson.title.toLowerCase().includes(currentSearch) ||
      String(lesson.num).includes(currentSearch) ||
      card.textContent.toLowerCase().includes(currentSearch);
    
    if (inFilter && inSearch) {{
      card.classList.remove('hidden');
      visible++;
      
      // Highlight search terms
      if (currentSearch) {{
        highlightInCard(card, currentSearch);
      }} else {{
        removeHighlights(card);
      }}
    }} else {{
      card.classList.add('hidden');
    }}
  }});
  
  const countEl = document.getElementById('results-count');
  if (currentSearch || currentFilter !== 'all') {{
    countEl.textContent = visible + ' lesson' + (visible !== 1 ? 's' : '') + ' shown';
  }} else {{
    countEl.textContent = 'All ' + LESSON_INDEX.length + ' lessons';
  }}
}}

function highlightInCard(card, term) {{
  // Only highlight in title for performance
  const titleEl = card.querySelector('.lesson-title-text');
  if (!titleEl) return;
  const text = titleEl.textContent;
  const regex = new RegExp('(' + escapeRegex(term) + ')', 'gi');
  titleEl.innerHTML = text.replace(regex, '<mark>$1</mark>');
}}

function removeHighlights(card) {{
  const titleEl = card.querySelector('.lesson-title-text');
  if (!titleEl) return;
  titleEl.innerHTML = titleEl.textContent;
}}

function escapeRegex(str) {{
  return str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
}}

// ── Jump to Lesson ──
function jumpToLesson(num) {{
  const card = document.getElementById('lesson-' + num);
  if (card) {{
    // Switch to lessons tab
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('panel-lessons').classList.add('active');
    document.querySelector('.tab-btn').classList.add('active');
    
    // Open and scroll
    const body = document.getElementById('body-' + num);
    const icon = document.getElementById('toggle-' + num);
    body.style.display = 'block';
    icon.classList.add('open');
    card.classList.remove('hidden');
    setTimeout(() => card.scrollIntoView({{ behavior: 'smooth', block: 'start' }}), 100);
  }}
}}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {{
  const countEl = document.getElementById('results-count');
  if (countEl) countEl.textContent = 'All ' + LESSON_INDEX.length + ' lessons';
}});
</script>
</body>
</html>'''

output_path = '/home/ubuntu/acim_flashcards/studyguide.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"\nStudy Guide HTML generated: {output_path}")
print(f"Part I lessons parsed: {len(part1_lessons)}")
print(f"Part II lessons parsed: {len(part2_lessons)}")
print(f"Total lessons: {len(all_lessons)}")
print(f"Reviews parsed: {len(reviews)}")
print(f"What Is sections parsed: {len(what_is_sections)}")
print(f"Appendix sections: {len(appendix_1) + len(appendix_2)}")

import os
size = os.path.getsize(output_path)
print(f"File size: {size:,} bytes ({size//1024} KB)")
