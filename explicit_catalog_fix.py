import os

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Array espliciti definiti sulla base della struttura file in public/brand/
col_viola = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg', '/brand/hoodie-11.jpg']"
col_azzurro = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
col_giallo = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

def replace_product_images(html, title_keyword, explicit_array):
    if title_keyword in html:
        parts = html.split(title_keyword)
        head = parts[0] + title_keyword
        rest = parts[1]
        
        # Individuiamo la prima occorrenza di "images:" dopo il titolo
        if 'images:' in rest:
            sub_parts = rest.split('images:', 1)
            before_images = sub_parts[0] + 'images: '
            after_images = sub_parts[1]
            
            # Troviamo la chiusura della parentesi quadra dell'array
            close_bracket = after_images.find(']')
            if close_bracket != -1:
                remainder = after_images[close_bracket+1:]
                return head + before_images + explicit_array + remainder
    return html

# Applichiamo le sostituzioni per le 3 colonne
content = replace_product_images(content, "CLASSIC HOODIE", col_viola)
content = replace_product_images(content, "FULL-ZIP HOODIE", col_azzurro)
content = replace_product_images(content, "ESSENTIALS & GEAR", col_giallo)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Mappatura esplicita 1:1 completata per tutte e tre le colonne.")
