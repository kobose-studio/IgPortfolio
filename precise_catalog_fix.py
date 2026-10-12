target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# Array definiti con i percorsi 1:1 dei tuoi file in public/brand/
arr_viola = "['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_azzurro = "['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_giallo = "['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

def force_replace_array(text, title_keyword, new_array_str):
    idx_title = text.find(title_keyword)
    if idx_title == -1:
        print(f"❌ Titolo non trovato: {title_keyword}")
        return text
    
    idx_images = text.find("images", idx_title)
    if idx_images == -1:
        print(f"❌ Chiave 'images' non trovata dopo {title_keyword}")
        return text
        
    bracket_open = text.find("[", idx_images)
    bracket_close = text.find("]", bracket_open)
    
    if bracket_open != -1 and bracket_close != -1:
        print(f"✅ Array sostituito con successo per: {title_keyword}")
        return text[:bracket_open] + new_array_str + text[bracket_close+1:]
    
    return text

content = force_replace_array(content, "CLASSIC HOODIE", arr_viola)
content = force_replace_array(content, "FULL-ZIP HOODIE", arr_azzurro)
content = force_replace_array(content, "ESSENTIALS & GEAR", arr_giallo)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 PARSER COMPLETATO CON SUCCESSO.")
