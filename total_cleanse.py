import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- A. INIEZIONE MODALE CONTATTI (ZERO FANTASMI, STILE BOLD EXTENDED) ---
clean_contacts = '''<div class="brand-panel-content p-6 md:p-10 w-[92vw] md:w-full max-w-2xl mx-auto" id="contacts-content">
  <div class="mb-8 border-b border-[#222] pb-4">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-[clamp(1.2rem,4vw,2.2rem)] font-black uppercase tracking-tighter text-[#111] transform scale-x-[1.15] origin-left" style="font-stretch: expanded;">CONNETTITI CON L'ARCHIVIO</h2>
  </div>
  <div class="flex flex-col w-full divide-y divide-[#eee]">
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Info" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline" style="display: block; margin-bottom: 0.8rem;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase block mb-1 group-hover:text-[#111] transition-colors">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase block group-hover:text-[#b3a082] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>
    <a href="https://instagram.com/imlandmonterosa" target="_blank" rel="noopener noreferrer" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline" style="display: block; margin-bottom: 0.8rem;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase block mb-1 group-hover:text-[#111] transition-colors">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase block group-hover:text-[#b3a082] transition-colors">@IMLANDMONTEROSA ↗</span>
    </a>
    <a href="mailto:imlandmoterosa@gmail.com?subject=Richiesta%20Appuntamento%20Osservatorio" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 group no-underline" style="display: block;">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase block group-hover:text-[#111] transition-colors">OSSERVATORIO / SHOWROOM //</span>
      <span class="font-mono-tech text-[9px] text-[#b3a082] font-bold uppercase block mb-1">(SU APPUNTAMENTO)</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase block group-hover:text-[#b3a082] transition-colors">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗</span>
    </a>
  </div>
</div>'''

# Troviamo l'ancora e sostituiamo per intero, spazzando via vecchi codici
pos = content.find("CONNETTITI CON L'ARCHIVIO")
if pos != -1:
    start = content.rfind('<div class="brand-panel-content"', 0, pos)
    if start == -1:
        start_id = content.rfind('id="contacts-content"', 0, pos)
        if start_id != -1: start = content.rfind('<div', 0, start_id)
        
    if start != -1:
        depth = 0
        i = start
        end = -1
        while i < len(content):
            if content[i:].startswith('<div'): depth += 1; i += 4
            elif content[i:].startswith('</div'):
                depth -= 1
                if depth == 0: end = i + 6; break
                i += 6
            else: i += 1

        if end != -1:
            content = content[:start] + clean_contacts_html + content[end:]
            print("✅ Contatti iniettati a freddo.")

# --- B. FIX MOBILE CLIPPING E SCUDO ANTI-BLU ---
css_mobile_fix = '''
  /* IMLAND GLOBAL FIXES */
  .carousel-wrapper img:first-child { opacity: 1 !important; }
  #contacts-content a, #contacts-content a:visited { color: #111111 !important; text-decoration: none !important; }
  #contacts-content a:hover span { color: #b3a082 !important; }
  
  /* Responsive Panel Constraints */
  @media (max-width: 768px) {
    /* Impedisce al box descrittivo inferiore di strabordare e tagliare l'immagine */
    .brand-panel-content, .info-panel {
      width: 92vw !important;
      left: 4vw !important;
      right: 4vw !important;
      box-sizing: border-box !important;
    }
    
    /* Ridimensiona l'immagine WebGL o sposta il blocco testuale per non accavallarsi */
    #image-info-panel {
      max-height: 35vh; /* Limita l'altezza del testo */
      overflow-y: auto; /* Aggiunge scroll se il testo è lungo */
      bottom: 2vh !important; /* Dà aria rispetto al fondo */
    }
  }
</style>'''

idx_s = content.rfind('</style>')
if idx_s != -1:
    content = content[:idx_s] + css_mobile_fix + content[idx_s+8:]

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 BONIFICA TOTALE ESEGUITA.")
