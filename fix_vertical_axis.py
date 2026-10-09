import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Distruzione totale dei vecchi CSS mobili e verticali fallati
content = re.sub(r'/\* IMLAND MOBILE OVERRIDES \*/.*?</style>', '</style>', content, flags=re.DOTALL)
content = re.sub(r'/\* IMLAND VERTICAL LEFT NAVIGATION \*/.*?</style>', '</style>', content, flags=re.DOTALL)

# 2. Iniezione del CSS originale e perfetto per la barra sinistra
css_restoration = '''
  /* IMLAND ORIGINAL LEFT AXIS (NO GLITCH) */
  header, nav, .nav-container, #main-nav {
    position: fixed !important;
    left: -120px !important; /* Regola lo spostamento a sinistra */
    top: 50% !important;
    transform: translateY(-50%) rotate(-90deg) !important;
    transform-origin: center center !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    z-index: 9999 !important;
    background: transparent !important; /* Niente sfondo grigio */
    border: none !important; /* Niente box bianco */
    box-shadow: none !important;
    width: auto !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  /* I link tornano orizzontali all'interno del box ruotato */
  header a, nav a, .nav-container a {
    display: inline-block !important;
    margin: 0 1rem !important;
    letter-spacing: 0.15em !important;
    white-space: nowrap !important;
    color: #111 !important; /* Testo nero */
  }
  
  header a:hover, nav a:hover, .nav-container a:hover {
    color: #b3a082 !important; /* Hover Seppia */
  }
</style>'''

content = content.replace('</style>', css_restoration)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ALCHIMIA RIUSCITA: Glitch distrutto. Barra di navigazione originale ripristinata sul fianco sinistro.")
