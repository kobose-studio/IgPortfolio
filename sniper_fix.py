import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Taglio netto: mandiamo a capo Instagram fisicamente
# Sostituiamo la stringa con se stessa preceduta da due a capo (line breaks HTML)
if 'INSTAGRAM DIRECT' in content:
    # Preveniamo la duplicazione se lanci lo script due volte
    content = content.replace('<br><br>INSTAGRAM DIRECT', 'INSTAGRAM DIRECT')
    content = content.replace('INSTAGRAM DIRECT', '<br><br>INSTAGRAM DIRECT')

# 2. Scudo CSS per impilare verticalmente gli elementi e dare spazio
css_shield = '''
  /* IMLAND VERTICAL RHYTHM SHIELD */
  #contacts-content a, #contacts-content span {
    display: block !important;
    margin-bottom: 0.8rem !important;
    line-height: 1.4 !important;
  }
</style>'''

if 'VERTICAL RHYTHM SHIELD' not in content:
    idx_s = content.rfind('</style>')
    if idx_s != -1:
        content = content[:idx_s] + css_shield + content[idx_s+8:]

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎯 SNIPER FIX: Instagram mandato a capo e ritmo verticale applicato.")
