import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. AGGANCIO DIRETTO DEL TITOLO "CONNETTITI CON L'ARCHIVIO" AL FONT SYNE EXTRABOLD
content = re.sub(
    r'(<(?:h1|h2|h3|div|p)[^>]*>)\s*(CONNETTITI CON L[\'’]ARCHIVIO)\s*(</(?:h1|h2|h3|div|p)>)',
    r'<h2 style="font-family: \'Syne\', sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: -0.02em; line-height: 1.05;">\2</h2>',
    content,
    flags=re.IGNORECASE
)

# B. SCUDO CSS GLOBALE: Syne 800, Zero Frame Nero, Gabbia 680px e Stacking Caroselli
refined_global_css = '''
<style is:global>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

  /* 1. CAROUSEL STACKING: Sovrappone le immagini IMWEAR nello stesso riquadro */
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

  /* 2. FOGLIO MODALE PURO SENZA FRAME NERO (IMWEAR, CONTACTS, MANIFESTO) */
  #brand-modal, #contacts-modal, #manifesto-modal {
    box-sizing: border-box !important;
  }

  .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
    position: relative !important;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    margin: auto !important;
    width: min(92vw, 880px) !important;
    max-width: min(92vw, 880px) !important;
    max-height: 85vh !important;
    overflow-y: auto !important;
    background: #ffffff !important;
    border: none !important;
    outline: none !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.06) !important;
    padding: 36px !important;
  }

  /* 3. TITOLI MONUMENTALI IN SYNE EXTRABOLD SU TUTTE LE SCHEDE */
  .brand-panel-content h1, .brand-panel-content h2,
  .contacts-panel-content h1, .contacts-panel-content h2,
  .manifesto-panel-content h1, .manifesto-panel-content h2,
  #contacts-modal h1, #contacts-modal h2 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: -0.02em !important;
    line-height: 1.05 !important;
  }

  /* 4. GABBIA EDITORIALE COERENTE PER TESTI E RIGHE */
  .brand-panel-content p, .contacts-panel-content p, .manifesto-panel-content p,
  .brand-panel-content div, .contacts-panel-content div, .manifesto-panel-content div {
    max-width: 680px !important;
    margin-left: 0 !important;
    margin-right: auto !important;
    line-height: 1.6 !important;
  }

  .brand-panel-content header, .contacts-panel-content header, .manifesto-panel-content header {
    max-width: 100% !important;
  }

  /* 5. PULIZIA MOBILE */
  @media (max-width: 768px) {
    .vertical-nav, #axis-nav, .sidebar-nav {
      display: none !important;
    }
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      padding: 24px !important;
    }
  }
</style>
'''

# Sostituisce il blocco <style is:global> mantenendo pulito il componente
content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + refined_global_css

# Assicura che il cap mobile resti calibrato a 150 nodi
content = re.sub(r'res\.data\.slice\(0, 90\)', 'res.data.slice(0, 150)', content)
content = re.sub(r'res\.slice\(0, 90\)', 'res.slice(0, 150)', content)
content = re.sub(r'> 90', '> 150', content)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("SYNE EXTRABOLD ATTIVATO SU CONTATTI E FRAME NERO RIMOSSO.")
