# Root seviyesindeki web alanını contact altına taşıma script'i (v2 - Hashtable yaklaşımı)
# UTF-8 encoding kullanarak JSON dosyalarını güvenle işler

$folders = @(
    "public\data\company",
    "docs\data\company"
)

$totalCount = 0
$updatedCount = 0
$skippedCount = 0
$errorCount = 0

foreach ($folder in $folders) {
    Write-Host ""
    Write-Host "📁 İşleniyor: $folder" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""

    if (-not (Test-Path $folder)) {
        Write-Host "  ⚠️  Klasör bulunamadı: $folder" -ForegroundColor Yellow
        continue
    }

    $files = Get-ChildItem "$folder\*.json" -File

    foreach ($file in $files) {
        $totalCount++

        try {
            # JSON dosyasını UTF-8 encoding ile oku
            $jsonContent = Get-Content $file.FullName -Raw -Encoding UTF8
            $data = $jsonContent | ConvertFrom-Json

            # Root seviyede web var mı kontrol et
            $rootWeb = $null
            if ($data.PSObject.Properties.Name -contains 'web') {
                $rootWeb = $data.web
            }

            # Eğer root level web yoksa veya boşsa, atla
            if ([string]::IsNullOrWhiteSpace($rootWeb)) {
                $skippedCount++
                continue
            }

            # contact nesnesini hashtable'a çevir veya yeni oluştur
            $contactHash = @{}
            if ($data.PSObject.Properties.Name -contains 'contact' -and $data.contact -ne $null) {
                # Mevcut contact properties'i kopyala
                $data.contact.PSObject.Properties | ForEach-Object {
                    $contactHash[$_.Name] = $_.Value
                }
            }

            # Eğer contact.web zaten doluysa, atla
            if ($contactHash.ContainsKey('web') -and -not [string]::IsNullOrWhiteSpace($contactHash['web'])) {
                $skippedCount++
                Write-Host "  ⚪ $($file.Name): Zaten contact.web dolu, atlandı" -ForegroundColor Gray
                continue
            }

            # Web'i contact hash'ine ekle
            $contactHash['web'] = $rootWeb

            # Tüm data'yı hashtable'a çevir
            $dataHash = @{}
            $data.PSObject.Properties | ForEach-Object {
                if ($_.Name -ne 'contact' -and $_.Name -ne 'web') {
                    $dataHash[$_.Name] = $_.Value
                }
            }

            # contact hash'ini ekle
            $dataHash['contact'] = $contactHash

            # Hashtable'dan PSCustomObject'e çevir ve JSON'a serialize et
            $newJsonContent = $dataHash | ConvertTo-Json -Depth 100 -Compress

            # Dosyaya UTF-8 encoding (BOM'suz) ile yaz
            [System.IO.File]::WriteAllText($file.FullName, $newJsonContent, [System.Text.UTF8Encoding]::new($false))

            $updatedCount++
            Write-Host "  ✅ $($file.Name): web → contact.web taşındı" -ForegroundColor Green

        } catch {
            $errorCount++
            Write-Host "  ❌ $($file.Name): Hata - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Özet
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "📊 ÖZET" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Toplam dosya      : $totalCount"
Write-Host "Güncellenen       : $updatedCount ✅" -ForegroundColor Green
Write-Host "Atlanılan         : $skippedCount ⚪" -ForegroundColor Gray
Write-Host "Hatalı            : $errorCount ❌" -ForegroundColor Red
