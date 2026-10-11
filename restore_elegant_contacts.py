import re

target_file = 'src/components/PortfolioSceneSphere.astro'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# LA GRIGLIA PERFETTA (Stili Tailwind Integrali Ripristinati)
new_contacts = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content">
  <div class="mb-8 border-b border-[#222] pb-4">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <div class="flex flex-col w-full">
    <!-- Item 1: EMAIL DIRECT -->
    <a href="mailto:imlandmoterosa@gmail.com" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <!-- Item 2: INSTAGRAM DIRECT -->
    <a href="https://instagram.com/imland.monterosa" target="_blank" rel="noopener" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">@IMLAND.MONTEROSA ↗</span>
    </a>

    <!-- Item 3: PRESS & PR -->
    <a href="mailto:info.imland@gmail.com" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">PRESS & PR //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">INFO.IMLAND@GMAIL.COM ↗</span>
    </a>

    <!-- Item 4: SHOWROOM / HEADQUARTER -->
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Showroom" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <div class="flex flex-col">
        <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 group-hover:text-[#111] transition-colors">SHOWROOM / HEADQUARTER //</span>
        <span class="font-mono-tech text-[9px] text-[#b3a082] font-bold uppercase">(SU APPUNTAMENTO)</span>
      </div>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors mt-2 md:mt-0">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>
  </div>
</div>'''

# Troviamo l'ancora e assicurarci di prendere il contenitore MADRE (Outer Bound)
pos = content.find("CONNETTITI CON L'ARCHIVIO")
if pos != -1:
    start = content.rfind('<div class="brand-panel-content"', 0, pos)
    if start == -1:
        start = content.rfind('<div id="contacts-content"', 0, pos)
    
    if start != -1:
        depth = 0
        i = start
        end = -1
        while i < len(content):
            if content.startswith('<div', i):
                depth += 1
                i += 4
            elif content.startswith('</div', i):
                depth -= 1
                if depth == 0:
                    end = i + 6
                    break
                i += 6
            else:
                i += 1
                
        if end != -1:
            content = content[:start] + new_contacts + content[end:]
            print("✅ Modale Contatti estratta e ricostruita 1:1 con stile Elegante.")
        else:
            print("⚠️ Errore: Fine del contenitore non trovata.")
    else:
        print("⚠️ Errore: Contenitore madre non trovato.")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)
