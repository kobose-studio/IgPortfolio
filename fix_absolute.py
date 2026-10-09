import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- AZIONE 1: RIPRISTINO DELLA NAVIGAZIONE VERTICALE A SINISTRA SU TUTTI I DEVICE ---
# Distruggiamo le vecchie regole CSS per la navigazione
content = re.sub(r'/\* IMLAND DYNAMIC AXIS SWITCH.*?</style>', '</style>', content, flags=re.DOTALL)
content = re.sub(r'/\* IMLAND ORIGINAL LEFT AXIS.*?</style>', '</style>', content, flags=re.DOTALL)

css_left_nav = '''
  /* IMLAND ABSOLUTE LEFT AXIS (DESKTOP & MOBILE) */
  header, nav, .nav-container, #main-nav {
    position: fixed !important;
    left: -120px !important;
    top: 50% !important;
    transform: translateY(-50%) rotate(-90deg) !important;
    transform-origin: center center !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    z-index: 9999 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: auto !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  header a, nav a, .nav-container a {
    display: inline-block !important;
    margin: 0 1.25rem !important;
    letter-spacing: 0.15em !important;
    white-space: nowrap !important;
    color: #111 !important;
    font-size: 11px !important;
    transition: color 0.3s ease !important;
  }
  
  header a:hover, nav a:hover, .nav-container a:hover {
    color: #b3a082 !important;
  }
</style>'''

content = content.replace('</style>', css_left_nav)


# --- AZIONE 2: SOSTITUZIONE SPIETATA DEL PANNELLO CONTATTI ---
new_contacts_block = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
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
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] uppercase text-right md:text-left group-hover:text-[#111]">VIA DEI WALSER 23, ALAGNA (VC) ↗</span>
            </a>

            <!-- BOX 3: CREATIVE LAB -->
            <div class="flex flex-col md:flex-row justify-between items-center p-4 border border-[#eee] bg-[#fafafa]">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0">CREATIVE LAB //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#888] uppercase text-right md:text-left">NAVIGLIO PAVESE 114, MILANO (MI)</span>
            </div>

            <!-- BOX 4: COLLAB & PRESS -->
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex flex-col md:flex-row justify-between items-center p-4 border border-[#eee] bg-[#fafafa] hover:border-[#b3a082] transition-colors group text-decoration-none">
              <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111]">COLLAB & PRESS //</span>
              <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] uppercase group-hover:text-[#111]">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>

          <!-- TESTO DESCRITTIVO SNELLITO -->
          <p class="font-inter text-xs text-[#444] leading-relaxed">
            Il nostro campo base operativo nel cuore di Alagna. L'Atelier non vive solo nello spazio digitale: è uno studio di creazione e materia. È possibile visionare, toccare e provare fisicamente le collezioni direttamente in sede, esclusivamente su appuntamento.
          </p>
        </div>'''

# Troviamo il blocco contacts-content esistente e lo sovrascriviamo
c_start = content.find('id="contacts-content"')
if c_start != -1:
    div_start = content.rfind('<div', 0, c_start)
    count = 0
    i = div_start
    div_end = -1
    while i < len(content):
        if content.startswith('<div', i): count += 1
        elif content.startswith('</div', i):
            count -= 1
            if count == 0:
                div_end = i + 6
                break
        i += 1
    if div_end != -1:
        content = content[:div_start] + new_contacts_block + content[div_end:]
        print("✅ ALCHIMIA RIUSCITA: Pannello Contatti Minimalista applicato.")
else:
    print("⚠️ ERRORE: Non trovo la fine del div dei contatti.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
