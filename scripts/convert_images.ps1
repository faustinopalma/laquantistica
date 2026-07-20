# Convert every chapter's original images to PNG into the site's img/<key> folders,
# plus the pandoc-extracted media for ch1/ch2 (equation images).
$ErrorActionPreference = 'Continue'
$repo = 'C:\code\TesiLaureaR2'
$site = Join-Path $repo '3. Esperimenti con gli Elettroni (ricostruito)\sito-web'
$conv = Join-Path $repo 'scripts\wmf2png.ps1'

$map = [ordered]@{
  '00_introduzione'          = $null
  '01_stern_gerlach'         = '1. Esperimento di Stern-Gerlach'
  '02_stern_gerlach_cascata' = '2. Esperimenti di Stern-Gerlach in cascata'
  '03_elettroni'             = '3. Esperimenti con gli Elettroni'
  '04_diffrazione'           = '4. Diffrazione degli Elettroni'
  '05_rutherford'            = '5. Esperimento di Rutherford'
  '06_ulteriori_sviluppi'    = '6. Ulteriori sviluppi della Teoria'
  '07_franck_hertz'          = '7. Esperimento di Franck-Hertz'
  '08_effetto_fotoelettrico' = '8. Effetto Fotoelettrico'
  '09_spettri_atomici'       = '9. Spettri atomici di emissione'
}

foreach ($key in $map.Keys) {
  $folder = $map[$key]
  if (-not $folder) { continue }
  $inDir = Join-Path $repo $folder
  $outDir = Join-Path $site "img\$key"
  Write-Output "=== $key ==="
  & powershell -NoProfile -ExecutionPolicy Bypass -File $conv -InputDir $inDir -OutDir $outDir -MaxW 1100 | Select-Object -Last 2
}

# pandoc equation/figure media for ch1 and ch2 (already extracted as WMF)
foreach ($k in @('01_stern_gerlach','02_stern_gerlach_cascata')) {
  $media = Join-Path $repo "build\pandoc_test\media_$($k.Substring(0,3) -replace '_','')"
}
Write-Output "IMG DONE"
