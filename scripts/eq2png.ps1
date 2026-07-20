# Render equation metafiles (WMF/EMF) to crisp PNGs at their TRUE physical size.
# Unlike wmf2png.ps1 (tuned for large figures), this keeps the original inches and
# renders at a high effective DPI so inline single-symbol equations stay small and
# display equations stay sharp. Emits a manifest (name,wIn,hIn) for the generator.
param(
  [string]$InputDir,
  [string]$OutDir,
  [int]$Dpi = 400
)
Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$manifest = Join-Path $OutDir 'manifest.csv'
"name,wIn,hIn" | Set-Content -Encoding utf8 $manifest

$exts = @('.wmf', '.emf')
$n = 0
Get-ChildItem -LiteralPath $InputDir -File | Where-Object { $exts -contains $_.Extension.ToLower() } | ForEach-Object {
  $src = $_.FullName
  $outName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name) + '.png'
  $out = Join-Path $OutDir $outName
  try {
    $img = [System.Drawing.Image]::FromFile($src)
    $nw = [double]$img.Width; $nh = [double]$img.Height
    $hr = [double]$img.HorizontalResolution; if ($hr -le 1) { $hr = 96 }
    $vr = [double]$img.VerticalResolution;   if ($vr -le 1) { $vr = 96 }
    $wIn = $nw / $hr; $hIn = $nh / $vr
    if ($wIn -le 0) { $wIn = 0.1 }; if ($hIn -le 0) { $hIn = 0.1 }
    $tw = [int][math]::Max(24, [math]::Round($wIn * $Dpi))
    $th = [int][math]::Max(12, [math]::Round($hIn * $Dpi))
    if ($tw -gt 4000) { $tw = 4000 }
    if ($th -gt 4000) { $th = 4000 }
    $bmp = New-Object System.Drawing.Bitmap($tw, $th)
    $bmp.SetResolution($Dpi, $Dpi)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::Transparent)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($img, 0, 0, $tw, $th)
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    ('{0},{1:N4},{2:N4}' -f $outName, $wIn, $hIn) | Add-Content -Encoding utf8 $manifest
    $n++
  } catch {
    Write-Output ("ERR {0}: {1}" -f $_.Name, $_.Exception.Message)
  }
}
Write-Output ("rendered {0} equations -> {1}" -f $n, $OutDir)
