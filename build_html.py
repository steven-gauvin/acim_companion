"""Build the unified ACIM Companion App HTML — v2 with blue theme, zoom viewer, custom charts."""
import json, base64, os

# Load pre-built data
with open('/tmp/app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lessons_json = json.dumps(data['lessons'], ensure_ascii=False)
quotes_json = json.dumps(data['quotes'], ensure_ascii=False)
sg_json = json.dumps(data['sg_data'], ensure_ascii=False)
meditations_json = json.dumps(data['meditations'], ensure_ascii=False)
principles_json = json.dumps(data['principles'], ensure_ascii=False)
rules_json = json.dumps(data['rules'], ensure_ascii=False)
cause_effect_json = json.dumps(data['cause_effect'], ensure_ascii=False)

# Review map: lesson_num -> review info
with open('/tmp/review_map.json', 'r', encoding='utf-8') as _rf:
    review_map_json = _rf.read()

# Part II data: intro, practice instructions, What Is commentaries
with open('/tmp/part2_data.json', 'r', encoding='utf-8') as _p2:
    part2_data_raw = json.load(_p2)
part2_json = json.dumps(part2_data_raw, ensure_ascii=False)

# Load reviews raw from original HTML
with open('/home/ubuntu/upload/flashcards_original.html', 'r', encoding='utf-8') as f:
    orig = f.read()
import re

# Embed photo charts as base64
def embed_img(path):
    with open(path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()

img_dawson = embed_img('/home/ubuntu/acim_flashcards/chart_dawson_sm.jpg')
img_heaven = embed_img('/home/ubuntu/acim_flashcards/chart_heaven_sm.jpg')
img_mind   = embed_img('/home/ubuntu/acim_flashcards/chart_mind_sm.jpg')
img_thought= embed_img('/home/ubuntu/acim_flashcards/chart_thought_sm.jpg')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
<title>A Course in Miracles — Personal Companion</title>
<style>
/* ============================================================
   BASE & RESET
   ============================================================ */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --blue: #4a8fc4;
  --blue-light: #7ab8e8;
  --blue-dim: #2a5a84;
  --blue-glow: rgba(74,143,196,0.15);
  --gold: #c9a84c;
  --gold-light: #e8c97a;
  --gold-dim: #7a6030;
  --gold-glow: rgba(201,168,76,0.15);
  --bg: #0a0d12;
  --bg2: #0f1520;
  --bg3: #161e2e;
  --bg4: #1d2840;
  --border: #1e2d45;
  --text: #c8d8e8;
  --text-dim: #5a7a9a;
  --text-bright: #f0ead8;
  --accent: #c9a84c;
  --edited: #4a9a6a;
  --radius: 10px;
  --tab-h: 48px;
  --header-h: 64px;
}}
html, body {{ height: 100%; overflow: hidden; background: var(--bg); color: var(--text); font-family: Georgia, 'Times New Roman', serif; font-size: 15px; line-height: 1.6; }}

/* ============================================================
   SPLASH SCREEN
   ============================================================ */
#splash {{
  position: fixed; inset: 0; z-index: 1000;
  background: var(--bg);
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  padding: 24px 32px calc(60px + env(safe-area-inset-bottom, 0px));
  overflow-y: auto; overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  transition: opacity 0.8s ease;
}}
#splash > * {{ flex-shrink: 0; }}
#splash.hidden {{ opacity: 0; pointer-events: none; }}
.splash-diamonds {{ color: var(--gold); font-size: 18px; letter-spacing: 12px; margin-bottom: 20px; }}
.splash-title {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); margin-bottom: 6px; }}
.splash-subtitle {{ font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 20px; }}
.splash-quote-wrap {{ max-width: 480px; text-align: center; margin-bottom: 24px; }}
.splash-quote-label {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 12px; }}
#splash-quote {{
  font-size: 18px; line-height: 1.8; color: var(--text-bright);
  font-style: italic; white-space: pre-line;
  margin-bottom: 16px;
}}
#splash-source {{ font-size: 11px; letter-spacing: 2px; color: var(--gold-dim); text-transform: uppercase; }}
.splash-today {{
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 16px 24px;
  text-align: center; max-width: 380px; width: 100%;
  margin-bottom: 28px;
  border-left: 3px solid var(--gold-dim);
}}
.splash-today-label {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 6px; }}
.splash-today-lesson {{ font-size: 13px; letter-spacing: 2px; color: var(--gold); margin-bottom: 4px; }}
.splash-today-title {{ font-size: 15px; color: var(--text-bright); font-style: italic; }}
.splash-enter {{
  background: transparent; border: 1px solid var(--gold-dim);
  color: var(--gold); font-size: 12px; letter-spacing: 3px;
  text-transform: uppercase; padding: 12px 32px;
  border-radius: 30px; cursor: pointer;
  transition: all 0.3s;
}}
.splash-enter:hover {{ background: var(--gold); color: var(--bg); border-color: var(--gold); }}
.splash-dedication {{
  max-width: 420px; text-align: center; margin-top: 20px;
  padding-top: 16px; border-top: 1px solid var(--border);
}}
.splash-dedication-text {{ font-size: 13px; color: var(--text-dim); font-style: italic; line-height: 1.7; margin-bottom: 8px; }}
.splash-dedication-names {{ font-size: 11px; color: var(--gold-dim); letter-spacing: 1px; line-height: 1.6; }}

/* ============================================================
   MAIN LAYOUT
   ============================================================ */
#app {{ height: 100%; display: flex; flex-direction: column; }}
.app-header {{
  height: var(--header-h); background: var(--bg2);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 16px; flex-shrink: 0;
}}
.header-title {{ text-align: center; flex: 1; }}
.header-title-main {{ font-size: 13px; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); }}
.header-title-sub {{ font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--text-dim); margin-top: 2px; }}
.header-btn {{
  background: transparent; border: 1px solid var(--border);
  color: var(--text-dim); font-size: 11px; letter-spacing: 1px;
  padding: 6px 10px; border-radius: 6px; cursor: pointer;
  white-space: nowrap; transition: all 0.2s;
}}
.header-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
/* App Footer */
.app-footer {{
  flex-shrink: 0; padding: 14px 20px;
  border-top: 1px solid var(--border);
  font-size: 12px; color: var(--text-dim); font-style: italic;
  line-height: 1.6; text-align: center;
}}
.app-footer-name {{
  display: block; margin-top: 6px;
  font-size: 11px; color: var(--gold-dim); letter-spacing: 0.5px; font-style: normal;
}}
/* Charts dropdown */
.charts-dropdown {{
  position: absolute; top: calc(var(--header-h) + var(--tab-h)); right: 0; /* tab-h now used by companion-nav */
  background: var(--bg2); border: 1px solid var(--border); border-radius: 0 0 8px 8px;
  z-index: 200; min-width: 160px; box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}}
.charts-dropdown-item {{
  padding: 12px 16px; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--text-dim); cursor: pointer; border-bottom: 1px solid var(--border);
  transition: all 0.15s;
}}
.charts-dropdown-item:last-child {{ border-bottom: none; }}
.charts-dropdown-item:hover {{ color: var(--gold); background: var(--bg3); }}

/* Companion dropdown nav */
.companion-nav {{
  height: var(--tab-h); background: var(--bg2);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; position: relative;
}}
.companion-btn {{
  background: transparent; border: none;
  color: var(--gold); font-family: Georgia, 'Times New Roman', serif;
  font-size: 12px; letter-spacing: 3px; text-transform: uppercase;
  cursor: pointer; padding: 8px 16px;
  display: flex; align-items: center; gap: 8px;
  transition: all 0.2s;
}}
.companion-btn:hover {{ color: var(--gold-light); }}
.companion-btn .companion-arrow {{
  font-size: 8px; transition: transform 0.2s;
}}
.companion-btn.open .companion-arrow {{ transform: rotate(180deg); }}
.companion-menu {{
  display: none; position: absolute; top: 100%; left: 50%;
  transform: translateX(-50%);
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 0 0 10px 10px;
  z-index: 300; min-width: 220px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}}
.companion-menu.open {{ display: block; }}
.companion-menu-item {{
  padding: 14px 20px; font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--text-dim); cursor: pointer; border-bottom: 1px solid var(--border);
  transition: all 0.15s; text-align: center; font-family: Georgia, 'Times New Roman', serif;
}}
.companion-menu-item:last-child {{ border-bottom: none; border-radius: 0 0 10px 10px; }}
.companion-menu-item:hover {{ color: var(--gold); background: var(--bg3); }}
.companion-menu-item.active {{ color: var(--gold); }}
.companion-overlay {{
  display: none; position: fixed; inset: 0; z-index: 250;
}}
.companion-overlay.open {{ display: block; }}

.panels {{ flex: 1; overflow: hidden; position: relative; }}
.panel {{ position: absolute; inset: 0; overflow-y: auto; display: none; }}
.panel.active {{ display: block; }}

/* ============================================================
   CARDS PANEL
   ============================================================ */
.cards-panel {{ background: var(--bg); }}
.card-above {{
  padding: 16px 20px 8px;
  display: flex; align-items: center; justify-content: space-between;
}}
.card-above-info {{ text-align: center; flex: 1; }}
.cf-num {{ font-size: 10px; letter-spacing: 3px; color: var(--gold-dim); text-transform: uppercase; }}
.cf-title {{ font-size: 13px; color: var(--text-dim); font-style: italic; margin-top: 2px; }}
.card-counter {{ font-size: 11px; color: var(--text-dim); }}
.progress-bar {{ height: 2px; background: var(--border); margin: 0 20px 12px; border-radius: 2px; }}
.progress-fill {{ height: 100%; background: var(--gold); border-radius: 2px; transition: width 0.3s; }}
.card-scene {{ padding: 0 16px 16px; perspective: 1200px; }}
.card-3d {{
  width: 100%; min-height: 520px;
  transform-style: preserve-3d;
  transition: transform 0.55s cubic-bezier(.4,0,.2,1);
  cursor: pointer; position: relative;
}}
.card-3d.flipped {{ transform: rotateY(180deg); }}
.card-face, .card-back {{
  position: absolute; inset: 0;
  backface-visibility: hidden; -webkit-backface-visibility: hidden;
  border-radius: 14px; padding: 28px 24px;
  border: 1px solid var(--border);
  min-height: 520px;
}}
.card-face {{ background: var(--bg2); display: flex; flex-direction: column; }}
.card-back {{ background: var(--bg3); transform: rotateY(180deg); display: flex; flex-direction: column; overflow: hidden; }}
.card-face-num {{ font-size: 10px; letter-spacing: 3px; color: var(--gold-dim); text-transform: uppercase; margin-bottom: 8px; }}
.card-face-title {{ font-size: 24px; color: var(--text-bright); line-height: 1.5; font-style: italic; margin-bottom: 24px; }}
.card-face-hint {{ font-size: 11px; color: var(--text-dim); letter-spacing: 1px; text-align: center; margin-top: auto; padding-top: 20px; }}
.card-back-num {{ font-size: 10px; letter-spacing: 3px; color: var(--gold-dim); text-transform: uppercase; margin-bottom: 4px; flex-shrink: 0; }}
.card-back-title {{ font-size: 13px; color: var(--text-dim); font-style: italic; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 16px; flex-shrink: 0; }}
.card-notes {{ font-size: 14px; color: var(--text); line-height: 1.7; white-space: pre-wrap; overflow-y: auto; flex: 1; padding-right: 4px; margin-bottom: 12px; }}
.card-notes.edited {{ color: #6fbc8f; }}
/* Special completion card */
.special-card .card-face {{ background: linear-gradient(135deg, var(--bg2) 0%, #2a2520 100%); border: 1px solid var(--gold-dim); }}
.special-card .card-back {{ background: linear-gradient(135deg, var(--bg3) 0%, #2a2520 100%); border: 1px solid var(--gold-dim); }}
.special-card .card-face-num {{ color: var(--gold); font-size: 13px; letter-spacing: 4px; }}
.special-card .card-face-title {{ color: var(--gold); font-size: 24px; }}
.special-card .card-face-hint {{ color: var(--gold-dim); }}
.special-card .card-back-num {{ color: var(--gold); font-size: 13px; }}
.special-card .card-notes {{ font-size: 13px; line-height: 1.8; max-height: 450px; overflow-y: auto; padding-right: 8px; }}
.special-lesson .lesson-num-badge {{ background: var(--gold) !important; color: var(--bg1) !important; font-size: 14px !important; }}
.special-lesson .lesson-header {{ border-left: 3px solid var(--gold); }}
.card-edit-area {{
  width: 100%; background: var(--bg4); border: 1px solid var(--border);
  color: var(--text); font-family: Georgia, serif; font-size: 14px;
  line-height: 1.7; padding: 12px; border-radius: 8px;
  resize: vertical; min-height: 120px; display: none; margin-bottom: 12px;
}}
.card-actions {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
.btn-action {{
  font-size: 11px; letter-spacing: 1px; padding: 7px 14px;
  border-radius: 20px; cursor: pointer; border: 1px solid;
  text-decoration: none; display: inline-block;
  transition: all 0.2s; white-space: nowrap;
}}
.btn-edit {{ border-color: var(--border); color: var(--text-dim); background: transparent; }}
.btn-edit:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.btn-save {{ border-color: var(--edited); color: var(--edited); background: transparent; }}
.btn-save:hover {{ background: var(--edited); color: var(--bg); }}
.btn-cancel {{ border-color: var(--border); color: var(--text-dim); background: transparent; }}
.btn-restore {{ border-color: #8a4040; color: #c07070; background: transparent; }}
.btn-link {{ border-color: var(--gold-dim); color: var(--gold); background: transparent; }}
.btn-link:hover {{ background: var(--gold); color: var(--bg); }}
.btn-link-secondary {{ border-color: #2a5a7a; color: #5a9abc; background: transparent; }}
.btn-link-secondary:hover {{ background: #2a5a7a; color: #fff; }}
.card-nav {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 16px 16px;
}}
.nav-btn {{
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 18px; width: 44px; height: 44px;
  border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}}
.nav-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.goto-row {{ display: flex; gap: 8px; align-items: center; }}
.goto-input {{
  width: 64px; background: var(--bg3); border: 1px solid var(--border);
  color: var(--text); font-size: 13px; padding: 8px 10px;
  border-radius: 8px; text-align: center;
}}
.goto-btn {{
  background: transparent; border: 1px solid var(--border);
  color: var(--text-dim); font-size: 11px; padding: 8px 12px;
  border-radius: 8px; cursor: pointer;
}}
.deck-btns {{ display: flex; gap: 8px; padding: 0 16px 16px; }}
.deck-btn {{
  flex: 1; background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 10px; letter-spacing: 1px;
  text-transform: uppercase; padding: 10px; border-radius: 8px;
  cursor: pointer; transition: all 0.2s;
}}
.deck-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}

/* Daily quote on Cards tab */
.cards-daily-quote {{
  margin: 8px 16px 16px;
  padding: 20px 24px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  text-align: center;
}}
.cards-daily-quote-label {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 10px; }}
.cards-daily-quote-text {{ font-size: 14px; color: var(--text-dim); font-style: italic; line-height: 1.7; white-space: pre-line; margin-bottom: 8px; }}
.cards-daily-quote-source {{ font-size: 10px; letter-spacing: 2px; color: var(--gold-dim); text-transform: uppercase; }}

/* ============================================================
   LIBRARY PANEL
   ============================================================ */
.library-panel {{ background: var(--bg); }}
.library-search {{
  padding: 12px 16px 8px;
  position: sticky; top: 0; background: var(--bg); z-index: 10;
  border-bottom: 1px solid var(--border);
}}
.search-input {{
  width: 100%; background: var(--bg3); border: 1px solid var(--border);
  color: var(--text); font-size: 14px; padding: 10px 14px 10px 36px;
  border-radius: 10px; outline: none;
}}
.search-wrap {{ position: relative; margin-bottom: 10px; }}
.search-icon {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-dim); font-size: 14px; }}
.filter-row {{ display: flex; gap: 6px; overflow-x: auto; padding-bottom: 4px; scrollbar-width: none; }}
.filter-row::-webkit-scrollbar {{ display: none; }}
.filter-btn {{
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 10px; letter-spacing: 1px;
  padding: 5px 12px; border-radius: 20px; cursor: pointer;
  white-space: nowrap; transition: all 0.2s;
}}
.filter-btn.active {{ background: var(--gold); border-color: var(--gold); color: var(--bg); }}
.results-count {{ font-size: 11px; color: var(--text-dim); padding: 6px 16px; }}
.lesson-item {{ border-bottom: 1px solid var(--border); }}
.lesson-header {{
  display: flex; align-items: center; padding: 14px 16px;
  cursor: pointer; gap: 12px;
}}
.lesson-header:hover {{ background: var(--bg2); }}
.lesson-num-badge {{
  min-width: 32px; height: 32px; background: var(--bg3);
  border: 1px solid var(--border); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: var(--gold-dim); flex-shrink: 0;
}}
.lesson-item.has-edit .lesson-num-badge {{ border-color: var(--edited); color: var(--edited); }}
.lesson-item.starred .lesson-num-badge {{ border-color: var(--gold); color: var(--gold); background: var(--gold-glow); }}
.lesson-title-text {{ flex: 1; font-size: 14px; color: var(--text); font-style: italic; }}
.lesson-expand-icon {{ color: var(--text-dim); font-size: 12px; transition: transform 0.2s; }}
.lesson-item.expanded .lesson-expand-icon {{ transform: rotate(180deg); }}
.lesson-body {{ display: none; padding: 0 16px 16px; }}
.lesson-item.expanded .lesson-body {{ display: block; }}
.lesson-notes-text {{
  font-size: 14px; color: var(--text); line-height: 1.7;
  white-space: pre-wrap; padding: 12px; background: var(--bg3);
  border-radius: 8px; margin-bottom: 12px;
  border-left: 3px solid var(--gold-dim);
}}
.lesson-notes-text.edited {{ border-left-color: var(--edited); color: #6fbc8f; }}
.lesson-edit-area {{
  width: 100%; background: var(--bg4); border: 1px solid var(--border);
  color: var(--text); font-family: Georgia, serif; font-size: 14px;
  line-height: 1.7; padding: 12px; border-radius: 8px;
  resize: vertical; min-height: 100px; display: none; margin-bottom: 10px;
}}
.lesson-actions {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
.highlight {{ background: rgba(201,168,76,0.25); border-radius: 2px; }}

/* Dee Doyle & Allen Watson Commentary */
.sg-toggle-btn {{
  width: 100%; background: var(--bg2); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 11px; letter-spacing: 1px;
  text-transform: uppercase; padding: 10px 14px;
  border-radius: 8px; cursor: pointer; text-align: left;
  display: flex; align-items: center; justify-content: space-between;
  transition: all 0.2s; margin-top: 4px;
}}
.sg-toggle-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.sg-toggle-btn.open {{ border-color: var(--gold-dim); color: var(--gold); }}
.sg-body {{
  display: none; background: var(--bg2); border: 1px solid var(--border);
  border-top: none; border-radius: 0 0 8px 8px; padding: 16px;
  margin-top: -1px;
}}
.sg-body.open {{ display: block; }}
.sg-section {{ margin-bottom: 16px; }}
.sg-section:last-child {{ margin-bottom: 0; }}
.sg-section-label {{
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--gold-dim); margin-bottom: 8px;
  padding-bottom: 4px; border-bottom: 1px solid var(--border);
}}
.sg-section-text {{
  font-size: 13px; color: var(--text-dim); line-height: 1.75;
  white-space: pre-wrap;
}}


/* ============================================================
   QUOTES PANEL
   ============================================================ */
.quotes-panel {{ background: var(--bg); padding: 16px; }}
.quotes-daily-card {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px; padding: 28px 24px; text-align: center;
  margin-bottom: 16px;
  border-top: 3px solid var(--gold-dim);
}}
.quotes-daily-label {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 12px; }}
.quotes-daily-diamonds {{ color: var(--gold); font-size: 14px; letter-spacing: 8px; margin-bottom: 20px; opacity: 0.7; }}
.quotes-daily-text {{
  font-size: 16px; color: var(--text-bright); font-style: italic;
  line-height: 1.8; white-space: pre-line; margin-bottom: 16px;
}}
.quotes-daily-source {{ font-size: 11px; letter-spacing: 2px; color: var(--gold-dim); text-transform: uppercase; }}
.quotes-nav-row {{ display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 24px; }}
.quotes-nav-btn {{
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 18px; width: 40px; height: 40px;
  border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
}}
.quotes-nav-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.quotes-counter {{ font-size: 12px; color: var(--text-dim); }}

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

.back-to-review-breadcrumb {{ margin-bottom: 10px; }}

/* Part II styles */
.part2-badge {{
  font-size: 9px; font-weight: bold; letter-spacing: 1px;
  background: rgba(74,143,196,0.2); color: var(--blue-light);
  border: 1px solid var(--blue-dim);
  padding: 2px 6px; border-radius: 3px;
  margin-left: 6px; vertical-align: middle; text-transform: uppercase;
}}
.part2-intro-btn {{
  display: inline-block; background: transparent;
  border: 1px solid var(--gold-dim); color: var(--gold);
  font-size: 11px; padding: 4px 10px; border-radius: 4px;
  cursor: pointer; margin: 6px 4px 6px 0;
}}
.part2-intro-btn:hover {{ background: var(--bg3); }}
.part2-intro-content {{
  display: none; background: var(--bg2);
  border-left: 3px solid var(--blue-dim);
  padding: 12px 14px; margin: 8px 0;
  font-size: 12px; color: var(--text-dim);
  line-height: 1.7; white-space: pre-wrap;
  border-radius: 0 4px 4px 0; max-height: 400px; overflow-y: auto;
}}
.part2-intro-content.open {{ display: block; }}
.part2-section-header {{
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--blue-light); margin: 12px 0 6px;
  padding: 6px 10px; background: rgba(74,143,196,0.1);
  border-radius: 4px; border-left: 3px solid var(--blue-dim);
}}
/* Part II section divider */
.part2-divider {{
  display: flex; align-items: center; gap: 12px;
  padding: 16px 0 8px; margin-bottom: 4px;
}}
.part2-divider::before, .part2-divider::after {{
  content: ''; flex: 1; height: 1px; background: var(--blue-dim);
}}
.part2-divider-label {{
  font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
  color: var(--blue-light); white-space: nowrap;
}}
/* Part II intro card in library */
.part2-intro-card {{
  background: var(--bg2); border: 1px solid var(--blue-dim);
  border-radius: 10px; padding: 16px; margin-bottom: 12px;
}}
.part2-intro-card-title {{
  font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--blue-light); margin-bottom: 8px;
}}
.part2-intro-card-subtitle {{
  font-size: 13px; color: var(--text-dim); font-style: italic; margin-bottom: 12px;
}}
.part2-intro-card-body {{
  display: none; font-size: 12px; color: var(--text-dim);
  line-height: 1.7; white-space: pre-wrap; margin-top: 10px;
  max-height: 500px; overflow-y: auto;
}}
.part2-intro-card-body.open {{ display: block; }}
.back-to-review-btn {{
  background: rgba(201,168,76,0.15); border: 1px solid var(--gold);
  color: var(--gold); font-size: 12px; padding: 8px 16px;
  border-radius: 8px; cursor: pointer; letter-spacing: 0.5px;
  transition: all 0.2s; width: 100%; text-align: left;
}}
.back-to-review-btn:hover {{ background: var(--gold); color: var(--bg); }}

.quotes-section-title {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 12px; }}
.quote-item {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.2s;
}}
.quote-item:hover {{ border-color: var(--gold-dim); }}
.quote-item.active-quote {{ border-color: var(--gold); background: var(--bg3); }}
.quote-item-text {{ font-size: 13px; color: var(--text); font-style: italic; line-height: 1.7; white-space: pre-line; margin-bottom: 6px; }}
.quote-item-source {{ font-size: 10px; letter-spacing: 1px; color: var(--gold-dim); text-transform: uppercase; }}

/* Personal Quotes */
.personal-quote-item {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px; padding: 28px 24px; text-align: center;
  margin-bottom: 20px;
  border-top: 3px solid var(--gold-dim);
}}
.personal-quote-poem {{
  font-size: 17px; color: var(--text-bright); font-style: italic;
  line-height: 2; margin-bottom: 20px;
}}
.personal-quote-title {{
  font-size: 13px; letter-spacing: 2px; color: var(--gold);
  text-transform: uppercase; margin-bottom: 6px;
}}
.personal-quote-author {{
  font-size: 12px; color: var(--text-dim); letter-spacing: 1px;
}}

/* Dedications Panel */
.dedications-panel {{ background: var(--bg); padding: 24px 16px; }}
.dedications-wrap {{
  max-width: 480px; margin: 0 auto; text-align: center;
  padding: 20px 0;
}}
.dedications-diamonds {{
  color: var(--gold); font-size: 16px; letter-spacing: 10px;
  margin-bottom: 32px; opacity: 0.8;
}}
.dedications-text {{
  font-size: 15px; color: var(--text-bright); font-style: italic;
  line-height: 1.8; margin-bottom: 4px;
}}
.dedications-names {{
  font-size: 13px; color: var(--text-dim); line-height: 1.8;
}}
.dedications-highlight {{
  font-size: 16px; font-style: italic; color: var(--gold);
  letter-spacing: 0.5px;
}}
.dedications-compiled {{
  font-size: 11px; letter-spacing: 1.5px; color: var(--text-dim);
  text-transform: uppercase;
}}
.dedications-spacer {{ height: 20px; }}

/* ============================================================
   MEDITATIONS PANEL
   ============================================================ */
.meditations-panel {{ background: var(--bg); padding: 12px; }}
.med-card {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: var(--radius); margin-bottom: 10px; overflow: hidden;
}}
.med-header {{
  padding: 16px; cursor: pointer; display: flex;
  align-items: center; justify-content: space-between;
}}
.med-header:hover {{ background: var(--bg3); }}
.med-title {{ font-size: 15px; color: var(--gold); margin-bottom: 2px; }}
.med-subtitle {{ font-size: 12px; color: var(--text-dim); }}
.med-body {{ display: none; padding: 0 16px 20px; }}
.med-card.expanded .med-body {{ display: block; }}
.med-card.expanded .lesson-expand-icon {{ transform: rotate(180deg); }}
.med-section {{ margin-bottom: 16px; }}
.med-section-heading {{
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--gold-dim); margin-bottom: 10px; margin-top: 16px;
  padding-bottom: 4px; border-bottom: 1px solid var(--border);
}}
.med-text {{
  font-size: 14px; color: #d8e4f0; line-height: 1.8;
  white-space: pre-wrap;
}}

/* ============================================================
   REFERENCE PANEL
   ============================================================ */
.reference-panel {{ background: var(--bg); padding: 12px; }}
.ref-section {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: var(--radius); margin-bottom: 10px; overflow: hidden;
}}
.ref-header {{
  padding: 16px; cursor: pointer; display: flex;
  align-items: center; justify-content: space-between;
}}
.ref-header:hover {{ background: var(--bg3); }}
.ref-title {{ font-size: 15px; color: var(--gold); margin-bottom: 2px; }}
.ref-subtitle {{ font-size: 12px; color: var(--text-dim); }}
.ref-body {{ display: none; padding: 0 16px 16px; }}
.ref-section.expanded .ref-body {{ display: block; }}
.ref-section.expanded .lesson-expand-icon {{ transform: rotate(180deg); }}
/* Big T / Little t Chart */
.bigt-chart {{ padding: 8px 0; }}
.bigt-row {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid rgba(201,168,76,0.08);
}}
.bigt-row:last-child {{ border-bottom: none; }}
.bigt-left {{
  flex: 1; text-align: left; font-size: 14px; color: var(--text-dim);
  font-style: italic; letter-spacing: 0.5px;
}}
.bigt-center {{
  width: 40px; text-align: center; font-size: 16px; color: rgba(201,168,76,0.25);
}}
.bigt-right {{
  flex: 1; text-align: right; font-size: 14px; color: var(--gold);
  font-weight: 600; letter-spacing: 0.5px;
}}
.bigt-header-row {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 0 8px; border-bottom: 2px solid var(--gold-dim);
  margin-bottom: 4px;
}}
.bigt-header-left {{
  flex: 1; text-align: left; font-size: 11px; color: var(--text-dim);
  letter-spacing: 2px; text-transform: uppercase;
}}
.bigt-header-right {{
  flex: 1; text-align: right; font-size: 11px; color: var(--gold);
  letter-spacing: 2px; text-transform: uppercase;
}}
.bigt-quote {{
  margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border);
  text-align: center;
}}
.bigt-quote-text {{
  font-size: 14px; color: var(--text); font-style: italic; line-height: 1.6;
  margin-bottom: 8px;
}}
.bigt-quote-source {{
  font-size: 11px; color: var(--gold-dim); letter-spacing: 1px;
}}

/* Study Themes */
.study-theme {{ padding: 4px 0 8px; }}
.st-section-label {{
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--gold); opacity: 0.7; margin: 20px 0 10px; padding-bottom: 6px;
  border-bottom: 1px solid rgba(201,168,76,0.15);
}}
.st-framing {{
  font-size: 14px; color: var(--text); line-height: 1.7;
  margin: 0 0 8px; font-style: italic; opacity: 0.9;
}}
.st-quote {{
  margin-bottom: 14px; padding: 12px 14px;
  background: rgba(201,168,76,0.04); border-left: 2px solid rgba(201,168,76,0.3);
  border-radius: 0 6px 6px 0;
}}
.st-quote-text {{
  font-size: 14px; color: var(--text); line-height: 1.65; font-style: italic;
  margin-bottom: 6px;
}}
.st-quote-ref {{
  font-size: 11px; color: var(--gold-dim); letter-spacing: 0.5px;
}}
/* Principles */
.principle-item {{
  padding: 12px 0; border-bottom: 1px solid var(--border);
  display: flex; gap: 12px;
}}
.principle-item:last-child {{ border-bottom: none; }}
.principle-num {{
  min-width: 32px; height: 32px; background: var(--bg3);
  border: 1px solid var(--border); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: var(--gold-dim); flex-shrink: 0;
}}
.principle-text {{ font-size: 13px; color: var(--text); line-height: 1.7; }}
/* Rules */
.rule-item {{ padding: 14px 0; border-bottom: 1px solid var(--border); }}
.rule-item:last-child {{ border-bottom: none; }}
.rule-num {{ font-size: 10px; letter-spacing: 2px; color: var(--gold-dim); text-transform: uppercase; margin-bottom: 6px; }}
.rule-phrase {{
  font-size: 15px; color: var(--gold-light); font-style: italic;
  margin-bottom: 8px; line-height: 1.5;
}}
.rule-text {{ font-size: 13px; color: var(--text-dim); line-height: 1.7; }}

/* Rules for Decision expandable */
.rfd-rule {{
  border-bottom: 1px solid var(--border);
  margin-bottom: 2px;
}}
.rfd-rule:last-child {{ border-bottom: none; }}
.rfd-header {{
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px 4px; cursor: pointer; user-select: none;
}}
.rfd-header:hover {{ background: rgba(201,168,76,0.04); border-radius: 6px; }}
.rfd-num {{
  min-width: 28px; height: 28px; border-radius: 50%;
  background: rgba(201,168,76,0.15); color: var(--gold);
  font-size: 13px; font-weight: bold;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 2px;
}}
.rfd-summary {{ flex: 1; }}
.rfd-label {{ font-size: 11px; color: var(--text-dim); margin-bottom: 3px; }}
.rfd-phrase {{
  font-size: 14px; color: var(--gold-light); font-style: italic; line-height: 1.5;
}}
.rfd-icon {{
  font-size: 10px; color: var(--text-dim); margin-top: 6px; flex-shrink: 0;
  transition: transform 0.2s;
}}
.rfd-body {{
  display: none; padding: 0 4px 14px 40px;
  font-size: 13px; color: var(--text-dim); line-height: 1.75;
}}
.rfd-body p {{ margin: 0 0 10px; }}
.rfd-body p:last-child {{ margin-bottom: 0; }}
.rfd-rule.rfd-open .rfd-body {{ display: block; }}
.rfd-rule.rfd-open .rfd-icon {{ transform: rotate(180deg); }}

/* ============================================================
   CUSTOM CHARTS (HTML diagrams)
   ============================================================ */
.custom-chart {{
  background: var(--bg3); border-radius: 10px; padding: 24px 20px;
  margin-bottom: 8px;
}}
/* Cause & Effect diagram */
.ce-flow {{
  display: flex; align-items: flex-start; justify-content: center;
  gap: 0; flex-wrap: nowrap; overflow-x: auto;
  padding: 8px 0 16px;
}}
.ce-node {{
  text-align: center; min-width: 80px; flex-shrink: 0;
}}
.ce-node-label {{
  font-size: 16px; font-weight: bold; color: var(--gold-light);
  letter-spacing: 1px; margin-bottom: 4px;
}}
.ce-node-sub {{
  font-size: 11px; color: var(--text-dim); font-style: italic;
  line-height: 1.4;
}}
.ce-arrow {{
  color: #c04040; font-size: 22px; padding: 0 4px;
  align-self: flex-start; padding-top: 6px; flex-shrink: 0;
}}
.ce-callout {{
  background: rgba(201,168,76,0.12); border: 1px solid var(--gold-dim);
  border-radius: 8px; padding: 10px 14px; text-align: center;
  font-size: 12px; color: var(--gold-light); letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 16px;
  position: relative;
}}
.ce-callout::after {{
  content: '▼'; position: absolute; bottom: -18px; left: 50%;
  transform: translateX(-50%); color: var(--gold-dim); font-size: 14px;
}}
.ce-fork {{
  display: flex; justify-content: center; gap: 40px;
  margin: 24px 0 16px;
}}
.ce-fork-item {{
  text-align: center;
}}
.ce-fork-label {{
  font-size: 18px; font-weight: bold; letter-spacing: 2px;
  margin-top: 8px;
}}
.ce-fork-fear {{ color: #c04040; }}
.ce-fork-love {{ color: #4a9a7a; }}
.ce-insight-box {{
  border: 1px dashed var(--border); border-radius: 8px;
  padding: 14px 16px; font-size: 13px; color: var(--text-dim);
  line-height: 1.7; text-align: center; margin-top: 8px;
}}
.ce-insight-box strong {{ color: var(--text-bright); }}
.ce-result-note {{
  font-size: 13px; color: var(--text-dim); line-height: 1.7;
  padding: 12px 0; border-top: 1px solid var(--border); margin-top: 16px;
}}
/* Experience Chart */
.exp-chart {{
  position: relative; padding: 16px 0;
}}
.exp-v-container {{
  display: flex; justify-content: center; position: relative;
  padding: 0 20px;
}}
.exp-v-left, .exp-v-right {{
  width: 2px; background: var(--text-dim);
  position: absolute; top: 0; bottom: 0;
}}
.exp-v-left {{ left: 50%; transform: translateX(-80px) rotate(-15deg); transform-origin: top; }}
.exp-v-right {{ right: 50%; transform: translateX(80px) rotate(15deg); transform-origin: top; }}
.exp-center {{
  text-align: center; z-index: 1; width: 100%;
}}
.exp-something {{
  background: var(--bg4); border: 2px solid var(--gold-dim);
  border-radius: 8px; padding: 12px 20px; display: inline-block;
  font-size: 16px; color: var(--text-bright); margin: 0 auto 16px;
  font-style: italic;
}}
.exp-path-up {{
  display: flex; flex-direction: column; align-items: center;
  gap: 2px; margin-bottom: 16px;
}}
.exp-path-down {{
  display: flex; flex-direction: column; align-items: center;
  gap: 2px; margin-top: 8px;
}}
.exp-step-up {{
  font-size: 13px; color: #4a9a7a; padding: 3px 0;
}}
.exp-step-down {{
  font-size: 13px; color: #c06060; padding: 3px 0;
}}
.exp-arrow-up {{ color: #4a9a7a; font-size: 16px; }}
.exp-arrow-down {{ color: #c06060; font-size: 16px; }}
.exp-choice-note {{
  background: rgba(201,168,76,0.08); border: 1px solid var(--gold-dim);
  border-radius: 8px; padding: 12px 16px; font-size: 13px;
  color: var(--text-dim); line-height: 1.6; margin: 16px 0;
}}
.exp-choice-note strong {{ color: var(--gold-light); }}
/* How to Let Go */
.letgo-steps {{
  counter-reset: letgo;
}}
.letgo-step {{
  display: flex; gap: 12px; padding: 12px 0;
  border-bottom: 1px solid var(--border);
}}
.letgo-step:last-child {{ border-bottom: none; }}
.letgo-num {{
  min-width: 28px; height: 28px; background: var(--gold-dim);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 12px; color: var(--bg); font-weight: bold; flex-shrink: 0;
}}
.letgo-text {{ font-size: 14px; color: var(--text); line-height: 1.7; }}
.letgo-text strong {{ color: var(--text-bright); }}
.incorrectable-box {{
  background: rgba(192,64,64,0.08); border: 1px solid #6a3030;
  border-radius: 8px; padding: 16px; margin-top: 16px;
}}
.incorrectable-title {{
  font-size: 12px; color: #c07070; letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 12px;
}}
.incorrectable-step {{
  display: flex; gap: 10px; padding: 8px 0;
  border-bottom: 1px solid rgba(106,48,48,0.4);
  font-size: 13px; color: var(--text-dim); line-height: 1.6;
}}
.incorrectable-step:last-child {{ border-bottom: none; }}
.incorrectable-num {{
  min-width: 22px; color: #c07070; font-weight: bold; flex-shrink: 0;
}}
/* Thought System Comparison */
.thought-comparison {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
}}
.thought-col {{
  border-radius: 8px; padding: 14px;
}}
.thought-col-ego {{ background: rgba(160,48,48,0.15); border: 1px solid #6a3030; }}
.thought-col-hs {{ background: rgba(48,120,80,0.15); border: 1px solid #2a6040; }}
.thought-col-title {{
  font-size: 12px; font-weight: bold; letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 10px; padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}}
.thought-col-ego .thought-col-title {{ color: #e07070; }}
.thought-col-hs .thought-col-title {{ color: #70c090; }}
.thought-item {{
  font-size: 11px; color: var(--text-dim); padding: 3px 0;
  line-height: 1.5;
}}

/* ============================================================
   PHOTO CHARTS (zoomable image viewer)
   ============================================================ */
.photo-chart-wrap {{
  position: relative; overflow: hidden; border-radius: 8px;
  background: #fff; touch-action: none;
  cursor: grab;
}}
.photo-chart-wrap:active {{ cursor: grabbing; }}
.photo-chart-img {{
  width: 100%; display: block;
  transform-origin: 0 0;
  transition: transform 0.1s;
  user-select: none; pointer-events: none;
}}
.zoom-controls {{
  display: flex; gap: 8px; justify-content: center;
  padding: 10px 0 4px;
}}
.zoom-btn {{
  background: var(--bg4); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 18px; width: 36px; height: 36px;
  border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}}
.zoom-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.zoom-label {{ font-size: 11px; color: var(--text-dim); align-self: center; min-width: 40px; text-align: center; }}

/* ============================================================
   CHARTS MODAL (for chart1.html / chart2.html)
   ============================================================ */
#charts-modal {{
  display: none; position: fixed; inset: 0; z-index: 500;
  background: rgba(0,0,0,0.9); overflow: hidden;
}}
#charts-modal.open {{ display: flex; flex-direction: column; }}
.charts-modal-header {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; background: var(--bg2); border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}}
.charts-modal-title {{ font-size: 13px; letter-spacing: 3px; text-transform: uppercase; color: var(--gold); }}
.charts-close {{
  background: transparent; border: 1px solid var(--border);
  color: var(--text-dim); font-size: 18px; width: 36px; height: 36px;
  border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
}}
.charts-close:hover {{ border-color: var(--gold-dim); color: var(--gold); }}
.charts-tab-bar {{
  display: flex; background: var(--bg2); border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}}
.charts-tab {{
  flex: 1; padding: 10px; text-align: center; cursor: pointer;
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--text-dim); border-bottom: 2px solid transparent;
  transition: all 0.2s;
}}
.charts-tab.active {{ color: var(--gold); border-bottom-color: var(--gold); }}
.charts-content {{ flex: 1; overflow: hidden; position: relative; }}
.charts-frame {{ position: absolute; inset: 0; display: none; }}
.charts-frame.active {{ display: block; }}
.charts-frame iframe {{ width: 100%; height: 100%; border: none; }}
.charts-zoom-bar {{
  position: absolute; bottom: 16px; right: 16px; z-index: 10;
  display: flex; flex-direction: column; gap: 6px;
}}
.charts-zoom-btn {{
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text-dim); font-size: 20px; width: 40px; height: 40px;
  border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}}
.charts-zoom-btn:hover {{ border-color: var(--gold-dim); color: var(--gold); }}

/* ============================================================
   TOAST
   ============================================================ */
.toast {{
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(20px);
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text); font-size: 13px; padding: 10px 20px;
  border-radius: 20px; opacity: 0; transition: all 0.3s;
  pointer-events: none; z-index: 900; white-space: nowrap;
}}
.toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 480px) {{
  .card-face-title {{ font-size: 20px; }}
  .tab {{ font-size: 9px; letter-spacing: 1px; min-width: 60px; }}
  .thought-comparison {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<!-- SPLASH -->
<div id="splash">
  <div class="splash-diamonds">✦ ✦ ✦</div>
  <div class="splash-title">A Course in Miracles</div>
  <div class="splash-subtitle">Personal Companion</div>
  <div class="splash-today">
    <div class="splash-today-label">Today's Lesson</div>
    <div class="splash-today-lesson" id="splash-lesson-num"></div>
    <div class="splash-today-title" id="splash-lesson-title"></div>
  </div>
  <div class="splash-quote-wrap">
    <div class="splash-quote-label">✦ My Favourite ACIM Daily Quote</div>
    <div id="splash-quote"></div>
    <div id="splash-source"></div>
    <div id="splash-ref-link" style="display:none;margin-top:10px">
      <button onclick="splashGoToRef()" style="background:rgba(201,168,76,0.12);border:1px solid rgba(201,168,76,0.4);color:var(--gold);font-size:11px;letter-spacing:1px;padding:5px 14px;border-radius:20px;cursor:pointer">Read in Reference &#8594;</button>
    </div>
  </div>
  <button class="splash-enter" onclick="closeSplash()">Enter ✦</button>
  <div class="splash-dedication">
    <div class="splash-dedication-names" style="font-style:italic;color:var(--gold)">To Him Who sent me.</div>
    <div class="splash-dedication-names" style="margin-top:10px">Thank you.</div>
  </div>
</div>

<!-- APP -->
<div id="app">
  <div class="app-header">
    <button class="header-btn" onclick="showSplash()" title="Home" style="font-size:16px;padding:6px 12px">⌂</button>
    <div class="header-title">
      <div class="header-title-main">A Course in Miracles</div>
      <div class="header-title-sub">Personal Companion</div>
    </div>
    <div style="width:44px"></div>
  </div>

  <div class="companion-nav">
    <button class="companion-btn" onclick="toggleCompanionMenu()">
      <span id="companion-current">Cards</span>
      <span class="companion-arrow">&#9660;</span>
    </button>
    <div class="companion-overlay" id="companion-overlay" onclick="toggleCompanionMenu()"></div>
    <div class="companion-menu" id="companion-menu">
      <div class="companion-menu-item active" onclick="selectCompanion('cards','Cards')">Cards</div>
      <div class="companion-menu-item" onclick="selectCompanion('library','Workbook Library')">Workbook Library</div>
      <div class="companion-menu-item" onclick="selectCompanion('acim-quotes','ACIM Quotes')">ACIM Quotes</div>
      <div class="companion-menu-item" onclick="selectCompanion('quotes','Quotes')">Quotes</div>
      <div class="companion-menu-item" onclick="selectCompanion('meditations','Meditations')">Meditations</div>
      <div class="companion-menu-item" onclick="selectCompanion('reference','Reference')">Reference</div>
      <div class="companion-menu-item" onclick="selectCompanion('themes','Study Themes')">Study Themes</div>
      <div class="companion-menu-item" onclick="selectCompanion('dedications','Dedications')">Dedications</div>
    </div>
  </div>

  <div class="panels">

    <!-- CARDS PANEL -->
    <div id="panel-cards" class="panel cards-panel active">
      <div class="card-above">
        <div style="width:44px"></div>
        <div class="card-above-info">
          <div class="cf-num" id="cf-num"></div>
          <div class="cf-title" id="cf-title"></div>
        </div>
        <div class="card-counter" id="card-counter"></div>
      </div>
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="card-scene" id="card-scene">
        <div class="card-3d" id="card-3d" onclick="flipCard(event)">
          <div class="card-face">
            <div class="card-face-num" id="cf-num-card"></div>
            <div class="card-face-title" id="cf-title-card"></div>
            <div class="card-face-hint">Tap to reveal your notes</div>
          </div>
          <div class="card-back">
            <div class="card-back-num" id="cb-num"></div>
            <div class="card-back-title" id="cb-title"></div>
            <div class="card-notes" id="cb-notes"></div>
            <textarea class="card-edit-area" id="cb-edit"></textarea>
            <div class="card-actions">
              <button class="btn-action btn-edit" id="cb-btn-edit" onclick="startEditCard(event)">Edit Notes</button>
              <button class="btn-action btn-save" id="cb-btn-save" onclick="saveEditCard(event)" style="display:none">Save</button>
              <button class="btn-action btn-cancel" id="cb-btn-cancel" onclick="cancelEditCard(event)" style="display:none">Cancel</button>
              <button class="btn-action btn-restore" id="cb-btn-restore" onclick="restoreCard(event)" style="display:none">Restore Original</button>
              <a class="btn-action btn-link" id="cb-link" href="#" target="_blank" onclick="event.stopPropagation()">Read on christmind.info ↗</a>
              <a class="btn-action btn-link-secondary" id="cb-bla-link" href="#" target="_blank" onclick="event.stopPropagation()">Read on BLA (FIP) ↗</a>
            </div>
          </div>
        </div>
      </div>
      <div class="card-nav">
        <button class="nav-btn" onclick="prevCard()">&#8592;</button>
        <div class="goto-row">
          <input class="goto-input" id="goto-input" type="number" min="1" max="366" placeholder="Go to">
          <button class="goto-btn" onclick="gotoLesson()">Go</button>
        </div>
        <button class="nav-btn" onclick="nextCard()">&#8594;</button>
      </div>
      <div class="deck-btns">
        <button class="deck-btn" onclick="shuffleDeck()">Shuffle</button>
        <button class="deck-btn" onclick="resetDeck()">Reset Order</button>
        <button class="deck-btn" onclick="openCurrentInLibrary()">Open in Library</button>
      </div>
      <div class="cards-daily-quote" id="cards-daily-quote">
        <div class="cards-daily-quote-label">✦ Quote of the Day</div>
        <div class="cards-daily-quote-text" id="cards-quote-text"></div>
        <div class="cards-daily-quote-source" id="cards-quote-source"></div>
      </div>
    </div>

    <!-- LIBRARY PANEL -->
    <div id="panel-library" class="panel library-panel">
      <div class="library-search">
        <div class="search-wrap">
          <span class="search-icon">&#9906;</span>
          <input class="search-input" id="search-input" type="text" placeholder="Search lessons, notes..." oninput="filterLibrary()">
        </div>
        <div class="filter-row">
          <button class="filter-btn active" onclick="setFilter('all', this)">All 365</button>
          <button class="filter-btn" onclick="setFilter('1-50', this)">1–50</button>
          <button class="filter-btn" onclick="setFilter('51-100', this)">51–100</button>
          <button class="filter-btn" onclick="setFilter('101-150', this)">101–150</button>
          <button class="filter-btn" onclick="setFilter('151-200', this)">151–200</button>
          <button class="filter-btn" onclick="setFilter('201-250', this)">201–250</button>
          <button class="filter-btn" onclick="setFilter('251-300', this)">251–300</button>
          <button class="filter-btn" onclick="setFilter('301-365', this)">301–365</button>
          <button class="filter-btn" onclick="setFilter('notes', this)">Has Notes</button>
          <button class="filter-btn" onclick="setFilter('edited', this)">My Edits</button>
          <button class="filter-btn" onclick="setFilter('starred', this)">&#9733; Starred</button>
        </div>
      </div>
      <div class="results-count" id="results-count"></div>
      <div id="library-list"></div>
    </div>



    <!-- ACIM QUOTES PANEL -->
    <div id="panel-acim-quotes" class="panel quotes-panel">
      <div class="quotes-daily-card">
        <div class="quotes-daily-label">✦ Quote of the Day</div>
        <div class="quotes-daily-diamonds">✦ ✦ ✦</div>
        <div class="quotes-daily-text" id="daily-quote-text"></div>
        <div class="quotes-daily-source" id="daily-quote-source"></div>
      </div>
      <div class="quotes-nav-row">
        <button class="quotes-nav-btn" onclick="prevQuote()">&larr;</button>
        <span class="quotes-counter" id="quotes-counter">1 / 24</span>
        <button class="quotes-nav-btn" onclick="nextQuote()">&rarr;</button>
      </div>
      <div class="quotes-section-title">All Quotes</div>
      <div id="quotes-list"></div>
    </div>

    <!-- PERSONAL QUOTES PANEL -->
    <div id="panel-quotes" class="panel quotes-panel">
      <div class="quotes-section-title" style="margin-bottom:24px">Favourite Quotes</div>
      <div class="personal-quote-item">
        <div class="personal-quote-poem">As swimmers dare<br>to lie face to the sky<br>and water bears them,<br>as hawks rest upon air<br>and air sustains them,<br>so would I learn to attain<br>freefall, and float<br>into Creator Spirit&rsquo;s deep embrace,<br>knowing no effort earns<br>that all-surrounding grace.</div>
        <div class="personal-quote-title">The Avowal</div>
        <div class="personal-quote-author">&mdash; Denise Levertov</div>
      </div>
    </div>

    <!-- MEDITATIONS PANEL -->
    <div id="panel-meditations" class="panel meditations-panel">
      <div id="meditations-list"></div>
    </div>

    <!-- REFERENCE PANEL -->
     <div id="panel-reference" class="panel reference-panel">
      <div id="reference-list"></div>
    </div>

    <!-- STUDY THEMES PANEL -->
    <div id="panel-themes" class="panel reference-panel">
      <div id="themes-list"></div>
    </div>

    <!-- DEDICATIONS PANEL -->
    <div id="panel-dedications" class="panel dedications-panel">
      <div class="dedications-wrap">
        <div class="dedications-diamonds">✦ ✦ ✦</div>
        <div class="dedications-text">To the One Self we all share.</div>
        <div class="dedications-text">To each and every soul that I have met along my journey.</div>
        <div class="dedications-text">To those in every corner of the world who have touched my life.</div>
        <div class="dedications-text">And to those who have not yet crossed paths.</div>
        <div class="dedications-spacer"></div>
        <div class="dedications-names">To my brother JP, my grandparents, P.P. &amp; Jens (two angels), my friends at On Purpose, Sandy Levey-Lund&eacute;n, Clearmind, Duane O&rsquo;Kane, and Sharon.</div>
        <div class="dedications-spacer"></div>
        <div class="dedications-names">To the Circle of Atonement, the Foundation for Inner Peace,<br>and to Helen Schucman and Bill Thetford.</div>
        <div class="dedications-spacer"></div>
        <div class="dedications-highlight">To Him Who sent me.</div>
        <div class="dedications-spacer"></div>
        <div class="dedications-names">Thank you.</div>
        <div class="dedications-spacer"></div>
        <div class="dedications-compiled">Compiled with love by Steven Gauvin</div>
      </div>
    </div>
  </div>
  <div class="app-footer">
    <em>This is for you. Through my darkest days, this material helped me find my way. When I lost faith, it restored it. When I was strong, it made me stronger. When I thought I was alone &mdash; it reminded me that we are not. Years of studying, learning, forgetting, and remembering, distilled into something we can carry in our pocket.</em><br><br><em>I dedicate this to you.</em>
    <span class="app-footer-name">&mdash; Steven Gauvin, Copenhagen</span>
  </div>
</div>

<!-- CHARTS MODAL (chart1.html / chart2.html with zoom) -->
<div id="charts-modal">
  <div class="charts-modal-header">
    <div class="charts-modal-title">Reference Charts</div>
    <button class="charts-close" onclick="closeCharts()">&#10005;</button>
  </div>
  <div class="charts-tab-bar">
    <div class="charts-tab active" onclick="switchChartTab(0, this)">Map of the Mind</div>
    <div class="charts-tab" onclick="switchChartTab(1, this)">Key Teachings</div>
  </div>
  <div class="charts-content">
    <div class="charts-frame active" id="cframe-0">
      <iframe src="chart1.html" id="ciframe-0"></iframe>
    </div>
    <div class="charts-frame" id="cframe-1">
      <iframe src="chart2.html" id="ciframe-1"></iframe>
    </div>
    <div class="charts-zoom-bar">
      <button class="charts-zoom-btn" onclick="zoomChart(1.25)" title="Zoom in">+</button>
      <button class="charts-zoom-btn" onclick="zoomChart(1/1.25)" title="Zoom out">−</button>
      <button class="charts-zoom-btn" onclick="resetChartZoom()" title="Reset" style="font-size:13px">↺</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
// ============================================================
// DATA
// ============================================================
const LESSONS = {lessons_json};
const QUOTES = {quotes_json};
const REVIEW_MAP = {review_map_json};
const SG_DATA = {sg_json};
const PART2 = {part2_json};
const MEDITATIONS = {meditations_json};
const PRINCIPLES = {principles_json};
const RULES = {rules_json};
const CAUSE_EFFECT = {cause_effect_json};
const STORAGE_KEY = 'acim_notes_v3';
const STARS_KEY = 'acim_stars_v1';

// Photo charts (base64 embedded) - only keeping the ones not yet rebuilt as HTML
const PHOTO_CHARTS = [
  {{ id: 'heaven', title: 'Heaven is the Decision I Must Make', credit: 'ACIM — Workbook Lesson 138 — Michael Dawson, 1993', src: '{img_heaven}' }},
];

// ============================================================
// STATE
// ============================================================
let deck = LESSONS.map((_, i) => i);
let currentIdx = 0;
let isFlipped = false;
let isEditing = false;
let activeFilter = 'all';
let searchQuery = '';
let touchStartX = 0, touchStartY = 0;
let currentQuoteIdx = 0;
let activeChartIdx = 0;
let jumpedFromReview = null;  // tracks which review lesson we jumped from
let chartZoom = 1.0;

// ============================================================
// STORAGE
// ============================================================
function loadNotes() {{
  try {{ return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {{}}; }}
  catch(e) {{ return {{}}; }}
}}
function saveNotes(notes) {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(notes)); }}
function getNoteForLesson(num) {{
  const notes = loadNotes();
  return notes[num] !== undefined ? notes[num] : null;
}}
function setNoteForLesson(num, text) {{
  const notes = loadNotes();
  notes[num] = text;
  saveNotes(notes);
}}
function deleteNoteForLesson(num) {{
  const notes = loadNotes();
  delete notes[num];
  saveNotes(notes);
}}

function loadStars() {{
  try {{ return JSON.parse(localStorage.getItem(STARS_KEY)) || {{}}; }}
  catch(e) {{ return {{}}; }}
}}
function toggleStar(num) {{
  const stars = loadStars();
  if (stars[num]) {{ delete stars[num]; }} else {{ stars[num] = true; }}
  localStorage.setItem(STARS_KEY, JSON.stringify(stars));
}}
function isStarred(num) {{
  return !!loadStars()[num];
}}

// ============================================================
// TABS
// ============================================================
function switchTab(name) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  // Update companion menu active state
  document.querySelectorAll('.companion-menu-item').forEach(item => {{
    const itemName = item.getAttribute('onclick').match(/selectCompanion\('([^']+)'/)?.[1];
    item.classList.toggle('active', itemName === name);
  }});
  if (name === 'library') {{ renderLibrary(); scrollToTodayLesson(); }}
  if (name === 'acim-quotes') renderQuotes();
  if (name === 'meditations') renderMeditations();
  if (name === 'reference') renderReference();
  if (name === 'themes') renderThemes();
}}

function toggleCompanionMenu() {{
  const btn = document.querySelector('.companion-btn');
  const menu = document.getElementById('companion-menu');
  const overlay = document.getElementById('companion-overlay');
  const isOpen = menu.classList.contains('open');
  btn.classList.toggle('open', !isOpen);
  menu.classList.toggle('open', !isOpen);
  overlay.classList.toggle('open', !isOpen);
}}

function selectCompanion(name, label) {{
  document.getElementById('companion-current').textContent = label;
  toggleCompanionMenu();
  switchTab(name);
}}

// ============================================================
// SPLASH
// ============================================================
function getDayOfYear() {{
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  return Math.floor((now - start) / 86400000);
}}

function initSplash() {{
  const day = getDayOfYear();
  const qIdx = day % QUOTES.length;
  currentQuoteIdx = qIdx;
  document.getElementById('splash-quote').textContent = QUOTES[qIdx].text;
  document.getElementById('splash-source').textContent = QUOTES[qIdx].source;
  const splashRefEl = document.getElementById('splash-ref-link');
  if (QUOTES[qIdx].ref_link) {{
    splashRefEl.style.display = 'block';
    splashRefEl.dataset.target = QUOTES[qIdx].ref_link;
  }} else {{
    splashRefEl.style.display = 'none';
  }}
  const lessonNum = ((day - 1) % 365) + 1;
  const lesson = LESSONS.find(l => l.num === lessonNum) || LESSONS[0];
  const splashReviewInfo = REVIEW_MAP[lesson.num];
  const splashNumLabel = splashReviewInfo ? 'Lesson ' + lesson.num + ' \u2014 ' + splashReviewInfo.name : 'Lesson ' + lesson.num;
  document.getElementById('splash-lesson-num').textContent = splashNumLabel;
  const splashTitleEl = document.getElementById('splash-lesson-title');
  if (splashReviewInfo && lesson.title.includes(' / ')) {{
    const splashParts = lesson.title.split(' / ');
    splashTitleEl.innerHTML = splashParts[0] + '<br>' + splashParts[1];
  }} else {{
    splashTitleEl.textContent = lesson.title;
  }}
  // Also populate the daily quote on the Cards tab
  document.getElementById('cards-quote-text').textContent = QUOTES[qIdx].text;
  document.getElementById('cards-quote-source').textContent = QUOTES[qIdx].source;
}}

function splashGoToRef() {{
  const el = document.getElementById('splash-ref-link');
  const target = el.dataset.target;
  closeSplash();
  setTimeout(() => {{
    document.getElementById('companion-current').textContent = 'Reference';
    switchTab('reference');
    setTimeout(() => {{
      const sec = document.getElementById(target);
      if (sec) {{
        sec.classList.add('open');
        sec.scrollIntoView({{behavior:'smooth', block:'start'}});
      }}
    }}, 300);
  }}, 900);
}}

function showSplash() {{
  const splash = document.getElementById('splash');
  splash.style.display = 'flex';
  splash.classList.remove('hidden');
}}
function closeSplash() {{
  const splash = document.getElementById('splash');
  splash.classList.add('hidden');
  // Navigate to today's lesson
  const day = getDayOfYear();
  const lessonNum = ((day - 1) % 365) + 1;
  const idx = deck.indexOf(LESSONS.findIndex(l => l.num === lessonNum));
  if (idx >= 0) {{ currentIdx = idx; }}
  // Wait for splash fade to finish before rendering card so layout is computed correctly
  setTimeout(() => {{
    splash.style.display = 'none';
    renderCard();
    // Force a second render after a brief delay to fix iOS layout quirks
    requestAnimationFrame(() => renderCard());
  }}, 850);
}}

// ============================================================
// CARDS
// ============================================================
function getCurrentLesson() {{ return LESSONS[deck[currentIdx]]; }}

function renderCard() {{
  const l = getCurrentLesson();
  const saved = getNoteForLesson(l.num);
  const notes = saved !== null ? saved : l.notes;
  const isEdited = saved !== null;
  const isSpecial = l.num === 366;
  const reviewInfo = REVIEW_MAP[l.num];
  const isReview = !!reviewInfo;

  // Build num label
  let numLabel;
  if (isSpecial) {{ numLabel = '✦ COMPLETION ✦'; }}
  else if (isReview) {{ numLabel = 'LESSON ' + l.num + ' \u2014 ' + reviewInfo.name.toUpperCase(); }}
  else {{ numLabel = 'LESSON ' + l.num; }}

  // Build title HTML — split review lessons onto two lines (same size/colour)
  let titleHtml;
  if (isReview && l.title.includes(' / ')) {{
    const parts = l.title.split(' / ');
    titleHtml = escHtml(parts[0]) + '<br>' + escHtml(parts[1]);
  }} else {{
    titleHtml = escHtml(l.title);
  }}

  document.getElementById('cf-num').textContent = numLabel;
  document.getElementById('cf-title').innerHTML = titleHtml;
  document.getElementById('cf-num-card').textContent = numLabel;
  document.getElementById('cf-title-card').innerHTML = titleHtml;
  document.getElementById('cb-num').textContent = numLabel;
  document.getElementById('cb-title').innerHTML = titleHtml;

  // Special card styling
  const card3d = document.getElementById('card-3d');
  if (isSpecial) {{ card3d.classList.add('special-card'); }} else {{ card3d.classList.remove('special-card'); }}

  const notesEl = document.getElementById('cb-notes');
  notesEl.textContent = notes;
  notesEl.className = 'card-notes' + (isEdited ? ' edited' : '');

  document.getElementById('cb-link').href = l.url;
  document.getElementById('cb-bla-link').href = l.bla_url || '#';
  // Hide external links for special card
  document.getElementById('cb-link').style.display = isSpecial ? 'none' : '';
  document.getElementById('cb-bla-link').style.display = isSpecial ? 'none' : '';
  document.getElementById('card-counter').textContent = (currentIdx + 1) + ' / ' + deck.length;

  const fill = ((currentIdx + 1) / deck.length * 100).toFixed(1);
  document.getElementById('progress-fill').style.width = fill + '%';
  document.getElementById('cb-btn-restore').style.display = isEdited ? 'inline-block' : 'none';
  cancelEditCard(null, true);
}}

function flipCard(e) {{
  if (isEditing) return;
  isFlipped = !isFlipped;
  document.getElementById('card-3d').classList.toggle('flipped', isFlipped);
}}

function nextCard() {{
  if (isEditing) return;
  if (currentIdx < deck.length - 1) {{
    currentIdx++; isFlipped = false;
    document.getElementById('card-3d').classList.remove('flipped');
    renderCard();
  }}
}}

function prevCard() {{
  if (isEditing) return;
  if (currentIdx > 0) {{
    currentIdx--; isFlipped = false;
    document.getElementById('card-3d').classList.remove('flipped');
    renderCard();
  }}
}}

function gotoLesson() {{
  const val = parseInt(document.getElementById('goto-input').value);
  if (isNaN(val) || val < 1 || val > 366) {{ showToast('Enter a number 1–366'); return; }}
  const idx = deck.findIndex(i => LESSONS[i].num === val);
  if (idx === -1) {{ showToast('Lesson ' + val + ' not in current deck'); return; }}
  currentIdx = idx; isFlipped = false;
  document.getElementById('card-3d').classList.remove('flipped');
  renderCard();
  document.getElementById('goto-input').value = '';
}}

function shuffleDeck() {{
  for (let i = deck.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }}
  currentIdx = 0; isFlipped = false;
  document.getElementById('card-3d').classList.remove('flipped');
  renderCard(); showToast('Deck shuffled');
}}

function resetDeck() {{
  deck = LESSONS.map((_, i) => i);
  currentIdx = 0; isFlipped = false;
  document.getElementById('card-3d').classList.remove('flipped');
  renderCard(); showToast('Deck reset to lesson order');
}}

function startEditCard(e) {{
  e.stopPropagation(); isEditing = true;
  const l = getCurrentLesson();
  const saved = getNoteForLesson(l.num);
  const notes = saved !== null ? saved : l.notes;
  const editArea = document.getElementById('cb-edit');
  editArea.value = notes; editArea.style.display = 'block';
  document.getElementById('cb-notes').style.display = 'none';
  document.getElementById('cb-btn-edit').style.display = 'none';
  document.getElementById('cb-btn-save').style.display = 'inline-block';
  document.getElementById('cb-btn-cancel').style.display = 'inline-block';
  document.getElementById('cb-btn-restore').style.display = 'none';
  editArea.focus();
}}

function saveEditCard(e) {{
  e.stopPropagation();
  const l = getCurrentLesson();
  const text = document.getElementById('cb-edit').value;
  setNoteForLesson(l.num, text);
  isEditing = false; renderCard(); showToast('Notes saved');
}}

function cancelEditCard(e, silent) {{
  if (e) e.stopPropagation();
  isEditing = false;
  document.getElementById('cb-edit').style.display = 'none';
  document.getElementById('cb-notes').style.display = 'block';
  document.getElementById('cb-btn-edit').style.display = 'inline-block';
  document.getElementById('cb-btn-save').style.display = 'none';
  document.getElementById('cb-btn-cancel').style.display = 'none';
}}

function restoreCard(e) {{
  e.stopPropagation();
  const l = getCurrentLesson();
  if (confirm('Restore original notes for Lesson ' + l.num + '?')) {{
    deleteNoteForLesson(l.num); renderCard(); showToast('Original notes restored');
  }}
}}

// Swipe
const scene = document.getElementById('card-scene');
scene.addEventListener('touchstart', e => {{
  touchStartX = e.touches[0].clientX; touchStartY = e.touches[0].clientY;
}}, {{passive: true}});
scene.addEventListener('touchend', e => {{
  if (isEditing) return;
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {{
    if (dx < 0) nextCard(); else prevCard();
  }}
}}, {{passive: true}});

// ============================================================
// LIBRARY
// ============================================================
function setFilter(f, el) {{
  activeFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  renderLibrary();
}}

function filterLibrary() {{
  searchQuery = document.getElementById('search-input').value.toLowerCase();
  renderLibrary();
}}

function getDisplayNotes(lesson) {{
  const saved = getNoteForLesson(lesson.num);
  return {{ text: saved !== null ? saved : lesson.notes, isEdited: saved !== null }};
}}

function renderLibrary() {{
  const list = document.getElementById('library-list');
  const query = searchQuery;
  const stars = loadStars();

  let filtered = LESSONS.filter(l => {{
    if (activeFilter === 'notes') {{
      if (!l.notes && getNoteForLesson(l.num) === null) return false;
    }} else if (activeFilter === 'edited') {{
      if (getNoteForLesson(l.num) === null) return false;
    }} else if (activeFilter === 'starred') {{
      if (!stars[l.num]) return false;
    }} else if (activeFilter !== 'all') {{
      const [lo, hi] = activeFilter.split('-').map(Number);
      if (l.num < lo || l.num > hi) return false;
    }}
    if (query) {{
      const {{ text }} = getDisplayNotes(l);
      const haystack = ('lesson ' + l.num + ' ' + l.title + ' ' + text).toLowerCase();
      if (!haystack.includes(query)) return false;
    }}
    return true;
  }});

  document.getElementById('results-count').textContent = filtered.length + ' lesson' + (filtered.length !== 1 ? 's' : '');

   // Part II intro card HTML — injected inline before lesson 221
  const part2IntroCardHtml = `
    <div class="part2-intro-card" id="part2-intro-card">
      <div class="part2-intro-card-title">✦ Part II — Lessons 221–365</div>
      <div class="part2-intro-card-subtitle">"What Is" sections and general practice instructions</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:4px">
        <button class="part2-intro-btn" onclick="togglePart2Section('intro', event)">▶ Introduction to Part II</button>
        <button class="part2-intro-btn" onclick="togglePart2Section('practice', event)">▶ Practice Instructions</button>
      </div>
      <div class="part2-intro-content" id="part2-section-intro">${{escHtml(PART2.intro.text)}}</div>
      <div class="part2-intro-content" id="part2-section-practice">${{escHtml(PART2.practice_instructions.text)}}</div>
    </div>`;
  list.innerHTML = filtered.map((l, idx) => {{
    const {{ text: notes, isEdited }} = getDisplayNotes(l);
    const starred = isStarred(l.num);
    const escRe = (s) => s.replace(/[.*+?^$|()[\\]\\\\]/g, '\\\\$&');
    const hl = (str) => query ? str.replace(new RegExp(escRe(query), 'gi'), m => '<mark class="highlight">' + m + '</mark>') : str;
    // Inject Part II divider + intro card before lesson 221
    const prevLesson = idx > 0 ? filtered[idx - 1] : null;
    const injectPart2Header = l.num === 221 || (l.num > 221 && l.num <= 365 && (!prevLesson || prevLesson.num < 221));
    const part2HeaderHtml = injectPart2Header ? `
      <div class="part2-divider">
        <span class="part2-divider-label">PART II — LESSONS 221–365</span>
      </div>
      ${{part2IntroCardHtml}}` : '';
    const notesHtml = notes ? '<div class="lesson-notes-text' + (isEdited ? ' edited' : '') + '">' + hl(escHtml(notes)) + '</div>' : '';
    const sgId = 'sg-' + l.num;
    const sgBodyId = 'sgb-' + l.num;
    const sgData = SG_DATA[l.num];
    let sgHtml = '';
    if (sgData && sgData.parts && sgData.parts.length > 0) {{
      const partsHtml = sgData.parts.map(p => {{
        let rendered = escHtml(p.text);
        // Replace "See review X practice instructions on page Y" with clickable link
        rendered = rendered.replace(
          /See (review \w+) practice instructions on page \d+[-.]?/i,
          (match, revName) => {{
            return `<a href="#" class="sg-review-link" onclick="event.preventDefault();event.stopPropagation();toggleReviewIntro(${{l.num}}, event)" style="color:var(--gold);text-decoration:underline;cursor:pointer">\u25b6 See ${{revName.charAt(0).toUpperCase() + revName.slice(1)}} Practice Instructions</a>`;
          }}
        );
        // Replace "See complete instructions on page X" with clickable Part II link
        rendered = rendered.replace(
          /See complete instructions on page (\d+)\./i,
          (match, pg) => {{
            return `<a href="#" class="sg-review-link" onclick="event.preventDefault();event.stopPropagation();scrollToPart2Intro('practice', event)" style="color:var(--gold);text-decoration:underline;cursor:pointer">▶ See Part II Practice Instructions</a>`;
          }}
        );
        return `
        <div class="sg-section">
          ${{p.label ? '<div class="sg-section-label">' + escHtml(p.label) + '</div>' : ''}}
          <div class="sg-section-text">${{rendered}}</div>
        </div>`;
      }}).join('');
      const blaLink = sgData.bla_url ? `<a class="btn-action btn-link-secondary" href="${{escHtml(sgData.bla_url)}}" target="_blank" style="font-size:10px;margin-bottom:12px;display:inline-block">Read on BLA (FIP) ↗</a>` : '';
      sgHtml = `
        <button class="sg-toggle-btn" id="${{sgId}}" onclick="toggleSG(${{l.num}}, event)">
          <span>▼ Commentary by Dee Doyle & Allen Watson</span><span></span>
        </button>
        <div class="sg-body" id="${{sgBodyId}}">
          ${{blaLink}}
          ${{partsHtml}}
          <div style="font-size:9px;color:var(--text-dim);text-align:center;margin-top:12px;letter-spacing:0.5px;opacity:0.7">Special thanks to the Circle of Atonement</div>
        </div>`;
    }}
    const isSpecialLib = l.num === 366;
    const isPart2 = l.num >= 221 && l.num <= 365;
    const whatIsKey = isPart2 ? PART2.lesson_to_whatis[l.num] : null;
    const whatIsSection = whatIsKey ? PART2.whatis_sections[whatIsKey] : null;
    return part2HeaderHtml + `<div class="lesson-item${{isEdited ? ' has-edit' : ''}}${{starred ? ' starred' : ''}}${{isSpecialLib ? ' special-lesson' : ''}}" id="lib-${{l.num}}">
      <div class="lesson-header" onclick="toggleLesson(${{l.num}})">
        <span class="lesson-num-badge">${{isSpecialLib ? '\u2726' : l.num}}</span>
        ${{REVIEW_MAP[l.num] ? '<span class="review-badge">' + REVIEW_MAP[l.num].name + '</span>' : ''}}
        <span class="lesson-title-text">${{hl(escHtml(l.title))}}</span>
        <span style="color:var(--gold);font-size:14px;margin-right:4px;cursor:pointer" onclick="starLesson(${{l.num}},event)">${{starred ? '★' : '☆'}}</span>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="lesson-body">
        <div class="back-to-review-breadcrumb" id="breadcrumb-${{l.num}}" style="display:none"></div>
        ${{REVIEW_MAP[l.num] ? `
          <button class="review-intro-btn" onclick="toggleReviewIntro(${{l.num}}, event)">
            ▶ ${{REVIEW_MAP[l.num].name}} Introduction
          </button>
          <div class="review-intro-content" id="rev-intro-${{l.num}}">${{escHtml(REVIEW_MAP[l.num].instructions)}}</div>
          <div class="review-refs">
            <div class="review-refs-title">Reviewing Lessons</div>
            ${{REVIEW_MAP[l.num].reviewed.map(n => '<span class="review-ref-link" onclick="jumpToLesson(' + n + ', event, ' + l.num + ')">' + n + '. ' + escHtml((LESSONS.find(x => x.num === n) || {{}}).title || '') + '</span>').join('')}}
          </div>` : ''}}
        ${{isPart2 && whatIsSection ? `
          <div class="part2-section-header">✦ ${{escHtml(whatIsSection.title)}}</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px">
            <button class="part2-intro-btn" onclick="togglePart2WhatIsText(${{l.num}}, event)">▶ Workbook Text</button>
            <button class="part2-intro-btn" onclick="togglePart2WhatIs(${{l.num}}, event)">▶ Read Commentary</button>
            <button class="part2-intro-btn" id="pi-btn-${{l.num}}" onclick="togglePart2PI(${{l.num}}, event)">▶ Practice Instructions</button>
          </div>
          <div class="part2-intro-content" id="whatis-wb-${{l.num}}">${{escHtml(whatIsSection.workbook_text || '')}}</div>
          <div class="part2-intro-content" id="whatis-${{l.num}}">${{escHtml(whatIsSection.text)}}</div>
          <div class="part2-intro-content" id="pi-${{l.num}}"></div>` : ''}}
        ${{notesHtml}}
        <textarea class="lesson-edit-area" id="lib-edit-${{l.num}}" placeholder="Write your notes here…"></textarea>
        <div class="lesson-actions">
          <button class="btn-action btn-edit" onclick="startEditLib(${{l.num}}, event)">Edit Notes</button>
          <button class="btn-action btn-save" id="lib-save-${{l.num}}" onclick="saveEditLib(${{l.num}}, event)" style="display:none">Save</button>
          <button class="btn-action btn-cancel" id="lib-cancel-${{l.num}}" onclick="cancelEditLib(${{l.num}}, event)" style="display:none">Cancel</button>
          ${{isEdited ? `<button class="btn-action btn-restore" onclick="restoreLib(${{l.num}}, event)">Restore Original</button>` : ''}}
          ${{isSpecialLib ? '' : `<a class="btn-action btn-link" href="${{l.url}}" target="_blank" onclick="event.stopPropagation()">Read on christmind.info ↗</a>`}}
          ${{isSpecialLib ? '' : `<a class="btn-action btn-link-secondary" href="${{l.bla_url || '#'}}" target="_blank" onclick="event.stopPropagation()">Read on BLA (FIP) ↗</a>`}}
          <button class="btn-action btn-edit" onclick="openAsCard(${{l.num}})">Open as Card</button>
        </div>
        ${{sgHtml}}
      </div>
    </div>`;
  }}).join('');
}}

function toggleLesson(num) {{
  document.getElementById('lib-' + num).classList.toggle('expanded');
}}

function starLesson(num, e) {{
  e.stopPropagation();
  toggleStar(num);
  renderLibrary();
  setTimeout(() => {{
    const el = document.getElementById('lib-' + num);
    if (el) el.classList.add('expanded');
  }}, 50);
}}

function toggleSG(num, e) {{
  e.stopPropagation();
  const btn = document.getElementById('sg-' + num);
  const body = document.getElementById('sgb-' + num);
  const isOpen = body.classList.contains('open');
  body.classList.toggle('open', !isOpen);
  btn.classList.toggle('open', !isOpen);
  btn.querySelector('span').textContent = isOpen ? '▼ Commentary by Dee Doyle & Allen Watson' : '▲ Commentary by Dee Doyle & Allen Watson';
}}

function startEditLib(num, e) {{
  e.stopPropagation();
  const {{ text }} = getDisplayNotes(LESSONS.find(l => l.num === num));
  const area = document.getElementById('lib-edit-' + num);
  area.value = text; area.style.display = 'block';
  const item = document.getElementById('lib-' + num);
  const notesEl = item.querySelector('.lesson-notes-text');
  if (notesEl) notesEl.style.display = 'none';
  document.getElementById('lib-save-' + num).style.display = 'inline-block';
  document.getElementById('lib-cancel-' + num).style.display = 'inline-block';
  area.focus();
}}

function saveEditLib(num, e) {{
  e.stopPropagation();
  const text = document.getElementById('lib-edit-' + num).value;
  setNoteForLesson(num, text);
  renderLibrary();
  setTimeout(() => {{
    const el = document.getElementById('lib-' + num);
    if (el) el.classList.add('expanded');
  }}, 50);
  showToast('Notes saved');
}}

function cancelEditLib(num, e) {{
  e.stopPropagation();
  renderLibrary();
  setTimeout(() => {{
    const el = document.getElementById('lib-' + num);
    if (el) el.classList.add('expanded');
  }}, 50);
}}

function restoreLib(num, e) {{
  e.stopPropagation();
  if (confirm('Restore original notes for Lesson ' + num + '?')) {{
    deleteNoteForLesson(num); renderLibrary(); showToast('Original notes restored');
  }}
}}

function openAsCard(num) {{
  const idx = LESSONS.findIndex(l => l.num === num);
  if (idx === -1) return;
  deck = LESSONS.map((_, i) => i);
  currentIdx = idx; isFlipped = false;
  renderCard();
  document.getElementById('companion-current').textContent = 'Cards';
  switchTab('cards');
}}

function openCurrentInLibrary() {{
  const l = getCurrentLesson();
  deck = LESSONS.map((_, i) => i);
  document.getElementById('companion-current').textContent = 'WB Library';
  switchTab('library');
  setTimeout(() => {{
    const el = document.getElementById('lib-' + l.num);
    if (el) {{ el.scrollIntoView({{behavior:'smooth', block:'center'}}); el.classList.add('expanded'); }}
  }}, 200);
}}

function scrollToTodayLesson() {{
  const day = getDayOfYear();
  const lessonNum = ((day - 1) % 365) + 1;
  setTimeout(() => {{
    const el = document.getElementById('lib-' + lessonNum);
    if (el) {{
      el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
      // Briefly highlight so it's easy to spot
      el.style.transition = 'box-shadow 0.4s';
      el.style.boxShadow = '0 0 0 2px var(--gold)';
      setTimeout(() => {{ el.style.boxShadow = ''; }}, 2000);
    }}
  }}, 250);
}}

// ============================================================


function toggleReviewIntro(num, e) {{
  e.stopPropagation();
  const el = document.getElementById('rev-intro-' + num);
  const btn = el.previousElementSibling;
  el.classList.toggle('open');
  btn.textContent = el.classList.contains('open')
    ? '▼ ' + REVIEW_MAP[num].name + ' Introduction'
    : '▶ ' + REVIEW_MAP[num].name + ' Introduction';
}}

function togglePart2Section(section, e) {{
  if (e) e.stopPropagation();
  const el = document.getElementById('part2-section-' + section);
  if (!el) return;
  const btn = e && e.target ? e.target : null;
  const isOpen = el.classList.contains('open');
  el.classList.toggle('open', !isOpen);
  if (btn) {{
    const label = section === 'intro' ? 'Introduction to Part II' : 'Practice Instructions';
    btn.textContent = (isOpen ? '▶ ' : '▼ ') + label;
  }}
}}

function togglePart2WhatIs(num, e) {{
  if (e) e.stopPropagation();
  const el = document.getElementById('whatis-' + num);
  if (!el) return;
  const btn = e && e.target ? e.target : null;
  const isOpen = el.classList.contains('open');
  el.classList.toggle('open', !isOpen);
  if (btn) btn.textContent = isOpen ? '▶ Read Commentary' : '▼ Read Commentary';
}}
function togglePart2WhatIsText(num, e) {{
  if (e) e.stopPropagation();
  const el = document.getElementById('whatis-wb-' + num);
  if (!el) return;
  const btn = e && e.target ? e.target : null;
  const isOpen = el.classList.contains('open');
  el.classList.toggle('open', !isOpen);
  if (btn) btn.textContent = isOpen ? '▶ Workbook Text' : '▼ Workbook Text';
}}

function togglePart2PI(num, e) {{
  if (e) e.stopPropagation();
  const el = document.getElementById('pi-' + num);
  if (!el) return;
  const btn = document.getElementById('pi-btn-' + num);
  const isOpen = el.classList.contains('open');
  if (!isOpen && !el.dataset.loaded) {{
    el.textContent = PART2.practice_instructions.text;
    el.dataset.loaded = '1';
  }}
  el.classList.toggle('open', !isOpen);
  if (btn) btn.textContent = isOpen ? '▶ Practice Instructions' : '▼ Practice Instructions';
}}

function scrollToPart2Intro(section, e) {{
  if (e) e.stopPropagation();
  // Switch to library tab if not already there
  switchTab('library');
  // Scroll to the Part II intro card and open the section
  setTimeout(() => {{
    const card = document.getElementById('part2-intro-card');
    if (card) {{
      card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      // Open the section
      const el = document.getElementById('part2-section-' + section);
      if (el && !el.classList.contains('open')) {{
        el.classList.add('open');
        // Update button text
        const btns = card.querySelectorAll('.part2-intro-btn');
        btns.forEach(b => {{
          if (section === 'intro' && b.textContent.includes('Introduction')) b.textContent = '▼ Introduction to Part II';
          if (section === 'practice' && b.textContent.includes('Practice')) b.textContent = '▼ Practice Instructions';
        }});
      }}
    }}
  }}, 300);
}}

function jumpToLesson(num, e, fromReviewNum) {{
  if (e) e.stopPropagation();
  jumpedFromReview = fromReviewNum || null;
  // Figure out which filter range this lesson belongs to
  let targetFilter = 'all';
  if (num >= 1 && num <= 50) targetFilter = '1-50';
  else if (num >= 51 && num <= 100) targetFilter = '51-100';
  else if (num >= 101 && num <= 150) targetFilter = '101-150';
  else if (num >= 151 && num <= 200) targetFilter = '151-200';
  else if (num >= 201 && num <= 250) targetFilter = '201-250';
  else if (num >= 251 && num <= 300) targetFilter = '251-300';
  else if (num >= 301 && num <= 365) targetFilter = '301-365';
  // Switch filter if needed
  activeFilter = targetFilter;
  document.querySelectorAll('.filter-btn').forEach(b => {{
    b.classList.remove('active');
    const btnNorm = b.textContent.trim().replace('\u2013', '-');
    if (btnNorm.includes(targetFilter) ||
        (targetFilter === 'all' && btnNorm.includes('All'))) {{
      b.classList.add('active');
    }}
  }});
  renderLibrary();
  // After render, scroll to and expand the target lesson
  setTimeout(() => {{
    const el = document.getElementById('lib-' + num);
    if (el) {{
      el.classList.add('expanded');
      el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      // Brief highlight
      el.style.boxShadow = '0 0 12px var(--gold)';
      setTimeout(() => el.style.boxShadow = '', 2000);
      // Show breadcrumb if we came from a review lesson
      if (jumpedFromReview) {{
        const bc = document.getElementById('breadcrumb-' + num);
        if (bc) {{
          const revLesson = LESSONS.find(x => x.num === jumpedFromReview);
          const revName = REVIEW_MAP[jumpedFromReview] ? REVIEW_MAP[jumpedFromReview].name : 'Review';
          bc.innerHTML = '<button class="back-to-review-btn" data-review-num="' + jumpedFromReview + '">← Back to Lesson ' + jumpedFromReview + ' (' + revName + ')</button>';
          bc.style.display = 'block';
        }}
      }}
    }}
  }}, 100);
}}

function jumpBackToReview(num) {{
  jumpedFromReview = null;
  // Directly do the jump instead of calling jumpToLesson which needs a real event
  let targetFilter = 'all';
  if (num >= 1 && num <= 50) targetFilter = '1-50';
  else if (num >= 51 && num <= 100) targetFilter = '51-100';
  else if (num >= 101 && num <= 150) targetFilter = '101-150';
  else if (num >= 151 && num <= 200) targetFilter = '151-200';
  else if (num >= 201 && num <= 250) targetFilter = '201-250';
  else if (num >= 251 && num <= 300) targetFilter = '251-300';
  else if (num >= 301 && num <= 365) targetFilter = '301-365';
  activeFilter = targetFilter;
  document.querySelectorAll('.filter-btn').forEach(b => {{
    b.classList.remove('active');
    const btnNorm = b.textContent.trim().replace('\u2013', '-');
    if (btnNorm.includes(targetFilter) ||
        (targetFilter === 'all' && btnNorm.includes('All'))) {{
      b.classList.add('active');
    }}
  }});
  renderLibrary();
  setTimeout(() => {{
    const el = document.getElementById('lib-' + num);
    if (el) {{
      el.classList.add('expanded');
      el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      el.style.boxShadow = '0 0 12px var(--gold)';
      setTimeout(() => el.style.boxShadow = '', 2000);
    }}
  }}, 100);
}}

// ============================================================
// QUOTES
// ============================================================
function renderQuotes() {{
  document.getElementById('daily-quote-text').textContent = QUOTES[currentQuoteIdx].text;
  document.getElementById('daily-quote-source').textContent = QUOTES[currentQuoteIdx].source;
  document.getElementById('quotes-counter').textContent = (currentQuoteIdx + 1) + ' / ' + QUOTES.length;
  const list = document.getElementById('quotes-list');
  list.innerHTML = QUOTES.map((q, i) => `
    <div class="quote-item ${{i === currentQuoteIdx ? 'active-quote' : ''}}" onclick="selectQuote(${{i}})" id="qi-${{i}}">
      <div class="quote-item-text">${{escHtml(q.text)}}</div>
      <div class="quote-item-source">${{escHtml(q.source)}}</div>
    </div>`).join('');
}}

function selectQuote(idx) {{
  currentQuoteIdx = idx; renderQuotes();
  document.querySelector('.quotes-daily-card').scrollIntoView({{behavior: 'smooth', block: 'start'}});
}}
function prevQuote() {{ currentQuoteIdx = (currentQuoteIdx - 1 + QUOTES.length) % QUOTES.length; renderQuotes(); }}
function nextQuote() {{ currentQuoteIdx = (currentQuoteIdx + 1) % QUOTES.length; renderQuotes(); }}

// ============================================================
// MEDITATIONS
// ============================================================
function renderMeditations() {{
  const list = document.getElementById('meditations-list');
  if (list.innerHTML) return;
  list.innerHTML = MEDITATIONS.map((m, i) => {{
    const sectionsHtml = m.sections.map(s => `
      <div class="med-section">
        ${{s.heading ? '<div class="med-section-heading">' + escHtml(s.heading) + '</div>' : ''}}
        <div class="med-text">${{escHtml(s.text)}}</div>
      </div>`).join('');
    return `<div class="med-card" id="med-${{i}}">
      <div class="med-header" onclick="toggleMed(${{i}})">
        <div>
          <div class="med-title">${{escHtml(m.title)}}</div>
          <div class="med-subtitle">${{escHtml(m.subtitle)}}</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="med-body">${{sectionsHtml}}</div>
    </div>`;
  }}).join('');
}}

function toggleMed(i) {{ document.getElementById('med-' + i).classList.toggle('expanded'); }}

// ============================================================
// REFERENCE
// ============================================================
function renderReference() {{
  const list = document.getElementById('reference-list');
  if (list.innerHTML) return;

  // Principles of Miracles
  const principlesHtml = PRINCIPLES.map(p => `
    <div class="principle-item">
      <div class="principle-num">${{p.num}}</div>
      <div class="principle-text">${{escHtml(p.text)}}</div>
    </div>`).join('');

  // Rules for Decision — full expandable version
  const rulesHtml = `
  <div style="font-size:13px;color:var(--text-main);line-height:1.7">

    <!-- Opening paragraph -->
    <div style="background:rgba(201,168,76,0.07);border-left:3px solid var(--gold);padding:12px 14px;border-radius:0 8px 8px 0;margin-bottom:18px;font-style:italic;color:var(--text-dim)">
      Decisions are continuous. You do not always know when you are making them. But with a little practice
      with the ones you recognize, a set begins to form which sees you through the rest. It is not wise to let
      yourself become preoccupied with every step you take. The proper set, adopted consciously each time you
      wake, will put you well ahead. And if you find resistance strong and dedication weak, you are not ready.
      Do not fight yourself. But think about the kind of day you want, and tell yourself there is a way in which
      this very day can happen just like that. Then try again to have the day you want.
    </div>

    <!-- Rule 1 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">1</div>
        <div class="rfd-summary">
          <div class="rfd-label">The outlook starts with this:</div>
          <div class="rfd-phrase">&ldquo;Today I will make no decisions by myself.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>This means that you are choosing not to be the judge of what to do. But it must also mean you will not
        judge the situations where you will be called upon to make response. For if you judge them, you have set
        the rules for how you should react to them. And then another answer cannot but produce confusion and
        uncertainty and fear.</p>
        <p>This is your major problem now. You still make up your mind, and then decide to ask what you should do.
        And what you hear may not resolve the problem as you saw it first. This leads to fear, because it contradicts
        what you perceive and so you feel attacked. And therefore angry. There are rules by which this will not
        happen. But it does occur at first, while you are learning how to hear.</p>
      </div>
    </div>

    <!-- Rule 2 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">2</div>
        <div class="rfd-summary">
          <div class="rfd-label">Throughout the day, at any quiet moment, say:</div>
          <div class="rfd-phrase">&ldquo;If I make no decisions by myself, this is the day that will be given me.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>These two procedures, practiced well, will serve to let you be directed without fear, for opposition will not
        first arise and then become a problem in itself.</p>
        <p>But there will still be times when you have judged already. Now the answer will provoke attack, unless you
        quickly straighten out your mind to want an answer that will work. Be certain this has happened if you feel
        yourself unwilling to sit by and ask to have the answer given you. This means you have decided by
        yourself, and cannot see the question. Now you need a quick restorative before you ask again.</p>
      </div>
    </div>

    <!-- Rule 3 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">3</div>
        <div class="rfd-summary">
          <div class="rfd-label">Remember the day you want, then say:</div>
          <div class="rfd-phrase">&ldquo;I have no question. I forgot what to decide.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>This cancels out the terms that you have set, and lets the answer show you what the question must have
        really been.</p>
        <p>Try to observe this rule without delay, despite your opposition. For you have already gotten angry. And
        your fear of being answered in a different way from what your version of the question asks will gain
        momentum, until you believe the day you want is one in which you get your answer to your question. And
        you will not get it, for it would destroy the day by robbing you of what you really want. This can be very
        hard to realize, when once you have decided by yourself the rules that promise you a happy day. Yet this
        decision still can be undone, by simple methods that you can accept.</p>
      </div>
    </div>

    <!-- Rule 4 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">4</div>
        <div class="rfd-summary">
          <div class="rfd-label">If you cannot even let the question go, begin with:</div>
          <div class="rfd-phrase">&ldquo;At least I can decide I do not like what I feel now.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>This much is obvious, and paves the way for the next easy step.</p>
      </div>
    </div>

    <!-- Rule 5 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">5</div>
        <div class="rfd-summary">
          <div class="rfd-label">Having decided you do not like how you feel, continue with:</div>
          <div class="rfd-phrase">&ldquo;And so I hope I have been wrong.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>This works against the sense of opposition, and reminds you that help is not being thrust upon you but is
        something that you want and that you need, because you do not like the way you feel. This tiny opening
        will be enough to let you go ahead with just a few more steps you need to let yourself be helped.</p>
        <p>Now you have reached the turning point, because it has occurred to you that you will gain if what you have
        decided is not so. Until this point is reached, you will believe your happiness depends on being right. But
        this much reason have you now attained; you would be better off if you were wrong.</p>
      </div>
    </div>

    <!-- Rule 6 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">6</div>
        <div class="rfd-summary">
          <div class="rfd-label">This tiny grain of wisdom will take you further:</div>
          <div class="rfd-phrase">&ldquo;I want another way to look at this.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>Now you have changed your mind about the day, and have remembered what you really want. Its purpose
        has no longer been obscured by the insane belief you want it for the goal of being right when you are
        wrong. Thus is the readiness for asking brought to your awareness, for you cannot be in conflict when you
        ask for what you want, and see that it is this for which you ask.</p>
      </div>
    </div>

    <!-- Rule 7 -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num">7</div>
        <div class="rfd-summary">
          <div class="rfd-label">This final step is an open mind, willing to be shown:</div>
          <div class="rfd-phrase">&ldquo;Perhaps there is another way to look at this. What can I lose by asking?&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>Thus you now can ask a question that makes sense, and so the answer will make sense as well. Nor will
        you fight against it, for you see that it is you who will be helped by it.</p>
        <p>It must be clear that it is easier to have a happy day if you prevent unhappiness from entering at all. But
        this takes practice in the rules that will protect you from the ravages of fear. When this has been achieved,
        the sorry dream of judgment has forever been undone. But meanwhile, you have need for practicing the
        rules for its undoing.</p>
      </div>
    </div>

    <!-- Closing commentary -->
    <div class="rfd-rule">
      <div class="rfd-header" onclick="this.parentElement.classList.toggle('rfd-open')">
        <div class="rfd-num" style="background:rgba(201,168,76,0.15);color:var(--gold);font-size:11px;padding:6px 8px">&#9670;</div>
        <div class="rfd-summary">
          <div class="rfd-label" style="font-style:italic">Commentary on Rules 1 &amp; 2</div>
          <div class="rfd-phrase" style="font-size:12px">&ldquo;Your day is not at random. It is set by what you choose to live it with.&rdquo;</div>
        </div>
        <span class="rfd-icon">&#9660;</span>
      </div>
      <div class="rfd-body">
        <p>Let us, then, consider once again the very first of the decisions which are offered here.
        We said you can begin a happy day with the determination not to make decisions by yourself. This seems to
        be a real decision in itself. And yet, you cannot make decisions by yourself. The only question really is
        with what you choose to make them. That is really all. The first rule, then, is not coercion, but a simple
        statement of a simple fact. You will not make decisions by yourself whatever you decide. For they are
        made with idols or with God. And you ask help of anti-Christ or Christ, and which you choose will join
        with you and tell you what to do.</p>
        <p>Your day is not at random. It is set by what you choose to live it with, and how the friend whose counsel
        you have sought perceives your happiness. You always ask advice before you can decide on anything. Let
        this be understood, and you can see there cannot be coercion here, nor grounds for opposition that you may
        be free. There is no freedom from what must occur. And if you think there is, you must be wrong.</p>
        <p>The second rule as well is but a fact. For you and your adviser must agree on what you want before it can
        occur. It is but this agreement that permits all things to happen. Nothing can be caused without some form
        of union, be it with a dream of judgment or the Voice for God. Decisions cause results because they are not
        made in isolation. They are made by you and your adviser, for yourself and for the world as well. The day
        you want you offer to the world, for it will be what you have asked for, and will reinforce the rule of your
        adviser in the world. Whose kingdom is the world for you today? What kind of day will you decide to have?</p>
        <p>It needs but two who would have happiness this day to promise it to all the world. It needs but two to
        understand that they cannot decide alone, to guarantee the joy they asked for will be wholly shared. For they
        have understood the basic law that makes decision powerful, and gives it all effects that it will ever have. It
        needs but two. These two are joined before there can be a decision. Let this be the one reminder that you
        keep in mind, and you will have the day you want, and give it to the world by having it yourself. Your
        judgment has been lifted from the world by your decision for a happy day. And as you have received, so
        must you give.</p>
      </div>
    </div>

  </div>`;

  // Custom Cause & Effect diagrams
  const ceDiagramHtml = buildCEDiagram();

  // Experience Chart (Sandy Levey-Lunden)
  const expChartHtml = buildExpChart();

  // How to Let Go
  const letGoHtml = buildLetGoChart();

  // Thought System Comparison
  const thoughtHtml = buildThoughtComparison();

  // Dawson Key Concepts chart
  const dawsonHtml = buildDawsonChart();

  // Conscious/Subconscious/Unconscious Mind chart
  const consciousHtml = buildConsciousChart();

  // Heaven is the Decision I Must Make (Lesson 138)
  const heavenHtml = buildHeavenChart();

  // Photo charts (legacy — kept for any remaining photo charts)
  const photoHtml = PHOTO_CHARTS.map((pc, i) => `
    <div class="ref-section" id="ref-photo-${{i}}">
      <div class="ref-header" onclick="toggleRef('ref-photo-${{i}}')">
        <div>
          <div class="ref-title">${{escHtml(pc.title)}}</div>
          <div class="ref-subtitle">${{escHtml(pc.credit)}}</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">
        <div class="zoom-controls">
          <button class="zoom-btn" onclick="photoZoomIn('pz-${{i}}', event)">+</button>
          <span class="zoom-label" id="pzl-${{i}}">100%</span>
          <button class="zoom-btn" onclick="photoZoomOut('pz-${{i}}', event)">−</button>
          <button class="zoom-btn" onclick="photoZoomReset('pz-${{i}}', event)" style="font-size:13px">↺</button>
        </div>
        <div class="photo-chart-wrap" id="pz-${{i}}" style="max-height:500px">
          <img class="photo-chart-img" src="${{pc.src}}" alt="${{escHtml(pc.title)}}" draggable="false">
        </div>
      </div>
    </div>`).join('');

  list.innerHTML = `
    <div class="ref-section" id="ref-bigt">
      <div class="ref-header" onclick="toggleRef('ref-bigt')">
        <div>
          <div class="ref-title">Big T / Little t</div>
          <div class="ref-subtitle">Truth vs. perception &mdash; Sandy Levey-Lund&eacute;n, OnPurpose</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body"><div class="bigt-chart">
  <div class="bigt-header-row">
    <div class="bigt-header-left">little t</div>
    <div style="width:40px"></div>
    <div class="bigt-header-right">Big T</div>
  </div>
  <div class="bigt-row"><div class="bigt-left">death</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Life</div></div>
<div class="bigt-row"><div class="bigt-left">darkness</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Light</div></div>
<div class="bigt-row"><div class="bigt-left">perception</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Knowledge</div></div>
<div class="bigt-row"><div class="bigt-left">false</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">True</div></div>
<div class="bigt-row"><div class="bigt-left">ego</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Soul</div></div>
<div class="bigt-row"><div class="bigt-left">wrong mind</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Right Mind</div></div>
<div class="bigt-row"><div class="bigt-left">ego / body</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Holy Spirit</div></div>
<div class="bigt-row"><div class="bigt-left">fear</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Love</div></div>
<div class="bigt-row"><div class="bigt-left">make</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Create</div></div>
<div class="bigt-row"><div class="bigt-left">illusions</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Reality</div></div>
<div class="bigt-row"><div class="bigt-left">man's self</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">God's Self</div></div>
<div class="bigt-row"><div class="bigt-left">conflict</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Peace</div></div>
<div class="bigt-row"><div class="bigt-left">imprisonment</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Freedom</div></div>
<div class="bigt-row"><div class="bigt-left">time</div><div class="bigt-center">&#x2726;</div><div class="bigt-right">Eternity</div></div>

  <div class="bigt-quote">
    <div class="bigt-quote-text">&ldquo;I am that I am being present in all there is.&rdquo;</div>
    <div class="bigt-quote-source">Sandy Levey-Lund&eacute;n &middot; <em>I Just Want Peace</em></div>
  </div>
</div></div>
    </div>
    <div class="ref-section" id="ref-ce">
      <div class="ref-header" onclick="toggleRef('ref-ce')">
        <div>
          <div class="ref-title">True Cause &amp; Effect</div>
          <div class="ref-subtitle">How I interpret events determines how I feel — Steven Gauvin</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{ceDiagramHtml}}</div>
    </div>
    <div class="ref-section" id="ref-exp">
      <div class="ref-header" onclick="toggleRef('ref-exp')">
        <div>
          <div class="ref-title">Experience Chart</div>
          <div class="ref-subtitle">The choice between Mistake and Sin — Sandy Levey-Lunden</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{expChartHtml}}</div>
    </div>
    <div class="ref-section" id="ref-letgo">
      <div class="ref-header" onclick="toggleRef('ref-letgo')">
        <div>
          <div class="ref-title">How to Let Go of an Upset</div>
          <div class="ref-subtitle">3 Steps + the Incorrectable Sequence — Steven Gauvin</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{letGoHtml}}</div>
    </div>
    <div class="ref-section" id="ref-thought">
      <div class="ref-header" onclick="toggleRef('ref-thought')">
        <div>
          <div class="ref-title">Thought System Comparison</div>
          <div class="ref-subtitle">EGO: 100% Insane · Holy Spirit: 100% Sane</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{thoughtHtml}}</div>
    </div>
    <div class="ref-section" id="ref-principles">
      <div class="ref-header" onclick="toggleRef('ref-principles')">
        <div>
          <div class="ref-title">Principles of Miracles</div>
          <div class="ref-subtitle">All 50 Principles — T-1.I</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{principlesHtml}}</div>
    </div>
    <div class="ref-section" id="ref-rules">
      <div class="ref-header" onclick="toggleRef('ref-rules')">
        <div>
          <div class="ref-title">Rules for Decision</div>
          <div class="ref-subtitle">7 Steps — T-30.I</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{rulesHtml}}</div>
    </div>
    <div class="ref-section" id="ref-dawson">
      <div class="ref-header" onclick="toggleRef('ref-dawson')">
        <div>
          <div class="ref-title">Key Concepts in A Course in Miracles</div>
          <div class="ref-subtitle">Michael Dawson, 1993</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{dawsonHtml}}</div>
    </div>
    <div class="ref-section" id="ref-conscious">
      <div class="ref-header" onclick="toggleRef('ref-conscious')">
        <div>
          <div class="ref-title">Conscious / Subconscious / Unconscious Mind</div>
          <div class="ref-subtitle">Gemma &amp; Bette Brain Waves</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">${{consciousHtml}}</div>
    </div>
    <div class="ref-section" id="ref-heaven">
      <div class="ref-header" onclick="toggleRef('ref-heaven')">
        <div>
          <div class="ref-title">Heaven is the Decision I Must Make</div>
          <div class="ref-subtitle">Workbook Lesson 138 &middot; Michael Dawson, 1993</div>
        </div>
        <span class="lesson-expand-icon">▼</span>
      </div>
      <div class="ref-body">
        <div class="zoom-controls">
          <button class="zoom-btn" onclick="heavenZoom(1.25)">+</button>
          <span class="zoom-label" id="hz-label">100%</span>
          <button class="zoom-btn" onclick="heavenZoom(1/1.25)">−</button>
          <button class="zoom-btn" onclick="heavenZoom(0)" style="font-size:13px">↺</button>
        </div>
        <div id="hz-scroll" style="overflow:auto;-webkit-overflow-scrolling:touch">
          <div id="hz-wrap" style="transform-origin:top left;transition:transform 0.15s ease">${{heavenHtml}}</div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-charts-link" style="cursor:pointer" onclick="openCharts()">
      <div class="ref-header" style="pointer-events:none">
        <div>
          <div class="ref-title">&#9635; Reference Charts</div>
          <div class="ref-subtitle">Map of the Mind &middot; Key Teachings</div>
        </div>
        <span class="lesson-expand-icon" style="font-size:16px">&#8599;</span>
      </div>
    </div>`;  // end renderReference

  // Init photo zoom state
  PHOTO_CHARTS.forEach((_, i) => {{
    photoZoomState['pz-' + i] = {{ scale: 1, tx: 0, ty: 0, dragging: false, startX: 0, startY: 0, startTx: 0, startTy: 0 }};
    initPhotoZoom('pz-' + i);
  }});
}}

function renderThemes() {{
  const list = document.getElementById('themes-list');
  if (list.innerHTML) return;
  list.innerHTML = `
    <div class="ref-section" id="ref-study-always-remember">
      <div class="ref-header" onclick="toggleRef('ref-study-always-remember')">
        <div>
          <div class="ref-title">Always Remember</div>
          <div class="ref-subtitle">What the miracle worker must never forget</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The sole responsibility of the miracle worker is to accept the Atonement for himself. This is not a burden &mdash; it is a release. Atonement is not punishment or sacrifice. It is the recognition that the separation from God never actually occurred. The world we see is the projection of a belief &mdash; and that belief can be released. Salvation is simply the acceptance of peace, which cannot be withheld, because ideas leave not their source. We cannot be apart from God.</p>

          <div class="st-section-label">The chain of realisation</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The sole responsibility of the miracle worker is to accept the Atonement for himself.&rdquo;</div>
            <div class="st-quote-ref">T 2:3:65</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I loose the world from all I thought it was.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 132</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Ideas leave not their source. And this remains forever true.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 167</div>
          </div>

          <div class="st-section-label">There is no world</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;There is no world! This is the central thought the course attempts to teach.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 132</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The world you see is an illusion of a world. God did not create it, for what He creates must be eternal as Himself.&rdquo;</div>
            <div class="st-quote-ref">C 4:1</div>
          </div>

          <div class="st-section-label">I am as God created me</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I am as God created me. His Son can suffer nothing. And I am His Son.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 248</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;You are as God created you. The sounds of this world are still, the sights of this world disappear, and all the thoughts that this world ever held are wiped away forever by this one idea.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 110</div>
          </div>

          <div class="st-section-label">He walks with me always</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;God goes with me wherever I go.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 41</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I am never alone. God&rsquo;s Voice speaks to me all through the day.&rdquo;</div>
            <div class="st-quote-ref">W Lesson 49</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Salvation is a collaborative venture. It cannot be undertaken successfully by those who disengage themselves from the Sonship, because they are disengaging themselves from me.&rdquo;</div>
            <div class="st-quote-ref">T 4:7:8</div>
          </div>

          <div class="st-section-label">What to always remember</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Remember always that you cannot be anywhere except in the Mind of God.&rdquo;</div>
            <div class="st-quote-ref">T 9:8:5</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Always remember that it is impossible to use one relationship at the expense of another and not suffer guilt.&rdquo;</div>
            <div class="st-quote-ref">T 15:7:11</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Remember always that what you believe you will teach. Believe with me, and we will become equal as teachers.&rdquo;</div>
            <div class="st-quote-ref">T 6:1:7</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-atonement">
      <div class="ref-header" onclick="toggleRef('ref-study-atonement')">
        <div>
          <div class="ref-title">Atonement</div>
          <div class="ref-subtitle">The correction at the heart of the Course</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The Atonement is the Course&rsquo;s central act &mdash; not punishment, but correction. It is the undoing of the belief that separation from God ever happened. To accept the Atonement is not a sacrifice; it is the recognition that the Kingdom was never lost. It is a lesson in sharing, offered because we forgot how.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The full awareness of the Atonement, then, is the recognition that the separation never occurred.&rdquo;</div>
            <div class="st-quote-ref">T 6:3:34</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Kingdom of Heaven is you. What else but you did the Creator create, and what else but you is His Kingdom? This is the whole message of the Atonement, a message which in its totality transcends the sum of its parts.&rdquo;</div>
            <div class="st-quote-ref">T 4:4:41</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Atonement was an act based on true perception.&rdquo;</div>
            <div class="st-quote-ref">T 3:6:49</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Voice of the Holy Spirit is the call to Atonement, or the restoration of the integrity of the mind.&rdquo;</div>
            <div class="st-quote-ref">T 5:4:20</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Atonement cannot be understood except as a pure act of sharing.&rdquo;</div>
            <div class="st-quote-ref">T 5:6:50</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Atonement is for all because it is the way to undo the belief that anything is for you alone.&rdquo;</div>
            <div class="st-quote-ref">T 9:3:9</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;If the sole responsibility of the miracle-worker is to accept the Atonement for himself, and I assure you that it is, then the responsibility for what is atoned for cannot be yours.&rdquo;</div>
            <div class="st-quote-ref">T 5:7:6&ndash;8</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Atonement is a lesson in sharing, which is given you because you have forgotten how to do it.&rdquo;</div>
            <div class="st-quote-ref">T 9:3:11</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-perception">
      <div class="ref-header" onclick="toggleRef('ref-study-perception')">
        <div>
          <div class="ref-title">Perception</div>
          <div class="ref-subtitle">The world the separated mind made</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">Perception is the world the separated mind made &mdash; a substitute for Knowledge. Unlike Knowledge, which is certain and timeless, perception varies, and that variation is its limitation. The Course does not ask us to destroy perception but to correct it &mdash; moving from misperception (fear) to true perception (love), until perception itself dissolves back into Knowledge.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Perception is a result of learning. In fact, it is the outcome of learning, and if it reflects false teaching, it reflects errors.&rdquo;</div>
            <div class="st-quote-ref">T-3.III.1 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Perception did not exist until the separation introduced degrees, aspects and intervals.&rdquo;</div>
            <div class="st-quote-ref">T 3:6:38</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;To perceive is not to know.&rdquo;</div>
            <div class="st-quote-ref">T 3:6:34</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Perception always involves some misuse of will because it involves the mind in areas of uncertainty.&rdquo;</div>
            <div class="st-quote-ref">T 3:6:44</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The world you see is an outside picture of an inward condition.&rdquo;</div>
            <div class="st-quote-ref">T-21.in.1 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;You see what you believe is there, and you believe it there because you want it there.&rdquo;</div>
            <div class="st-quote-ref">T-25.III.1 &#9733;</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Innocent, or true, perception means that you never misperceive and always see truly.&rdquo;</div>
            <div class="st-quote-ref">T 3:4:27</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is the healing of the perception of separation.&rdquo;</div>
            <div class="st-quote-ref">T 3:7:59</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Perception is a mirror, not a fact. And what I look on is my state of mind, reflected outward.&rdquo;</div>
            <div class="st-quote-ref">W-304.1 &#9733;</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-holyspirit">
      <div class="ref-header" onclick="toggleRef('ref-study-holyspirit')">
        <div>
          <div class="ref-title">The Holy Spirit</div>
          <div class="ref-subtitle">God&rsquo;s Answer to the separation</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The Holy Spirit is not a distant force &mdash; He is the part of your mind that never forgot God. He came into being with the separation as a protection, and He is God&rsquo;s Answer to it. He is the bridge between perception and Knowledge, the Mediator between the ego and the Soul, always speaking for the right choice. His direction is freedom. His goal is God.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit is nothing more than your right mind.&rdquo;</div>
            <div class="st-quote-ref">T 5:2:9</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit is the Mind of the Atonement.&rdquo;</div>
            <div class="st-quote-ref">T 5:3:12</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit remains the bridge between perception and knowledge.&rdquo;</div>
            <div class="st-quote-ref">T 6:3:31</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit is the Mediator between the interpretations of the ego and the knowledge of the Soul.&rdquo;</div>
            <div class="st-quote-ref">T 5:5:38</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit has the task of translating the useless into the useful, the meaningless into the meaningful and the temporary into the timeless.&rdquo;</div>
            <div class="st-quote-ref">T 7:2:6</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit is the part of the mind that lies between the ego and the Soul, mediating between them always in favour of the Soul.&rdquo;</div>
            <div class="st-quote-ref">T 7:10:91</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit&rsquo;s teaching takes only one direction and has only one goal. His direction is freedom and His goal is God.&rdquo;</div>
            <div class="st-quote-ref">T 8:3:13</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit will always guide you truly because your joy is His.&rdquo;</div>
            <div class="st-quote-ref">T 7:12:109</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Remember that the Holy Spirit is the communication link between God the Father and His separated Sons.&rdquo;</div>
            <div class="st-quote-ref">T 6:2:16</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Teach only love, for that is what you are.&rdquo;</div>
            <div class="st-quote-ref">T 6:2:18</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-forgiveness">
      <div class="ref-header" onclick="toggleRef('ref-study-forgiveness')">
        <div>
          <div class="ref-title">Forgiveness</div>
          <div class="ref-subtitle">The healing of the perception of separation</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">Forgiveness in the Course is not what the world calls forgiveness. It is not excusing, tolerating, or overlooking. It is the recognition that there was never anything real to forgive. Forgiveness looks beyond error from the beginning and keeps it unreal. It is the healing of the perception of separation &mdash; and it is the same as salvation.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is the healing of the perception of separation.&rdquo;</div>
            <div class="st-quote-ref">T 3:7:59</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Salvation and forgiveness are the same.&rdquo;</div>
            <div class="st-quote-ref">W 99:1</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is the means by which I will recognise my innocence.&rdquo;</div>
            <div class="st-quote-ref">W-62.1 &#9733;</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;A prayer for forgiveness is a request that we may be able to recognise that we already have.&rdquo;</div>
            <div class="st-quote-ref">T 3:7:56</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness through the Holy Spirit lies simply in looking beyond error from the beginning and thus keeping it unreal for you.&rdquo;</div>
            <div class="st-quote-ref">T 9:3:14</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The unforgiving mind is full of fear, and offers love no room to be itself; no place where God can enter in and be at home.&rdquo;</div>
            <div class="st-quote-ref">W-121.2 &#9733;</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is the key to happiness.&rdquo;</div>
            <div class="st-quote-ref">W-121 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness offers everything I want.&rdquo;</div>
            <div class="st-quote-ref">W-122 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is my function as the light of the world.&rdquo;</div>
            <div class="st-quote-ref">W-62 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Forgiveness is still, and quietly does nothing. It merely looks, and waits, and judges not.&rdquo;</div>
            <div class="st-quote-ref">W-pII.1.4 &#9733;</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-healing">
      <div class="ref-header" onclick="toggleRef('ref-study-healing')">
        <div>
          <div class="ref-title">Healing</div>
          <div class="ref-subtitle">The removal of all that stands in the way of knowledge</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">Healing in the Course is not about the body &mdash; it is about the mind. The body can only be sick if the mind has decided it is. Healing is the result of using the body solely for communication, and it happens when the will to wake replaces the will to fear. The Holy Spirit is the healer &mdash; and the invitation must come from you.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Healing is the result of using the body solely for communication.&rdquo;</div>
            <div class="st-quote-ref">T 8:7:62</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;What is healing but the removal of all that stands in the way of knowledge?&rdquo;</div>
            <div class="st-quote-ref">T 10:6:40</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Healing is a sign that he wants to make whole.&rdquo;</div>
            <div class="st-quote-ref">T 10:3:19</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The will to wake is the will to love, since all healing involves replacing fear with love.&rdquo;</div>
            <div class="st-quote-ref">T 8:9:84</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The unification of purpose, then, is the Holy Spirit&rsquo;s only way of healing.&rdquo;</div>
            <div class="st-quote-ref">T 8:9:89</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Healing thus becomes a lesson in understanding, and the more you practise it, the better teacher and learner you become.&rdquo;</div>
            <div class="st-quote-ref">T 10:3:17</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;This willingness opens his own ears to the Voice of the Holy Spirit, whose message is wholeness.&rdquo;</div>
            <div class="st-quote-ref">T 10:3:19</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Healing is of God.&rdquo;</div>
            <div class="st-quote-ref">W-137 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I am not a body. I am free. For I am still as God created me.&rdquo;</div>
            <div class="st-quote-ref">W-201 &#9733;</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-miracle">
      <div class="ref-header" onclick="toggleRef('ref-study-miracle')">
        <div>
          <div class="ref-title">Miracle</div>
          <div class="ref-subtitle">A shift in perception &mdash; the natural expression of love</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The miracle is not a supernatural event &mdash; it is a shift in perception. It is the right answer, the natural expression of love, and the sign of your willingness to follow the Holy Spirit&rsquo;s plan. Miracles are not performed by you; they flow through you when you step aside. They do not restore truth &mdash; they lift the veil so truth can shine.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The miracle is therefore a lesson in what joy is. Being a lesson in sharing, it is a lesson in love, which is joy.&rdquo;</div>
            <div class="st-quote-ref">T 7:11:106</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Miracles are merely the sign of your willingness to follow the Holy Spirit&rsquo;s plan of salvation in recognition of the fact you do not know what it is.&rdquo;</div>
            <div class="st-quote-ref">T 9:3:15</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The miracle is the act of a Son of God who has laid aside all false gods and who calls on his brother to do likewise.&rdquo;</div>
            <div class="st-quote-ref">T 9:10:90</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit is the motivation for miracle-mindedness, the will to heal the separation by letting it go.&rdquo;</div>
            <div class="st-quote-ref">T 5:3:17</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Your miracles are the only witnesses to your reality which you can recognise.&rdquo;</div>
            <div class="st-quote-ref">T 9:5:36</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Prayer is the medium of miracles.&rdquo;</div>
            <div class="st-quote-ref">T 3:7:56</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The miracle does not restore the truth, the light the veil has not put out. It merely lifts the veil, and lets the truth shine forth unimpeded.&rdquo;</div>
            <div class="st-quote-ref">T-28.II.12 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Miracles are natural. When they do not occur something has gone wrong.&rdquo;</div>
            <div class="st-quote-ref">T-1.I.6 &#9733;</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;A miracle is a correction. It does not create, nor really change at all. It merely looks on devastation, and reminds the mind that what it sees is false.&rdquo;</div>
            <div class="st-quote-ref">W-pII.13.1 &#9733;</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-crucifixion">
      <div class="ref-header" onclick="toggleRef('ref-study-crucifixion')">
        <div>
          <div class="ref-title">Message of the Crucifixion</div>
          <div class="ref-subtitle">Teach only love, for that is what you are</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The crucifixion was not a punishment &mdash; it was a demonstration. Jesus elected to show that the most outrageous assault the ego could devise simply did not matter. The message was not about suffering. It was not about guilt. It was a call to peace &mdash; and its meaning is perfectly clear: teach only love, for that is what you are.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The crucifixion is nothing more than an extreme example. Its value, like the value of any teaching device, lies solely in the kind of learning it facilitates.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.4</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The message which the crucifixion was intended to teach was that it is not necessary to perceive any form of assault in persecution, because you cannot be persecuted.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.7</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The message of the crucifixion is perfectly clear: Teach only love, for that is what you are.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.17&ndash;18</div>
          </div>

          <div class="st-section-label">The mechanism</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I elected both for your sake and mine to demonstrate that the most outrageous assault as judged by the ego did not matter.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.13</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The crucifixion cannot be shared, because it is the symbol of projection, but the resurrection is the symbol of sharing.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.16</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;I do not call for martyrs but for teachers. No one is &lsquo;punished&rsquo; for sins, and the Sons of God are not sinners.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.22</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Teach your own perfect immunity, which is the truth in you, and know that it cannot be assailed.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.9</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Your resurrection is your reawakening. I am the model for rebirth, but rebirth itself is merely the dawning on your minds of what is already in them.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.10</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;You are not persecuted, nor was I. You are not asked to repeat my experiences.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.II.14</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ref-section" id="ref-study-lessons-hs">
      <div class="ref-header" onclick="toggleRef('ref-study-lessons-hs')">
        <div>
          <div class="ref-title">Lessons of the Holy Spirit</div>
          <div class="ref-subtitle">I am Love &bull; I have Peace &bull; I feel Joy</div>
        </div>
        <span class="lesson-expand-icon">&#9660;</span>
      </div>
      <div class="ref-body">
        <div class="study-theme">
          <div class="st-section-label">The Teaching</div>
          <p class="st-framing">The Holy Spirit teaches three lessons &mdash; not as rules to follow, but as a progression. Each one builds on the last. Together they move the mind from the ego&rsquo;s getting to God&rsquo;s giving, from conflict to peace, from doubt to certainty. I am Love. I have Peace. I feel Joy.</p>

          <div class="st-section-label">What it is</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;Hear then the one answer of the Holy Spirit to all the questions which the ego raises. You are a Child of God, a priceless part of His Kingdom, which He created as part of Him. Nothing else exists, and only this is real.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.V.50</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;The Holy Spirit does not speak first, but He always answers.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.V.47</div>
          </div>

          <div class="st-section-label">The mechanism &mdash; the three lessons</div>
          <div class="st-quote">
            <div class="st-quote-text"><strong>Lesson A:</strong> &ldquo;To have, give all to all.&rdquo;<br><em>The undoing of the getting concept &mdash; a thought reversal.</em></div>
            <div class="st-quote-ref">Tx.6.V.67</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text"><strong>Lesson B:</strong> &ldquo;To have peace, teach peace to learn it.&rdquo;<br><em>A positive affirmation of what you want.</em></div>
            <div class="st-quote-ref">Tx.6.V.78</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text"><strong>Lesson C:</strong> &ldquo;Be vigilant only for God and His Kingdom.&rdquo;<br><em>A major step toward fundamental change &mdash; one of protection for your mind.</em></div>
            <div class="st-quote-ref">Tx.6.V.85</div>
          </div>

          <div class="st-section-label">The correction</div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;You learn first that having rests on giving and not on getting. Next you learn that you learn what you teach and that you want to learn peace.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.V.90</div>
          </div>
          <div class="st-quote">
            <div class="st-quote-text">&ldquo;If you allow yourselves to have in your minds only what God put there, you are acknowledging your mind as God created it.&rdquo;</div>
            <div class="st-quote-ref">Tx.6.V.89</div>
          </div>
        </div>
      </div>
    </div>`;
}}

function buildCEDiagram() {{
  return `
  <div class="custom-chart">
    <div style="text-align:center;margin-bottom:20px">
      <div class="ce-callout" style="display:inline-block;min-width:200px">Change occurs here</div>
    </div>
    <div class="ce-flow" style="margin-top:24px">
      <div class="ce-node">
        <div class="ce-node-label">Past</div>
        <div class="ce-node-sub">Separation<br>from God</div>
      </div>
      <div class="ce-arrow">→</div>
      <div class="ce-node">
        <div class="ce-node-label" style="color:var(--gold-light)">Cause</div>
        <div class="ce-node-sub">Interpretation<br>Perception</div>
      </div>
      <div class="ce-arrow">→</div>
      <div class="ce-node">
        <div class="ce-node-label">Effect</div>
        <div class="ce-node-sub">Actions</div>
      </div>
      <div class="ce-arrow">→</div>
      <div class="ce-node">
        <div class="ce-node-label">Results</div>
        <div class="ce-node-sub">Events</div>
      </div>
    </div>
    <div style="text-align:center;margin:20px 0 8px;font-size:13px;color:var(--text-dim)">
      At <strong style="color:var(--gold-light)">Cause</strong>, I can react with either:
    </div>
    <div class="ce-fork">
      <div class="ce-fork-item">
        <div style="font-size:28px">↙</div>
        <div class="ce-fork-label ce-fork-fear" style="font-variant:small-caps">Fear</div>
      </div>
      <div class="ce-fork-item">
        <div style="font-size:28px">↘</div>
        <div class="ce-fork-label ce-fork-love" style="font-variant:small-caps">Love</div>
      </div>
    </div>
    <div class="ce-insight-box">
      These feelings occur <em>or</em> are experienced independent of the results in my life.<br>
      They occur based on a <strong style="font-variant:small-caps">Choice</strong> — how I interpret what I think I see.
    </div>
    <div class="ce-result-note">
      <strong style="color:var(--text-bright)">Actions or events in my life are <span style="font-variant:small-caps">Always</span> a result of how I interpret things.</strong><br><br>
      The world (<span style="font-variant:small-caps">Effect</span>) is <span style="font-variant:small-caps">Not</span> the cause of the way I feel. The way I feel is based on a <span style="font-variant:small-caps">Choice</span> that I made to choose a thought system (<span style="font-variant:small-caps">Cause</span>) that believes the <span style="font-variant:small-caps">Separation Happened</span> and is <span style="font-variant:small-caps">Real</span>.<br><br>
      <strong style="color:var(--text-bright);font-variant:small-caps">Nothing Means Anything — But It Matters!</strong><br><br>
      We normally reverse cause and effect. This comes from the original belief that we created God.<br><br>
      <em>For example: "I feel sad because you didn't say hi to me."</em><br><br>
      The true <span style="font-variant:small-caps">Cause</span> and <span style="font-variant:small-caps">Effect</span> is that I already feel sad and I am looking for a reason to explain my sadness. The cause of my sadness is not that you didn't say hi to me, but a choice that I already have made to think in a thought system that says the <strong style="color:var(--text-bright);font-variant:small-caps">Separation Is Real</strong>.<br><br>
      <strong>To find the true <span style="font-variant:small-caps">Cause</span> of an <span style="font-variant:small-caps">Effect</span>, they must comply to these rules:</strong><br>
      1. It must happen all of the time.<br>
      2. No other <span style="font-variant:small-caps">Cause</span> can produce that specific <span style="font-variant:small-caps">Effect</span>.
    </div>
  </div>`;
}}

function buildExpChart() {{
  // Layout matches Steven's sketch:
  // TOP HALF: Mistake stairs ascending UP (Truth at top, Mistake at bottom of top half)
  // MIDDLE ROW: Sin [box] ← Something Happens (oval) → Mistake [box]  (all same level)
  // BOTTOM HALF: Sin stairs descending DOWN (Sin at top of bottom half, Death at bottom)
  return `
  <div class="custom-chart" style="padding:0">
    <!-- Header note -->
    <div style="background:rgba(100,80,180,0.12);border:1px solid rgba(160,144,208,0.35);border-radius:10px;padding:12px 16px;margin-bottom:20px;font-size:13px;color:#c8c0e8;line-height:1.6;text-align:center">
      Something happens in life that we call a <em style="color:#e0d8f8;font-weight:600">'negative' experience</em>.
      We can <strong style="color:#f0ead8">choose</strong> to see it as a <strong style="color:#4a9a7a">'mistake'</strong> <span style="color:var(--text-dim);font-size:11px">(right mind)</span> or a <strong style="color:#c06060">'sin'</strong> <span style="color:var(--text-dim);font-size:11px">(wrong mind)</span>.
    </div>

    <!-- TOP: Mistake path ascending (Truth at top, steps going down to Mistake box) -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:0">
      <!-- Left column: empty top -->
      <div></div>
      <!-- Centre column: empty top -->
      <div></div>
      <!-- Right column: ascending steps (read bottom-to-top: Mistake→Forgiveness→Correction→Innocence→Truth) -->
      <div style="display:flex;flex-direction:column;align-items:center;gap:0">
        <div style="font-size:10px;font-weight:bold;letter-spacing:1.5px;color:#4a9a7a;margin-bottom:6px;text-align:center"><span style="font-variant:small-caps">Right Mind</span> · <span style="font-variant:small-caps">Mistake</span> ↑</div>
        <div style="background:rgba(74,154,122,0.22);border:2px solid #4a9a7a;border-radius:8px;padding:8px 10px;font-size:13px;font-weight:bold;color:#4a9a7a;width:100%;text-align:center;box-sizing:border-box">Truth</div>
        <div style="color:#4a9a7a;font-size:20px;line-height:1.2">↑</div>
        <div style="background:rgba(74,154,122,0.08);border:1px solid rgba(74,154,122,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#6abf9a;width:100%;text-align:center;box-sizing:border-box">Innocence</div>
        <div style="color:#4a9a7a;font-size:20px;line-height:1.2">↑</div>
        <div style="background:rgba(74,154,122,0.08);border:1px solid rgba(74,154,122,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#6abf9a;width:100%;text-align:center;box-sizing:border-box">Correction</div>
        <div style="color:#4a9a7a;font-size:20px;line-height:1.2">↑</div>
        <div style="background:rgba(74,154,122,0.08);border:1px solid rgba(74,154,122,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#6abf9a;width:100%;text-align:center;box-sizing:border-box">Forgiveness</div>
        <div style="color:#4a9a7a;font-size:20px;line-height:1.2">↑</div>
      </div>
    </div>

    <!-- MIDDLE ROW: Sin box | Something Happens | Mistake box (all same level) -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;align-items:center;margin:4px 0">
      <!-- Sin box (left) -->
      <div style="display:flex;flex-direction:column;align-items:center">
        <div style="font-size:10px;font-weight:bold;letter-spacing:1.5px;color:#c06060;margin-bottom:6px;text-align:center"><span style="font-variant:small-caps">Wrong Mind</span> · <span style="font-variant:small-caps">Sin</span> ↓</div>
        <div style="background:rgba(192,96,96,0.18);border:2px solid #c06060;border-radius:8px;padding:10px 12px;font-size:14px;font-weight:bold;color:#c06060;width:100%;text-align:center;box-sizing:border-box">Sin</div>
      </div>

      <!-- Something Happens oval (centre) -->
      <div style="text-align:center">
        <div style="background:rgba(201,168,76,0.12);border:2px solid #c9a84c;border-radius:50px;padding:14px 16px;font-size:14px;font-weight:bold;color:#c9a84c;text-align:center">
          Something<br>Happens
        </div>
        <div style="margin-top:6px;font-size:11px;color:var(--text-dim)">← &nbsp; choose &nbsp; →</div>
      </div>

      <!-- Mistake box (right) -->
      <div style="display:flex;flex-direction:column;align-items:center">
        <div style="font-size:10px;font-weight:bold;letter-spacing:1.5px;color:#4a9a7a;margin-bottom:6px;text-align:center"><span style="font-variant:small-caps">Right Mind</span> · <span style="font-variant:small-caps">Mistake</span> ↑</div>
        <div style="background:rgba(74,154,122,0.15);border:2px solid #4a9a7a;border-radius:8px;padding:10px 12px;font-size:14px;font-weight:bold;color:#4a9a7a;width:100%;text-align:center;box-sizing:border-box">Mistake</div>
      </div>
    </div>

    <!-- BOTTOM: Sin path descending -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:0">
      <!-- Left column: descending steps -->
      <div style="display:flex;flex-direction:column;align-items:center;gap:0">
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#d08080;width:100%;text-align:center;box-sizing:border-box">Guilt</div>
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#d08080;width:100%;text-align:center;box-sizing:border-box">Punishment</div>
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.3);border-radius:6px;padding:6px 10px;font-size:12px;color:#d08080;width:100%;text-align:center;box-sizing:border-box">Fear</div>
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.3);border-radius:6px;padding:5px 10px;font-size:11px;color:#d08080;width:100%;text-align:center;box-sizing:border-box">Attack / Defense<br>Pleasure / Pain</div>
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.3);border-radius:6px;padding:6px 10px;font-size:11px;color:#d08080;width:100%;text-align:center;box-sizing:border-box">Sickness &amp; Suffering</div>
        <div style="color:#c06060;font-size:20px;line-height:1.2">↓</div>
        <div style="background:rgba(192,96,96,0.22);border:2px solid #c06060;border-radius:8px;padding:9px 10px;font-size:13px;font-weight:bold;color:#c06060;width:100%;text-align:center;box-sizing:border-box">Death</div>
      </div>
      <!-- Centre and right: empty bottom -->
      <div></div>
      <div></div>
    </div>

    <div style="margin-top:16px;font-size:11px;color:var(--text-dim);text-align:right">— Sandy Levey-Lunden</div>
  </div>`;
}}

function buildLetGoChart() {{
  return `
  <div class="custom-chart">
    <div class="letgo-steps">
      <div class="letgo-step">
        <div class="letgo-num">1</div>
        <div class="letgo-text">Identify the true <strong style="font-variant:small-caps">Cause</strong>.</div>
      </div>
      <div class="letgo-step">
        <div class="letgo-num">2</div>
        <div class="letgo-text">Remove the <strong style="font-variant:small-caps">Cause</strong> from where it is not. <em>(It is in your mind and not in the world.)</em></div>
      </div>
      <div class="letgo-step">
        <div class="letgo-num">3</div>
        <div class="letgo-text">Get help from the loving part of your mind (The Holy Spirit) and ask it to help you choose the other thought system without judgment and guilt. <strong style="font-variant:small-caps">Ask for Forgiveness!!!</strong></div>
      </div>
    </div>
    <div class="incorrectable-box">
      <div class="incorrectable-title">If we choose to see the experience as <span style="font-variant:small-caps">Incorrectable</span>, the following sequence is logically inevitable:</div>
      <div class="incorrectable-step"><div class="incorrectable-num">1.</div><div>Something 'negative' that I have experienced, that I think I caused and I think is uncorrectable, I feel guilty for.</div></div>
      <div class="incorrectable-step"><div class="incorrectable-num">2.</div><div>When I feel guilty, <strong style="font-variant:small-caps">I Believe</strong> that I should be punished.</div></div>
      <div class="incorrectable-step"><div class="incorrectable-num">3.</div><div>When I expect punishment, I punish myself, <strong style="font-variant:small-caps">Or</strong> I attract it from others. At the same time I am afraid of this punishment.</div></div>
      <div class="incorrectable-step"><div class="incorrectable-num">4.</div><div>When I am afraid, I either attack others or defend myself.</div></div>
      <div class="incorrectable-step"><div class="incorrectable-num">5.</div><div>In my attack or defense, I suffer because in my True self I know I am only attacking myself. In this I can become sick.</div></div>
    </div>
  </div>`;
}}

function buildThoughtComparison() {{
  const egoItems = [
    'Identity: Separate, finite, temporary, valueless, "me/they"',
    'Dream figure: Oblivious, mindless, self-absorbed, exclusive',
    'Consistently merciless, cruel, annoying, condemning, vicious',
    'Sin, guilt and fear for all, but projected to other "enemies"',
    'Sacrifice, martyrdom, victimhood, scapegoats required',
    'Uncertainty from trusting in lonely personal interests',
    'Differences are crucial to appearing misunderstood',
    'Obsessed with form, appearances, invested in conflict',
    'Miserable, but in deep denial, seeks but never finds',
    'Body identification, limited by birth, dreams, and death',
    'Divisive, narcissistic, paranoid, defensive, separate interests',
    'Threatened by everything, takes its special story seriously',
  ];
  const hsItems = [
    'Identity: Shared, infinite, permanent, invaluable, non-dual',
    'Dreamer: Observes without judgment, mindful, inclusive',
    'Consistently merciful, gentle, patient, tolerant, joyous',
    'Generous innocence for all throughout eternity',
    'Not upset by a completely neutral world',
    'Feel supported, calm from trusting in shared interests',
    'Universal sameness affords effortless compassion',
    'Gentle acceptance of mind’s content of guiltlessness',
    'Happily corrected, finds lovingkindness and extends to all',
    'Spirit identification, not limited by what seems to change',
    'Shared interests, your call for love is mine, open-hearted',
    'Sees its stories as silly, funny, forgivable blips in the radar',
  ];
  const egoHtml = egoItems.map(t => `<div class="thought-item">✗ ${{escHtml(t)}}</div>`).join('');
  const hsHtml = hsItems.map(t => `<div class="thought-item">✓ ${{escHtml(t)}}</div>`).join('');
  return `
  <div class="custom-chart">
    <div class="thought-comparison">
      <div class="thought-col thought-col-ego">
        <div class="thought-col-title">EGO — 100% Insane 24/7/365</div>
        ${{egoHtml}}
      </div>
      <div class="thought-col thought-col-hs">
        <div class="thought-col-title">Holy Spirit — 100% Sane</div>
        ${{hsHtml}}
      </div>
    </div>
  </div>`;
}}

function buildDawsonChart() {{
  return `
  <div class="custom-chart" style="padding:16px 12px">


    <!-- ═══ SECTION 1: THE JOURNEY ═══ -->
    <!-- Two-column layout: left = journey flow, right = Truth/Illusion zone -->
    <div style="display:grid;grid-template-columns:1fr 140px;gap:0;align-items:stretch">

      <!-- LEFT: Journey flow cards -->
      <div style="border-right:2px solid var(--border);padding-right:16px">

        <!-- HEAVEN -->
        <div style="background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.4);border-left:4px solid #c9a84c;border-radius:8px;padding:12px 14px;margin-bottom:0">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <div style="font-size:14px;font-weight:bold;color:#c9a84c">Heaven</div>
            <div style="font-size:9px;font-variant:small-caps;color:#c9a84c;background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.3);border-radius:4px;padding:2px 6px;letter-spacing:1px">Truth</div>
          </div>
          <div style="font-size:11px;color:rgba(201,168,76,0.7);font-style:italic;margin-bottom:6px">The perfect unity of God and Christ</div>
          <div style="font-size:11px;color:rgba(201,168,76,0.6);line-height:1.8">
            Christ &middot; Extension &middot; Knowledge &middot; Spirit &middot; One Mind &middot; Will &middot; Love &middot; Life &middot; Eternity
          </div>
        </div>

        <!-- Arrow: Projection (red, going down) -->
        <div style="display:flex;align-items:center;gap:8px;padding:8px 14px">
          <div style="flex:1;height:2px;background:linear-gradient(to right,rgba(192,96,96,0.1),rgba(192,96,96,0.5))"></div>
          <div style="font-size:12px;color:#c06060;font-weight:600;letter-spacing:0.5px">Projection &#8595;</div>
          <div style="flex:1;height:2px;background:linear-gradient(to left,rgba(192,96,96,0.1),rgba(192,96,96,0.5))"></div>
        </div>

        <!-- THE FALL -->
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.35);border-left:4px solid #c06060;border-radius:8px;padding:12px 14px;margin-bottom:0">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <div style="font-size:14px;font-weight:bold;color:#c06060">The Fall &mdash; Separation</div>
            <div style="font-size:9px;font-variant:small-caps;color:#c06060;background:rgba(192,96,96,0.12);border:1px solid rgba(192,96,96,0.3);border-radius:4px;padding:2px 6px;letter-spacing:1px">Illusion</div>
          </div>
          <div style="font-size:11px;color:rgba(192,96,96,0.7);font-style:italic;margin-bottom:6px">The state of apparent separation</div>
          <div style="font-size:11px;color:rgba(192,96,96,0.65);line-height:1.8">
            Ego &middot; Projection &middot; Perception &middot; Body &middot; Split mind &middot; Decisions &middot; Fear &middot; Death &middot; Time
          </div>
        </div>

        <!-- Arrow: Special Relationships (red, going down) -->
        <div style="display:flex;align-items:center;gap:8px;padding:8px 14px">
          <div style="flex:1;height:2px;background:linear-gradient(to right,rgba(160,70,70,0.1),rgba(160,70,70,0.5))"></div>
          <div style="font-size:12px;color:#b05050;font-weight:600;letter-spacing:0.5px">Special Relationships &#8595;</div>
          <div style="flex:1;height:2px;background:linear-gradient(to left,rgba(160,70,70,0.1),rgba(160,70,70,0.5))"></div>
        </div>

        <!-- THE WORLD -->
        <div style="background:rgba(160,70,70,0.08);border:1px solid rgba(160,70,70,0.3);border-left:4px solid #a04646;border-radius:8px;padding:12px 14px;margin-bottom:0">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <div style="font-size:14px;font-weight:bold;color:#b05050">The World &mdash; Ego</div>
            <div style="font-size:9px;font-variant:small-caps;color:#b05050;background:rgba(160,70,70,0.12);border:1px solid rgba(160,70,70,0.3);border-radius:4px;padding:2px 6px;letter-spacing:1px">Illusion</div>
          </div>
          <div style="font-size:11px;color:rgba(160,70,70,0.7);font-style:italic">The dream of separation made solid</div>
        </div>

        <!-- Arrow: Forgiveness (green, going up) -->
        <div style="display:flex;align-items:center;gap:8px;padding:8px 14px">
          <div style="flex:1;height:2px;background:linear-gradient(to right,rgba(74,154,122,0.1),rgba(74,154,122,0.5))"></div>
          <div style="font-size:12px;color:#4a9a7a;font-weight:600;letter-spacing:0.5px">&#8593; Forgiveness</div>
          <div style="flex:1;height:2px;background:linear-gradient(to left,rgba(74,154,122,0.1),rgba(74,154,122,0.5))"></div>
        </div>

        <!-- REAL WORLD -->
        <div style="background:rgba(74,154,122,0.08);border:1px solid rgba(74,154,122,0.35);border-left:4px solid #4a9a7a;border-radius:8px;padding:12px 14px;margin-bottom:0">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <div style="font-size:14px;font-weight:bold;color:#4a9a7a">Real World &mdash; Holy Spirit</div>
            <div style="font-size:9px;font-variant:small-caps;color:#4a9a7a;background:rgba(74,154,122,0.12);border:1px solid rgba(74,154,122,0.3);border-radius:4px;padding:2px 6px;letter-spacing:1px">Truth</div>
          </div>
          <div style="font-size:11px;color:rgba(74,154,122,0.7);font-style:italic;margin-bottom:6px">Completion of our individual path</div>
          <div style="font-size:11px;color:rgba(74,154,122,0.65);line-height:1.8">
            End of Atonement &middot; Happy dreams &middot; Right perception &middot; Peace &amp; vision attained
          </div>
        </div>

        <!-- Arrow: Atonement + Going Home Together (green, going up) -->
        <div style="display:flex;align-items:center;gap:8px;padding:8px 14px">
          <div style="flex:1;height:2px;background:linear-gradient(to right,rgba(74,154,122,0.1),rgba(74,154,122,0.6))"></div>
          <div style="font-size:12px;color:#4a9a7a;font-weight:600;letter-spacing:0.5px">&#8593; Atonement</div>
          <div style="flex:1;height:2px;background:linear-gradient(to left,rgba(74,154,122,0.1),rgba(74,154,122,0.6))"></div>
        </div>

        <!-- Going Home Together note -->
        <div style="background:linear-gradient(135deg,rgba(74,154,122,0.12),rgba(201,168,76,0.08));border:1px solid rgba(74,154,122,0.4);border-radius:8px;padding:12px 14px;box-shadow:0 0 16px rgba(74,154,122,0.12)">
          <div style="font-size:13px;font-weight:bold;color:#4a9a7a;margin-bottom:4px">Going Home Together</div>
          <div style="font-size:11px;color:rgba(74,154,122,0.7);font-style:italic;margin-bottom:6px">The Second Coming &middot; The Last Judgement</div>
          <div style="font-size:11px;color:rgba(201,168,76,0.7)">&#8594; Return to Heaven &mdash; the perfect unity of God and Christ</div>
        </div>

      </div>

      <!-- RIGHT: Truth / Illusion zone indicator -->
      <div style="display:flex;flex-direction:column;padding-left:16px">

        <!-- TRUTH zone -->
        <div style="flex:0 0 auto;background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.4);border-radius:8px;padding:10px 8px;text-align:center;margin-bottom:8px">
          <div style="font-size:11px;font-weight:bold;color:#c9a84c;letter-spacing:1px;font-variant:small-caps">Truth</div>
          <div style="font-size:10px;color:rgba(201,168,76,0.6);margin-top:4px;line-height:1.5">Heaven<br>Real World</div>
        </div>

        <!-- Divider label -->
        <div style="text-align:center;padding:6px 0;font-size:10px;color:var(--text-dim);font-style:italic;flex:0 0 auto">
          &#8597; Holy Spirit<br>bridges both
        </div>

        <!-- ILLUSION zone -->
        <div style="flex:0 0 auto;background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.35);border-radius:8px;padding:10px 8px;text-align:center;margin-bottom:8px">
          <div style="font-size:11px;font-weight:bold;color:#c06060;letter-spacing:1px;font-variant:small-caps">Illusion</div>
          <div style="font-size:10px;color:rgba(192,96,96,0.6);margin-top:4px;line-height:1.5">The Fall<br>The World</div>
        </div>



      </div>
    </div>

    <!-- ═══ SECTION 2: THE SPLIT MIND ═══ -->
    <div style="margin-top:24px;border-top:1px solid var(--border);padding-top:20px">
      <div style="text-align:center;font-size:13px;font-weight:bold;color:#c9a84c;letter-spacing:1px;margin-bottom:4px">The Split Mind</div>
      <div style="text-align:center;font-size:11px;color:var(--text-dim);font-style:italic;margin-bottom:16px">The Decision Maker chooses between the Ego and the Holy Spirit</div>

      <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:stretch">

        <!-- Wrong Mind -->
        <div style="background:rgba(192,96,96,0.08);border:1px solid rgba(192,96,96,0.35);border-top:3px solid #c06060;border-radius:8px;padding:14px">
          <div style="font-size:12px;font-weight:bold;color:#c06060;margin-bottom:2px">Wrong Mind</div>
          <div style="font-size:11px;color:rgba(192,96,96,0.7);font-style:italic;margin-bottom:10px">Ego</div>
          <div style="font-size:11px;color:var(--text-dim);line-height:2">
            &bull; Sin<br>&bull; Guilt<br>&bull; Fear<br>&bull; Denial<br>&bull; Projection<br>&bull; Special relationships
          </div>
        </div>

        <!-- Decision Maker -->
        <div style="background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.3);border-top:3px solid #c9a84c;border-radius:8px;padding:14px;text-align:center;min-width:120px">
          <div style="font-size:12px;font-weight:bold;color:#c9a84c;margin-bottom:8px">Decision Maker</div>
          <!-- Simple scales icon in CSS -->
          <div style="margin:8px auto;width:60px">
            <div style="width:2px;height:20px;background:#c9a84c;margin:0 auto"></div>
            <div style="width:60px;height:2px;background:#c9a84c;margin:0 auto"></div>
            <div style="display:flex;justify-content:space-between;margin-top:2px">
              <div style="width:2px;height:14px;background:#c06060"></div>
              <div style="width:2px;height:14px;background:#4a9a7a"></div>
            </div>
            <div style="display:flex;justify-content:space-between">
              <div style="width:22px;height:4px;background:rgba(192,96,96,0.3);border-radius:2px"></div>
              <div style="width:22px;height:4px;background:rgba(74,154,122,0.3);border-radius:2px"></div>
            </div>
          </div>
          <div style="font-size:10px;color:var(--text-dim);margin-top:10px;line-height:1.6">
            Chooses between<br>Ego &amp; Holy Spirit
          </div>
          <div style="margin-top:10px;font-size:18px">
            <span style="color:#c06060">←</span>&nbsp;<span style="color:#4a9a7a">→</span>
          </div>
        </div>

        <!-- Right Mind -->
        <div style="background:rgba(74,154,122,0.08);border:1px solid rgba(74,154,122,0.35);border-top:3px solid #4a9a7a;border-radius:8px;padding:14px">
          <div style="font-size:12px;font-weight:bold;color:#4a9a7a;margin-bottom:2px">Right Mind</div>
          <div style="font-size:11px;color:rgba(74,154,122,0.7);font-style:italic;margin-bottom:10px">Holy Spirit</div>
          <div style="font-size:11px;color:var(--text-dim);line-height:2">
            &bull; Atonement<br>&bull; Forgiveness<br>&bull; Healing<br>&bull; Miracles<br>&bull; Holy relationships
          </div>
        </div>

      </div>
    </div>

  </div>`;
}}

function buildConsciousChart() {{
  return `
  <div class="custom-chart">
    <p style="font-size:13px;color:var(--text-dim);margin-bottom:16px">
      The mind operates at three levels. The conscious mind is only the tip of the iceberg — the subconscious and unconscious hold the real programming.
    </p>
    <!-- Layered mind diagram -->
    <div style="border-radius:12px;overflow:hidden;border:1px solid rgba(201,168,76,0.2)">
      <!-- Conscious Mind -->
      <div style="background:rgba(74,100,154,0.25);border-bottom:2px solid rgba(74,100,154,0.5);padding:14px 16px">
        <div style="font-size:13px;font-weight:bold;color:#7090d0;margin-bottom:8px;letter-spacing:0.5px">▲ CONSCIOUS MIND</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;color:var(--text)">
          <div style="background:rgba(74,100,154,0.2);border-radius:5px;padding:6px 8px">💭 Short term memory</div>
          <div style="background:rgba(74,100,154,0.2);border-radius:5px;padding:6px 8px">⚡ Will Power <span style="color:var(--text-dim);font-size:10px">(ignored when emotional)</span></div>
          <div style="background:rgba(74,100,154,0.2);border-radius:5px;padding:6px 8px">🔢 Processes 5–7 pieces of info</div>
          <div style="background:rgba(74,100,154,0.2);border-radius:5px;padding:6px 8px">🎮 Tries to control behaviour</div>
        </div>
      </div>
      <!-- Subconscious Mind -->
      <div style="background:rgba(100,74,154,0.25);border-bottom:2px solid rgba(100,74,154,0.5);padding:14px 16px">
        <div style="font-size:13px;font-weight:bold;color:#a080d0;margin-bottom:4px;letter-spacing:0.5px">▼ SUBCONSCIOUS MIND <span style="font-size:11px;font-weight:normal;color:var(--text-dim)">50–60%</span></div>
        <div style="font-size:11px;color:var(--text-dim);margin-bottom:8px">Alpha / Theta Brain Waves · Hypnotherapy accesses this level</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;color:var(--text)">
          <div style="background:rgba(100,74,154,0.2);border-radius:5px;padding:6px 8px">💾 Long term &amp; permanent memory</div>
          <div style="background:rgba(100,74,154,0.2);border-radius:5px;padding:6px 8px">💪 More powerful than conscious</div>
          <div style="background:rgba(100,74,154,0.2);border-radius:5px;padding:6px 8px">🛡️ Behaviours &amp; Habits stored</div>
          <div style="background:rgba(100,74,154,0.2);border-radius:5px;padding:6px 8px">🔥 Strong emotions veto conscious</div>
        </div>
      </div>
      <!-- Programmed & Conditioned -->
      <div style="background:rgba(120,80,60,0.25);border-bottom:2px solid rgba(120,80,60,0.5);padding:14px 16px">
        <div style="font-size:13px;font-weight:bold;color:#c09060;margin-bottom:8px;letter-spacing:0.5px">▼ PROGRAMMED &amp; CONDITIONED RESPONSES</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;color:var(--text)">
          <div style="background:rgba(120,80,60,0.2);border-radius:5px;padding:6px 8px">📜 Belief System</div>
          <div style="background:rgba(120,80,60,0.2);border-radius:5px;padding:6px 8px">❤️ Emotions &amp; Feelings stored</div>
          <div style="background:rgba(120,80,60,0.2);border-radius:5px;padding:6px 8px">🎯 Values &amp; Attitudes</div>
          <div style="background:rgba(120,80,60,0.2);border-radius:5px;padding:6px 8px">✨ Creativity</div>
        </div>
      </div>
      <!-- Unconscious / Deep -->
      <div style="background:rgba(30,20,50,0.6);padding:14px 16px">
        <div style="font-size:13px;font-weight:bold;color:#8060a0;margin-bottom:8px;letter-spacing:0.5px">▼ UNCONSCIOUS / DEEP MIND</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;color:var(--text)">
          <div style="background:rgba(80,60,120,0.2);border-radius:5px;padding:6px 8px">🌌 Spiritual connections</div>
          <div style="background:rgba(80,60,120,0.2);border-radius:5px;padding:6px 8px">🔑 Core identity &amp; deep drives</div>
          <div style="background:rgba(80,60,120,0.2);border-radius:5px;padding:6px 8px;grid-column:span 2">💤 Delta Brain Waves · Deep sleep · Unconscious processing</div>
        </div>
      </div>
    </div>
    <div style="margin-top:8px;font-size:11px;color:var(--text-dim);text-align:right;padding-right:8px">— Gemma &amp; Bette Brain Waves</div>
  </div>`;
}}

function buildHeavenChart() {{
  return `
  <div class="custom-chart" style="padding:16px 12px">

    <!-- HEAVEN header -->
    <div style="background:linear-gradient(135deg,rgba(201,168,76,0.15),rgba(201,168,76,0.05));border:1px solid rgba(201,168,76,0.5);border-radius:10px;padding:14px 16px;margin-bottom:6px;text-align:center;box-shadow:0 0 20px rgba(201,168,76,0.1)">
      <div style="font-size:18px;font-weight:bold;color:#c9a84c;letter-spacing:2px;margin-bottom:6px">HEAVEN</div>
      <div style="font-size:11px;color:rgba(201,168,76,0.75);line-height:1.7">
        God &middot; Pure Non-duality &middot; Christ &middot; All-Inclusive Self &middot; Ineffable Spirit<br>
        Love &middot; Truth &middot; Perfection &middot; Changeless Creation<br>
        <span style="font-style:italic">Everything below is a purposive illusion &mdash; a dream of separation</span>
      </div>
    </div>

    <!-- Arrow down from Heaven -->
    <div style="text-align:center;color:rgba(201,168,76,0.4);font-size:18px;line-height:1.2;margin-bottom:4px">&#8595;</div>

    <!-- DECISION MAKER BLOCK -->
    <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.35);border-radius:10px;padding:12px 8px;margin-bottom:8px">

      <!-- Decision Maker label -->
      <div style="text-align:center;margin-bottom:10px">
        <span style="display:inline-block;background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.4);border-radius:6px;padding:6px 20px;font-size:13px;font-weight:bold;font-variant:small-caps;color:#c9a84c;letter-spacing:1.5px">Decision Maker</span>
      </div>

      <!-- Row 1: Denial of Innocence (red, pointing left) -->
      <div style="display:flex;align-items:center;margin-bottom:6px">
        <div style="position:relative;flex:1;display:flex;justify-content:center">
          <div style="background:rgba(192,96,96,0.85);border-radius:4px;padding:7px 14px 7px 22px;display:inline-flex;align-items:center;position:relative;max-width:100%">
            <div style="position:absolute;left:-10px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:12px solid transparent;border-bottom:12px solid transparent;border-right:10px solid rgba(192,96,96,0.85)"></div>
            <span style="font-size:11px;font-weight:600;color:#fff;white-space:nowrap">&larr; Denial of Innocence</span>
          </div>
        </div>
        <div style="width:1px;height:24px;background:rgba(201,168,76,0.3);margin:0 4px"></div>
        <div style="flex:1"></div>
      </div>

      <!-- Row 2: Denial of denial of Innocence (green, pointing right) -->
      <div style="display:flex;align-items:center;margin-bottom:10px">
        <div style="flex:1"></div>
        <div style="width:1px;height:24px;background:rgba(201,168,76,0.3);margin:0 4px"></div>
        <div style="position:relative;flex:1;display:flex;justify-content:center">
          <div style="background:rgba(74,154,122,0.85);border-radius:4px;padding:7px 22px 7px 14px;display:inline-flex;align-items:center;position:relative;max-width:100%">
            <span style="font-size:11px;font-weight:600;color:#fff;white-space:nowrap">Denial of denial of Innocence &rarr;</span>
            <div style="position:absolute;right:-10px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:12px solid transparent;border-bottom:12px solid transparent;border-left:10px solid rgba(74,154,122,0.85)"></div>
          </div>
        </div>
      </div>

      <!-- Thin divider -->
      <div style="height:1px;background:rgba(201,168,76,0.2);margin:0 20px 10px 20px"></div>

      <!-- Row 3: Differences are important (red, pointing left) -->
      <div style="display:flex;align-items:center;margin-bottom:6px">
        <div style="position:relative;flex:1;display:flex;justify-content:center">
          <div style="background:rgba(192,96,96,0.7);border-radius:4px;padding:6px 12px 6px 20px;display:inline-flex;align-items:center;position:relative;max-width:100%">
            <div style="position:absolute;left:-9px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:11px solid transparent;border-bottom:11px solid transparent;border-right:9px solid rgba(192,96,96,0.7)"></div>
            <span style="font-size:10px;color:#fff;font-style:italic">&larr; &ldquo;Differences are important.&rdquo;</span>
          </div>
        </div>
        <div style="width:1px;height:22px;background:rgba(201,168,76,0.2);margin:0 4px"></div>
        <div style="flex:1"></div>
      </div>

      <!-- Row 4: Sameness is important (green, pointing right) -->
      <div style="display:flex;align-items:center">
        <div style="flex:1"></div>
        <div style="width:1px;height:22px;background:rgba(201,168,76,0.2);margin:0 4px"></div>
        <div style="position:relative;flex:1;display:flex;justify-content:center">
          <div style="background:rgba(74,154,122,0.7);border-radius:4px;padding:6px 20px 6px 12px;display:inline-flex;align-items:center;position:relative;max-width:100%">
            <span style="font-size:10px;color:#fff;font-style:italic">&ldquo;Sameness is important.&rdquo; &rarr;</span>
            <div style="position:absolute;right:-9px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:11px solid transparent;border-bottom:11px solid transparent;border-left:9px solid rgba(74,154,122,0.7)"></div>
          </div>
        </div>
      </div>

    </div>

    <!-- Two-column body: EGO left, HOLY SPIRIT right -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px">

      <!-- EGO column -->
      <div style="border:1px solid rgba(192,96,96,0.35);border-radius:10px;overflow:hidden">
        <div style="background:rgba(192,96,96,0.15);border-bottom:2px solid rgba(192,96,96,0.4);padding:10px 14px;text-align:center">
          <div style="font-size:13px;font-weight:bold;color:#c06060;letter-spacing:1px">EGO</div>
          <div style="font-size:10px;color:rgba(192,96,96,0.7);font-style:italic">Wrong mind &middot; insanity</div>
        </div>
        <div style="padding:12px 14px">

          <!-- Cause -->
          <div style="margin-bottom:10px">
            <div style="font-size:10px;font-variant:small-caps;color:#c06060;letter-spacing:1px;margin-bottom:4px">Cause</div>
            <div style="font-size:11px;color:var(--text-dim);line-height:1.7">
              Split mind &middot; Content &middot; Special &middot; Love/hate &middot; Thoughts
            </div>
          </div>

          <!-- Core belief -->
          <div style="background:rgba(192,96,96,0.08);border-left:3px solid #c06060;border-radius:4px;padding:8px 10px;margin-bottom:12px">
            <div style="font-size:11px;color:#c06060;font-style:italic">&ldquo;Sin, guilt, fear are serious.&rdquo;</div>
          </div>

          <!-- Projected grievances label -->
          <div style="font-size:10px;color:rgba(192,96,96,0.8);text-align:center;margin-bottom:6px;font-style:italic">
            Projected grievances &middot; my condemnations<br>attacks are justified
          </div>

          <!-- Fragment / Project fan-down SVG -->
          <div style="text-align:center;margin:8px 0 12px 0">
            <svg width="160" height="85" viewBox="0 0 160 85" style="display:block;margin:0 auto">
              <circle cx="80" cy="10" r="8" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1.5"/>
              <line x1="80" y1="18" x2="16" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <line x1="80" y1="18" x2="40" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <line x1="80" y1="18" x2="64" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <line x1="80" y1="18" x2="96" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <line x1="80" y1="18" x2="120" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <line x1="80" y1="18" x2="144" y2="58" stroke="#c06060" stroke-width="1" opacity="0.6"/>
              <polygon points="16,58 12,50 20,50" fill="#c06060" opacity="0.7"/>
              <polygon points="40,58 36,50 44,50" fill="#c06060" opacity="0.7"/>
              <polygon points="64,58 60,50 68,50" fill="#c06060" opacity="0.7"/>
              <polygon points="96,58 92,50 100,50" fill="#c06060" opacity="0.7"/>
              <polygon points="120,58 116,50 124,50" fill="#c06060" opacity="0.7"/>
              <polygon points="144,58 140,50 148,50" fill="#c06060" opacity="0.7"/>
              <text x="80" y="38" text-anchor="middle" font-size="8" fill="rgba(192,96,96,0.5)" letter-spacing="2" font-family="inherit">Fragment</text>
              <text x="80" y="48" text-anchor="middle" font-size="8" fill="rgba(192,96,96,0.5)" letter-spacing="2" font-family="inherit">Project</text>
              <rect x="9" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
              <rect x="33" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
              <rect x="57" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
              <rect x="89" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
              <rect x="113" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
              <rect x="137" y="60" width="14" height="14" rx="2" fill="rgba(192,96,96,0.45)" stroke="#c06060" stroke-width="1"/>
            </svg>
          </div>

          <!-- Prison -->
          <div style="background:rgba(192,96,96,0.06);border:1px dashed rgba(192,96,96,0.25);border-radius:6px;padding:8px 10px;margin-bottom:10px">
            <div style="font-size:10px;color:rgba(192,96,96,0.7);font-style:italic">Ego doesn&rsquo;t tolerate looking outside its prison walls</div>
            <div style="font-size:10px;color:var(--text-dim);margin-top:4px">Special love/hate objects &mdash; &ldquo;wheel of misfortune&rdquo;</div>
          </div>

          <!-- Effect -->
          <div>
            <div style="font-size:10px;font-variant:small-caps;color:#c06060;letter-spacing:1px;margin-bottom:4px">Effect</div>
            <div style="font-size:11px;color:var(--text-dim);line-height:1.8">
              Mindlessness &middot; Form &middot; Space &middot; Time<br>Individuality &middot; Duality
            </div>
          </div>

        </div>
      </div>

      <!-- HOLY SPIRIT column -->
      <div style="border:1px solid rgba(74,154,122,0.35);border-radius:10px;overflow:hidden">
        <div style="background:rgba(74,154,122,0.15);border-bottom:2px solid rgba(74,154,122,0.4);padding:10px 14px;text-align:center">
          <div style="font-size:13px;font-weight:bold;color:#4a9a7a;letter-spacing:1px">HOLY SPIRIT</div>
          <div style="font-size:10px;color:rgba(74,154,122,0.7);font-style:italic">Right mind &middot; sanity</div>
        </div>
        <div style="padding:12px 14px">

          <!-- Core belief -->
          <div style="background:rgba(74,154,122,0.08);border-left:3px solid #4a9a7a;border-radius:4px;padding:8px 10px;margin-bottom:12px">
            <div style="font-size:11px;color:#4a9a7a;font-style:italic">&ldquo;Error is just silly.&rdquo;</div>
          </div>

          <!-- Forgiving thoughts label -->
          <div style="font-size:10px;color:rgba(74,154,122,0.8);text-align:center;margin-bottom:6px;font-style:italic">
            Forgiving thoughts<br>these are my calls for lovingkindness
          </div>

          <!-- Generalise / Extend fan-up SVG -->
          <div style="text-align:center;margin:8px 0 12px 0">
            <svg width="160" height="85" viewBox="0 0 160 85" style="display:block;margin:0 auto">
              <circle cx="80" cy="10" r="8" fill="rgba(74,154,122,0.25)" stroke="#4a9a7a" stroke-width="1.5"/>
              <line x1="16" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <line x1="40" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <line x1="64" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <line x1="96" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <line x1="120" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <line x1="144" y1="72" x2="80" y2="18" stroke="#4a9a7a" stroke-width="1" opacity="0.6"/>
              <polygon points="80,18 76,26 84,26" fill="#4a9a7a" opacity="0.7"/>
              <text x="80" y="40" text-anchor="middle" font-size="8" fill="rgba(74,154,122,0.6)" letter-spacing="2" font-family="inherit">Generalize</text>
              <text x="80" y="50" text-anchor="middle" font-size="8" fill="rgba(74,154,122,0.6)" letter-spacing="2" font-family="inherit">Extend</text>
              <rect x="9" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="33" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="57" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="89" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="113" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="137" y="60" width="14" height="14" rx="2" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
            </svg>
          </div>

          <!-- Forgiveness -->
          <div style="background:linear-gradient(135deg,rgba(74,154,122,0.08),rgba(201,168,76,0.05));border:1px solid rgba(74,154,122,0.25);border-radius:6px;padding:8px 10px;margin-bottom:10px">
            <div style="font-size:11px;color:#4a9a7a;font-style:italic">Forgiveness awakens us from dreams of separation</div>
            <div style="font-size:10px;color:var(--text-dim);margin-top:4px">Forgivable classmates &mdash; others are calling for lovingkindness</div>
          </div>

          <!-- Denial of denial -->
          <div style="background:rgba(74,154,122,0.1);border:1px solid rgba(74,154,122,0.25);border-radius:6px;padding:8px 10px">
            <div style="font-size:11px;font-weight:600;color:#4a9a7a">Denial of Denial of Innocence</div>
            <div style="font-size:10px;color:rgba(74,154,122,0.7);margin-top:2px;font-style:italic">restoring innocence</div>
          </div>

        </div>
      </div>

    </div>

    <!-- Footer -->
    <div style="margin-top:14px;font-size:10px;color:var(--text-dim);text-align:right;font-style:italic">
      &mdash; Workbook Lesson 138 &middot; Michael Dawson, 1993
    </div>

  </div>`;
}}
function toggleRef(id) {{ document.getElementById(id).classList.toggle('expanded'); }}

// ============================================================
// PHOTO ZOOM
// ============================================================
const photoZoomState = {{}};

function initPhotoZoom(id) {{
  const wrap = document.getElementById(id);
  if (!wrap) return;
  const img = wrap.querySelector('.photo-chart-img');
  const state = photoZoomState[id];

  // Mouse drag
  wrap.addEventListener('mousedown', e => {{
    state.dragging = true; state.startX = e.clientX; state.startY = e.clientY;
    state.startTx = state.tx; state.startTy = state.ty;
    e.preventDefault();
  }});
  window.addEventListener('mousemove', e => {{
    if (!state.dragging) return;
    state.tx = state.startTx + (e.clientX - state.startX);
    state.ty = state.startTy + (e.clientY - state.startY);
    applyPhotoTransform(id);
  }});
  window.addEventListener('mouseup', () => {{ state.dragging = false; }});

  // Touch drag
  let lastDist = 0;
  wrap.addEventListener('touchstart', e => {{
    if (e.touches.length === 1) {{
      state.dragging = true;
      state.startX = e.touches[0].clientX; state.startY = e.touches[0].clientY;
      state.startTx = state.tx; state.startTy = state.ty;
    }} else if (e.touches.length === 2) {{
      lastDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
    }}
  }}, {{passive: true}});
  wrap.addEventListener('touchmove', e => {{
    if (e.touches.length === 1 && state.dragging) {{
      state.tx = state.startTx + (e.touches[0].clientX - state.startX);
      state.ty = state.startTy + (e.touches[0].clientY - state.startY);
      applyPhotoTransform(id);
    }} else if (e.touches.length === 2) {{
      const dist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      if (lastDist > 0) {{
        state.scale = Math.max(0.5, Math.min(5, state.scale * (dist / lastDist)));
        applyPhotoTransform(id);
      }}
      lastDist = dist;
    }}
    e.preventDefault();
  }}, {{passive: false}});
  wrap.addEventListener('touchend', () => {{ state.dragging = false; lastDist = 0; }});
}}

function applyPhotoTransform(id) {{
  const wrap = document.getElementById(id);
  if (!wrap) return;
  const img = wrap.querySelector('.photo-chart-img');
  const state = photoZoomState[id];
  img.style.transform = `translate(${{state.tx}}px, ${{state.ty}}px) scale(${{state.scale}})`;
  let labelEl = document.getElementById(id.replace('pz-', 'pzl-'));
  if (!labelEl && id === 'hz-wrap') labelEl = document.getElementById('hz-label');
  if (labelEl) labelEl.textContent = Math.round(state.scale * 100) + '%';
}}

function photoZoomIn(id, e) {{
  e.stopPropagation();
  const state = photoZoomState[id];
  if (!state) return;
  state.scale = Math.min(5, state.scale * 1.3);
  applyPhotoTransform(id);
}}

function photoZoomOut(id, e) {{
  e.stopPropagation();
  const state = photoZoomState[id];
  if (!state) return;
  state.scale = Math.max(0.3, state.scale / 1.3);
  applyPhotoTransform(id);
}}

function photoZoomReset(id, e) {{
  e.stopPropagation();
  const state = photoZoomState[id];
  if (!state) return;
  state.scale = 1; state.tx = 0; state.ty = 0;
  applyPhotoTransform(id);
}}

// ============================================================
// CHARTS MODAL (chart1/chart2 with zoom)
// ============================================================
function openCharts() {{
  document.getElementById('charts-modal').classList.add('open');
  chartZoom = 1.0;
}}
function closeCharts() {{ document.getElementById('charts-modal').classList.remove('open'); }}
function toggleChartsDropdown() {{
  const dd = document.getElementById('charts-dropdown');
  const isOpen = dd.style.display !== 'none';
  dd.style.display = isOpen ? 'none' : 'block';
  // close on outside click
  if (!isOpen) {{
    setTimeout(() => document.addEventListener('click', function closeDD(e) {{
      if (!document.getElementById('charts-tab-trigger').contains(e.target)) {{
        dd.style.display = 'none';
        document.removeEventListener('click', closeDD);
      }}
    }}), 10);
  }}
}}
function openChartsTab(idx) {{
  document.getElementById('charts-dropdown').style.display = 'none';
  openCharts();
  // switch to the correct tab
  const tabs = document.querySelectorAll('.charts-tab');
  tabs.forEach((t, i) => t.classList.toggle('active', i === idx));
  const frames = document.querySelectorAll('.charts-frame');
  frames.forEach((f, i) => f.classList.toggle('active', i === idx));
}}

function switchChartTab(idx, el) {{
  activeChartIdx = idx;
  document.querySelectorAll('.charts-tab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('.charts-frame').forEach((f, i) => f.classList.toggle('active', i === idx));
  chartZoom = 1.0;
  applyChartZoom();
}}

function applyChartZoom() {{
  const iframe = document.getElementById('ciframe-' + activeChartIdx);
  if (!iframe) return;
  try {{
    const doc = iframe.contentDocument || iframe.contentWindow.document;
    doc.body.style.zoom = chartZoom;
  }} catch(e) {{
    // cross-origin fallback: use CSS transform on iframe
    iframe.style.transform = `scale(${{chartZoom}})`;
    iframe.style.transformOrigin = '0 0';
    iframe.style.width = (100 / chartZoom) + '%';
    iframe.style.height = (100 / chartZoom) + '%';
  }}
}}

function zoomChart(factor) {{
  chartZoom = Math.max(0.3, Math.min(4, chartZoom * factor));
  applyChartZoom();
}}

function resetChartZoom() {{
  chartZoom = 1.0;
  applyChartZoom();
}}

let heavenZoomScale = 1.0;
function heavenZoom(factor) {{
  const scroller = document.getElementById('hz-scroll');
  const wrap = document.getElementById('hz-wrap');
  if (!scroller || !wrap) return;

  const oldScale = heavenZoomScale;
  if (factor === 0) {{
    heavenZoomScale = 1.0;
  }} else {{
    heavenZoomScale = Math.max(0.4, Math.min(4, heavenZoomScale * factor));
  }}

  // Find the reference panel scroll container (the parent that scrolls vertically)
  const refPanel = scroller.closest('.ref-body') || scroller.parentElement;
  const refScroller = refPanel ? refPanel.closest('[style*="overflow"]') || document.querySelector('#tab-reference') : null;

  // Preserve scroll ratios
  const sLeft = scroller.scrollLeft;
  const sTop = scroller.scrollTop;
  const cw = scroller.clientWidth;
  const ch = scroller.clientHeight;
  // Center point in content coordinates at old scale
  const cx = (sLeft + cw / 2) / oldScale;
  const cy = (sTop + ch / 2) / oldScale;

  wrap.style.transform = `scale(${{heavenZoomScale}})`;

  // Adjust scroll to keep the same center point
  requestAnimationFrame(() => {{
    scroller.scrollLeft = cx * heavenZoomScale - cw / 2;
    scroller.scrollTop = cy * heavenZoomScale - ch / 2;
  }});

  const label = document.getElementById('hz-label');
  if (label) label.textContent = Math.round(heavenZoomScale * 100) + '%';
}}

let dawsonZoomScale = 1.0;
function dawsonZoom(factor) {{
  if (factor === 0) {{
    dawsonZoomScale = 1.0;
  }} else {{
    dawsonZoomScale = Math.max(0.4, Math.min(4, dawsonZoomScale * factor));
  }}
  const wrap = document.getElementById('dawson-zoom-wrap');
  if (wrap) wrap.style.transform = `scale(${{dawsonZoomScale}})`;
  const label = document.getElementById('dawson-zoom-label');
  if (label) label.textContent = Math.round(dawsonZoomScale * 100) + '%';
}}

// ============================================================
// UTILS
// ============================================================
function escHtml(str) {{
  if (!str) return '';
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2200);
}}

// ============================================================
// INIT
// ============================================================

// Delegated click handler for breadcrumb "Back to Review" buttons
// This fires on the library-list container so it works even after DOM re-renders
document.getElementById('library-list').addEventListener('click', function(e) {{
  const btn = e.target.closest('.back-to-review-btn');
  if (btn) {{
    e.stopPropagation();
    e.preventDefault();
    const revNum = parseInt(btn.getAttribute('data-review-num'), 10);
    if (revNum) {{
      jumpBackToReview(revNum);
    }}
    return;
  }}
}}, true);


// PWA Install
let deferredPrompt = null;
window.addEventListener("beforeinstallprompt", (e) => {{
  e.preventDefault(); deferredPrompt = e;
  const b = document.getElementById("btn-install");
  if (b) b.style.display = "";
}});
window.addEventListener("appinstalled", () => {{
  deferredPrompt = null;
  const b = document.getElementById("btn-install");
  if (b) b.style.display = "none";
}});
function installApp() {{
  if (deferredPrompt) {{
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(() => {{ deferredPrompt = null; }});
  }} else {{
    showToast("In Safari: tap Share then Add to Home Screen");
  }}
}}
initSplash();
renderCard();
</script>
</body>
</html>"""

# Write the output
out_path = '/home/ubuntu/acim_flashcards/acim_companion.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize(out_path)
print(f"Written: {out_path}")
print(f"File size: {size:,} bytes ({size/1024/1024:.1f} MB)")
