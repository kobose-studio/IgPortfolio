import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# I tre array esatti dai file verificati su GitHub
arr_hoodie = "images: ['/brand/hoodie-1.jpg', '/brand/hoodie-2.jpg', '/brand/hoodie-3.jpg', '/brand/hoodie-4.jpg', '/brand/hoodie-5.jpg', '/brand/hoodie-6.jpg', '/brand/hoodie-7.jpg', '/brand/hoodie-8.jpg', '/brand/hoodie-9.jpg']"
arr_zip    = "images: ['/brand/hoodie_zip-1.jpg', '/brand/hoodie_zip-2.jpg', '/brand/hoodie_zip-3.jpg']"
arr_tee    = "images: ['/brand/tee-1.jpg', '/brand/tee-2.jpg', '/brand/tee-3.jpg', '/brand/tee-4.jpg', '/brand/tee-5.jpg']"

# Troviamo tutti i blocchi images: [...]
pattern = re.compile(r'images:\s*\[[\s\S]*?\]')
matches = list(pattern.finditer(content))

print(f"🔍 Trovati {len(matches)} blocchi 'images' nel file.")

if len(matches) >= 3:
    # Sostituiamo a partire dall'ultimo per preservare gli indici di memoria
    content = content[:matches[2].start()] + arr_tee + content[matches[2].end():]
    content = content[:matches[1].start()] + arr_zip + content[matches[1].end():]
    content = content[:matches[0].start()] + arr_hoodie + content[matches[0].end():]
    print("✅ Tutti e 3 gli array (9, 3, 5) sostituiti con successo!")
else:
    print("⚠️ Trovati meno di 3 blocchi array nel file.")

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print("🚀 Sostituzione cataloghi completata.")
