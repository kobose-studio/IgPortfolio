import re

file_path = 'src/components/PortfolioSceneSphere.astro'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Sostituiamo il rendering dell'immagine con la logica del carosello
old_img_block = r'<img src=\{prod\.image\} alt=\{prod\.title\} class="product-img".*?/>'
new_img_block = '''{prod.images ? (
                  <div class="carousel-wrapper">
                    {prod.images.map((img, i) => (
                      <img src={img} alt={prod.title} class={`product-img crossfade-layer delay-${i}`} />
                    ))}
                  </div>
                ) : (
                  <img src={prod.image} alt={prod.title} class="product-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                )}'''
content = re.sub(old_img_block, new_img_block, content, flags=re.DOTALL)

# Assicuriamoci che i bottoni siano link mailto
old_btn = r'<button class="btn-product-action font-mono-tech">\{prod\.status\}</button>'
new_btn = r'<a href={prod.mailto} class="btn-product-action font-mono-tech" style="text-decoration:none; text-align:center;">{prod.status}</a>'
content = re.sub(old_btn, new_btn, content)

# Aggiungiamo il CSS del carosello alla fine dello blocco <style>
css_carousel = '''
  /* IMLAND CSS CROSSFADE CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; }
  .crossfade-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; animation: imlandCrossfade 12s infinite; }
  .delay-0 { animation-delay: 0s; }
  .delay-1 { animation-delay: 4s; }
  .delay-2 { animation-delay: 8s; }
  @keyframes imlandCrossfade { 0%, 25% { opacity: 1; } 33%, 92% { opacity: 0; } 100% { opacity: 1; } }
</style>'''
content = content.replace('</style>', css_carousel)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Componente Astro patchato con successo: Carosello Olografico Inserito.")
