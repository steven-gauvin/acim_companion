#!/usr/bin/env python3
"""Add 'Install' button to the app header with iOS instructions fallback."""

with open('/home/ubuntu/acim_flashcards/build_html.py', 'r') as f:
    content = f.read()

# 1. Add the install button next to the Charts button in the header
old_header = '    <button class="header-btn" onclick="openCharts()">&#8862; Charts</button>'
new_header = (
    '    <div style="display:flex;gap:6px;align-items:center">\n'
    '      <button class="header-btn" id="btn-install" onclick="installApp()" style="display:none">&#8962; Install</button>\n'
    '      <button class="header-btn" onclick="openCharts()">&#8862; Charts</button>\n'
    '    </div>'
)
if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header button replaced OK")
else:
    print("ERROR: header button not found")

# 2. Add PWA JS before the closing script tag
pwa_js = (
    '\n// PWA Install\n'
    'let deferredPrompt = null;\n'
    'window.addEventListener("beforeinstallprompt", (e) => {{\n'
    '  e.preventDefault(); deferredPrompt = e;\n'
    '  const b = document.getElementById("btn-install");\n'
    '  if (b) b.style.display = "";\n'
    '}});\n'
    'window.addEventListener("appinstalled", () => {{\n'
    '  deferredPrompt = null;\n'
    '  const b = document.getElementById("btn-install");\n'
    '  if (b) b.style.display = "none";\n'
    '}});\n'
    'function installApp() {{\n'
    '  if (deferredPrompt) {{\n'
    '    deferredPrompt.prompt();\n'
    '    deferredPrompt.userChoice.then(() => {{ deferredPrompt = null; }});\n'
    '  }} else {{\n'
    '    showToast("In Safari: tap Share then Add to Home Screen");\n'
    '  }}\n'
    '}}\n'
)

old_end = 'initSplash();\nrenderCard();\n</script>'
new_end = pwa_js + 'initSplash();\nrenderCard();\n</script>'
if old_end in content:
    content = content.replace(old_end, new_end)
    print("PWA JS added OK")
else:
    print("ERROR: script end not found")

with open('/home/ubuntu/acim_flashcards/build_html.py', 'w') as f:
    f.write(content)

print("Done!")
