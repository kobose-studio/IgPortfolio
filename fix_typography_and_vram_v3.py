import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# A. STANDARDIZZAZIONE TIPOGRAFICA GLOBALE E CORNICI
global_typography_css = '''
<style is:global>
  /* Uniforma l'impostazione editoriale di tutte le modali (IMWEAR, CONTACTS, MANIFESTO) */
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
    border: 1px solid #111111 !important;
    padding: 32px !important;
  }

  /* Gabbia di testo identica per paragrafi e descrizioni interne */
  .brand-panel-content p, .contacts-panel-content p, .manifesto-panel-content p,
  .brand-panel-content div, .contacts-panel-content div, .manifesto-panel-content div {
    max-width: 680px !important;
    margin-left: 0 !important;
    margin-right: auto !important;
    line-height: 1.6 !important;
  }

  /* Eccezione: resetta la larghezza delle intestazioni principali per i flex container */
  .brand-panel-content header, .contacts-panel-content header, .manifesto-panel-content header {
    max-width: 100% !important;
  }

  /* Ottimizzazione margini su smartphone */
  @media (max-width: 768px) {
    .brand-panel-content, .contacts-panel-content, .manifesto-panel-content {
      padding: 24px !important;
    }
  }
</style>
'''

# Iniettiamo lo stile globale in fondo al file (sostituendo eventuali vecchie regole per i panel)
content = re.sub(r'<style is:global>[\s\S]*?</style>', '', content)
content += "\n" + global_typography_css

# B. CALIBRAZIONE FEATHERWEIGHT ENGINE V3 (150 nodi su Mobile)
content = re.sub(r'res\.data\.slice\(0, 90\)', 'res.data.slice(0, 150)', content)
content = re.sub(r'res\.slice\(0, 90\)', 'res.slice(0, 150)', content)
content = re.sub(r'> 90', '> 150', content)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("NORMA EDITORIALE APPLICATA E LIMITI VRAM AMMORBIDITI.")
