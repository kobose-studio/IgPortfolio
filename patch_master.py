import re
with open('src/components/PortfolioSceneSphere.astro', 'r', encoding='utf-8') as f:
    content = f.read()

# Stabilizzazione della Matematica dei Caroselli
content = re.sub(r'/\* IMLAND BRUTALIST.*?CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)

css_carousel = '''
  /* IMLAND STABILIZED TECH-CUT CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; background: #eaeaea; overflow: hidden; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; object-fit: cover; }
  
  /* 5 Immagini (15s Loop - Classic Hoodie) */
  .cut-5 { animation: cut5 15s infinite; }
  @keyframes cut5 { 0%, 19.9% { opacity: 1; } 20%, 100% { opacity: 0; } }
  
  /* 3 Immagini (9s Loop - Essentials) */
  .cut-3 { animation: cut3 9s infinite; }
  @keyframes cut3 { 0%, 33.2% { opacity: 1; } 33.3%, 100% { opacity: 0; } }
  
  /* 2 Immagini (6s Loop - Zip Hoodie) */
  .cut-2 { animation: cut2 6s infinite; }
  @keyframes cut2 { 0%, 49.9% { opacity: 1; } 50%, 100% { opacity: 0; } }
</style>'''
content = content.replace('</style>', css_carousel)

# Ripristino Sezione Contatti con Campo Base
old_contacts = r'<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">.*?</div>\s*</div>\s*</div>'
new_contacts = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-8 border-b border-[#222] pb-6">
            <h3 class="font-syne text-sm uppercase tracking-widest text-[#555] mb-2">HEADQUARTER // CAMPO BASE</h3>
            <h2 class="font-syne text-2xl font-bold tracking-tight text-[#111]">L'OSSERVATORIO IMLAND</h2>
            <p class="font-inter text-sm text-[#444] mt-4 leading-relaxed">
              Il nostro campo base operativo. L'Atelier non è solo digitale: è uno spazio fisico di test e creazione. Per visonare e provare fisicamente la collezione, contattaci per fissare un appuntamento presso il nostro Osservatorio.
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
        </div>
      </div>
    </div>'''

if re.search(old_contacts, content, flags=re.DOTALL):
    content = re.sub(old_contacts, new_contacts, content, flags=re.DOTALL)
else:
    print("ATTENZIONE: Blocco contatti non trovato, potrebbe essere stato modificato.")

with open('src/components/PortfolioSceneSphere.astro', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Moduli Astro Iniettati: Carosello Stabilizzato e Contatti Campo Base Ripristinati.")
