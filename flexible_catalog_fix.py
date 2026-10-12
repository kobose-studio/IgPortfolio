import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I tre array esatti dei 17 file presenti in public/brand/
arr_hoodie = "images: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_zip    = "images: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_tee    = "images: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

# Pattern flessibile: gestisce virgolette opzionali e formattazione multilinea
pattern = re.compile(r'[\'"]?images[\'"]?\s*:\s*\[[\s\S]*?\]', re.IGNORECASE)
matches = list(pattern.finditer(content))

print(f"🔍 Trovati {len(matches)} blocchi array nel file.")

if len(matches) >= 3:
    # Sostituzione a ritroso per preservare gli indici
    content = content[:matches[2].start()] + arr_tee + content[matches[2].end():]
    content = content[:matches[1].start()] + arr_zip + content[matches[1].end():]
    content = content[:matches[0].start()] + arr_hoodie + content[matches[0].end():]
    print("✅ Tutti e 3 gli array (9, 3, 5) sostituiti con successo!")
else:
    print("⚠️ Meno di 3 blocchi trovati con la chiave 'images'. Forzatura mirata...")
    # Fallback su array specifici presenti nel codice
    content = re.sub(r'[\'"]?images[\'"]?\s*:\s*\[[^\]]*hoodie[^\]]*\]', arr_hoodie, content, count=1)
    content = re.sub(r'[\'"]?images[\'"]?\s*:\s*\[[^\]]*zip[^\]]*\]', arr_zip, content, count=1)
    content = re.sub(r'[\'"]?images[\'"]?\s*:\s*\[[^\]]*tee[^\]]*\]', arr_tee, content, count=1)

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 PARSER COMPLETATO CON SUCCESSO.")
