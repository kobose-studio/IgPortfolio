import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Struttura dati esplicita per i 3 prodotti (9, 3, 5 immagini)
new_products_block = '''const products = [
  {
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']
  },
  {
    title: "IMLAND / FULL-ZIP HOODIE",
    subtitle: "Alpine Edition",
    category: "UNISEX // DYNAMIC LAYER",
    desc: "Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.",
    images: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']
  },
  {
    title: "IMLAND / ESSENTIALS & GEAR",
    subtitle: "Raw Cotton & Lightwear",
    category: "APPAREL & ACCESSORIES",
    desc: "L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.",
    images: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']
  }
];'''

# A. RISCRITTURA STRUTTURA DATI PRODUCTS
if 'const products =' in content:
    content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)
    print("✅ Blocco 'const products' interamente riscritto!")
else:
    # Fallback: se la variabile ha un nome leggermente diverso o è dentro il JSX
    pattern = re.compile(r'images:\s*\[[\s\S]*?\]')
    matches = list(pattern.finditer(content))
    if len(matches) >= 3:
        arr_v = "images: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
        arr_a = "images: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
        arr_g = "images: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"
        content = content[:matches[2].start()] + arr_g + content[matches[2].end():]
        content = content[:matches[1].start()] + arr_a + content[matches[1].end():]
        content = content[:matches[0].start()] + arr_v + content[matches[0].end():]
        print("✅ Fallback: Sostituiti i 3 vettori 'images' per posizione!")

# B. INIEZIONE SCUDO CSS GLOBALE PER CENTRATURA E STACKING CAROSELLI
global_css_shield = '''
<style is:global>
  /* 1. STACKING CAROSELLO: Sovrappone le immagini invece di affiancarle */
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

  /* 2. MOBILE LAYOUT: Centratura assoluta e distruzione menu laterale */
  @media (max-width: 768px) {
    .vertical-nav, #axis-nav, [class*="nav-container"], .sidebar-nav {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }
    .brand-panel-content, #brand-modal, .info-panel, [class*="brand-panel"] {
      position: fixed !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      width: 90vw !important;
      max-width: 90vw !important;
      max-height: 82vh !important;
      overflow-y: auto !important;
      margin: 0 !important;
      padding: 18px !important;
      box-sizing: border-box !important;
      z-index: 99999 !important;
    }
    canvas {
      transform: translateY(-18vh) scale(0.85) !important;
    }
  }

  /* 3. DESKTOP CENTERING: Modale esattamente al centro dello schermo */
  @media (min-width: 769px) {
    .brand-panel-content, #brand-modal {
      position: fixed !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      max-width: 880px !important;
      width: 85vw !important;
      margin: 0 !important;
      box-sizing: border-box !important;
    }
  }
</style>
'''

# Rimuoviamo eventuali vecchie iniezioni e colleghiamo lo scudo globale in fondo
content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + global_css_shield

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 MASTER FIX COMPLETO. Dati e Layout sincronizzati.")
