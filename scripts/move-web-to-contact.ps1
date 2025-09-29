# Web alanını root seviyeden contact altına taşıyan script
# Usage: .\scripts\move-web-to-contact.ps1

$publicPath = "public\data\company"
$docsPath = "docs\data\company"

$totalFiles = 0
$updatedFiles = 0
$skippedFiles = 0
$errorFiles = 0

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Web alanını contact altına taşıma scripti" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

foreach ($basePath in @($publicPath, $docsPath)) {
    if (-not (Test-Path $basePath)) {
        Write-Host "⚠️  Klasör bulunamadı: $basePath" -ForegroundColor Yellow
        continue
    }

    Write-Host "`n📁 İşleniyor: $basePath" -ForegroundColor Green
    Write-Host "─────────────────────────────────────────────`n"

    $jsonFiles = Get-ChildItem -Path $basePath -Filter "*.json" -File

    foreach ($file in $jsonFiles) {
        $totalFiles++

        try {
            # JSON'u oku
            $content = Get-Content $file.FullName -Raw -Encoding UTF8
            $json = $content | ConvertFrom-Json

            # Root seviyede web alanı var mı kontrol et
            if ($json.PSObject.Properties.Name -contains "web") {
                $webValue = $json.web

                # Contact objesi yoksa oluştur
                if (-not $json.contact) {
                    $json | Add-Member -MemberType NoteProperty -Name "contact" -Value ([PSCustomObject]@{
                        web = ""
                        email = ""
                        phone = ""
                        phone2 = ""
                        address = ""
                        googleMaps = ""
                        googleMapsIframe = ""
                        formEndpoint = ""
                    })
                }

                # Web değerini contact altına taşı (sadece contact.web boşsa)
                if ([string]::IsNullOrWhiteSpace($json.contact.web) -and -not [string]::IsNullOrWhiteSpace($webValue)) {
                    $json.contact.web = $webValue
                    Write-Host "  📝 $($file.Name): web taşındı ($webValue)" -ForegroundColor Green
                }
                elseif ([string]::IsNullOrWhiteSpace($webValue)) {
                    Write-Host "  ⚪ $($file.Name): root.web boş, siliniyor" -ForegroundColor Gray
                }
                else {
                    Write-Host "  ⚠️  $($file.Name): contact.web zaten dolu, root.web siliniyor" -ForegroundColor Yellow
                }

                # Root seviyeden web alanını sil
                $json.PSObject.Properties.Remove("web")

                # JSON'u kaydet
                $json | ConvertTo-Json -Depth 100 | Set-Content $file.FullName -Encoding UTF8
                $updatedFiles++
            }
            else {
                $skippedFiles++
            }
        }
        catch {
            Write-Host "  ❌ $($file.Name): Hata - $($_.Exception.Message)" -ForegroundColor Red
            $errorFiles++
        }
    }
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "📊 ÖZET" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Toplam dosya      : $totalFiles"
Write-Host "Güncellenen       : $updatedFiles ✅" -ForegroundColor Green
Write-Host "Atlanılan         : $skippedFiles ⚪" -ForegroundColor Gray
Write-Host "Hatalı            : $errorFiles ❌" -ForegroundColor Red
Write-Host ""
