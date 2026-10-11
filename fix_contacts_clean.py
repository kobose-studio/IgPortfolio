import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# STRUTTURA HTML PULITA A 3 RIGHE (ONLY TAILWIND CLASSES)
clean_contacts_html = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content">
  <!-- Header Pannello -->
  <div class="mb-8 border-b border-[#222] pb-4">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <!-- Griglia a 3 Righe -->
  <div class="flex flex-col w-full divide-y divide-[#eee]">
    
    <!-- Row 1: EMAIL DIRECT -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- Row 2: INSTAGRAM DIRECT -->
    <a href="https://instagram.com/imlandmonterosa" target="_blank" rel="noopener" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">@IMLANDMONTEROSA ↗</span>
    </a>

    <!-- Row 3: OSSERVATORIO / SHOWROOM -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline">
      <div class="flex flex-col">
        <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 group-hover:text-[#111] transition-colors">OSSERVATORIO / SHOWROOM //</span>
        <span class="font-mono-tech text-[9px] text-[#b3a082] font-bold uppercase">(SU APPUNTAMENTO)</span>
      </div>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors mt-2 md:mt-0">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>

  </div>
</div>'''

# Troviamo ed eliminiamo il vecchio contenitore dei contatti
idx = content.find('id="contacts-content"')
if idx == -1:
    idx = content.find("CONNETTITI CON L'ARCHIVIO")

if idx != -1:
    start = content.rfind('<div', 0, idx)
    depth = 0
    i = start
    end = -1
    while i < len(content):
        if content[i:].startswith('<div'):
            depth += 1
            i += 4
        elif content[i:].startswith('</div>'):
            depth -= 1
            if depth == 0:
                end = i + 6
                break
            i += 6
        else:
            i += 1
            
    if end != -1:
        content = content[:start] + clean_contacts_html + content[end:]
        print("✅ Blocco contatti sostituito con la griglia Tailwind pulita.")

# Iniezione isolata CSS per prevenire collegamenti blu
anti_blue_style = '''
  #contacts-content a { color: #111111 !important; text-decoration: none !important; }
  #contacts-content a:hover span { color: #b3a082 !important; }
</style>'''

if '</style>' in content:
    idx_s = content.rfind('</style>')
    content = content[:idx_s] + anti_blue_style + content[idx_s+8:]

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 Patch completata con successo.")
