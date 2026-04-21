NEW_HEAVEN = '''function buildHeavenChart() {{
  return `
  <div class="custom-chart" style="padding:16px 12px">

    <!-- HEAVEN header -->
    <div style="background:linear-gradient(135deg,rgba(201,168,76,0.15),rgba(201,168,76,0.05));border:1px solid rgba(201,168,76,0.5);border-radius:10px;padding:14px 16px;margin-bottom:4px;text-align:center;box-shadow:0 0 20px rgba(201,168,76,0.1)">
      <div style="font-size:18px;font-weight:bold;color:#c9a84c;letter-spacing:2px;margin-bottom:6px">HEAVEN</div>
      <div style="font-size:11px;color:rgba(201,168,76,0.75);line-height:1.7">
        God &middot; Pure Non-duality &middot; Christ &middot; All-Inclusive Self &middot; Ineffable Spirit<br>
        Love &middot; Truth &middot; Perfection &middot; Changeless Creation<br>
        <span style="font-style:italic">Everything below is a purposive illusion &mdash; a dream of separation</span>
      </div>
    </div>

    <!-- Arrow down from Heaven into the dream -->
    <div style="text-align:center;color:rgba(201,168,76,0.4);font-size:18px;line-height:1.2">&#8595;</div>

    <!-- DECISION MAKER pivot row -->
    <div style="position:relative;margin:0 0 4px 0">
      <!-- Left arrow: Denial of Innocence pointing LEFT -->
      <div style="display:flex;align-items:center;margin-bottom:6px">
        <div style="flex:1;height:32px;background:rgba(192,96,96,0.85);border-radius:4px 0 0 4px;display:flex;align-items:center;padding:0 10px;position:relative">
          <div style="position:absolute;left:-14px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:16px solid transparent;border-bottom:16px solid transparent;border-right:14px solid rgba(192,96,96,0.85)"></div>
          <span style="font-size:11px;font-weight:600;color:#fff;letter-spacing:0.3px">Denial of Innocence</span>
        </div>
        <div style="width:80px;background:rgba(201,168,76,0.15);border-top:1px solid rgba(201,168,76,0.4);border-bottom:1px solid rgba(201,168,76,0.4);height:32px;display:flex;align-items:center;justify-content:center">
          <span style="font-size:9px;font-variant:small-caps;color:#c9a84c;letter-spacing:0.5px">Decision<br>Maker</span>
        </div>
        <div style="flex:1;height:32px;background:rgba(74,154,122,0.15);border-radius:0 4px 4px 0;border:1px dashed rgba(74,154,122,0.2)"></div>
      </div>
      <!-- Right arrow: Denial of denial of Innocence pointing RIGHT -->
      <div style="display:flex;align-items:center">
        <div style="flex:1;height:32px;background:rgba(192,96,96,0.08);border-radius:4px 0 0 4px;border:1px dashed rgba(192,96,96,0.2)"></div>
        <div style="width:80px;background:rgba(201,168,76,0.15);border-top:1px solid rgba(201,168,76,0.4);border-bottom:1px solid rgba(201,168,76,0.4);height:32px;display:flex;align-items:center;justify-content:center">
          <span style="font-size:9px;font-variant:small-caps;color:#c9a84c;letter-spacing:0.5px">Decision<br>Maker</span>
        </div>
        <div style="flex:1;height:32px;background:rgba(74,154,122,0.85);border-radius:0 4px 4px 0;display:flex;align-items:center;justify-content:flex-end;padding:0 10px;position:relative">
          <span style="font-size:11px;font-weight:600;color:#fff;letter-spacing:0.3px">Denial of denial of Innocence</span>
          <div style="position:absolute;right:-14px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:16px solid transparent;border-bottom:16px solid transparent;border-left:14px solid rgba(74,154,122,0.85)"></div>
        </div>
      </div>
    </div>

    <!-- Differences / Sameness arrows -->
    <div style="margin-bottom:4px">
      <div style="display:flex;align-items:center;margin-bottom:6px">
        <div style="flex:1;height:28px;background:rgba(192,96,96,0.75);border-radius:4px 0 0 4px;display:flex;align-items:center;padding:0 10px;position:relative">
          <div style="position:absolute;left:-12px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:14px solid transparent;border-bottom:14px solid transparent;border-right:12px solid rgba(192,96,96,0.75)"></div>
          <span style="font-size:11px;color:#fff;font-style:italic">&ldquo;Differences are important.&rdquo;</span>
        </div>
        <div style="width:80px;height:28px;background:rgba(201,168,76,0.08);border-top:1px solid rgba(201,168,76,0.3);border-bottom:1px solid rgba(201,168,76,0.3)"></div>
        <div style="flex:1;height:28px;background:rgba(74,154,122,0.08);border-radius:0 4px 4px 0;border:1px dashed rgba(74,154,122,0.15)"></div>
      </div>
      <div style="display:flex;align-items:center">
        <div style="flex:1;height:28px;background:rgba(192,96,96,0.08);border-radius:4px 0 0 4px;border:1px dashed rgba(192,96,96,0.15)"></div>
        <div style="width:80px;height:28px;background:rgba(201,168,76,0.08);border-top:1px solid rgba(201,168,76,0.3);border-bottom:1px solid rgba(201,168,76,0.3)"></div>
        <div style="flex:1;height:28px;background:rgba(74,154,122,0.75);border-radius:0 4px 4px 0;display:flex;align-items:center;justify-content:flex-end;padding:0 10px;position:relative">
          <span style="font-size:11px;color:#fff;font-style:italic">&ldquo;Sameness is important.&rdquo;</span>
          <div style="position:absolute;right:-12px;top:50%;transform:translateY(-50%);width:0;height:0;border-top:14px solid transparent;border-bottom:14px solid transparent;border-left:12px solid rgba(74,154,122,0.75)"></div>
        </div>
      </div>
    </div>

    <!-- Two-column body: EGO left, HOLY SPIRIT right -->
    <div style="display:grid;grid-template-columns:1fr 80px 1fr;gap:0;align-items:start;margin-top:8px">

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
          <div style="text-align:center;margin-bottom:10px">
            <svg width="140" height="80" viewBox="0 0 140 80" style="overflow:visible">
              <!-- Source node at top centre -->
              <circle cx="70" cy="8" r="7" fill="rgba(192,96,96,0.6)" stroke="#c06060" stroke-width="1.5"/>
              <!-- Fan lines going down to 6 boxes -->
              <line x1="70" y1="15" x2="10" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <line x1="70" y1="15" x2="34" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <line x1="70" y1="15" x2="58" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <line x1="70" y1="15" x2="82" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <line x1="70" y1="15" x2="106" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <line x1="70" y1="15" x2="130" y2="55" stroke="#c06060" stroke-width="1.2" opacity="0.7"/>
              <!-- Arrowheads -->
              <polygon points="10,55 6,47 14,47" fill="#c06060" opacity="0.8"/>
              <polygon points="34,55 30,47 38,47" fill="#c06060" opacity="0.8"/>
              <polygon points="58,55 54,47 62,47" fill="#c06060" opacity="0.8"/>
              <polygon points="82,55 78,47 86,47" fill="#c06060" opacity="0.8"/>
              <polygon points="106,55 102,47 110,47" fill="#c06060" opacity="0.8"/>
              <polygon points="130,55 126,47 134,47" fill="#c06060" opacity="0.8"/>
              <!-- Label: Fragment -->
              <text x="70" y="36" text-anchor="middle" font-size="9" fill="rgba(192,96,96,0.6)" letter-spacing="3" font-family="monospace">Fragment</text>
              <!-- Label: Project -->
              <text x="70" y="48" text-anchor="middle" font-size="9" fill="rgba(192,96,96,0.6)" letter-spacing="3" font-family="monospace">Project</text>
              <!-- Bottom boxes (filled) -->
              <rect x="3" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
              <rect x="27" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
              <rect x="51" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
              <rect x="75" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
              <rect x="99" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
              <rect x="123" y="57" width="14" height="14" fill="rgba(192,96,96,0.5)" stroke="#c06060" stroke-width="1"/>
            </svg>
          </div>

          <!-- Prison / wheel of misfortune -->
          <div style="background:rgba(192,96,96,0.08);border:1px dashed rgba(192,96,96,0.3);border-radius:6px;padding:8px 10px;margin-bottom:10px">
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

      <!-- Centre divider -->
      <div style="display:flex;flex-direction:column;align-items:center;padding:8px 0;height:100%">
        <div style="width:1px;flex:1;background:linear-gradient(to bottom,rgba(201,168,76,0.5),rgba(201,168,76,0.1))"></div>
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
          <div style="text-align:center;margin-bottom:10px">
            <svg width="140" height="80" viewBox="0 0 140 80" style="overflow:visible">
              <!-- Top destination node -->
              <circle cx="70" cy="8" r="7" fill="rgba(74,154,122,0.3)" stroke="#4a9a7a" stroke-width="1.5"/>
              <!-- Fan lines going UP from 6 boxes -->
              <line x1="10" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <line x1="34" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <line x1="58" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <line x1="82" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <line x1="106" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <line x1="130" y1="65" x2="70" y2="15" stroke="#4a9a7a" stroke-width="1.2" opacity="0.7"/>
              <!-- Arrowheads pointing UP toward centre -->
              <polygon points="70,15 66,23 74,23" fill="#4a9a7a" opacity="0.8"/>
              <!-- Label: Generalize -->
              <text x="70" y="36" text-anchor="middle" font-size="9" fill="rgba(74,154,122,0.7)" letter-spacing="2" font-family="monospace">Generalize</text>
              <!-- Label: Extend -->
              <text x="70" y="48" text-anchor="middle" font-size="9" fill="rgba(74,154,122,0.7)" letter-spacing="4" font-family="monospace">Extend</text>
              <!-- Bottom boxes (open) -->
              <rect x="3" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="27" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="51" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="75" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="99" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
              <rect x="123" y="66" width="14" height="14" fill="none" stroke="#4a9a7a" stroke-width="1.2"/>
            </svg>
          </div>

          <!-- Forgiveness awakens -->
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

print(NEW_HEAVEN[:200])
