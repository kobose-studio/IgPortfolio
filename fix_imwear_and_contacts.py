import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. AGGIORNAMENTO TITOLO IMWEAR
content = re.sub(r'(IMWEAR\s*//\s*|IMWEAR:\s*)?EQUIPAGGIAMENTO MINERALE', 'IMWEAR: EQUIPAGGIAMENTO MINERALE', content)

# 2. ERADICAZIONE LEAK CONTATTI DA IMWEAR
leak_pattern = r'<div class="mb-8 border-b border-[#222] pb-6">[\s\S]*?HEADQUARTER // CAMPO BASE[\s\S]*?INFO\.IMLAND@GMAIL\.COM ↗\s*</a>\s*</div>\s*</div>'
content = re.sub(leak_pattern, '', content)

# 3. NUOVO PANNELLO CONTATTI: 4 BOX MINIMALI DUPLICATI
new_contacts_drawer = '''<div class="brand-panel-content p-6" id="contacts-content" style="display: none;">
          <div class="mb-6 border-b border-[#222] pb-4">
            <h2 class="font-syne text-xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
          </div>
          
          <div class="flex flex-col gap-3">
            <!-- BOX 1: EMAIL DIRECT -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info%20/%20Atelier" class="flex justify-between items-center p-4 border border-[#eee] hover:border-[#b3a082] bg-[#fafafa] hover:bg-[#fff] transition-all group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111]">EMAIL DIRECT //</span>
              <span class="font-syne text-xs font-bold text-[#b3a082] group-hover:text-[#111]">IMLANDMOTEROSA@GMAIL.COM ↗</span>
            </a>

            <!-- BOX 2: OSSERVATORIO SHOWROOM (RETTANGOLO DUPLICATO) -->
            <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex justify-between items-center p-4 border border-[#eee] hover:border-[#b3a082] bg-[#fafafa] hover:bg-[#fff] transition-all group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111]">OSSERVATORIO / SHOWROOM //</span>
              <span class="font-mono-tech text-xs font-bold text-[#b3a082] group-hover:text-[#111]">VIA DEI WALSER 23, ALAGNA VALSESIA (VC) ↗</span>
            </a>

            <!-- BOX 3: CREATIVE LAB -->
            <div class="flex justify-between items-center p-4 border border-[#eee] bg-[#fafafa]">
              <span class="font-mono-tech text-xs tracking-wider text-[#555]">CREATIVE LAB //</span>
              <span class="font-mono-tech text-xs font-bold text-[#888]">NAVIGLIO PAVESE 114, MILANO (MI)</span>
            </div>

            <!-- BOX 4: COLLAB & PRESS -->
            <a href="mailto:info.imland@gmail.com?subject=Richiesta%20Collaborazione/Press" class="flex justify-between items-center p-4 border border-[#eee] hover:border-[#b3a082] bg-[#fafafa] hover:bg-[#fff] transition-all group text-decoration-none">
              <span class="font-mono-tech text-xs tracking-wider text-[#555] group-hover:text-[#111]">COLLAB & PRESS //</span>
              <span class="font-syne text-xs font-bold text-[#b3a082] group-hover:text-[#111]">INFO.IMLAND@GMAIL.COM ↗</span>
            </a>
          </div>
        </div>'''

# Sostituzione sicura della modale Contatti tramite DOM bounds
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
        content = content[:div_start] + new_contacts_drawer + content[div_end:]
        print("✅ ALCHIMIA RIUSCITA: 4 Box Minimali per Contatti e Titolo IMWEAR inseriti!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
