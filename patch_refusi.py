import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rinominiamo la voce di menu OUTDOOR GEAR in IMWEAR
content = content.replace('OUTDOOR GEAR', 'IMWEAR')

# 2. Struttura Contatti con Indirizzo Fisico Walser
new_contacts = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-8 border-b border-[#222] pb-6">
            <h3 class="font-syne text-sm uppercase tracking-widest text-[#555] mb-2">HEADQUARTER // CAMPO BASE</h3>
            <h2 class="font-syne text-2xl font-bold tracking-tight text-[#111]">L'OSSERVATORIO IMLAND</h2>
            <p class="font-mono-tech text-xs text-[#666] mt-2 tracking-wider">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</p>
            <p class="font-inter text-sm text-[#444] mt-4 leading-relaxed">
              Il nostro campo base operativo nel cuore di Alagna. L'Atelier non vive solo nello spazio digitale: è uno studio di creazione e materia. È possibile visionare, toccare e provare fisicamente le collezioni direttamente in sede, esclusivamente su appuntamento.
            </p>
          </div>
          <div class="flex flex-col gap-4">
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex justify-between items-center py-4 border-b border-[#ddd] hover:text-[#000] text-[#555] transition-colors text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider">VISITA L'ATELIER (SU APPUNTAMENTO) //</span>
              <span class="font-syne text-sm font-bold">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex justify-between items-center py-4 border-b border-[#ddd] hover:text-[#000] text-[#555] transition-colors text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider">COLLAB & PRESS //</span>
              <span class="font-syne text-sm font-bold">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

pattern_contacts = r'<div class="brand-panel-content[^"]*" id="contacts-content".*?</div>\s*</div>\s*</div>'
if re.search(pattern_contacts, content, flags=re.DOTALL):
    content = re.sub(pattern_contacts, new_contacts, content, flags=re.DOTALL)
    print("✅ Contatti aggiornati con indirizzo Walser!")
else:
    print("⚠️ Impossibile sostituire i contatti, applico sostituzione diretta del div.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Menu IMWEAR e descrizioni purificate con successo.")
