# Angular Build ve Deploy Script
# Kullanım: .\deploy.ps1 -TargetPath "C:\hedef\klasor" [-BuildConfig "production"]

param(
  [Parameter(Mandatory = $true)]
  [string]$TargetPath,

  [string]$BuildConfig = "production",

  [switch]$SkipBuild,

  [switch]$Clean
)

# Terminal ekranını temizle
cls

# Renkli mesajlar için fonksiyonlar
function Write-Success {
  param([string]$Message)
  Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
  param([string]$Message)
  Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-Warning {
  param([string]$Message)
  Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
  param([string]$Message)
  Write-Host "❌ $Message" -ForegroundColor Red
}

# Script başlangıcı
Write-Info "Angular Deploy Script Başlatıldı"
Write-Info "Hedef Klasör: $TargetPath"
Write-Info "Build Konfigürasyonu: $BuildConfig"

# Build aşaması (eğer atlama bayrağı yoksa)
if (-not $SkipBuild) {
  Write-Warning "Angular uygulaması build ediliyor..."

  try {
    ng build --configuration=$BuildConfig

    if ($LASTEXITCODE -eq 0) {
      Write-Success "Build başarılı!"
    }
    else {
      Write-Error "Build başarısız! Çıkış kodu: $LASTEXITCODE"
      exit 1
    }
  }
  catch {
    Write-Error "Build sırasında hata oluştu: $($_.Exception.Message)"
    exit 1
  }
}
else {
  Write-Info "Build atlandı (SkipBuild bayrağı aktif)"
}

# Hedef klasörü kontrol et ve oluştur
try {
  if (!(Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    Write-Info "Hedef klasör oluşturuldu: $TargetPath"
  }
  else {
    Write-Info "Hedef klasör mevcut: $TargetPath"
  }
}
catch {
  Write-Error "Hedef klasör oluşturulamadı: $($_.Exception.Message)"
  exit 1
}

Write-Warning "Hedef klasördeki eski dosyalar temizleniyor..."
try {
  if (Test-Path "$TargetPath\*") {
    Remove-Item "$TargetPath\*" -Recurse -Force -ErrorAction Stop
    Write-Success "Eski dosyalar temizlendi"
  }
  else {
    Write-Info "Temizlenecek dosya bulunamadı"
  }
}
catch {
  Write-Error "Dosya temizleme hatası: $($_.Exception.Message)"
  exit 1
}


# Build çıktısını kontrol et
$SourcePath = "dist/browser"
if (!(Test-Path $SourcePath)) {
  Write-Error "Build çıktısı bulunamadı: $SourcePath"
  Write-Info "Lütfen önce 'ng build' komutunu çalıştırın"
  exit 1
}

# Dosyaları kopyala
Write-Warning "Dosyalar kopyalanıyor..."
try {
  $FileCount = (Get-ChildItem -Path $SourcePath -Recurse -File | Measure-Object).Count
  Write-Info "Kopyalanacak dosya sayısı: $FileCount"

  Copy-Item "$SourcePath\*" -Destination $TargetPath -Recurse -Force -ErrorAction Stop

  # Kopyalanan dosyaları doğrula
  $CopiedCount = (Get-ChildItem -Path $TargetPath -Recurse -File | Measure-Object).Count
  Write-Success "Dosyalar başarıyla kopyalandı! Toplam: $CopiedCount dosya"
}
catch {
  Write-Error "Dosya kopyalama hatası: $($_.Exception.Message)"
  exit 1
}

# GitHub Pages için index.html'i 404.html olarak da kopyala
Write-Warning "GitHub Pages için 404.html oluşturuluyor..."
try {
  $IndexPath = Join-Path $TargetPath "index.html"
  $NotFoundPath = Join-Path $TargetPath "404.html"

  if (Test-Path $IndexPath) {
    Copy-Item $IndexPath -Destination $NotFoundPath -Force -ErrorAction Stop
    Write-Success "index.html → 404.html kopyalandı (GitHub Pages SPA routing için)"
  } else {
    Write-Warning "index.html bulunamadı, 404.html oluşturulamadı"
  }
}
catch {
  Write-Error "404.html oluşturma hatası: $($_.Exception.Message)"
  # Bu hata kritik değil, devam et
}

# Özet bilgiler
Write-Info "═══════════════════════════════════════"
Write-Success "Deploy işlemi tamamlandı!"
Write-Info "Kaynak: $SourcePath"
Write-Info "Hedef: $TargetPath"
Write-Info "Build Config: $BuildConfig"
Write-Info "═══════════════════════════════════════"

# # Hedef klasörü explorer'da aç (opsiyonel)
# $OpenExplorer = Read-Host "Hedef klasörü Explorer'da açmak ister misiniz? (y/N)"
# if ($OpenExplorer -eq 'y' -or $OpenExplorer -eq 'Y') {
#   Start-Process "explorer.exe" -ArgumentList $TargetPath
# }
