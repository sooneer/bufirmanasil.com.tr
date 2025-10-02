const fs = require('fs');
const path = require('path');
const https = require('https');

// Konfigürasyon
const CONFIG = {
  inputFile: path.join(__dirname, '..', 'linkedin-links-list.txt'),
  outputDir: path.join(__dirname, '..', 'linkedin-responses'),
  delay: 3000, // Her istek arasında 3 saniye bekle
  timeout: 30000, // 30 saniye timeout
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
};

// Output klasörünü oluştur
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

// URL'den dosya adı oluştur
function getFilename(url) {
  const match = url.match(/linkedin\.com\/company\/([^/?#]+)/);
  if (match) {
    return `${match[1].replace(/[^a-z0-9-]/gi, '_')}.txt`;
  }
  return `unknown_${Date.now()}.txt`;
}

// HTTP/HTTPS isteği yap
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const options = {
      headers: {
        'User-Agent': CONFIG.userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
      },
      timeout: CONFIG.timeout
    };

    https.get(url, options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    }).on('error', (err) => {
      reject(err);
    }).on('timeout', () => {
      reject(new Error('Request timeout'));
    });
  });
}

// Bekleme fonksiyonu
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Ana işlem
async function processUrls() {
  try {
    // URL listesini oku
    const content = fs.readFileSync(CONFIG.inputFile, 'utf-8');
    const urls = content.split('\n')
      .map(line => line.trim())
      .filter(line => line && line.startsWith('http'));

    console.log(`Toplam ${urls.length} URL bulundu.\n`);

    let successful = 0;
    let failed = 0;

    // Her URL için işlem yap
    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      const filename = getFilename(url);
      const outputPath = path.join(CONFIG.outputDir, filename);

      console.log(`[${i + 1}/${urls.length}] İşleniyor: ${url}`);

      try {
        // URL'ye istek at
        const response = await fetchUrl(url);

        // Sonucu formatla
        const output = [
          `URL: ${url}`,
          `Tarih: ${new Date().toISOString()}`,
          `Status: ${response.statusCode}`,
          ``,
          `=== HEADERS ===`,
          JSON.stringify(response.headers, null, 2),
          ``,
          `=== BODY ===`,
          response.body
        ].join('\n');

        // Dosyaya kaydet
        fs.writeFileSync(outputPath, output, 'utf-8');

        console.log(`  ✓ Kaydedildi: ${filename} (Status: ${response.statusCode})`);
        successful++;

      } catch (error) {
        console.error(`  ✗ Hata: ${error.message}`);

        // Hata durumunu da kaydet
        const errorOutput = [
          `URL: ${url}`,
          `Tarih: ${new Date().toISOString()}`,
          `Hata: ${error.message}`,
          ``,
          error.stack || ''
        ].join('\n');

        fs.writeFileSync(outputPath, errorOutput, 'utf-8');
        failed++;
      }

      // Son URL değilse bekle
      if (i < urls.length - 1) {
        console.log(`  Bekleniyor... (${CONFIG.delay / 1000}s)\n`);
        await sleep(CONFIG.delay);
      }
    }

    // Özet
    console.log('\n' + '='.repeat(50));
    console.log(`İşlem tamamlandı!`);
    console.log(`Başarılı: ${successful}`);
    console.log(`Başarısız: ${failed}`);
    console.log(`Toplam: ${urls.length}`);
    console.log(`Sonuçlar: ${CONFIG.outputDir}`);
    console.log('='.repeat(50));

  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

// Script'i çalıştır
console.log('LinkedIn URL Fetcher');
console.log('='.repeat(50));
console.log(`Input: ${CONFIG.inputFile}`);
console.log(`Output: ${CONFIG.outputDir}`);
console.log(`Delay: ${CONFIG.delay}ms`);
console.log(`Timeout: ${CONFIG.timeout}ms`);
console.log('='.repeat(50) + '\n');

processUrls();
