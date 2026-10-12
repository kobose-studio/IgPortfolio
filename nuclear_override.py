import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- A. INIEZIONE DEGLI ARRAY PER SEQUENZA (1=Viola, 2=Azzurro, 3=Giallo) ---
arr_viola = "images: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_azzurro = "images: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_giallo = "images: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

# Trova tutti i blocchi images: [...]
matches = re.findall(r'images:\s*\[.*?\]', content, re.DOTALL)
if len(matches) >= 3:
    content = content.replace(matches[0], arr_viola, 1)
    content = content.replace(matches[1], arr_azzurro, 1)
    content = content.replace(matches[2], arr_giallo, 1)
    print("✅ Arrays di immagini (9, 3, 5) sovrascritti con forza bruta.")
else:
    print("⚠️ Attenzione: Non ho trovato i 3 blocchi array.")

# --- B. INIEZIONE CSS NUCLEARE GLOBALE ---
nuclear_css = '''
<style is:global>
  /* 1. CAROUSEL STACKING: Immagini sovrapposte per il Poliritmo */
  .carousel-wrapper {
    position: relative !important;
    width: 100% !important;
    height: 240px !important;
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
    /* Uccide il menu che spinge il layout */
    .vertical-nav, #axis-nav, [class*="nav-container"] {
      display: none !important;
    }
    /* Centra il box e lo rende più compatto per far respirare il 3D */
    .brand-panel-content, #brand-modal, .info-panel {
      position: fixed !important;
      bottom: 2vh !important;
      left: 4vw !important;
      width: 92vw !important;
      max-width: 92vw !important;
      max-height: 42vh !important;
      overflow-y: auto !important;
      margin: 0 !important;
      box-sizing: border-box !important;
      z-index: 9999 !important;
    }
    /* Solleva la foto 3D per non toccare il box testuale */
    canvas {
      transform: translateY(-22vh) scale(0.85) !important;
    }
  }

  /* 3. DESKTOP CENTERING: Modale perfettamente al centro */
  @media (min-width: 769px) {
    .brand-panel-content {
      margin: 0 auto !important;
      left: 0 !important;
      right: 0 !important;
      position: absolute !important;
      max-width: 860px !important;
    }
  }
</style>
'''

# Rimuove vecchie iniezioni nucleari per evitare duplicati
content = re.sub(r'<style is:global>.*?</style>', '', content, flags=re.DOTALL)
# Incolla brutalmente alla fine del file
content += "\n" + nuclear_css

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 OVERRIDE GLOBALE INIETTATO. Vercel obbedirà.")
