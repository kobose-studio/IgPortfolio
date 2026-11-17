import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. PULIZIA E RISCRITTURA STATICA DEL BLOCCO "const products = [...]"
arr_classic = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_zip     = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_tee     = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

new_products_block = f'''const products = [
  {{
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: {arr_classic}
  }},
  {{
    title: "IMLAND / FULL-ZIP HOODIE",
    subtitle: "Alpine Edition",
    category: "UNISEX // DYNAMIC LAYER",
    desc: "Strato versatile con zip integrale a scorrimento rapido. Morbida, pratica e avvolgente, offre la giusta protezione termica durante le giornate all'aria aperta e nei cambi di temperatura.",
    images: {arr_zip}
  }},
  {{
    title: "IMLAND / ESSENTIALS & GEAR",
    subtitle: "Raw Cotton & Lightwear",
    category: "APPAREL & ACCESSORIES",
    desc: "L'ecosistema essenziale IMLAND. La T-Shirt e la sacca 'Gerla Bag' sono realizzate in purissimo cotone organico al 100%. Il Neck Warmer è un copricollo leggerissimo e traspirante, progettato per riparare dal vento con la massima discrezione.",
    images: {arr_tee}
  }}
];'''

# Sostituisce brutalmente l'intero blocco products per eliminare qualsiasi residuo di "hoodie-A.jpg" o simili
if 'const products =' in content:
    content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)

# B. CORREZIONE DEL PADDING ASIMMETRICO E CENTRATURA ASSOLUTA
symmetric_css = '''
<style id="imland-symmetric-padding-css" is:global>
  /* Forza la simmetria del padding su tutte le modali per correggere lo sbilanciamento a destra */
  #brand-modal, #contacts-modal, #manifesto-modal {
    padding: 16px !important;
    align-items: center !important;
    justify-content: center !important;
  }

  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    margin: 0 auto !important;
    padding: 36px 36px !important; /* Padding simmetrico essenziale */
    box-sizing: border-box !important;
    left: 0 !important;
    right: 0 !important;
    transform: none !important;
    position: relative !important;
  }

  /* Su mobile, riduciamo il padding simmetricamente */
  @media (max-width: 768px) {
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      padding: 24px 24px !important;
    }
  }
</style>
'''

# Rimuove vecchi fix e aggiunge la nuova regola simmetrica
content = re.sub(r'<style id="imland-symmetric-padding-css"[\s\S]*?</style>', '', content)
content += "\n" + symmetric_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("ARRAYS IMWEAR STATICAMENTE SOVRASCRITTI E PADDING SIMMETRICO APPLICATO.")
