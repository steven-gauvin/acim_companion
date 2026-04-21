import json
from collections import OrderedDict

with open('/home/ubuntu/transcribe_handwritten_notes.json', 'r') as f:
    data = json.load(f)

# Sort by page number
results = sorted(data['results'], key=lambda x: x['output']['page_number'])

# Build topic groups
topics = OrderedDict()
current_topic = None

for r in results:
    out = r['output']
    page = out['page_number']
    heading = out['topic_heading']
    text = out['transcription']
    has_diagram = out['has_diagram']
    confidence = out['confidence']
    
    if heading == 'BLANK' or text == 'BLANK PAGE':
        continue
    
    if heading == 'CONTINUATION':
        if current_topic:
            topics[current_topic]['pages'].append({
                'page': page,
                'text': text,
                'has_diagram': has_diagram,
                'confidence': confidence
            })
        continue
    
    if heading == 'DIAGRAM':
        # Check if it fits with current topic
        if current_topic:
            topics[current_topic]['pages'].append({
                'page': page,
                'text': text,
                'has_diagram': True,
                'confidence': confidence
            })
        else:
            current_topic = f"DIAGRAM (Page {page})"
            topics[current_topic] = {'pages': [{
                'page': page,
                'text': text,
                'has_diagram': True,
                'confidence': confidence
            }]}
        continue
    
    # New topic
    current_topic = heading
    if current_topic not in topics:
        topics[current_topic] = {'pages': []}
    topics[current_topic]['pages'].append({
        'page': page,
        'text': text,
        'has_diagram': has_diagram,
        'confidence': confidence
    })

# Print summary
print(f"Total topics found: {len(topics)}")
print("\nTopics and page counts:")
for topic, data in topics.items():
    pages = [p['page'] for p in data['pages']]
    diagrams = sum(1 for p in data['pages'] if p['has_diagram'])
    print(f"  {topic}: {len(data['pages'])} pages ({pages})" + (f" [{diagrams} diagram(s)]" if diagrams else ""))

# Write organized Markdown
md = []
md.append("# Steven's ACIM Study Notes")
md.append("")
md.append("*Transcribed from handwritten notes — 76 pages*")
md.append("*References are to the Original Edition of A Course in Miracles (Text)*")
md.append("*Format: Chapter:Section:Paragraph (e.g., 3:5:35 = Chapter 3, Section 5, Paragraph 35)*")
md.append("")
md.append("---")
md.append("")

# Table of contents
md.append("## Table of Contents")
md.append("")
for i, topic in enumerate(topics.keys(), 1):
    anchor = topic.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '').replace('/', '-')
    page_count = len(topics[topic]['pages'])
    md.append(f"{i}. [{topic}](#{anchor}) ({page_count} page{'s' if page_count > 1 else ''})")
md.append("")
md.append("---")
md.append("")

# Each topic
for topic, data in topics.items():
    md.append(f"## {topic}")
    md.append("")
    pages = [p['page'] for p in data['pages']]
    md.append(f"*PDF pages: {', '.join(str(p) for p in pages)}*")
    md.append("")
    
    for entry in data['pages']:
        text = entry['text']
        if entry['has_diagram']:
            md.append(f"**[Diagram — Page {entry['page']}]**")
            md.append("")
        md.append(text)
        md.append("")
    
    md.append("---")
    md.append("")

with open('/home/ubuntu/acim_flashcards/steven_acim_study_notes.md', 'w') as f:
    f.write('\n'.join(md))

print("\nWritten to: steven_acim_study_notes.md")
