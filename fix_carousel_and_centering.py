import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Array definiti (9 immagini, 3 immagini, 5 immagini)
col_viola = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
col_azzurro = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
col_giallo = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

def replace_array_strict(html, title_keyword, new_array_str):
    pattern = re.compile(
        r'(title:\s*["\'][^"\']*' + re.escape(title_keyword) + r'[^"\']*["\'][\s\S]*?images:\s*)\[[\s\S]*?\]',
        re.IGNORECASE
    )
    if pattern.search(html):
        html = pattern.sub(r'\g<1>' + new_array_str, html)
        print(f"✅ Array aggiornato per: {title_keyword}")
    return html

content = replace_array_strict(content, "CLASSIC HOODIE", col_viola)
content = replace_array_strict(content, "FULL-ZIP HOODIE", col_azzurro)
content = replace_array_strict(content, "ESSENTIALS & GEAR", col_giallo)

# CSS FIX PER SOVRAPPOSIZIONE CAROSELLO E CENTRATURA MODALE
master_fix_css = '''
  /* CAROUSEL STACKING FIX: Sovrappone le immagini invece di affiancarle */
  .carousel-wrapper {
    position: relative !important;
    width: 100% !important;
    height: 220px !important;
    overflow: hidden !important;
    display: block !important;
  }

  .carousel-wrapper img, .carousel-wrapper video {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
  }

  /* CENTRATURA MODALE & RISOLUZIONE TAGLIO DESTRO MOBILE */
  .brand-panel-content, #brand-modal, [class*="brand-panel"] {
    box-sizing: border-box !important;
  }

  @media (min-width: 769px) {
    .brand-panel-content {
      margin-left: auto !important;
      margin-right: auto !important;
      max-width: 860px !important;
      width: 90vw !important;
    }
  }

  @media (max-width: 768px) {
    .brand-panel-content, #brand-modal {
      position: relative !important;
      width: 92vw !important;
      max-width: 92vw !important;
      margin-left: auto !important;
      margin-right: auto !important;
      left: 0 !important;
      right: 0 !important;
      box-sizing: border-box !important;
      padding: 16px !important;
      overflow-x: hidden !important;
    }
  }
</style>'''

if 'CAROUSEL STACKING FIX' not in content:
    content = content.replace('</style>', master_fix_css)
    print("✅ Stacking CSS e Centratura Modale applicati.")

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 SCRIPT COMPLETO. Modale e Caroselli bilanciati.")
