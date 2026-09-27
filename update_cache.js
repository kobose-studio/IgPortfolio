import fs from 'fs';
import https from 'https';

const env = fs.readFileSync('.env', 'utf-8');
const tokenMatch = env.match(/IG_ACCESS_TOKEN=(.*)/);
const token = tokenMatch ? tokenMatch[1].trim() : null;

if (!token) {
  console.error("❌ Token non trovato in .env");
  process.exit(1);
}

// IMPOSTA QUI IL LIMITE TOTALE DESIDERATO (es. 200 per massima fluidità o 400 per tutto l'archivio)
const TARGET_LIMIT = 400; 
let allMedia = [];

function fetchPage(url) {
  https.get(url, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
      try {
        const json = JSON.parse(body);
        if (json.data && json.data.length > 0) {
          allMedia = allMedia.concat(json.data);
          console.log(`📦 Pagina scaricata: +${json.data.length} nodi. Accumulati: ${allMedia.length}`);
        }

        // Se esiste una pagina successiva e non abbiamo raggiunto il target, proseguiamo
        if (json.paging && json.paging.next && allMedia.length < TARGET_LIMIT) {
          fetchPage(json.paging.next);
        } else {
          // Tronchiamo esattamente al target o salviamo la totalità
          const finalData = { data: allMedia.slice(0, TARGET_LIMIT) };
          fs.writeFileSync('src/portfolio_cache.json', JSON.stringify(finalData, null, 2));
          console.log(`✅ CACHE COMPLETA: Estratti ${finalData.data.length} nodi unici totali da Meta.`);
        }
      } catch (e) {
        console.error("❌ Errore parsing JSON:", e);
      }
    });
  }).on('error', (e) => console.error("❌ Errore chiamata HTTP:", e));
}

const initialUrl = `https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&limit=100&access_token=${token}`;
fetchPage(initialUrl);
