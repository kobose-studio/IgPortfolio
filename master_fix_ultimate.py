import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. GRIGLIA CONTATTI BLINDATA CON CSS INLINE (3 RIGHE PULITE)
bulletproof_contacts_html = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content" style="display: block !important; width: 100% !important; box-sizing: border-box !important;">
  <div style="margin-bottom: 1.5rem; border-bottom: 1px solid #222222; padding-bottom: 1rem;">
    <span style="font-family: monospace; font-size: 9px; color: #b3a082; letter-spacing: 0.15em; text-transform: uppercase; display: block; margin-bottom: 0.5rem;">COMMUNICATION CHANNELS //</span>
    <h2 style="font-size: 1.6rem; font-weight: 900; color: #111111; text-transform: uppercase; margin: 0; letter-spacing: -0.02em;">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <div style="display: flex !important; flex-direction: column !important; width: 100% !important; gap: 0.25rem !important;">
    <!-- ROW 1: EMAIL DIRECT -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" style="display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 1.1rem 0 !important; border-bottom: 1px solid #eeeeee !important; text-decoration: none !important; color: #111111 !important;">
      <span style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">EMAIL DIRECT //</span>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- ROW 2: INSTAGRAM DIRECT -->
    <a href="https://instagram.com/imlandmonterosa" target="_blank" rel="noopener noreferrer" style="display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 1.1rem 0 !important; border-bottom: 1px solid #eeeeee !important; text-decoration: none !important; color: #111111 !important;">
      <span style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">INSTAGRAM DIRECT //</span>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">@IMLANDMONTEROSA ↗</span>
    </a>

    <!-- ROW 3: OSSERVATORIO / SHOWROOM -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" style="display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 1.1rem 0 !important; border-bottom: 1px solid #eeeeee !important; text-decoration: none !important; color: #111111 !important;">
      <div style="display: flex; flex-direction: column;">
        <span style="font-family: monospace; font-size: 10px; color: #555555; text-transform: uppercase;">OSSERVATORIO / SHOWROOM //</span>
        <span style="font-family: monospace; font-size: 9px; color: #b3a082; font-weight: bold; text-transform: uppercase;">(SU APPUNTAMENTO)</span>
      </div>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111111; text-transform: uppercase;">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>
  </div>
</div>'''

# Sostituzione sicura della sezione contatti
pos = content.find("CONNETTITI CON L'ARCHIVIO")
if pos != -1:
    start = content.rfind('<div', 0, pos)
    depth = 0
    i = start
    end = -1
    while i < len(content):
        if content[i:].startswith('<div'): depth += 1; i += 4
        elif content[i:].startswith('</div'):
            depth -= 1
            if depth == 0: end = i + 6; break
            i += 6
        else: i += 1
    if end != -1:
        content = content[:start] + bulletproof_contacts_html + content[end:]
        print("✅ Griglia Contatti blindata con CSS inline installata.")

# B. ELEVAZIONE IMMAGINE 3D SU MOBILE & STILI RESPONSIVE
mobile_3d_elevation_css = '''
  /* OVERRIDE DEFINITIVO LINK CONTATTI */
  #contacts-content a:hover span { color: #b3a082 !important; }

  /* ELEVAZIONE IMMAGINE 3D SU MOBILE PER EVITARE SOVRAPPOSIZIONE CARD */
  @media (max-width: 768px) {
    /* Quando un'immagine viene aperta nel dettaglio, trasliamo il Canvas WebGL verso l'alto */
    canvas {
      transform: translateY(-8vh) !important;
      transition: transform 0.4s ease-out !important;
    }

    /* Manteniamo la card info compatta e ancorata in basso */
    #image-info-panel, .info-panel {
      max-height: 38vh !important;
      bottom: 1.5vh !important;
      overflow-y: auto !important;
    }
  }
</style>'''

idx_s = content.rfind('</style>')
if idx_s != -1:
    content = content[:idx_s] + mobile_3d_elevation_css + content[idx_s+8:]

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 SOSTITUZIONE E PATCH MOBILE COMPLETATE.")
