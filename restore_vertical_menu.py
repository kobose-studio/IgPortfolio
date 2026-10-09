import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Eliminiamo eventuali override orizzontali precedenti
content = re.sub(r'/\* IMLAND MOBILE OVERRIDES \*/.*?</style>', '</style>', content, flags=re.DOTALL)
content = re.sub(r'/\* IMLAND VERTICAL LEFT NAVIGATION \*/.*?</style>', '</style>', content, flags=re.DOTALL)

# Iniezione del CSS per il Menu Verticale a Sinistra
css_vertical = '''
  /* IMLAND VERTICAL LEFT NAVIGATION */
  header, nav, .nav-container, #main-nav {
    position: fixed !important;
    left: 1.25rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    flex-direction: column !important;
    writing-mode: vertical-rl !important;
    rotate: 180deg !important;
    z-index: 9999 !important;
    background: transparent !important;
    border: none !important;
    width: auto !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  /* Styling dei singoli link dentro la barra verticale */
  header a, nav a, .nav-container a {
    display: inline-block !important;
    margin: 0.5rem 0 !important;
    letter-spacing: 0.15em !important;
    white-space: nowrap !important;
  }
</style>'''

content = content.replace('</style>', css_vertical)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ALCHIMIA RIUSCITA: Menu verticale a sinistra ripristinato con successo!")
