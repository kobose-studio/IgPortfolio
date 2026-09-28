import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log("🛠️ Inizializzazione Alchimia di Rete...");

const possibleEnvFiles = ['.env', '.env.local', '.env.development'];
let envFound = false;

for (const file of possibleEnvFiles) {
  const envPath = path.join(__dirname, file);
  if (fs.existsSync(envPath)) {
    console.log(`🔍 Rilevato file d'ambiente: [ ${file} ]`);
    const envFile = fs.readFileSync(envPath, 'utf8');
    
    envFile.split(/\r?\n/).forEach(line => {
      if (line.trim().startsWith('#') || !line.includes('=')) return;
      const [key, ...values] = line.split('=');
      const cleanKey = key.trim();
      let cleanValue = values.join('=').trim().replace(/^['"](.*)['"]$/, '$1'); 
      process.env[cleanKey] = cleanValue;
    });
    envFound = true;
    break;
  }
}

const ACCESS_TOKEN = process.env.IG_ACCESS_TOKEN || process.env.INSTAGRAM_TOKEN || process.env.PUBLIC_INSTAGRAM_TOKEN || ''; 
const CACHE_FILE = path.join(__dirname, 'src', 'portfolio_cache.json');

const FIELDS = 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,children{id,media_type,media_url,thumbnail_url}';

async function fetchInstagramArchive() {
  if (!ACCESS_TOKEN) {
    console.error('❌ ERRORE: Token non trovato in memoria!');
    return;
  }

  console.log('🔓 Chiave IG_ACCESS_TOKEN rilevata! Decrittazione Archivi in corso...');

  try {
    let allMedia = [];
    let url = `https://graph.instagram.com/me/media?fields=${FIELDS}&access_token=${ACCESS_TOKEN}&limit=50`;

    console.log('🔄 Avvio estrazione ricorsiva dell\'INTERO ARCHIVIO IMLAND (Target 500 nodi)...');

    // 🚀 UNLOCKED: Limite alzato a 500 per catturare l'intero patrimonio di 450+ post!
    while (url && allMedia.length < 500) {
      const response = await fetch(url);
      const data = await response.json();

      if (data.error) {
        console.error('❌ Errore API Instagram:', data.error.message);
        return;
      }

      if (data.data) {
        allMedia = [...allMedia, ...data.data];
        console.log(`📦 Scaricati ${data.data.length} nodi. Totale accumulato: ${allMedia.length}`);
        url = data.paging?.next || null;
      } else {
        break;
      }
    }

    const payload = {
      updated_at: new Date().toISOString(),
      count: allMedia.length,
      data: allMedia
    };

    fs.writeFileSync(CACHE_FILE, JSON.stringify(payload, null, 2));
    console.log(`✅ ARCHIVIO COMPLETO BLINDATO! Salvati ${allMedia.length} media totali con Caroselli!`);
  } catch (error) {
    console.error('❌ Errore critico durante la compilazione:', error);
  }
}

fetchInstagramArchive();
