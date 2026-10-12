import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# --- A. RIMOZIONE VECCHIO MENU BOTTOM E INIEZIONE CSS NASCONDIGLIO ---
old_css_pattern = r'/\* ARCHITETTURA RESPONSIVE MOBILE EXTREME \*/.*?</style>'

new_css = '''/* IMLAND MOBILE HAMBURGER & 3D ELEVATION */
  @media (max-width: 768px) {
    /* Nascondiamo il menu desktop originale per fare spazio all'hamburger */
    .vertical-nav, #axis-nav, [class*="nav-container"] {
      display: none !important;
    }

    /* Elevazione 3D Canvas intatta per non tagliare le foto in primo piano */
    canvas {
      transform: translateY(-12vh) !important;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    /* Scheda info compatta in basso */
    #image-info-panel, .info-panel {
      max-height: 38vh !important;
      bottom: 1.5vh !important;
      overflow-y: auto !important;
    }
  }
</style>'''

if 'ARCHITETTURA RESPONSIVE MOBILE EXTREME' in content:
    content = re.sub(old_css_pattern, new_css, content, flags=re.DOTALL)
else:
    content = content.replace('</style>', new_css.replace('</style>', '') + '</style>')

# --- B. INIEZIONE HTML & JS DEL MENU BRUTALISTA ---
hamburger_html = '''
<!-- IMLAND BRUTALIST MOBILE MENU -->
<div id="mobile-hamburger" class="md:hidden fixed top-6 right-6 z-[99999] cursor-pointer font-mono-tech text-[#111] text-xs tracking-[0.3em] bg-[#fafafa]/90 backdrop-blur-sm px-4 py-2 border border-[#eee] shadow-sm transition-all duration-300">
  / / /
</div>

<div id="mobile-nav-overlay" class="md:hidden fixed inset-0 bg-[#fafafa]/95 backdrop-blur-xl z-[99998] flex flex-col items-center justify-center opacity-0 pointer-events-none transition-opacity duration-500">
  <a href="#" class="mobile-nav-proxy font-syne text-4xl font-black uppercase mb-8 text-[#111] tracking-tighter hover:text-[#b3a082] transition-colors" data-target="MANIFESTO">MANIFESTO</a>
  <a href="#" class="mobile-nav-proxy font-syne text-4xl font-black uppercase mb-8 text-[#111] tracking-tighter hover:text-[#b3a082] transition-colors" data-target="IMWEAR">IMWEAR</a>
  <a href="#" class="mobile-nav-proxy font-syne text-4xl font-black uppercase mb-12 text-[#111] tracking-tighter hover:text-[#b3a082] transition-colors" data-target="CONTACTS">CONTACTS</a>
  
  <a href="#" class="mobile-nav-proxy font-mono-tech text-[10px] tracking-[0.2em] text-[#555] hover:text-[#111] transition-colors border border-[#ddd] px-6 py-3" data-target="SOUND">SOUND : TOGGLE</a>
</div>

<script>
  document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById('mobile-hamburger');
    const overlay = document.getElementById('mobile-nav-overlay');
    let menuOpen = false;

    if(burger && overlay) {
      burger.addEventListener('click', () => {
        menuOpen = !menuOpen;
        if(menuOpen) {
          overlay.style.opacity = '1';
          overlay.style.pointerEvents = 'auto';
          burger.innerText = '[ X ]';
          burger.style.backgroundColor = '#111';
          burger.style.color = '#fafafa';
        } else {
          overlay.style.opacity = '0';
          overlay.style.pointerEvents = 'none';
          burger.innerText = '/ / /';
          burger.style.backgroundColor = 'rgba(250, 250, 250, 0.9)';
          burger.style.color = '#111';
        }
      });

      // Il Telecomando: proxy dei click al menu desktop invisibile
      document.querySelectorAll('.mobile-nav-proxy').forEach(link => {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          const targetText = link.getAttribute('data-target');
          
          burger.click(); // Chiude il sipario
          
          // Trova il vero bottone e simula il click umano
          const realLinks = document.querySelectorAll('a, button, span');
          realLinks.forEach(rLink => {
            if(rLink.innerText.toUpperCase().includes(targetText) && rLink.closest('.vertical-nav, #axis-nav, [class*="nav-container"], #sound-toggle')) {
              rLink.click();
            }
          });
        });
      });
    }
  });
</script>
'''

if 'IMLAND BRUTALIST MOBILE MENU' not in content:
    content = content.replace('</body>', hamburger_html + '\n</body>')

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎯 THE PROXY BURGER IS LIVE. Interfaccia mobile evoluta.")
