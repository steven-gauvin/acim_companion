import json
from collections import OrderedDict

with open('/home/ubuntu/transcribe_handwritten_notes.json', 'r') as f:
    data = json.load(f)

# Sort by page number
results = sorted(data['results'], key=lambda x: x['output']['page_number'])

# Build raw page list (skip blanks)
pages = []
for r in results:
    out = r['output']
    if out['topic_heading'] == 'BLANK' or out['transcription'] == 'BLANK PAGE':
        continue
    pages.append(out)

# Define consolidated topic groups with desired order
# Map raw headings to consolidated names
consolidation_map = {
    'EGO 1': 'THE EGO',
    'EGO 2': 'THE EGO',
    'EGO 3': 'THE EGO',
    'EGO 4': 'THE EGO',
    'EGO 5': 'THE EGO',
    'EGO 6': 'THE EGO',
    'THE HOLY SPIRIT': 'THE HOLY SPIRIT',
    'THE HOLY SPIRIT - 2': 'THE HOLY SPIRIT',
    'THE HOLY SPIRIT 3': 'THE HOLY SPIRIT',
    'BODY': 'THE BODY',
    'BODY 2': 'THE BODY',
    'BODY 3': 'THE BODY',
    'PERCEPTION': 'PERCEPTION',
    'GOD': 'GOD',
    'THE SEPARATION (The Fall)': 'THE SEPARATION',
    'THE ILLUSION OF SEPARATION': 'THE ILLUSION OF SEPARATION',
    'ILLUSIONS': 'ILLUSIONS',
    'ATTACK (ANGER)': 'ATTACK AND ANGER',
    'GUILT': 'GUILT',
    'FEAR': 'FEAR',
    'DEATH': 'DEATH',
    'LESSONS OF THE HOLY SPIRIT': 'LESSONS OF THE HOLY SPIRIT',
    'PRINCIPLES OF MIRACLES': 'PRINCIPLES OF MIRACLES',
    'THE CORRECTION FOR LACK OF LOVE': 'THE CORRECTION FOR LACK OF LOVE',
    'MIRACLE PRINCIPLE #53': 'MIRACLE PRINCIPLE #53',
    'JUDGEMENT': 'JUDGEMENT',
    'HEALING': 'HEALING',
    'MIRACLE (THE, A)': 'THE MIRACLE',
    'FORGIVENESS': 'FORGIVENESS',
    'ATONEMENT': 'THE ATONEMENT',
    'LOVE': 'LOVE',
    'RESURRECTION': 'RESURRECTION',
    'SALVATION': 'SALVATION',
    'KNOWLEDGE': 'KNOWLEDGE',
}

# Desired topic order (thematic flow)
topic_order = [
    'GOD',
    'KNOWLEDGE',
    'PERCEPTION',
    'THE SEPARATION',
    'THE ILLUSION OF SEPARATION',
    'THE EGO',
    'THE BODY',
    'FEAR',
    'GUILT',
    'DEATH',
    'ILLUSIONS',
    'ATTACK AND ANGER',
    'THE CORRECTION FOR LACK OF LOVE',
    'THE HOLY SPIRIT',
    'LESSONS OF THE HOLY SPIRIT',
    'THE MIRACLE',
    'PRINCIPLES OF MIRACLES',
    'MIRACLE PRINCIPLE #53',
    'FORGIVENESS',
    'HEALING',
    'THE ATONEMENT',
    'SALVATION',
    'RESURRECTION',
    'LOVE',
    'JUDGEMENT',
]

# Collect entries by consolidated topic
topics = OrderedDict()
for t in topic_order:
    topics[t] = []

current_consolidated = None

for p in pages:
    heading = p['topic_heading']
    text = p['transcription']
    page_num = p['page_number']
    has_diagram = p['has_diagram']
    
    if heading == 'CONTINUATION':
        if current_consolidated and current_consolidated in topics:
            topics[current_consolidated].append({
                'page': page_num,
                'text': text,
                'has_diagram': has_diagram,
                'sub_heading': None
            })
        continue
    
    if heading == 'DIAGRAM':
        if current_consolidated and current_consolidated in topics:
            topics[current_consolidated].append({
                'page': page_num,
                'text': text,
                'has_diagram': True,
                'sub_heading': None
            })
        continue
    
    consolidated = consolidation_map.get(heading, heading)
    current_consolidated = consolidated
    
    if consolidated not in topics:
        topics[consolidated] = []
    
    # Determine sub-heading for numbered sections
    sub = None
    if heading != consolidated:
        sub = heading
    
    topics[consolidated].append({
        'page': page_num,
        'text': text,
        'has_diagram': has_diagram,
        'sub_heading': sub
    })

# Build the Markdown
md = []
md.append("# Steven's ACIM Study Notes")
md.append("")
md.append("> *Transcribed from 76 pages of handwritten study notes*")
md.append("> *A Course in Miracles — Original Edition (Text)*")
md.append("> *Reference format: Chapter:Section:Paragraph (e.g., 3:5:35)*")
md.append("> *Workbook references: W followed by lesson number (e.g., W43, W64, W99)*")
md.append("")
md.append("---")
md.append("")

# Table of contents
md.append("## Table of Contents")
md.append("")
for i, (topic, entries) in enumerate(topics.items(), 1):
    if not entries:
        continue
    anchor = topic.lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '').replace('/', '-').replace('#', '')
    quote_count = 0
    for e in entries:
        quote_count += e['text'].count('\n- ') + e['text'].count('\n* ') + e['text'].count('\n• ')
        if e['text'].startswith('- ') or e['text'].startswith('* ') or e['text'].startswith('• '):
            quote_count += 1
    md.append(f"{i}. [{topic}](#{anchor})")
md.append("")
md.append("---")
md.append("")

# Big T / Little t chart
md.append("## The Big T / Little t Chart")
md.append("")
md.append("*Based on the framework by Sandy Levey-Lunden, founder of OnPurpose*")
md.append("")
md.append("| Little t (perception / ego) | | Big T (Truth / God) |")
md.append("|:---|:---:|---:|")
md.append("| death | | **Life** |")
md.append("| darkness | | **Light** |")
md.append("| perception | | **Knowledge** |")
md.append("| false | | **True** |")
md.append("| ego | | **Soul** |")
md.append("| wrong mind | | **Right Mind** |")
md.append("| ego / body | | **Holy Spirit** |")
md.append("| fear | | **Love** |")
md.append("| make | | **Create** |")
md.append("| illusions | | **Reality** |")
md.append("| man's self | | **God's Self** |")
md.append("")
md.append("---")
md.append("")

# Diagrams section
md.append("## Diagrams")
md.append("")

md.append("### Diagram 1: Map of the Mind (Principles of Miracles 1:1)")
md.append("")
md.append("*PDF Page 43*")
md.append("")
md.append("This diagram maps the levels of consciousness and how God's love flows through them:")
md.append("")
md.append("```")
md.append("                        GOD")
md.append("                         |")
md.append("                       Souls          Love")
md.append("                    'transcends'")
md.append("                         |")
md.append("    Revelations    SUPER-CONSCIOUS         VISION")
md.append("   (unspeakable     (Knowledge)             end")
md.append("      love)           3:5:35")
md.append("         |                                3:6:41")
md.append("         |       'The mind returns to its proper")
md.append("      induce      function only when it wills")
md.append("         |        to know' 3:6:44")
md.append("         |")
md.append("    impulses      CONSCIOUS → Thought → Action")
md.append("         |         (Perception)")
md.append("         |       'to perceive is not to know' 3:6:34")
md.append("         |")
md.append("         v        SUB-CONSCIOUS / UNCONSCIOUS")
md.append("                   distortions of perception")
md.append("                   fantasy 1:102")
md.append("         ")
md.append("    MIRACLES ↑    'regards only the miracle ability,")
md.append("                   which should be under my direction' 3:6:38")
md.append("         ")
md.append("    Minds = 'love among equals'")
md.append("    miracle impulses")
md.append("    'Christ inspires all miracles' p.44")
md.append("         ")
md.append("    See 5:9:85 The Eternal Fixation")
md.append("```")
md.append("")

md.append("### Diagram 2: Miracle Principle #53")
md.append("")
md.append("*PDF Page 51*")
md.append("")
md.append("```")
md.append("                    True (accord)")
md.append("                         ↑")
md.append("                         |")
md.append("  'what man       →   MIRACLE   →   higher-level")
md.append("   has made'                          creation")
md.append("                         |")
md.append("                         ↓")
md.append("                    False (discord)")
md.append("                         |")
md.append("                        fear")
md.append("```")
md.append("")
md.append("The miracle takes what man has made and redirects it. When aligned with Truth (accord), it leads to higher-level creation. When aligned with falsity (discord), it leads to fear.")
md.append("")

md.append("### Diagram 3: The Mind of the Atonement (5:3)")
md.append("")
md.append("*PDF Page 53*")
md.append("")
md.append("```")
md.append("    'common           ╭──────────╮")
md.append("     elements'  →    │ Knowledge │")
md.append("                     │     ╭─────┤")
md.append("                     │     │trans-│    re-evaluation")
md.append("                     ├─────┤ fer  │  →")
md.append("                     │Perc-│  →   │    old learning")
md.append("                     │ept- │      │")
md.append("                     │ion  ╰──────╯")
md.append("                     ╰────────────╯")
md.append("```")
md.append("")
md.append("A Venn diagram showing how perception and knowledge overlap through 'common elements'. Perception can be *transferred* to knowledge — carried over. Old learning undergoes re-evaluation. This is the mechanism of the Atonement: purifying perception until it crosses into Knowledge.")
md.append("")
md.append("---")
md.append("")

# Each topic section
for topic, entries in topics.items():
    if not entries:
        continue
    
    md.append(f"## {topic}")
    md.append("")
    page_nums = sorted(set(e['page'] for e in entries))
    md.append(f"*PDF pages: {', '.join(str(p) for p in page_nums)}*")
    md.append("")
    
    for entry in entries:
        text = entry['text']
        if entry['has_diagram']:
            md.append(f"> **[Diagram — see Diagrams section above]**")
            md.append("")
            continue
        
        # Clean up the text
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                md.append("")
                continue
            # Ensure bullet points are consistent
            if line.startswith('* ') or line.startswith('• '):
                line = '- ' + line[2:]
            md.append(line)
        md.append("")
    
    md.append("---")
    md.append("")

# Write
output_path = '/home/ubuntu/acim_flashcards/steven_acim_study_notes.md'
with open(output_path, 'w') as f:
    f.write('\n'.join(md))

print(f"Written to: {output_path}")
print(f"Total lines: {len(md)}")

# Count non-blank topics
active = sum(1 for t, e in topics.items() if e)
print(f"Active topics: {active}")
