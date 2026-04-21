NEW_HEAVEN = '''function buildHeavenChart() {{
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
}}'''
