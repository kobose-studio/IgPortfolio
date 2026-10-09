import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# TRASMUTAZIONE 1: Aggiornamento CSS per 7 e 4 immagini
# Rimuoviamo il vecchio blocco CSS
content = re.sub(r'/\* IMLAND ASYNC KEN BURNS CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)

css_carousel = '''
  /* IMLAND ASYNC KEN BURNS CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; background: #eaeaea; overflow: hidden; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; object-fit: cover; transform-origin: center center; }
  
  /* 7 Immagini (28s Loop) */
  .kburns-7 { animation: kb7 28s infinite linear; }
  @keyframes kb7 { 0% { opacity: 0; transform: scale(1); } 1.5% { opacity: 1; transform: scale(1.005); } 13% { opacity: 1; transform: scale(1.04); } 14.3%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 5 Immagini (20s Loop) */
  .kburns-5 { animation: kb5 20s infinite linear; }
  @keyframes kb5 { 0% { opacity: 0; transform: scale(1); } 2% { opacity: 1; transform: scale(1.005); } 18% { opacity: 1; transform: scale(1.04); } 20%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 4 Immagini (17s Loop) */
  .kburns-4 { animation: kb4 17s infinite linear; }
  @keyframes kb4 { 0% { opacity: 0; transform: scale(1); } 2.5% { opacity: 1; transform: scale(1.005); } 22.5% { opacity: 1; transform: scale(1.04); } 25%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 3 Immagini (13s Loop) */
  .kburns-3 { animation: kb3 13s infinite linear; }
  @keyframes kb3 { 0% { opacity: 0; transform: scale(1); } 3% { opacity: 1; transform: scale(1.005); } 30% { opacity: 1; transform: scale(1.04); } 33.3%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 2 Immagini (9s Loop) */
  .kburns-2 { animation: kb2 9s infinite linear; }
  @keyframes kb2 { 0% { opacity: 0; transform: scale(1); } 5% { opacity: 1; transform: scale(1.005); } 45% { opacity: 1; transform: scale(1.04); } 50%, 100% { opacity: 0; transform: scale(1.05); } }
</style>'''
content = content.replace('</style>', css_carousel)

# TRASMUTAZIONE 2: Sostituzione Pannello Contatti via DOM Parsing
start_str = 'id="contacts-content"'
start_idx = content.find(start_str)

if start_idx != -1:
    div_start = content.rfind('<div', 0, start_idx)
    count = 0
    i = div_start
    end_idx = -1
    
    while i < len(content):
        if content.startswith('<div', i):
            count += 1
        elif content.startswith('</div', i):
            count -= 1
            if count == 0:
                end_idx = i + 6
                break
        i += 1
        
    if end_idx != -1:
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
        
        content = content[:div_start] + new_contacts + content[end_idx:]
        print("✅ ALCHIMIA RIUSCITA: Nuovi CSS per 7 e 4 immagini aggiunti. Contatti aggiornati.")
    else:
        print("⚠️ Errore di lettura strutturale HTML.")
else:
    print("⚠️ ID contacts-content sparito.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
