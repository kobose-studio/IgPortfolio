import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I tre vettori d'immagine purificati
col_viola = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
col_azzurro = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
col_giallo = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

def inject_pure_array(html, title_keyword, new_array_str):
    # Regex atomica per trovare il blocco images: associato al titolo
    pattern = re.compile(
        r'(title:\s*["\'][^"\']*' + re.escape(title_keyword) + r'[^"\']*["\'][\s\S]*?images:\s*)\[[\s\S]*?\]',
        re.IGNORECASE
    )
    if pattern.search(html):
        html = pattern.sub(r'\g<1>' + new_array_str, html)
        print(f"✅ Vettore di immagini allineato per: {title_keyword}")
    return html

# Applichiamo la mappatura
content = inject_pure_array(content, "CLASSIC HOODIE", col_viola)
content = inject_pure_array(content, "FULL-ZIP HOODIE", col_azzurro)
content = inject_pure_array(content, "ESSENTIALS & GEAR", col_giallo)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 CATALOGO IMWEAR SCOLPITO NELLA MATRICE.")
