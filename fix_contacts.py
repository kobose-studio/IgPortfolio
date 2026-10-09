import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Struttura HTML aggiornata per il Campo Base e le Email
new_contacts_inner = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-8 border-b border-[#222] pb-6">
            <h3 class="font-syne text-sm uppercase tracking-widest text-[#555] mb-2">HEADQUARTER // CAMPO BASE</h3>
            <h2 class="font-syne text-2xl font-bold tracking-tight text-[#111]">L'OSSERVATORIO IMLAND</h2>
            <p class="font-inter text-sm text-[#444] mt-4 leading-relaxed">
              Il nostro campo base operativo. L'Atelier non è solo digitale: è uno spazio fisico di test e creazione. Per visionare e provare fisicamente la collezione, contattaci per fissare un appuntamento presso il nostro Osservatorio.
            </p>
          </div>
          <div class="flex flex-col gap-4">
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex justify-between items-center py-4 border-b border-[#ddd] hover:text-[#000] text-[#555] transition-colors text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider">VISITA L'ATELIER //</span>
              <span class="font-syne text-sm font-bold">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex justify-between items-center py-4 border-b border-[#ddd] hover:text-[#000] text-[#555] transition-colors text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider">COLLAB & PRESS //</span>
              <span class="font-syne text-sm font-bold">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

# Sostituiamo il blocco id="contacts-content"
pattern = r'<div class="brand-panel-content[^"]*" id="contacts-content".*?</div>\s*</div>'
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_contacts_inner, content, flags=re.DOTALL)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Contatti Campo Base/Osservatorio aggiornati con successo!")
else:
    print("⚠️ Impossibile trovare id='contacts-content'. Verificare la struttura.")
