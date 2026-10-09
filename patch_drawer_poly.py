import re
with open('src/components/PortfolioSceneSphere.astro', 'r', encoding='utf-8') as f:
    content = f.read()

# Eliminiamo qualsiasi vecchio CSS carosello per fare tabula rasa
content = re.sub(r'/\* IMLAND.*?CAROUSEL \*/.*?</style>', '</style>', content, flags=re.DOTALL)

poly_code = '''{prod.images ? (
                  <div class="carousel-wrapper">
                    {prod.images.map((img, i) => (
                      <img src={img} alt={prod.title} class={`product-img crossfade-${prod.images.length} delay-${i}`} />
                    ))}
                  </div>
                ) : (
                  <img src={prod.image} alt={prod.title} class="product-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                )}'''

old_carousel = r'\{prod\.images \? \(.*?</div>\s*\)\s*:\s*\(.*?\)\}'
img_pattern = r'<img src=\{prod\.image\} alt=\{prod\.title\} class="product-img".*?/>'

if re.search(old_carousel, content, flags=re.DOTALL):
    content = re.sub(old_carousel, poly_code, content, flags=re.DOTALL)
elif re.search(img_pattern, content):
    content = re.sub(img_pattern, poly_code, content)

css_carousel = '''
  /* IMLAND POLYMORPHIC CSS CAROUSEL */
  .carousel-wrapper { position: relative; width: 100%; height: 100%; }
  .carousel-wrapper img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; }
  
  .delay-0 { animation-delay: 0s; } .delay-1 { animation-delay: 4s; } .delay-2 { animation-delay: 8s; }
  .delay-3 { animation-delay: 12s; } .delay-4 { animation-delay: 16s; } .delay-5 { animation-delay: 20s; }
  
  .crossfade-6 { animation: fade6 24s infinite ease-in-out; }
  @keyframes fade6 { 0%, 12% { opacity: 1; } 20%, 85% { opacity: 0; } 95%, 100% { opacity: 1; } }
  
  .crossfade-3 { animation: fade3 12s infinite ease-in-out; }
  @keyframes fade3 { 0%, 25% { opacity: 1; } 33%, 92% { opacity: 0; } 100% { opacity: 1; } }
  
  .crossfade-2 { animation: fade2 8s infinite ease-in-out; }
  @keyframes fade2 { 0%, 40% { opacity: 1; } 50%, 90% { opacity: 0; } 100% { opacity: 1; } }
</style>'''
content = content.replace('</style>', css_carousel)

with open('src/components/PortfolioSceneSphere.astro', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Componente Astro e Carosello Polimorfico Iniettati e Allineati.")
