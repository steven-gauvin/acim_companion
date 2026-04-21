#!/usr/bin/env python3
"""Add the 'Where Do I Go From Here?' special card as lesson 366."""

import json

# The notes text for the special card - carefully formatted for readability
SPECIAL_NOTES = """✦ CONGRATULATIONS! ✦

You have finished the entire Workbook. If you are new to the Course this last year, you may not realize how many students begin the Workbook and don't finish it, so finishing is no minor accomplishment. It really deserves congratulations.

Having completed a pass through the Workbook, there are two questions that might occur to you now:

• Should I repeat the Workbook lessons, or is one time through enough?
• If I feel I am done with the lessons, what should I do now to continue my work with A Course in Miracles?

═══════════════════════════
SHOULD I REPEAT THE WORKBOOK?
═══════════════════════════

The common sense test: "Have I learned what the course was intended to teach?" If you have, you don't need to repeat it. If you haven't, you could very likely profit from repeating it.

The immediate goal of the Workbook is to train us in daily spiritual practice — to establish in our lives:

• The habit of spending time every morning and evening to meet with God and set our minds on His truth
• The habit of turning our minds within to God every hour or so
• The habit of thinking frequently of God or of spiritual thoughts between those hourly remembrances
• The habit of responding immediately to temptation with some thought of God

If you have established these habits to the degree that you can carry them on daily without the Workbook's support, then you do not need to repeat it. You may still choose to, but you do not need to.

If you have not established these daily habits, then you should re-enroll yourself in the program designed to help you form such habits — the Workbook!

═══════════════════════════
WHAT DO I DO AFTER THE WORKBOOK?
═══════════════════════════

The Manual for Teachers offers clear instructions in "How Should the Teacher of God Spend His Day?" (M-16).

The post-Workbook practice, in simple outline:

1. Begin the day right — as soon as possible after waking, take your quiet time. The goal is to "join with God." (M-16.4:7)

2. Repeat the same procedures at night — just before sleeping if possible. (5:1)

3. Remember God all through the day. (6:1–14)

4. Turn to the Holy Spirit with all your problems. (7:4–5)

5. Respond to all temptations by reminding yourself of the truth. (8:1–3; 10:8; 11:9)

═══════════════════════════
HINTS FOR POST-WORKBOOK PRACTICE
═══════════════════════════

• Make a list of useful thoughts from the Course — thoughts effective in responding to temptation, or that help you move into that "quiet center."

• Look through the Text for passages in italic type — these are nearly all suggested spiritual practices. Make a collection and spend several days working with each.

• Study the Text! Don't just read it — study it. Give yourself plenty of time.

• Revisit powerful lessons occasionally. Follow your instinct, and do the lesson.

• Set your own individualized curriculum with the Holy Spirit. The point now is to maintain a habit of consistent, daily practice.

• Continue with such practices indefinitely until, like the Workbook itself, you no longer need them.

═══════════════════════════

"In time, with practice, you will never cease to think of Him, and hear His loving Voice guiding your footsteps into quiet ways, where you will walk in true defenselessness. For you will know that Heaven goes with you. Nor would you keep your mind away from Him a moment, even though your time is spent in offering salvation to the world. Think you He will not make this possible, for you who chose to carry out His plan for the salvation of the world and yours?"

— W-pI.153.18:1–4

— Allen Watson, Circle of Atonement"""

# Load the data file and add lesson 366
with open('/tmp/app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

special_lesson = {
    "num": 366,
    "title": "Where Do I Go From Here?",
    "notes": SPECIAL_NOTES.strip(),
    "url": "#",
    "bla_url": "#"
}

# Check if 366 already exists
if any(l['num'] == 366 for l in data['lessons']):
    data['lessons'] = [l for l in data['lessons'] if l['num'] != 366]

data['lessons'].append(special_lesson)

with open('/tmp/app_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Added lesson 366. Total lessons: {len(data['lessons'])}")
