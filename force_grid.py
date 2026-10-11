import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# LA GRIGLIA HARDCODED (Immune ai bug del CSS)
bulletproof_contacts = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content" style="width: 100%; max-width: 42rem; margin: 0 auto; color: #111;">
  
  <!-- Header -->
  <div style="margin-bottom: 2rem; border-bottom: 1px solid #222; padding-bottom: 1rem;">
    <span style="font-family: monospace; font-size: 9px; color: #b3a082; letter-spacing: 0.15em; text-transform: uppercase; display: block; margin-bottom: 0.5rem;">COMMUNICATION CHANNELS //</span>
    <h2 style="font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: bold; color: #111; text-transform: uppercase; margin: 0;">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <!-- Contenitore a Righe (Flexbox Forzato) -->
  <div style="display: flex; flex-direction: column; width: 100%;">
    
    <!-- Riga 1: EMAIL -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eee; text-decoration: none; color: #111;">
      <span style="font-family: monospace; font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 0.05em;">EMAIL DIRECT //</span>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111; text-transform: uppercase;">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- Riga 2: INSTAGRAM (Forzato a capo dal flex-direction: column) -->
    <a href="https://instagram.com/imlandmonterosa" target="_blank" rel="noopener noreferrer" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eee; text-decoration: none; color: #111;">
      <span style="font-family: monospace; font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 0.05em;">INSTAGRAM DIRECT //</span>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111; text-transform: uppercase;">@IMLANDMONTEROSA ↗</span>
    </a>

    <!-- Riga 3: OSSERVATORIO -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 1.25rem 0; border-bottom: 1px solid #eee; text-decoration: none; color: #111;">
      <div style="display: flex; flex-direction: column;">
        <span style="font-family: monospace; font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">OSSERVATORIO / SHOWROOM //</span>
        <span style="font-family: monospace; font-size: 9px; color: #b3a082; font-weight: bold; text-transform: uppercase;">(SU APPUNTAMENTO)</span>
      </div>
      <span style="font-family: monospace; font-size: 10px; font-weight: bold; color: #111; text-transform: uppercase;">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>

  </div>
</div>'''

# Troviamo l'inizio della sezione contatti
pos = content.find("CONNETTITI CON L'ARCHIVIO")
if pos != -1:
    start = content.rfind('<div class="brand-panel-content"', 0, pos)
    if start == -1:
        start = content.rfind('<div id="contacts-content"', 0, pos)
    if start == -1:
        start = content.rfind('<div', 0, pos)

    if start != -1:
        # Troviamo la fine del contenitore madre contando i div
        depth = 0
        i = start
        end = -1
        while i < len(content):
            if content[i:].startswith('<div'):
                depth += 1
                i += 4
            elif content[i:].startswith('</div'):
                depth -= 1
                if depth == 0:
                    end = i + 6
                    break
                i += 6
            else:
                i += 1
        
        if end != -1:
            # Sostituzione chirurgica del blocco malformato
            content = content[:start] + bulletproof_contacts + content[end:]
            print("✅ Modale Contatti piallata e ricostruita con Geometria Assoluta.")

# Aggiungiamo un hover effect minimale e infallibile
hover_css = '''
  <style>
    #contacts-content a:hover span:last-child { color: #b3a082 !important; }
  </style>
'''
if '#contacts-content a:hover' not in content:
    content = content.replace('</body>', hover_css + '\n</body>')

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
