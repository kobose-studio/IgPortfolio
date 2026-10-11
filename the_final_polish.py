import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# ABLAZIONE DEL FANTASMA: Rimuoviamo il testo duplicato in fondo alla modale
ghost_string = '''EMAIL DIRECT //IMLANDMOTEROSA@GMAIL.COM ↗INSTAGRAM DIRECT //
@IMLANDMONTEROSA ↗
OSSERVATORIO / SHOWROOM //(SU APPUNTAMENTO)
VIA DEI WALSER 23, 13021 ALAGNA VALSESIA (VC) ↗'''

# Rimuove il fantasma considerando eventuali spazi e a capo (approccio regex morbido)
ghost_pattern = re.compile(r'EMAIL DIRECT //IMLANDMOTEROSA@GMAIL\.COM ↗INSTAGRAM DIRECT //\s*@IMLANDMONTEROSA ↗\s*OSSERVATORIO / SHOWROOM //\(SU APPUNTAMENTO\)\s*VIA DEI WALSER 23, 13021 ALAGNA VALSESIA \(VC\) ↗', re.IGNORECASE)
content = re.sub(ghost_pattern, '', content)

# CLONAZIONE TIPOGRAFICA BOLD EXTENDED
# Sostituiamo il vecchio titolo con la nuova architettura tipografica "Extended"
old_title_pattern = r'<h2 class="font-syne text-2xl md:text-3xl font-bold tracking-tight text-\[#111\] uppercase">CONNETTITI CON L\'ARCHIVIO</h2>'
new_title_html = '<h2 class="font-syne text-[clamp(1.2rem,4vw,2.2rem)] font-black uppercase tracking-tighter text-[#111] transform scale-x-[1.15] origin-left" style="font-stretch: expanded;">CONNETTITI CON L\'ARCHIVIO</h2>'

if 'CONNETTITI CON L\'ARCHIVIO' in content:
    content = re.sub(old_title_pattern, new_title_html, content)
    # Nel caso non trovi il pattern esatto, usa un approccio fallback
    if new_title_html not in content:
        content = re.sub(r'<h2[^>]*>CONNETTITI CON L\'ARCHIVIO</h2>', new_title_html, content)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎯 THE FINAL POLISH: Fantasma asportato e Tipografia 'Bold Extended' innestata.")
