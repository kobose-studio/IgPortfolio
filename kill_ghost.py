import re

target = 'src/components/PortfolioSceneSphere.astro'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Mettiamo in cassaforte la griglia perfetta
start_id = content.find('id="contacts-content"')
if start_id != -1:
    start_good = content.rfind('<div', 0, start_id)
    depth = 0
    i = start_good
    end_good = -1
    
    # Navigazione profonda del DOM per trovare la chiusura esatta
    while i < len(content):
        if content[i:].startswith('<div'):
            depth += 1
            i += 4
        elif content[i:].startswith('</div'):
            depth -= 1
            if depth == 0:
                end_good = i + 6
                break
            i += 6
        else:
            i += 1

    if end_good != -1:
        good_block = content[start_good:end_good]
        before = content[:start_good]
        after = content[end_good:]

        # 2. Il pattern del mutante (Stringa grezza da "EMAIL DIRECT" a "(VC) ↗")
        ghost_pattern = re.compile(r'EMAIL DIRECT //IMLANDMOTEROSA@GMAIL\.COM.*?ALAGNA VALSESIA \(VC\)\s*↗?', re.DOTALL | re.IGNORECASE)

        # 3. Irradiamo il codice esterno alla cassaforte
        before_clean = re.sub(ghost_pattern, '', before)
        after_clean = re.sub(ghost_pattern, '', after)

        # Pulizia di eventuali gusci vuoti lasciati dal fantasma (es. <div></div>)
        empty_tags = re.compile(r'<([a-z]+)[^>]*>\s*</\1>', re.IGNORECASE)
        before_clean = re.sub(empty_tags, '', before_clean)
        after_clean = re.sub(empty_tags, '', after_clean)

        # 4. Ricostruiamo la tela
        content = before_clean + good_block + after_clean
        print("✅ Fantasma estirpato con successo dalla matrice.")
    else:
        print("⚠️ Errore: Fine del contenitore sacro non individuata.")
else:
    print("⚠️ Errore: Contenitore sacro non trovato.")

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)
