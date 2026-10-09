import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# TRASMUTAZIONE 1: Conversione Bottoni in Link Mailto Operativi
old_btn = r'<button class="btn-product-action font-mono-tech"[^>]*>\{prod\.status\}</button>'
new_btn = r'<a href={prod.mailto} class="btn-product-action font-mono-tech" style="text-decoration:none; text-align:center; display:block; width:100%; transition: all 0.3s ease;">{prod.status}</a>'
content = re.sub(old_btn, new_btn, content)

# TRASMUTAZIONE 2: Sostituzione Sicura della Sezione Contatti
new_contacts_block = '''<div class="brand-panel-content p-6" id="contacts-content">
          <div class="mb-8 border-b border-[#222] pb-6">
            <h3 class="font-syne text-sm uppercase tracking-widest text-[#555] mb-2">HEADQUARTER // CAMPO BASE</h3>
            <h2 class="font-syne text-2xl font-bold tracking-tight text-[#111]">L'OSSERVATORIO IMLAND</h2>
            <p class="font-mono-tech text-xs text-[#666] mt-2 tracking-wider">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</p>
            <p class="font-inter text-sm text-[#444] mt-4 leading-relaxed">
              Il nostro campo base operativo nel cuore di Alagna. L'Atelier non vive solo nello spazio digitale: è uno studio di creazione e materia. È possibile visionare, toccare e provare fisicamente le collezioni direttamente in sede, esclusivamente su appuntamento.
            </p>
          </div>
          <div class="flex flex-col gap-4">
            <div class="py-4 border-b border-[#ddd]">
                <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex justify-between items-center hover:text-[#000] text-[#555] transition-colors text-decoration-none">
                  <span class="font-mono-tech text-xs tracking-wider">VISITA L'ATELIER (SU APPUNTAMENTO) //</span>
                  <span class="font-syne text-sm font-bold">IMLANDMOTEROSA@GMAIL.COM ↗</span>
                </a>
                <p class="font-mono-tech text-[10px] text-[#888] mt-2 tracking-widest">SHOWROOM: VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</p>
            </div>
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex justify-between items-center py-4 border-b border-[#ddd] hover:text-[#000] text-[#555] transition-colors text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider">COLLAB & PRESS //</span>
              <span class="font-syne text-sm font-bold">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

# Se la sezione esiste la sostituiamo, altrimenti la iniettiamo nel pannello dedicato
if 'id="contacts-content"' in content:
    pattern = r'<div[^>]*id="contacts-content"[^>]*>.*?</div>\s*</div>'
    content = re.sub(pattern, new_contacts_block + '\n        </div>', content, flags=re.DOTALL)
    print("✅ Pannello Contatti sostituito con successo.")
else:
    # Iniezione di emergenza prima del closing tag del contenitore principale
    content = content.replace('</div>\n    </div>\n  </div>', new_contacts_block + '\n      </div>\n    </div>\n  </div>')
    print("✅ Pannello Contatti iniettato tramite fallback di sicurezza.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
