import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. INIEZIONE CSS SEPPIA PER I LINK EMAIL (Distrugge il blu del browser)
css_sepia_contacts = '''
  /* IMLAND MINIMAL CONTACTS & SEPIA EMAIL LINKS */
  #contacts-content a {
    color: #b3a082 !important;
    text-decoration: none !important;
    transition: color 0.3s ease, opacity 0.3s ease;
  }
  #contacts-content a:hover {
    color: #111111 !important;
    opacity: 0.8;
  }
</style>'''

if 'IMLAND MINIMAL CONTACTS' not in content:
    content = content.replace('</style>', css_sepia_contacts)

# 2. PANNELLO CONTATTI MINIMALE DUAL-HUB (ALAGNA + MILANO)
new_contacts = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <!-- HEADER -->
          <div class="mb-6 border-b border-[#222] pb-4">
            <h3 class="font-syne text-[10px] uppercase tracking-widest text-[#888] mb-1">DUAL HUB ARCHITECTURE</h3>
            <h2 class="font-syne text-xl font-bold tracking-tight text-[#111]">CONNETTI CON L'ATELIER</h2>
          </div>

          <!-- HUB 1: ALAGNA -->
          <div class="mb-6 pb-4 border-b border-[#eee]">
            <div class="flex justify-between items-baseline mb-1">
              <span class="font-mono-tech text-xs font-bold text-[#111] tracking-wider">CAMPO BASE // ALAGNA</span>
              <span class="font-mono-tech text-[10px] text-[#b3a082] uppercase tracking-wider">[ OSSERVATORIO & SHOWROOM ]</span>
            </div>
            <p class="font-mono-tech text-xs text-[#555] tracking-wide mb-2">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</p>
            <p class="font-inter text-xs text-[#666] leading-relaxed">
              Sede operativa e prototipazione in quota. Test dei capi e archivio materiale. Visite e prove collezioni esclusivamente su appuntamento.
            </p>
          </div>

          <!-- HUB 2: MILANO -->
          <div class="mb-6 pb-4 border-b border-[#eee]">
            <div class="flex justify-between items-baseline mb-1">
              <span class="font-mono-tech text-xs font-bold text-[#111] tracking-wider">CREATIVE LAB // MILANO</span>
              <span class="font-mono-tech text-[10px] text-[#b3a082] uppercase tracking-wider">[ DESIGN STUDIO ]</span>
            </div>
            <p class="font-mono-tech text-xs text-[#555] tracking-wide mb-2">NAVIGLIO PAVESE 114, MILANO (MI)</p>
            <p class="font-inter text-xs text-[#666] leading-relaxed">
              Direzione artistica, ricerca tessile e laboratorio concettuale tra i canali urbani.
            </p>
          </div>

          <!-- EMAIL DIRECT & CONTACTS -->
          <div class="flex flex-col gap-4 pt-1">
            <div>
              <span class="font-mono-tech text-[10px] text-[#888] tracking-widest block mb-1">EMAIL DIRECT // PRE-ORDER & APPOINTMENTS</span>
              <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info%20/%20Appuntamento%20Atelier" class="font-syne text-sm font-bold tracking-wide block">
                IMLANDMOTEROSA@GMAIL.COM ↗
              </a>
            </div>
            <div>
              <span class="font-mono-tech text-[10px] text-[#888] tracking-widest block mb-1">PRESS & COLLAB // ATELIER NETWORK</span>
              <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="font-syne text-sm font-bold tracking-wide block">
                INFO.IMLAND@GMAIL.COM ↗
              </a>
            </div>
          </div>
        </div>'''

# Sostituzione sicura tramite DOM Parser
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
        print("✅ ALCHIMIA RIUSCITA: Dual Hub Alagna/Milano e Stili Seppia Iniettati!")
    else:
        print("⚠️ Errore di lettura strutturale HTML.")
else:
    print("⚠️ ID contacts-content non trovato.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
