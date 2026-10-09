import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# --- FASE 1: INIEZIONE CSS DIFENSIVO PER MOBILE ---
css_mobile = '''
  /* IMLAND MOBILE OVERRIDES */
  @media (max-width: 768px) {
    /* Impedisce rotazioni strane e forza il menu in orizzontale */
    header, nav, .nav-container, [class*="nav"] {
      transform: none !important;
      writing-mode: horizontal-tb !important;
      flex-direction: row !important;
      flex-wrap: wrap !important;
      width: 100% !important;
      justify-content: center !important;
    }
    /* Riduciamo i font per farli stare nello schermo */
    .font-mono-tech { font-size: 9px !important; }
    .font-syne { font-size: 14px !important; }
  }
</style>'''

if 'IMLAND MOBILE OVERRIDES' not in content:
    content = content.replace('</style>', css_mobile)

# --- FASE 2: GRID MANIFESTO (PANNELLO CONTATTI) ---
new_contacts_block = '''<div class="brand-panel-content p-4 md:p-6" id="contacts-content" style="display: none;">
          <div class="mb-6 border-b border-[#222] pb-4">
            <h2 class="font-syne text-lg md:text-xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
          </div>
          
          <div class="flex flex-col gap-2 mb-6">
            <!-- BOX 1: EMAIL DIRECT -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center p-3 md:p-4 border border-[#eee] bg-[#fafafa]">
              <span class="font-mono-tech text-[9px] md:text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0">EMAIL DIRECT //</span>
              <span class="font-mono-tech text-[9px] md:text-[10px] font-bold text-[#b3a082] uppercase break-all">IMLANDMOTEROSA@GMAIL.COM</span>
            </div>

            <!-- BOX 2: OSSERVATORIO -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center p-3 md:p-4 border border-[#eee] bg-[#fafafa]">
              <span class="font-mono-tech text-[9px] md:text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 whitespace-nowrap">OSSERVATORIO IMLAND //</span>
              <span class="font-mono-tech text-[9px] md:text-[10px] font-bold text-[#b3a082] uppercase text-left md:text-right mt-1 md:mt-0">VIA DEI WALSER 23, ALAGNA VALSESIA, 13021 (VC)</span>
            </div>
          </div>

          <!-- TESTO DESCRITTIVO SNELLITO -->
          <p class="font-inter text-[11px] md:text-xs text-[#444] leading-relaxed mb-6">
            Il nostro campo base operativo nel cuore di Alagna. L'Atelier non vive solo nello spazio digitale: è uno studio di creazione e materia. È possibile visionare, toccare e provare fisicamente le collezioni direttamente in sede, esclusivamente su appuntamento.
          </p>

          <!-- TERMINALI DI CONTATTO FINALI (LINK ATTIVI) -->
          <div class="flex flex-col gap-2">
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row justify-between items-start md:items-center py-3 md:py-4 border-t border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-[9px] md:text-[10px] tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0 uppercase">VISITA L'ATELIER (SU APPUNTAMENTO) //</span>
              <span class="font-mono-tech text-[9px] md:text-[10px] font-bold text-[#b3a082] group-hover:text-[#111] transition-colors uppercase break-all">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex flex-col md:flex-row justify-between items-start md:items-center py-3 md:py-4 border-t border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-[9px] md:text-[10px] tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0 uppercase">COLLAB & PRESS //</span>
              <span class="font-mono-tech text-[9px] md:text-[10px] font-bold text-[#b3a082] group-hover:text-[#111] transition-colors uppercase break-all">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

# Isolamento e sostituzione del div
start_str = 'id="contacts-content"'
start_idx = content.find(start_str)

if start_idx != -1:
    div_start = content.rfind('<div', 0, start_idx)
    count = 0
    i = div_start
    end_idx = -1
    
    while i < len(content):
        if content.startswith('<div', i): count += 1
        elif content.startswith('</div', i):
            count -= 1
            if count == 0:
                end_idx = i + 6
                break
        i += 1
        
    if end_idx != -1:
        content = content[:div_start] + new_contacts_block + content[end_idx:]
        print("✅ ALCHIMIA RIUSCITA: CSS Mobile Difensivo e Griglia Contatti applicati.")
    else:
        print("⚠️ ERRORE: Non trovo la fine del div dei contatti.")
else:
    print("⚠️ ERRORE: ID contacts-content sparito dalla matrice.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
