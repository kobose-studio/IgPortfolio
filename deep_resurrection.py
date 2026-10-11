import subprocess, re

target = 'src/components/PortfolioSceneSphere.astro'

print("[*] Ispezione della cronologia Git per recuperare la versione originale integra...")
commits = subprocess.check_output(['git', 'log', '--format=%H', '--', target]).decode('utf-8').splitlines()

clean_content = None
# Cerchiamo un commit precedente alle modifiche odierne che contenga il CSS completo (>8000 caratteri)
for c in commits:
    try:
        raw = subprocess.check_output(['git', 'show', f'{c}:{target}']).decode('utf-8')
        if len(raw) > 8000 and '<style' in raw and 'THREE' in raw:
            print(f"✅ Trovato commit integro nativo: {c[:8]}")
            clean_content = raw
            break
    except Exception:
        pass

if not clean_content:
    print("⚠️ Fallback: recupero da HEAD~10")
    clean_content = subprocess.check_output(['git', 'show', f'HEAD~10:{target}']).decode('utf-8')

# A. REPLICA 1:1 CONTATTI TICINESE
new_contacts_html = '''<div class="brand-panel-content p-6 md:p-10 w-full max-w-2xl mx-auto" id="contacts-content">
  <div class="mb-8 border-b border-[#222] pb-4">
    <span class="font-mono-tech text-[9px] text-[#b3a082] tracking-widest uppercase block mb-2">COMMUNICATION CHANNELS //</span>
    <h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-[#111] uppercase">CONNETTITI CON L'ARCHIVIO</h2>
  </div>

  <div class="flex flex-col w-full">
    <a href="mailto:imlandmoterosa@gmail.com" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">EMAIL DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">IMLANDMOTEROSA@GMAIL.COM ↗</span>
    </a>

    <a href="https://instagram.com/imland.monterosa" target="_blank" rel="noopener" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">INSTAGRAM DIRECT //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right group-hover:text-[#b3a082] transition-colors">@IMLAND.MONTEROSA ↗</span>
    </a>

    <a href="mailto:info.imland@gmail.com" class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee] group text-decoration-none">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0 group-hover:text-[#111] transition-colors">PRESS & PR //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#b3a082] transition-colors">INFO.IMLAND@GMAIL.COM ↗</span>
    </a>

    <div class="flex flex-col md:flex-row justify-between items-start md:items-center py-5 border-b border-[#eee]">
      <span class="font-mono-tech text-[10px] tracking-wider text-[#555] uppercase mb-1 md:mb-0">HEADQUARTER //</span>
      <span class="font-mono-tech text-[10px] font-bold text-[#111] uppercase text-left md:text-right">VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ITALIA</span>
    </div>
  </div>
</div>'''

if 'id="contacts-content"' in clean_content:
    clean_content = re.sub(r'<div[^>]*id="contacts-content"[^>]*>[\s\S]*?</div>\s*</div>', new_contacts_html, clean_content, count=1)

# B. FIX CAROSELLO (PRIMA FOTO SUBITO VISIBILE)
css_carousel_fix = '''
  /* IMLAND FIRST FRAME FIX */
  .carousel-wrapper img:first-child { opacity: 1 !important; }
'''

if '</style>' in clean_content:
    idx_style = clean_content.rfind('</style>')
    clean_content = clean_content[:idx_style] + css_carousel_fix + '\n</style>' + clean_content[idx_style+8:]

with open(target, 'w', encoding='utf-8') as f:
    f.write(clean_content)

print("🚀 SITO RIPRISTINATO E PATCHATO CON SUCCESSO!")
