import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- FIX 1: CAROSELLO (Taglio Netto) ---
# Elimina i vecchi stili
content = re.sub(r'/\* IMLAND.*?CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)
content = re.sub(r'/\* IMLAND STABILIZED TECH-CUT CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)

# HTML Carosello
html_carousel = '''{prod.images ? (
                  <div class="carousel-wrapper">
                    {prod.images.map((img, i) => (
                      <img src={img} alt={prod.title} class={`product-img cut-${prod.images.length}`} style={`animation-delay: ${i * 2.5}s;`} />
                    ))}
                  </div>
                ) : (
                  <img src={prod.image} alt={prod.title} class="product-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                )}'''
old_img = r'\{prod\.images \? \(.*?</div>\s*\)\s*:\s*\(.*?\)\}'
content = re.sub(old_img, html_carousel, content, flags=re.DOTALL)

# CSS Carosello
css_carousel = '''
  /* IMLAND STABILIZED TECH-CUT CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; background: #eaeaea; overflow: hidden; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; object-fit: cover; }
  
  .cut-5 { animation: cut5 12.5s infinite; }
  @keyframes cut5 { 0%, 19.9% { opacity: 1; } 20%, 100% { opacity: 0; } }
  
  .cut-3 { animation: cut3 7.5s infinite; }
  @keyframes cut3 { 0%, 33.2% { opacity: 1; } 33.3%, 100% { opacity: 0; } }
  
  .cut-1 { opacity: 1 !important; animation: none !important; }
</style>'''
content = content.replace('</style>', css_carousel)

# --- FIX 2: CONTATTI OSSERVATORIO ---
new_contacts = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
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
        </div>
      </div>
    </div>'''

# Troviamo e sostituiamo l'intero blocco contatti a prescindere dall'indentazione
pattern_contacts = r'<div class="brand-panel-content[^"]*" id="contacts-content".*?</div>\s*</div>\s*</div>'
content = re.sub(pattern_contacts, new_contacts, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Motore Astro Ricostruito: Caroselli e Contatti iniettati senza errori di Regex.")
