import re

target_file = 'src/components/PortfolioSceneSphere.astro'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# ESTRATTO HTML RIGOROSO A 4 BOX (INLINE STYLES ANTI-BLU)
new_contacts_html = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content" style="color: #111111;">
  <!-- Header Pannello -->
  <div class="mb-6 border-b border-[#222] pb-4" style="border-bottom: 1px solid #222222; padding-bottom: 1rem; margin-bottom: 1.5rem;">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2" style="font-family: monospace; font-size: 9px; color: #b3a082; letter-spacing: 0.15em; text-transform: uppercase; display: block; margin-bottom: 0.5rem;">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-[#111] uppercase" style="font-size: 1.5rem; font-weight: bold; color: #111111; text-transform: uppercase; margin: 0;">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <!-- Griglia a 4 Righe con Bordi Puliti -->
  <div class="flex flex-col w-full divide-y divide-[#eee]" style="display: flex; flex-direction: column; width: 100%;">
    
    <!-- Row 1: EMAIL DIRECT -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 border-b border-[#eee] group" style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eeeeee; text-decoration: none !important; color: #111111 !important;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase" style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase group-hover:text-[#b3a082]" style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- Row 2: INSTAGRAM DIRECT -->
    <a href="https://instagram.com/imland.monterosa" target="_blank" rel="noopener" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 border-b border-[#eee] group" style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eeeeee; text-decoration: none !important; color: #111111 !important;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase" style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase group-hover:text-[#b3a082]" style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">@IMLAND.MONTEROSA ↗</span>
    </a>

    <!-- Row 3: PRESS & PR -->
    <a href="mailto:info.imland@gmail.com?subject=Press%20%26%20PR" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 border-b border-[#eee] group" style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eeeeee; text-decoration: none !important; color: #111111 !important;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase" style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">PRESS & PR //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase group-hover:text-[#b3a082]" style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">INFO.IMLAND@GMAIL.COM ↗</span>
    </a>

    <!-- Row 4: SHOWROOM / HEADQUARTER -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Showroom" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 border-b border-[#eee] group" style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eeeeee; text-decoration: none !important; color: #111111 !important;">
      <div style="display: flex; flex-direction: column;">
        <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase" style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">SHOWROOM / HEADQUARTER //</span>
        <span class="font-mono-tech text-[9px] text-[#b3a082] font-bold uppercase" style="font-family: monospace; font-size: 9px; color: #b3a082; font-weight: bold; text-transform: uppercase;">(SU APPUNTAMENTO)</span>
      </div>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase" style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase; margin-top: 0.25rem;">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>

  </div>
</div>'''

# Troviamo l'ancora madre e sostituiamo con conteggio di profondità
pos = content.find("CONNETTITI CON L'ARCHIVIO")
if pos != -1:
    start = content.rfind('<div class="brand-panel-content"', 0, pos)
    if start == -1:
        start = content.rfind('<div id="contacts-content"', 0, pos)
    if start == -1:
        start = content.rfind('<div', 0, pos)

    if start != -1:
        depth = 0
        i = start
        end = -1
        while i < len(content):
            if content.startswith('<div', i):
                depth += 1
                i += 4
            elif content.startswith('</div', i):
                depth -= 1
                if depth == 0:
                    end = i + 6
                    break
                i += 6
            else:
                i += 1

        if end != -1:
            content = content[:start] + new_contacts_html + content[end:]
            print("✅ Contatti sostituiti con successo.")

# Iniezione Regola Anti-Blu nello Style Scoped
anti_blue_css = '''
  /* OVERRIDE DEFINITIVO ANTI-BLU LINK */
  #contacts-content a, #contacts-content a:visited, #contacts-content a:hover, #contacts-content a:active {
    color: #111111 !important;
    text-decoration: none !important;
  }
  #contacts-content a:hover span:last-child {
    color: #b3a082 !important;
  }
</style>'''

if '</style>' in content:
    idx_style = content.rfind('</style>')
    content = content[:idx_style] + anti_blue_css + content[idx_style+8:]

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 Sostituzione conclusa.")
