import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# FASE 1: PULIZIA DI IMWEAR (Rimuoviamo l'Osservatorio intruso dalla vetrina prodotti)
# Cerchiamo se c'è un blocco "HEADQUARTER" dentro il div products-content
prod_start = content.find('id="products-content"')
if prod_start != -1:
    prod_end = content.find('id="contacts-content"', prod_start)
    if prod_end == -1: prod_end = len(content)
    
    prod_section = content[prod_start:prod_end]
    # Rimuoviamo il blocco estraneo se presente
    clean_prod_section = re.sub(r'<div[^>]*>\s*<h3[^>]*>HEADQUARTER // CAMPO BASE.*?</div>\s*</div>', '', prod_section, flags=re.DOTALL)
    content = content[:prod_start] + clean_prod_section + content[prod_end:]

# FASE 2: REDESIGN DEFINITIVO DEL PANNELLO CONTATTI (Dual Hub + Seppia)
new_contacts = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <!-- DUAL HUB HEADER -->
          <div class="mb-8 border-b border-[#222] pb-4 flex justify-between items-end">
            <h2 class="font-syne text-xl font-bold tracking-tight text-[#111]">ARCHIVE // NETWORK</h2>
            <span class="font-mono-tech text-[10px] text-[#b3a082] tracking-widest">[ DUAL HUB ARCHITECTURE ]</span>
          </div>

          <!-- HUB 1: ALAGNA (OSSERVATORIO) -->
          <div class="mb-6 pb-6 border-b border-[#eee]">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="font-syne text-sm font-bold text-[#111] tracking-wider uppercase">L'OSSERVATORIO IMLAND</h3>
              <span class="font-mono-tech text-[9px] px-2 py-1 bg-[#f5f5f5] text-[#555] tracking-widest">CAMPO BASE</span>
            </div>
            <p class="font-mono-tech text-xs text-[#888] tracking-widest mb-3">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</p>
            <p class="font-inter text-xs text-[#444] leading-relaxed mb-4">
              La nostra sede operativa in quota. Studio di creazione, archivio materico e test dei capi. <br/>È possibile visionare e provare fisicamente le collezioni in showroom, esclusivamente su appuntamento.
            </p>
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="inline-block font-mono-tech text-xs font-bold text-[#b3a082] hover:text-[#111] transition-colors text-decoration-none border border-[#b3a082] hover:border-[#111] px-4 py-2">
              PRENOTA VISITA ALL'ATELIER ↗
            </a>
          </div>

          <!-- HUB 2: MILANO (CREATIVE LAB) -->
          <div class="mb-6 pb-6 border-b border-[#eee]">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="font-syne text-sm font-bold text-[#111] tracking-wider uppercase">CREATIVE LAB</h3>
              <span class="font-mono-tech text-[9px] px-2 py-1 bg-[#f5f5f5] text-[#555] tracking-widest">DESIGN STUDIO</span>
            </div>
            <p class="font-mono-tech text-xs text-[#888] tracking-widest mb-3">NAVIGLIO PAVESE 114, MILANO (MI)</p>
            <p class="font-inter text-xs text-[#444] leading-relaxed">
              Direzione artistica, ricerca tessile e sviluppo concettuale nel tessuto urbano.
            </p>
          </div>

          <!-- COMUNICAZIONI GENERALI -->
          <div class="pt-2">
            <h3 class="font-syne text-xs font-bold text-[#111] tracking-wider uppercase mb-3">COMMUNICATION CHANNELS</h3>
            <div class="flex flex-col gap-3">
              <div class="flex justify-between items-center group">
                <span class="font-mono-tech text-[10px] text-[#888] tracking-widest">INFO & PRE-ORDER //</span>
                <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Generica%20Atelier" class="font-mono-tech text-xs font-bold text-[#b3a082] group-hover:text-[#111] transition-colors text-decoration-none">
                  IMLANDMOTEROSA@GMAIL.COM
                </a>
              </div>
              <div class="flex justify-between items-center group">
                <span class="font-mono-tech text-[10px] text-[#888] tracking-widest">PRESS & COLLAB //</span>
                <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="font-mono-tech text-xs font-bold text-[#b3a082] group-hover:text-[#111] transition-colors text-decoration-none">
                  INFO.IMLAND@GMAIL.COM
                </a>
              </div>
            </div>
          </div>
        </div>'''

# Troviamo e sostituiamo l'intero blocco contatti
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
        content = content[:div_start] + new_contacts + content[end_idx:]
        print("✅ Pannello Contatti ridisegnato con Gerarchie perfette e Dual Hub.")
    else:
        print("⚠️ Errore di chiusura tag nel blocco contatti.")
else:
    print("⚠️ ID contacts-content non trovato.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
