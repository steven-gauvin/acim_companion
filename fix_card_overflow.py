#!/usr/bin/env python3
"""Fix card back overflow - make notes scroll within the card."""

with open('/home/ubuntu/acim_flashcards/build_html.py', 'r') as f:
    content = f.read()

# 1. Make card-back use flex column layout so notes can scroll within it
old_card_back_css = '.card-back {{ background: var(--bg3); transform: rotateY(180deg); }}'
new_card_back_css = '.card-back {{ background: var(--bg3); transform: rotateY(180deg); display: flex; flex-direction: column; overflow: hidden; }}'
content = content.replace(old_card_back_css, new_card_back_css)

# 2. Make card-notes scrollable with a max-height that fills available space
old_notes_css = '.card-notes {{ font-size: 14px; color: var(--text); line-height: 1.7; white-space: pre-wrap; margin-bottom: 20px; }}'
new_notes_css = '.card-notes {{ font-size: 14px; color: var(--text); line-height: 1.7; white-space: pre-wrap; overflow-y: auto; flex: 1; padding-right: 4px; margin-bottom: 12px; }}'
content = content.replace(old_notes_css, new_notes_css)

# 3. Make card-back-title not shrink
old_title_css = '.card-back-title {{ font-size: 13px; color: var(--text-dim); font-style: italic; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }}'
new_title_css = '.card-back-title {{ font-size: 13px; color: var(--text-dim); font-style: italic; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 16px; flex-shrink: 0; }}'
content = content.replace(old_title_css, new_title_css)

# 4. Make card-back-num not shrink
old_num_css = '.card-back-num {{ font-size: 10px; letter-spacing: 3px; color: var(--gold-dim); text-transform: uppercase; margin-bottom: 4px; }}'
new_num_css = '.card-back-num {{ font-size: 10px; letter-spacing: 3px; color: var(--gold-dim); text-transform: uppercase; margin-bottom: 4px; flex-shrink: 0; }}'
content = content.replace(old_num_css, new_num_css)

with open('/home/ubuntu/acim_flashcards/build_html.py', 'w') as f:
    f.write(content)

print("Done!")
