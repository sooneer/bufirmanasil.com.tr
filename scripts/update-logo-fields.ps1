# Update Logo Field in Company JSON Files
# Adds logo field to each company JSON based on slug

$companyDir = "public/data/company"
$jsonFiles = Get-ChildItem "$companyDir/*.json"

$updateCount = 0

foreach ($file in $jsonFiles) {
    $slug = $file.BaseName
    $data = Get-Content $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json

    # Determine logo path based on existing files
    $logoPath = $null
    $possibleExtensions = @('.svg', '.png', '.jpg', '.jpeg', '.webp')

    foreach ($ext in $possibleExtensions) {
        $logoFile = "public/img/company/$slug$ext"
        if (Test-Path $logoFile) {
            $logoPath = "img/company/$slug$ext"
            break
        }
    }

    # If no logo file found, use default SVG path
    if (-not $logoPath) {
        $logoPath = "img/company/$slug.svg"
    }

    # Update logo field if different or missing
    if ($data.logo -ne $logoPath) {
        $data | Add-Member -NotePropertyName 'logo' -NotePropertyValue $logoPath -Force

        # Save back to file
        $json = $data | ConvertTo-Json -Depth 10 -Compress:$false
        [System.IO.File]::WriteAllText($file.FullName, $json, [System.Text.UTF8Encoding]::new($false))

        $updateCount++
        Write-Host "$slug : $logoPath"
    }
}

Write-Host "`nGuncellenen dosya sayisi: $updateCount / $($jsonFiles.Count)"
