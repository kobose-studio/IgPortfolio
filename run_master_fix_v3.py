import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- FASE 1: PULIZIA E INIEZIONE CSS RESPONSIVE & CROSSFADE ---
content = re.sub(r'/\* IMLAND.*?\*/.*?</style>', '</style>', content, flags=re.DOTALL)

css_master = '''
  /* IMLAND DYNAMIC AXIS SYSTEM */
  header, nav, .nav-container, #main-nav {
    position: fixed !important;
    z-index: 9999 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
  }

  header a, nav a, .nav-container a {
    display: inline-block !important;
    letter-spacing: 0.15em !important;
    white-space: nowrap !important;
    color: #111 !important;
    transition: color 0.3s ease !important;
  }

  header a:hover, nav a:hover, .nav-container a:hover {
    color: #b3a082 !important;
  }

  /* DESKTOP (>=769px): Orizzontale al Centro in Alto */
  @media (min-width: 769px) {
    header, nav, .nav-container, #main-nav {
      top: 3rem !important;
      left: 50% !important;
      transform: translateX(-50%) rotate(0deg) !important;
      flex-direction: row !important;
      width: auto !important;
    }
    header a, nav a, .nav-container a {
      margin: 0 1.5rem !important;
      font-size: 11px !important;
    }
  }

  /* MOBILE (<=768px): Verticale Ancorato sul Margine Sinistro */
  @media (max-width: 768px) {
    header, nav, .nav-container, #main-nav {
      top: 50% !important;
      left: -120px !important;
      transform: translateY(-50%) rotate(-90deg) !important;
      transform-origin: center center !important;
      width: auto !important;
    }
    header a, nav a, .nav-container a {
      margin: 0 1rem !important;
      font-size: 11px !important;
    }
  }

  /* IMLAND SEAMLESS CROSSFADE CAROUSEL (Zero-Grey & Double Hold Duration) */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; background: #eaeaea; overflow: hidden; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; object-fit: cover; transition: transform 0.8s ease-in-out; }
  
  /* 7 Immagini (42s Loop - 6s per foto) */
  .kburns-7 { animation: kb7 42s infinite linear; }
  @keyframes kb7 { 
    0% { opacity: 0; transform: scale(1); }
    2% { opacity: 1; transform: scale(1.01); }
    14.28% { opacity: 1; transform: scale(1.04); }
    16.28% { opacity: 0; transform: scale(1.05); }
    100% { opacity: 0; transform: scale(1); }
  }

  /* 5 Immagini (30s Loop - 6s per foto) */
  .kburns-5 { animation: kb5 30s infinite linear; }
  @keyframes kb5 { 
    0% { opacity: 0; transform: scale(1); }
    2.5% { opacity: 1; transform: scale(1.01); }
    20% { opacity: 1; transform: scale(1.04); }
    22.5% { opacity: 0; transform: scale(1.05); }
    100% { opacity: 0; transform: scale(1); }
  }

  /* 4 Immagini (24s Loop - 6s per foto) */
  .kburns-4 { animation: kb4 24s infinite linear; }
  @keyframes kb4 { 
    0% { opacity: 0; transform: scale(1); }
    3% { opacity: 1; transform: scale(1.01); }
    25% { opacity: 1; transform: scale(1.04); }
    28% { opacity: 0; transform: scale(1.05); }
    100% { opacity: 0; transform: scale(1); }
  }

  /* 2 Immagini (12s Loop - 6s per foto) */
  .kburns-2 { animation: kb2 12s infinite linear; }
  @keyframes kb2 { 
    0% { opacity: 0; transform: scale(1); }
    5% { opacity: 1; transform: scale(1.01); }
    50% { opacity: 1; transform: scale(1.04); }
    55% { opacity: 0; transform: scale(1.05); }
    100% { opacity: 0; transform: scale(1); }
  }
</style>'''

content = content.replace('</style>', css_master)

# --- FASE 2: RINCALCOLO MATEMATICO DEL DELAY DEL CAROSELLO (6s per Step) ---
html_carousel = '''{prod.images ? (
                  <div class="carousel-wrapper">
                    {prod.images.map((img, i) => (
                      <img src={img} alt={prod.title} class={`product-img kburns-${prod.images.length}`} style={`animation-delay: ${i * 6}s;`} />
                    ))}
                  </div>
                ) : (
                  <img src={prod.image} alt={prod.title} class="product-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                )}'''
old_carousel_pattern = r'\{prod\.images \? \(.*?</div>\s*\)\s*:\s*\(.*?\)\}'
content = re.sub(old_carousel_pattern, html_carousel, content, flags=re.DOTALL)

# --- FASE 3: ERADICAZIONE CLONI E INIEZIONE GRID MANIFESTO CONTATTI ---
def get_div_bounds(text, start_idx):
    div_start = text.rfind('<div', 0, start_idx)
    if div_start == -1: return -1, -1
    count = 0
    i = div_start
    while i < len(text):
        if text.startswith('<div', i): count += 1
        elif text.startswith('</div', i):
            count -= 1
            if count == 0: return div_start, i + 6
        i += 1
    return -1, -1

# Eradicazione completa di tutti i vecchi div contatti duplicati
eradicated = 0
while True:
    idx = content.find('id="contacts-content"')
    if idx == -1: break
    s, e = get_div_bounds(content, idx)
    if s != -1 and e != -1:
        content = content[:s] + content[e:]
        eradicated += 1
    else:
        break

new_contacts_block = '''
        <div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-8 border-b border-[#222] pb-4">
            <h2 class="font-syne text-xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
          </div>
          
          <div class="flex flex-col gap-3 mb-6">
            <!-- BOX 1: EMAIL DIRECT -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" class="flex flex-col md:flex-row justify-between items-center p-4 border border-[#eee] bg-[#fafafa] hover:border-[#b3a082] transition-colors group text-decoration-none">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111]">EMAIL DIRECT //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] uppercase group-hover:text-[#111]">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>

            <!-- BOX 2: OSSERVATORIO -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row justify-between items-center p-4 border border-[#eee] bg-[#fafafa] hover:border-[#b3a082] transition-colors group text-decoration-none">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111]">OSSERVATORIO IMLAND //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] uppercase text-right md:text-left group-hover:text-[#111]">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC) ↗</span>
            </a>
          </div>

          <!-- TESTO DESCRITTIVO SNELLITO -->
          <p class="font-inter text-xs text-[#444] leading-relaxed mb-6">
            Il nostro campo base operativo nel cuore di Alagna. L'Atelier non vive solo nello spazio digitale: è uno studio di creazione e materia. È possibile visionare, toccare e provare fisicamente le collezioni direttamente in sede, esclusivamente su appuntamento.
          </p>

          <!-- TERMINALI DI CONTATTO FINALI (LINK ATTIVI) -->
          <div class="flex flex-col gap-3">
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row justify-between items-center py-4 border-t border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0 uppercase">VISITA L'ATELIER (SU APPUNTAMENTO) //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] group-hover:text-[#111] transition-colors uppercase">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex flex-col md:flex-row justify-between items-center py-4 border-t border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0 uppercase">COLLAB & PRESS //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] group-hover:text-[#111] transition-colors uppercase">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

# Iniezione del nuovo blocco subito dopo il cassetto prodotti
p_idx = content.find('id="products-content"')
if p_idx != -1:
    _, e = get_div_bounds(content, p_idx)
    if e != -1:
        content = content[:e] + '\n' + new_contacts_block + '\n' + content[e:]
        print(f"✅ TRASMUTAZIONE COMPLETATA: {eradicated} vecchi cloni contatti rimossi. Asse dinamico, caroselli 6s e Grid Manifesto attivati.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
