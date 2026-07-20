# Convert WMF/EMF/BMP images to PNG using .NET GDI+ (Windows PowerShell).
# Renders metafiles crisply and records each image's TRUE physical size (inches)
# to a manifest, so the web page can display equations/figures at the size they
# had in the original Word document.
param(
  [string]$InputDir,
  [string]$OutDir
)
Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$manifest = Join-Path $OutDir 'manifest.csv'
"name,wIn,hIn" | Set-Content -Encoding utf8 $manifest

$exts = @('.wmf', '.emf', '.bmp')
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
    if ($wIn -le 0) { $wIn = 1 }; if ($hIn -le 0) { $hIn = 1 }
    # Render width: clamp physical*220 into [480,1800] px, keep aspect
    $tw = [int][math]::Round($wIn * 220)
    if ($tw -lt 480) { $tw = 480 }
    if ($tw -gt 1800) { $tw = 1800 }
    $th = [int][math]::Max(1, [math]::Round($tw * ($nh / $nw)))
    if ($th -gt 2200) { $th = 2200; $tw = [int][math]::Round($th * ($nw / $nh)) }
    $bmp = New-Object System.Drawing.Bitmap($tw, $th)
    $bmp.SetResolution(150, 150)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::White)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.DrawImage($img, 0, 0, $tw, $th)
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    ('{0},{1:N3},{2:N3}' -f $outName, $wIn, $hIn) | Add-Content -Encoding utf8 $manifest
    Write-Output ("OK  {0} -> {1} ({2}x{3}px, {4:N2}x{5:N2}in)" -f $_.Name, $outName, $tw, $th, $wIn, $hIn)
  } catch {
    Write-Output ("ERR {0}: {1}" -f $_.Name, $_.Exception.Message)
  }
}
# copy JPG/PNG/GIF as-is
Get-ChildItem -LiteralPath $InputDir -File | Where-Object { @('.jpg','.jpeg','.png','.gif') -contains $_.Extension.ToLower() } | ForEach-Object {
  $out = Join-Path $OutDir ([System.IO.Path]::GetFileNameWithoutExtension($_.Name) + $_.Extension.ToLower())
  Copy-Item -LiteralPath $_.FullName -Destination $out -Force
}
