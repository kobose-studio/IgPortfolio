import re

target_file = 'src/components/PortfolioSceneSphere.astro'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Struttura HTML completa a 4 moduli
new_contacts_html = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content">
  <!-- Header Pannello -->
  <div class="mb-6 border-b border-[#222] pb-4">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <!-- Griglia Contatti -->
  <div class="flex flex-col w-full divide-y divide-[#eee]">
    
    <!-- Item 1: EMAIL DIRECT -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 group text-decoration-none transition-colors">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- Item 2: INSTAGRAM DIRECT -->
    <a href="https://instagram.com/imland.monterosa" target="_blank" rel="noopener" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 group text-decoration-none transition-colors">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">@IMLAND.MONTEROSA ↗</span>
    </a>

    <!-- Item 3: PRESS & PR -->
    <a href="mailto:info.imland@gmail.com?subject=Press%20%26%20PR" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 group text-decoration-none transition-colors">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">PRESS & PR //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">INFO.IMLAND@GMAIL.COM ↗</span>
    </a>

    <!-- Item 4: SHOWROOM / HEADQUARTER -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Showroom" class="flex flex-col md:flex-row justify-between items-start md:items-center py-4 group text-decoration-none transition-colors">
      <div class="flex flex-col">
        <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-0.5 group-hover:text-[#111] transition-colors">SHOWROOM / HEADQUARTER //</span>
        <span class="font-mono-tech text-[9px] text-[#b3a082] uppercase">(SU APPUNTAMENTO)</span>
      </div>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors mt-1 md:mt-0">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>

  </div>
</div>'''

def replace_with_depth_counter(text, new_html):
    idx = text.find('id="contacts-content"')
    if idx == -1:
        idx = text.find("CONNETTITI CON L'ARCHIVIO")
    if idx == -1:
        print("⚠️ Impossibile individuare l'ancora dei contatti.")
        return text

    start = text.rfind('<div', 0, idx)
    
    # Conteggio della profondità dei tag div per trovare il tag finale corretto
    depth = 0
    i = start
    end = -1
    while i < len(text):
        if text[i:].startswith('<div'):
            depth += 1
            i += 4
        elif text[i:].startswith('</div>'):
            depth -= 1
            if depth == 0:
                end = i + 6
                break
            i += 6
        else:
            i += 1

    if end != -1:
        print("✅ Tag contenitore individuato con precisione. Esecuzione sostituzione...")
        return text[:start] + new_html + text[end:]
    else:
        print("⚠️ Impossibile calcolare la chiusura del tag div.")
        return text

content = replace_with_depth_counter(content, new_contacts_html)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 Sostituzione chirurgica completata.")
