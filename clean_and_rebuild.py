import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Algoritmo chirurgico per isolare un div e i suoi figli
def get_div_bounds(text, div_id):
    start_str = f'id="{div_id}"'
    start_idx = text.find(start_str)
    if start_idx == -1: return -1, -1
    div_start = text.rfind('<div', 0, start_idx)
    count = 0
    i = div_start
    while i < len(text):
        if text.startswith('<div', i): count += 1
        elif text.startswith('</div', i):
            count -= 1
            if count == 0: return div_start, i + 6
        i += 1
    return -1, -1

# 1. DISTRUZIONE VECCHIO PANNELLO CONTATTI
c_start, c_end = get_div_bounds(content, "contacts-content")
if c_start != -1: 
    content = content[:c_start] + content[c_end:]

# 2. PURIFICAZIONE DI IMWEAR (Rimuove il leak)
p_start, p_end = get_div_bounds(content, "products-content")
if p_start != -1:
    prod_block = content[p_start:p_end]
    
    # Scrubbing aggressivo del leak (Cerca HEADQUARTER, CONNETTITI, ecc. e polverizza il blocco)
    prod_block = re.sub(r'<div class="mb-[68][^>]*>[\s\S]*?(HEADQUARTER|CONNETTITI|ARCHIVE // NETWORK)[\s\S]*?INFO\.IMLAND@GMAIL\.COM[\s\S]*?</a>\s*</div>\s*</div>', '', prod_block)
    prod_block = re.sub(r'<div[^>]*>\s*<h[23][^>]*>HEADQUARTER.*?</div>\s*</div>', '', prod_block, flags=re.DOTALL)

    # 3. GENERAZIONE NUOVO PANNELLO CONTATTI MINIMALISTA (Elenco a righe)
    new_contacts_block = '''
        <div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-8 border-b border-[#222] pb-4">
            <h2 class="font-syne text-xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
          </div>
          <div class="flex flex-col gap-0">
            
            <!-- EMAIL DIRECT -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info%20/%20Atelier" class="flex flex-col md:flex-row md:justify-between md:items-center py-5 border-b border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0">EMAIL DIRECT //</span>
              <span class="font-syne text-sm font-bold text-[#b3a082] group-hover:text-[#111] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>

            <!-- OSSERVATORIO (ALAGNA) -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row md:justify-between md:items-center py-5 border-b border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0">L'OSSERVATORIO IMLAND //</span>
              <span class="font-mono-tech text-[10px] tracking-widest uppercase text-[#b3a082] group-hover:text-[#111] transition-colors">VIA DEI WALSER 23, ALAGNA VALSESIA (VC) ↗</span>
            </a>

            <!-- CREATIVE LAB (MILANO) -->
            <div class="flex flex-col md:flex-row md:justify-between md:items-center py-5 border-b border-[#eee]">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] mb-1 md:mb-0">CREATIVE LAB //</span>
              <span class="font-mono-tech text-[10px] tracking-widest uppercase text-[#888]">NAVIGLIO PAVESE 114, MILANO (MI)</span>
            </div>

            <!-- COLLAB & PRESS -->
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex flex-col md:flex-row md:justify-between md:items-center py-5 border-b border-[#eee] group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111] transition-colors mb-1 md:mb-0">COLLAB & PRESS //</span>
              <span class="font-syne text-sm font-bold text-[#b3a082] group-hover:text-[#111] transition-colors">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>

          </div>
        </div>
    '''
    
    # Reinseriamo il blocco prodotti pulito seguito dal nuovo blocco contatti
    content = content[:p_start] + prod_block + new_contacts_block + content[p_end:]
    print("✅ Falce e Martello Digitale: Leak IMWEAR eradicato e Layout Contatti Minimalista applicato.")
else:
    print("⚠️ ERRORE: Div products-content non trovato nella matrice.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
