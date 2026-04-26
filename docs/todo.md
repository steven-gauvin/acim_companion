# ACIM Companion — To Do

## Next Up

### Refine ALWAYS REMEMBER Study Theme
*Work through this together with Steven — content, quotes, and structure to be shaped collaboratively.*
- [ ] Review the current content and sections
- [ ] Add/remove quotes based on Steven's Apple Notes ("Always Remember" topic — 405 words)
- [ ] Consider adding a personal reflection or framing note from Steven

### Font Colour Consistency Review
*Meditations text brightened to #d8e4f0 — check if Reference and Study Themes body text should also be updated.*
- [ ] Review Reference section text readability
- [ ] Review Study Themes body text readability
- [ ] Decide whether to apply same colour or keep as-is

---

### Part II Workbook Integration (Lessons 221-365)
*Based on the Dee Doyle & Allen Watson commentary PDF.*

- [ ] **Extract Part II Content** — Pull the following from the PDF:
  - "The Introduction to Part II" (pages 9-10)
  - "Practice Instructions Part II" (pages 11-12)
  - The 14 "Commentary on What Is...?" sections (starting page 13)
  - Practice instructions for lessons 361-365 (page 263)
- [ ] **Design Part II UI** — Figure out how to display this content in the app:
  - A dedicated "Part II Introduction" card/entry
  - Clickable links for the general practice instructions (replacing "See complete instructions on page 19")
  - Section headers or links for the "What Is...?" commentaries
- [ ] **Implement Part II Links** — Update `build_html.py` to render the new Part II structure and clickable links.

### Apple Notes Research — Systematic Review
*Review each of Steven's 30 Apple Notes topics to identify material for Study Themes or Quotes.*

- [ ] Atonement (15,837 words)
- [ ] Law(s) (15,414 words)
- [ ] ! Exclamation Mark ! (11,071 words)
- [ ] This course (6,089 words)
- [ ] Redemption (3,626 words)
- [ ] Lessons 91 - 110 (3,271 words)
- [ ] The power of decision (2,727 words)
- [ ] Mission (1,400 words)
- [ ] Review I ( 1 - 50) (1,276 words)
- [ ] I am as God created me (1,031 words)
- [ ] Review III (Lessons 91 – 110) (969 words)
- [ ] Review II (61 - 80) (881 words)
- [ ] Angels (873 words)
- [ ] Never forget (847 words)
- [ ] A course (842 words)
- [ ] There is no order of difficulty (774 words)
- [ ] Brain (733 words)
- [ ] Ideas leave not their source (680 words)
- [ ] Lessons 1 - 50 (680 words)
- [ ] Lessons 61 - 80 (608 words)
- [ ] Here is the Answer (532 words)
- [ ] There is no world (520 words)
- [ ] Happy Dream (454 words)
- [ ] Always Remember (405 words)
- [ ] Goal - What is the goal of this course? (332 words)
- [ ] A healed mind (239 words)
- [ ] Keynote of ACIM (220 words)
- [ ] Let us not forget (191 words)
- [ ] Noteworthy Texts: (88 words)
- [ ] In progress (69 words)

---

- [ ] **Home Screen button** — Add an "Add to Home Screen" button/prompt in the app so users can easily install it on their phone without needing instructions

- [ ] **Verify all Study Theme quotes** against christmind.info before adding to app — references generated from AI memory, content confident but exact citations need checking
- [x] **Document quote selection process** — how quotes are chosen matters:
  1. The Course's **specific claim** about the concept (not general use of the word)
  2. The **most direct/clean expression** — short, unambiguous, quotable
  3. An **arc**: definition → mechanism → correction (not just a pile of quotes, but a progression)
  - *Why this works:* The Course has consistent internal logic. Certain passages crystallise a concept with unusual precision. Training on commentaries, study guides, and discussions gives weight to those passages. The arc turns a theme into a teaching tool, not just a reference list.
- [ ] **Study Themes section** — Add ~20 thematic categories (Perception, Ego, The Separation, Fear as Lack of Love, The Illusion of Separation, The Correction for Lack of Love, etc.) with curated quotes from Steven's handwritten notes. Based on transcribed `steven_acim_study_notes.md`.
- [ ] **Interactive Diagrams** — Build visual versions of the 3 hand-drawn diagrams:
  - Map of the Mind (1:1 — Principles of Miracles)
  - Miracle Principle #53 (true/accord → higher-level creation vs. false/discord/fear)
  - Mind of the Atonement Venn diagram (5:3 — Knowledge / Perception / Transfer)
- [x] **GitHub Pages hosting** — Deployed at https://steven-gauvin.github.io/acim_companion/acim_companion.html
- [ ] **Word/Concept Cards with Quotes** — Steven will scan ~20 handwritten half-A4 pages (front & back). Each page covers a word/concept (salvation, peace, forgiveness, etc.) with related quotes.

## Future / Ideas

- [ ] **Meditations section** — Revisit font sizes, colours, and layout for consistency with the new design system
- [ ] **Dee Doyle commentary formatting** — Selective italics for key ACIM phrases (e.g. "This thought I do not want. I choose instead the idea for today"), fix spacing after paragraphs, and tighten bullet point spacing

- [ ] Review overall app polish and consistency across all sections
- [ ] Consider export/backup functionality for user notes and edits
- [ ] Add "Compiled with love by Steven Gauvin" to the app's About or Reference section (already on splash)

## Completed ✓

- [x] **Splash dedication reduced to 2 lines** — "To Him Who sent me. / Thank you."
- [x] **New Dedications section** — Full dedication text accessible from Companion menu
- [x] **WB LIBRARY → WORKBOOK LIBRARY** — Menu label updated
- [x] **QUOTES → ACIM QUOTES** — Renamed in menu and panel
- [x] **New QUOTES section** — Personal favourite quotes; first entry is "The Avowal" by Denise Levertov
- [x] **ALWAYS REMEMBER Study Theme** — Added at top of Study Themes (starting point — to be refined with Steven)
- [x] **Splash quote label** — Updated to "My Favourite ACIM Daily Quote"
- [x] **Meditation text colour** — Brightened to #d8e4f0 for easier reading
- [x] **Breadcrumb "Back to Review" button** — Fixed click handler using delegated event listener
- [x] **Larger lesson card on Cards tab** — Increased from 420px to 520px, bigger font
- [x] **Daily Quote on Cards tab** — "My Favourite Daily Quote" section below the deck buttons
- [x] **Library tab renamed** to "Workbook Library"
- [x] **Splash screen redesign** — Lesson card as hero, quote below with label, dedication added
- [x] **Dedication updated** — Full text with JP, On Purpose, Sandy, Clearmind, Duane, Sharon, Circle of Atonement, Foundation for Inner Peace, Helen Schucman, Bill Thetford, "To Him Who sent me"
- [x] **Big T / Little t chart** — Added to Reference tab (first section), 14 pairs, Sandy's quote and credit
- [x] **Transcription of 76-page handwritten notes** — All pages digitized into `steven_acim_study_notes.md`
- [x] **Card back overflow fix** — Long notes now scroll within the card box
- [x] **Credit line added** — "Compiled with love by Steven Gauvin" on splash screen

---

## Session Summary — 26 April 2026

**Design rules agreed and applied across the app:**
- ACIM quote text → light blue `#d8e4f0`, no italic
- Commentary / narrative / framing text → warm cream `--text-bright` (`#f0ead8`), no italic
- Italic reserved for intentional emphasis only (e.g. "To Him Who sent me.", *Atonement*, *Redemption* mid-sentence)
- Working method going forward: agree 1–2 changes at a time, review before push

**Changes made this session:**

- [x] Splash screen — quote font size reduced to 15px to match lesson title; italic removed from daily quote and lesson title text
- [x] Cards page — top bar (lesson title, idea text, counter, progress bar) removed; Quote of the Day section removed; card face title de-italicised and reduced to 18px; JS fixed after top bar removal caused blank card
- [x] ACIM Quotes page — featured quote and list items de-italicised
- [x] Workbook Library — lesson list titles de-italicised
- [x] Dee Doyle commentary — colour changed from blue-grey to warm cream `--text-bright`
- [x] Study Themes (Always Remember) — framing/narrative text changed to warm cream; ACIM quotes changed to light blue; italic removed from reflective framing paragraphs ("Am I a miracle worker?", "Not 'lose' — but 'loose'...")
- [x] Study Themes — "Here is the Answer" moved to position 2 (after Always Remember, before Angels)
- [x] The Avowal poem (Personal Quotes) — italic removed, font size reduced to 14px
- [x] Dedications page — italic removed from all text except "To Him Who sent me." (gold, intentional); spacer height reduced from 16px to 10px; double spacer before body text collapsed to single; closing lines updated to: "I found my way; again. / You will too, for this is the way. / May this be a light for you to guide the way."; comma added after "grandparents"
- [x] Sandy Levey-Lundén quote (Reference / Big T Little t) — italic removed
- [x] Study Themes body text — `.bigt-quote-text` and `.st-quote-text` italic removed

**Email drafted:** `docs/companion_email.md` — warm personal email to Sandy, Duane, and Katrina sharing the app with a short guide to what's in it and home screen instructions.

**Still outstanding / to revisit:**
- Meditations section — font sizes, colours, layout (Future / Ideas)
- Dee Doyle commentary — selective italics for key ACIM phrases, paragraph spacing, bullet spacing (Future / Ideas)
