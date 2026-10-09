import re
with open('src/components/PortfolioSceneSphere.astro', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rimuoviamo il prezzo per elevare l'Atelier
content = re.sub(r'<div[^>]*>\{prod\.price\}</div>', '', content)

# 2. Trasformiamo il bottone rotto in un link mailto funzionante a tutta larghezza
old_btn = r'<button class="btn-product-action font-mono-tech"[^>]*>\{prod\.status\}</button>'
new_btn = r'<a href={prod.mailto} class="btn-product-action font-mono-tech" style="text-decoration:none; text-align:center; display:block; width:100%; transition: all 0.3s ease;">{prod.status}</a>'
content = re.sub(old_btn, new_btn, content)

# 3. Pulizia vecchi CSS Carosello
content = re.sub(r'/\* IMLAND.*?CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)

# 4. Nuovo JSX con calcolo delay matematico per l'asincronia
html_carousel = '''{prod.images ? (
                  <div class="carousel-wrapper">
                    {prod.images.map((img, i) => {
                      const delay = prod.images.length === 5 ? i * 4 : (prod.images.length === 3 ? i * 4.33 : i * 4.5);
                      return <img src={img} alt={prod.title} class={`product-img kburns-${prod.images.length}`} style={`animation-delay: ${delay}s;`} />
                    })}
                  </div>
                ) : (
                  <img src={prod.image} alt={prod.title} class="product-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                )}'''
old_img = r'\{prod\.images \? \(.*?</div>\s*\)\s*:\s*\(.*?\)\}'
content = re.sub(old_img, html_carousel, content, flags=re.DOTALL)

# 5. CSS Ken Burns: Zoom lento ed elegante
css_carousel = '''
  /* IMLAND ASYNC KEN BURNS CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; background: #eaeaea; overflow: hidden; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; object-fit: cover; transform-origin: center center; }
  
  /* 5 Immagini (20s Loop) */
  .kburns-5 { animation: kb5 20s infinite linear; }
  @keyframes kb5 { 0% { opacity: 0; transform: scale(1); } 2% { opacity: 1; transform: scale(1.005); } 18% { opacity: 1; transform: scale(1.04); } 20%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 3 Immagini (13s Loop - Sfalsato) */
  .kburns-3 { animation: kb3 13s infinite linear; }
  @keyframes kb3 { 0% { opacity: 0; transform: scale(1); } 3% { opacity: 1; transform: scale(1.005); } 30% { opacity: 1; transform: scale(1.04); } 33.3%, 100% { opacity: 0; transform: scale(1.05); } }
  
  /* 2 Immagini (9s Loop - Sfalsato) */
  .kburns-2 { animation: kb2 9s infinite linear; }
  @keyframes kb2 { 0% { opacity: 0; transform: scale(1); } 5% { opacity: 1; transform: scale(1.005); } 45% { opacity: 1; transform: scale(1.04); } 50%, 100% { opacity: 0; transform: scale(1.05); } }
</style>'''
content = content.replace('</style>', css_carousel)

with open('src/components/PortfolioSceneSphere.astro', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Alchimia Completata: Ken Burns Asincrono e Mailto Concierge attivati. Prezzo rimosso.")
