import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. IL NUOVO MANIFESTO POETICO (Scritto direttamente nel markup HTML)
old_manifesto_regex = r'(IMLAND MONTEROSA\s+nasce\s+sotto[\s\S]*?)(?:<div[^>]*>|"NON CERCHIAMO|<footer|<script|</article)'

new_manifesto = '''IMLAND nasce sotto l'ombra imponente della parete est del Monte Rosa. Non creiamo capi per il consumo di massa, né per la moda da passerella cittadina.
          </p>
          <p style="margin-top: 1.15rem; max-width: 680px; line-height: 1.6;">
            Progettiamo <strong>outfit outdoor ad alte prestazioni</strong> per chi vive la montagna con rispetto, silenzio e radici profonde. In un mondo saturo di rumore digitale, Alagna e le sue valli da scoprire rimangono la nostra unica bussola esistenziale.
          </p>
          <p style="margin-top: 1.15rem; max-width: 680px; line-height: 1.6;">
            Affiancando al rigore dell'equipaggiamento alpino la <strong>fotografia</strong> come strumento di ascolto lento, ogni immagine che ruota nel vortice smette di essere un semplice post e si trasforma in un indizio silenzioso nascosto tra le pieghe della valle.
          </p>
          '''

if re.search(old_manifesto_regex, content, flags=re.IGNORECASE):
    content = re.sub(
        old_manifesto_regex,
        new_manifesto + r'\n          \2',  # Mantiene il blocco successivo (es. il div della citazione)
        content,
        flags=re.IGNORECASE,
        count=1
    )
else:
    print("⚠️ Attenzione: Impossibile trovare il vecchio testo del manifesto per la sostituzione diretta.")


# B. OVERRIDE STATICO DELLE COLONNE IMWEAR (Hardcoded HTML generation)
# Sovrascriviamo l'array products e costringiamo Astro a usare questi dati
new_products_block = '''const products = [
  {
    title: "IMLAND / CLASSIC HOODIE",
    subtitle: "Signature Collection",
    category: "UNISEX & KIDS // HEAVYWEIGHT",
    desc: "Il capo iconico dell'Atelier IMLAND. Una felpa ad alta grammatura, morbida, densa e calda, pensata per accompagnare il ritmo della montagna e la vita di tutti i giorni. Struttura resistente e massimo comfort.",
    images: ['/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']
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

content = re.sub(r'const products\s*=\s*\[[\s\S]*?\];', new_products_block, content)


# C. CSS SCALPELLO: Centratura Assoluta e Inevitabile delle Modali
master_css = '''
<style id="imland-master-final-css" is:global>
  /* Forza la centratura matematica assoluta per evitare sbilanciamenti e padding asimmetrici */
  #brand-modal, #contacts-modal, #manifesto-modal {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100dvh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    z-index: 50 !important;
  }

  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: relative !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85dvh !important;
    margin: 0 auto !important;
    padding: 36px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    background: #ffffff !important;
    border: none !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.06) !important;
    box-sizing: border-box !important;
    left: auto !important;
    right: auto !important;
    top: auto !important;
    bottom: auto !important;
    transform: none !important;
  }

  /* Su mobile impila le 3 colonne in verticale nel box centrato (zero tagli a destra o sinistra) */
  @media (max-width: 768px) {
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      width: 94vw !important;
      max-width: 94vw !important;
      max-height: 82dvh !important;
      padding: 24px !important;
    }
    .brand-panel-content .grid,
    #brand-modal .grid,
    [class*="brand-panel"] [class*="grid"] {
      display: grid !important;
      grid-template-columns: 1fr !important;
      gap: 24px !important;
      width: 100% !important;
    }
  }
</style>
'''

# Rimuovi eventuali vecchi blocchi patch CSS e inietta quello definitivo
content = re.sub(r'<style id="imland-(?:master-v10|center-zip|symmetric-padding)-css"[\s\S]*?</style>', '', content)
content += "\n" + master_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("MANIFESTO POETICO SCOLPITO, ARRAY IMWEAR RISCRITTI E MODALI CENTRATE ASSOLUTAMENTE.")
