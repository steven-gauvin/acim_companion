#!/usr/bin/env python3
"""
Build the unified ACIM Companion App.
Merges flashcard app + study guide commentary + all reference material.
"""
import json, re, sys
sys.path.insert(0, '/home/ubuntu/acim_flashcards')

# ============================================================
# STEP 1: Load study guide lesson data
# ============================================================
print("Loading study guide data...")
with open('/home/ubuntu/acim_flashcards/build_studyguide.py', 'r') as f:
    build_code = f.read()

exec_lines = []
for line in build_code.split('\n'):
    exec_lines.append(line)
    if line.strip().startswith('all_lessons = sorted('):
        break

exec('\n'.join(exec_lines))
print(f"  Loaded {len(all_lessons)} lessons")
print(f"  Loaded {len(reviews)} reviews")
print(f"  Loaded {len(what_is_sections)} What Is sections")

# ============================================================
# STEP 2: Build study guide data as JS-injectable dict
# ============================================================
def clean_text(t):
    if not t:
        return ''
    return t.strip().replace('\t', '    ')

def build_sg_data():
    """Build a dict keyed by lesson number with study guide content."""
    sg = {}
    for lesson in all_lessons:
        num = lesson['num']
        secs = lesson.get('sections', {})
        
        parts = []
        
        pi = clean_text(secs.get('practice_instructions', ''))
        if pi:
            parts.append({'type': 'practice', 'label': 'Practice Instructions', 'text': pi})
        
        comm = clean_text(secs.get('commentary', ''))
        if comm:
            parts.append({'type': 'commentary', 'label': 'Commentary', 'text': comm})
        
        reading = clean_text(secs.get('recommended_reading', ''))
        if reading:
            parts.append({'type': 'reading', 'label': 'Recommended Reading', 'text': reading})
        
        bla_url = lesson.get('bla_url', '')
        
        sg[num] = {'parts': parts, 'bla_url': bla_url}
    
    return sg

sg_data = build_sg_data()
print(f"  Built study guide data for {len(sg_data)} lessons")

# Check a sample
sample = sg_data.get(1, {})
print(f"  Lesson 1 has {len(sample.get('parts',[]))} sections, bla_url={sample.get('bla_url','')[:50]}")

# ============================================================
# STEP 3: Load the original flashcard HTML
# ============================================================
print("Loading original flashcard HTML...")
with open('/home/ubuntu/upload/flashcards_original.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Extract the LESSONS data from the original
lessons_match = re.search(r'const LESSONS = (\[.*?\]);', orig_html, re.DOTALL)
if lessons_match:
    orig_lessons = json.loads(lessons_match.group(1))
    print(f"  Found {len(orig_lessons)} lessons in original app")
else:
    print("  ERROR: Could not find LESSONS data")
    sys.exit(1)

# Extract the REVIEWS data
reviews_match = re.search(r'const REVIEWS = (\[.*?\]);', orig_html, re.DOTALL)
if reviews_match:
    orig_reviews_raw = reviews_match.group(1)
    print(f"  Found REVIEWS data ({len(orig_reviews_raw)} chars)")
else:
    print("  WARNING: Could not find REVIEWS data")
    orig_reviews_raw = '[]'

# Extract the QUOTES data
quotes_match = re.search(r'const QUOTES = (\[.*?\]);', orig_html, re.DOTALL)
if quotes_match:
    orig_quotes = json.loads(quotes_match.group(1))
    print(f"  Found {len(orig_quotes)} quotes in original app")
else:
    orig_quotes = []

# ============================================================
# STEP 4: Build new QUOTES array (existing + new favourites)
# ============================================================
new_fav_quotes = [
    {
        "text": "You cannot lose your way because there is no way but His, and nowhere can you go except to Him.",
        "source": "A Course in Miracles"
    },
    {
        "text": "There is a place in you where there is perfect peace.\nThere is a place in you where nothing is impossible.\nThere is a place in you where the strength of God abides.",
        "source": "W-pI.47.7:4–6"
    },
    {
        "text": "Salvation is of the mind, and it is attained through peace.",
        "source": "T-12.III.5:1"
    },
    {
        "text": "In any situation in which you are uncertain, the first thing to consider, very simply, is \"What do I want to come of this? What is it for?\" The clarification of the goal belongs at the beginning, for it is this which will determine the outcome.",
        "source": "T-17.VI.2:1–3"
    },
    {
        "text": "My heart is beating in the peace of God...\nEach heartbeat brings me peace; each breath infuses me with strength.\nI am a messenger of God, directed by His Voice, sustained by Him in love,\nand held forever quiet and at peace within His loving Arms.",
        "source": "W-pII.267.Title; 1:5–6"
    },
    {
        "text": "Is it not strange that you should cherish still some hope of satisfaction from the world you see? In no respect, at any time or place, has anything but fear and guilt been your reward.",
        "source": "T-25.II.2:1–2"
    }
]

# Merge: avoid duplicates by checking text
existing_texts = {q['text'][:50] for q in orig_quotes}
all_quotes = list(orig_quotes)
for q in new_fav_quotes:
    if q['text'][:50] not in existing_texts:
        all_quotes.append(q)
        existing_texts.add(q['text'][:50])

print(f"  Total quotes: {len(all_quotes)} ({len(orig_quotes)} original + {len(all_quotes)-len(orig_quotes)} new)")

# ============================================================
# STEP 5: Build MEDITATIONS data
# ============================================================
meditations_data = [
    {
        "id": "open-mind",
        "title": "Open Mind Meditation",
        "subtitle": "The Workbook's Crowning Method — Lessons 221–365",
        "sections": [
            {
                "heading": "What It Is",
                "text": "Meditation is a fundamental part of Workbook practice. As the Workbook nears its second part, meditation begins to change in form. We are asked to go beyond words, to practice nonverbally.\n\nThis is the Workbook's crowning method — taught in Review V (171–180), Review VI (201–220), Part II (221–360), and the Final Lessons (361–365).\n\nOpen Mind Meditation takes us beyond words to direct experience. We clear away all words and thoughts from our mind. We hold a nonverbal intent — a pure, expectant waiting for the arrival of God. Our mind becomes like the cloudless sky, filled with nothing but \"still anticipation\" (W-pI.157.4:3), waiting for the sun to peek over the horizon."
            },
            {
                "heading": "The Technique",
                "text": "1. Repeat the idea for the day as an invitation to God to come to you.\n   Have a sense of placing the practice period in His Hands.\n\n2. Empty your mind of all words, all thoughts, and all that you think you know.\n   You may use these lines as an induction:\n\n   I do not know what I am.\n   I do not know what my attributes are.\n   I do not know what God is.\n   I do not know what the world is.\n   I do not know what is true and what is false.\n   I do not know what will make me happy.\n   I will forget my body, its comfort and its needs,\n   I will forget the past and future, and come with wholly empty hands unto my God.\n\n3. In the silence, hold your mind like a vacuum — empty of words and thoughts, yet waiting expectantly for a fullness to come from God.\n\n4. Whenever your mind wanders, use words to draw it back:\n   \"This thought I do not want. I choose instead [the idea for today].\"\n\n5. Realize the practice period is in the Holy Spirit's hands.\n\n6. Conclude by repeating the idea for the day."
            }
        ]
    },
    {
        "id": "i-need-do-nothing",
        "title": "I Need Do Nothing",
        "subtitle": "A Prayer of Rest — by Allen Watson",
        "sections": [
            {
                "heading": "",
                "text": "1. Father, how still today!\n   Let me imagine a day of perfect stillness,\n   in which everything is resting, everything is at peace, glowing with a soft radiance.\n\n2. How quietly do all things fall in place!\n   Normally, life seems to be a chaotic jumble of conflicting elements.\n   But today, all things have quietly fallen into their proper place.\n   As I look out on the world, everything is exactly where it belongs.\n\n3. This is the day\n   that has been chosen as the time\n   in which I come to understand the lesson\n   that there is no need that I do anything.\n   This is the day You have appointed for me to finally realize, \"I need do nothing.\"\n\n4. In You is every choice already made.\n   This is why I need do nothing.\n   In You all those hard choices that face me have already been made.\n   Let me feel myself resting in You, no more difficult decisions to make.\n\n5. In You has every conflict been resolved.\n   I feel constantly surrounded by conflict,\n   trying to resolve one while hoping that the others will not spring out of control.\n   But in You, all my conflicts are forever behind me.\n\n6. In You is everything I hope to find already given me.\n   I am always seeking, striving to find the happiness and safety that I lack.\n   But in You, I can rest from seeking, for I have found. In You I have everything.\n\n7. Your peace is mine.\n   You are totally free from choice, conflict, and seeking.\n   Your peace must be limitless, unfathomable!\n   Yet because I am in You, Your peace is mine.\n\n8. My heart is quiet, and my mind at rest.\n   In Your peace, with no need to do anything, I am totally at rest, completely filled.\n\n9. Your Love is Heaven, and Your Love is mine.\n   What could be more heavenly than being loved by You?\n   And I am loved by You; You love me with all that You are.\n   I need only accept Your Love, and Heaven is mine."
            }
        ]
    },
    {
        "id": "prayer-lesson-341",
        "title": "Prayer for Lesson 341",
        "subtitle": "Father, Your Son is holy — by Allen Watson",
        "sections": [
            {
                "heading": "",
                "text": "1. Father, Your Son is holy.\n   And Your Son is me.\n   You are my Father, Who loves me more than any earthly father could imagine.\n   Your Love created me holy, and that is how I remain, no matter what I think of myself.\n\n2. I am he on whom You smile\n   Your Smile is everything to me.\n   It is my sun, my Source of life, in which I abide.\n   What could be more joyous than feeling Your Smile shining on me?\n   in love and tenderness so dear and deep and still\n   Let me know the love of Your Smile, the tenderness of it.\n   Let me feel how dear is Your Love, how deep, how still.\n   the universe smiles back on You, and shares Your Holiness.\n   Your Holiness lies in Your loving Smile.\n   In smiling back on you, we share Your Holiness.\n\n3. How pure, how safe, how holy, then, are we,\n   How pure are we. How safe are we. How holy are we.\n   Let me feel this purity, rest in this safety, shine in this holiness.\n   abiding in Your Smile,\n   Basking in Your Smile.\n   Living in Your Smile like flowers live in the sunlight and turn their faces toward its warmth.\n   with all Your Love bestowed upon us,\n   All of Your Love. How could that be?\n   Let me know the joy of feeling all of Your Love bestowed on me.\n   living one with You,\n   With no distance between Us, no space for hate or discord to arise.\n   Living inside the warmth of Your Smile.\n   in brotherhood and Fatherhood complete;\n   The experience of brotherhood I long for is there, in Your Smile.\n   The perfect Father I long for is there, in Your Smile.\n   in sinlessness so perfect that the Lord of Sinlessness conceives us as His Son,\n   Only the perfectly sinless could be the Son of the Lord of Sinlessness.\n   And in my perfect sinlessness, I am Your Son.\n   a universe of Thought completing Him.\n   I and my brothers are a universe of thought.\n   So pure, so sinless, so vast, that we actually complete You.\n   What more hallowed honor could there be?"
            }
        ]
    },
    {
        "id": "holy-instant",
        "title": "Using the Holy Instant",
        "subtitle": "In Special Relationships — T-16.VI.12:1",
        "sections": [
            {
                "heading": "The Practice",
                "text": "\"The Holy Spirit asks only this little help of you: Whenever your thoughts wander to a special relationship which still attracts you, enter with Him into a holy instant, and there let Him release you.\" (T-16.VI.12:1)\n\n1. Watch your mind for the attraction of special love.\n   • When are you judging one person as better, more desirable, than another?\n   • When are you deciding what your needs are, how to meet them?\n   • When are you trying to prove to the people of your past that you are better?\n   • When are you believing that you are lacking and that someone else can make you whole?\n   • When are you feeling an attraction to bodies?\n   • When are you planning to pursue/woo/court someone?\n\n2. Be willing to see the pain in these thoughts.\n   • Be willing to see that your attraction will bring pain, not happiness.\n   • Be willing to see that your attraction is insane — not love but an attack.\n   • Be willing to see that it is really an attraction to guilt, not love.\n\n3. Recognize that a holy instant would make you happier.\n   Everything you seek for in a special relationship is really found in the holy instant.\n\n4. Enter into a holy instant.\n   • Be willing for an instant to completely step aside from your attractions, strategies, feelings and perspective.\n   • Desire the love, peace and unlimited communication of the holy instant.\n   • If it helps, ask Jesus to step between you and your fantasies.\n\n\"I am not alone, and I would not intrude the past upon my Guest. I have invited Him, and He is here. I need do nothing except not to interfere.\" (T-16.I.3)\n\n\"I give you to the Holy Spirit as part of myself. I know that you will be released, unless I want to use you to imprison myself. In the name of my freedom I choose your release, because I recognize that we will be released together.\" (T-15.XI.10:5-7)"
            }
        ]
    }
]

# ============================================================
# STEP 6: Build REFERENCE data
# ============================================================
principles_of_miracles = [
    {"num": 1, "text": "There is no order of difficulty in miracles. One is not \"harder\" or \"bigger\" than another. They are all the same. All expressions of love are maximal."},
    {"num": 2, "text": "Miracles as such do not matter. The only thing that matters is their Source, which is far beyond evaluation."},
    {"num": 3, "text": "Miracles occur naturally as expressions of love. The real miracle is the love that inspires them. In this sense everything that comes from love is a miracle."},
    {"num": 4, "text": "All miracles mean life, and God is the Giver of life. His Voice will direct you very specifically. You will be told all you need to know."},
    {"num": 5, "text": "Miracles are habits, and should be involuntary. They should not be under conscious control. Consciously selected miracles can be misguided."},
    {"num": 6, "text": "Miracles are natural. When they do not occur something has gone wrong."},
    {"num": 7, "text": "Miracles are everyone's right, but purification is necessary first."},
    {"num": 8, "text": "Miracles are healing because they supply a lack; they are performed by those who temporarily have more for those who temporarily have less."},
    {"num": 9, "text": "Miracles are a kind of exchange. Like all expressions of love, which are always miraculous in the true sense, the exchange reverses the physical laws. They bring more love both to the giver and the receiver."},
    {"num": 10, "text": "The use of miracles as spectacles to induce belief is a misunderstanding of their purpose."},
    {"num": 11, "text": "Prayer is the medium of miracles. It is a means of communication of the created with the Creator. Through prayer love is received, and through miracles love is expressed."},
    {"num": 12, "text": "Miracles are thoughts. Thoughts can represent the lower or bodily level of experience, or the higher or spiritual level of experience. One makes the physical, and the other creates the spiritual."},
    {"num": 13, "text": "Miracles are both beginnings and endings, and so they alter the temporal order. They are always affirmations of rebirth, which seem to go back but really go forward. They undo the past in the present, and thus release the future."},
    {"num": 14, "text": "Miracles bear witness to truth. They are convincing because they arise from conviction. Without conviction they deteriorate into magic, which is mindless and therefore destructive; or rather, the uncreative use of mind."},
    {"num": 15, "text": "Each day should be devoted to miracles. The purpose of time is to enable you to learn how to use time constructively. It is thus a teaching device and a means to an end. Time will cease when it is no longer useful in facilitating learning."},
    {"num": 16, "text": "Miracles are teaching devices for demonstrating it is as blessed to give as to receive. They simultaneously increase the strength of the giver and supply strength to the receiver."},
    {"num": 17, "text": "Miracles transcend the body. They are sudden shifts into invisibility, away from the bodily level. That is why they heal."},
    {"num": 18, "text": "A miracle is a service. It is the maximal service you can render to another. It is a way of loving your neighbor as yourself. You recognize your own and your neighbor's worth simultaneously."},
    {"num": 19, "text": "Miracles make minds one in God. They depend on cooperation because the Sonship is the sum of all that God created. Miracles therefore reflect the laws of eternity, not of time."},
    {"num": 20, "text": "Miracles reawaken the awareness that the spirit, not the body, is the altar of truth. This is the recognition that leads to the healing power of the miracle."},
    {"num": 21, "text": "Miracles are natural signs of forgiveness. Through miracles you accept God's forgiveness by extending it to others."},
    {"num": 22, "text": "Miracles are associated with fear only because of the belief that darkness can hide. You believe that what your physical eyes cannot see does not exist. This leads to a denial of spiritual sight."},
    {"num": 23, "text": "Miracles rearrange perception and place all levels in true perspective. This is healing because sickness comes from confusing the levels."},
    {"num": 24, "text": "Miracles enable you to heal the sick and raise the dead because you made sickness and death yourself, and can therefore abolish both. You are a miracle, capable of creating in the likeness of your Creator. Everything else is your own nightmare, and does not exist. Only the creations of light are real."},
    {"num": 25, "text": "Miracles are part of an interlocking chain of forgiveness which, when completed, is the Atonement. Atonement works all the time and in all the dimensions of time."},
    {"num": 26, "text": "Miracles represent freedom from fear. \"Atoning\" means \"undoing.\" The undoing of fear is an essential part of the Atonement value of miracles."},
    {"num": 27, "text": "A miracle is a universal blessing from God through me to all my brothers. It is the privilege of the forgiven to forgive."},
    {"num": 28, "text": "Miracles are a way of earning release from fear. Revelation induces a state in which fear has already been abolished. Miracles are thus a means and revelation is an end."},
    {"num": 29, "text": "Miracles praise God through you. They praise Him by honoring His creations, affirming their perfection. They heal because they deny body-identification and affirm spirit-identification."},
    {"num": 30, "text": "By recognizing spirit, miracles adjust the levels of perception and show them in proper alignment. This places spirit at the center, where it can communicate directly."},
    {"num": 31, "text": "Miracles should inspire gratitude, not awe. You should thank God for what you really are. The children of God are holy and the miracle honors their holiness, which can be hidden but never lost."},
    {"num": 32, "text": "I inspire all miracles, which are really intercessions. They intercede for your holiness and make your perceptions holy. By placing you beyond the physical laws they raise you into the sphere of celestial order. In this order you are perfect."},
    {"num": 33, "text": "Miracles honor you because you are lovable. They dispel illusions about yourself and perceive the light in you. They thus atone for your errors by freeing you from your nightmares. By releasing your mind from the imprisonment of your illusions, they restore your sanity."},
    {"num": 34, "text": "Miracles restore the mind to its fullness. By atoning for lack they establish perfect protection. The spirit's strength leaves no room for intrusions."},
    {"num": 35, "text": "Miracles are expressions of love, but they may not always have observable effects."},
    {"num": 36, "text": "Miracles are examples of right thinking, aligning your perceptions with truth as God created it."},
    {"num": 37, "text": "A miracle is a correction introduced into false thinking by me. It acts as a catalyst, breaking up erroneous perception and reorganizing it properly. This places you under the Atonement principle, where perception is healed. Until this has occurred, knowledge of the Divine Order is impossible."},
    {"num": 38, "text": "The Holy Spirit is the mechanism of miracles. He recognizes both God's creations and your illusions. He separates the true from the false by His ability to perceive totally rather than selectively."},
    {"num": 39, "text": "The miracle dissolves error because the Holy Spirit identifies error as false or unreal. This is the same as saying that by perceiving light, darkness automatically disappears."},
    {"num": 40, "text": "The miracle acknowledges everyone as your brother and mine. It is a way of perceiving the universal mark of God."},
    {"num": 41, "text": "Wholeness is the perceptual content of miracles. They thus correct, or atone for, the faulty perception of lack."},
    {"num": 42, "text": "A major contribution of miracles is their strength in releasing you from your false sense of isolation, deprivation and lack."},
    {"num": 43, "text": "Miracles arise from a miraculous state of mind, or a state of miracle-readiness."},
    {"num": 44, "text": "The miracle is an expression of an inner awareness of Christ and the acceptance of His Atonement."},
    {"num": 45, "text": "A miracle is never lost. It may touch many people you have not even met, and produce undreamed of changes in situations of which you are not even aware."},
    {"num": 46, "text": "The Holy Spirit is the highest communication medium. Miracles do not involve this type of communication, because they are temporary communication devices. When you return to your original form of communication with God by direct revelation, the need for miracles is over."},
    {"num": 47, "text": "The miracle is a learning device that lessens the need for time. It establishes an out-of-pattern time interval not under the usual laws of time. In this sense it is timeless."},
    {"num": 48, "text": "The miracle is the only device at your immediate disposal for controlling time. Only revelation transcends it, having nothing to do with time at all."},
    {"num": 49, "text": "The miracle makes no distinction among degrees of misperception. It is a device for perception correction, effective quite apart from either the degree or the direction of the error. This is its true indiscriminateness."},
    {"num": 50, "text": "The miracle compares what you have made with creation, accepting what is in accord with it as true, and rejecting what is out of accord as false."}
]

rules_for_decision = [
    {
        "num": 1,
        "key_phrase": "Today I will make no decisions by myself.",
        "text": "This means that you are choosing not to be the judge of what to do. But it must also mean you will not judge the situations where you will be called upon to make response. For if you judge them, you have set the rules for how you should react to them. And then another answer cannot but produce confusion and uncertainty and fear."
    },
    {
        "num": 2,
        "key_phrase": "If I make no decisions by myself, this is the day that will be given me.",
        "text": "Throughout the day, at any time you think of it and have a quiet moment for reflection, tell yourself again the kind of day you want; the feelings you would have, the things you want to happen to you, and the things you would experience."
    },
    {
        "num": 3,
        "key_phrase": "I have no question. I forgot what to decide.",
        "text": "Remember once again the day you want, and recognize that something has occurred that is not part of it. Then realize that you have asked a question by yourself, and must have set an answer in your terms. This cancels out the terms that you have set, and lets the answer show you what the question must have really been."
    },
    {
        "num": 4,
        "key_phrase": "At least I can decide I do not like what I feel now.",
        "text": "This much is obvious, and paves the way for the next easy step. If you are so unwilling to receive you cannot even let your question go, you can begin to change your mind with this."
    },
    {
        "num": 5,
        "key_phrase": "And so I hope I have been wrong.",
        "text": "This works against the sense of opposition, and reminds you that help is not being thrust upon you but is something that you want and that you need, because you do not like the way you feel. This tiny opening will be enough to let you go ahead with just a few more steps."
    },
    {
        "num": 6,
        "key_phrase": "I want another way to look at this.",
        "text": "Now you have changed your mind about the day, and have remembered what you really want. Its purpose has no longer been obscured by the insane belief you want it for the goal of being right when you are wrong."
    },
    {
        "num": 7,
        "key_phrase": "Perhaps there is another way to look at this. What can I lose by asking?",
        "text": "This final step is but acknowledgment of lack of opposition to be helped. It is a statement of an open mind, not certain yet, but willing to be shown. Thus you now can ask a question that makes sense, and so the answer will make sense as well."
    }
]

cause_and_effect = {
    "title": "Cause & Effect",
    "subtitle": "Understanding the True Cause of How I Feel",
    "text": "The world (EFFECT) is NOT the cause of the way I feel. The way I feel is based on a CHOICE that I made to choose a thought system (CAUSE) that believes the separation happened and is real.\n\nWe normally reverse cause and effect. This comes from the original belief that we created God.\n\nFor example: \"I feel sad because you didn't say hi to me.\"\nThe true cause and effect is that I already feel sad and I am looking for a reason to explain my sadness. The cause of my sadness is not that you didn't say hi to me, but a choice that I already made to think in a thought system that says the separation is real.\n\nHOW TO LET GO OF AN UPSET\n\n1. Identify the true cause.\n2. Remove the cause from where it is not — it is in your mind, not in the world.\n3. Get help from the loving part of your mind (the Holy Spirit) and ask it to help you choose the other thought system without judgment and guilt. Ask for forgiveness."
}

print("Reference data built.")

# ============================================================
# STEP 7: Build the BLA URL lookup for lessons
# ============================================================
def get_bla_lesson_url(num):
    return f"https://www.betterlifeawareness.com/acim-book-workbook-lesson-{num}"

# ============================================================
# STEP 8: Serialize all data to JSON strings for embedding
# ============================================================
print("Serializing data...")

# Add BLA URLs to lessons
for l in orig_lessons:
    l['bla_url'] = get_bla_lesson_url(l['num'])

lessons_json = json.dumps(orig_lessons, ensure_ascii=False)
quotes_json = json.dumps(all_quotes, ensure_ascii=False)
sg_json = json.dumps(sg_data, ensure_ascii=False)
meditations_json = json.dumps(meditations_data, ensure_ascii=False)
principles_json = json.dumps(principles_of_miracles, ensure_ascii=False)
rules_json = json.dumps(rules_for_decision, ensure_ascii=False)
cause_effect_json = json.dumps(cause_and_effect, ensure_ascii=False)

print(f"  lessons_json: {len(lessons_json):,} chars")
print(f"  quotes_json: {len(quotes_json):,} chars")
print(f"  sg_json: {len(sg_json):,} chars")
print(f"  meditations_json: {len(meditations_json):,} chars")
print(f"  principles_json: {len(principles_json):,} chars")
print(f"  rules_json: {len(rules_json):,} chars")

# Save intermediate data
with open('/tmp/app_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'lessons': orig_lessons,
        'quotes': all_quotes,
        'sg_data': sg_data,
        'meditations': meditations_data,
        'principles': principles_of_miracles,
        'rules': rules_for_decision,
        'cause_effect': cause_and_effect
    }, f, ensure_ascii=False)

print("Data saved to /tmp/app_data.json")
print("\nReady to build HTML.")
