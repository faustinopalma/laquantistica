param()
$env:PYTHONHOME = $null; $env:PYTHONPATH = $null; $env:PYTHONUTF8 = $null
$sw = [Diagnostics.Stopwatch]::StartNew()
$soffice = "C:\Program Files\LibreOffice\program\soffice.com"
$prof = "file:///" + ($PWD.Path -replace '\\', '/') + "/build/louser"
$map = @{ "media_ch1" = "pandoc_ch1"; "media_ch2" = "pandoc_ch2" }
foreach ($k in $map.Keys) {
  $indir = "build\pandoc_test\$k\media"
  $outdir = "build\pandoc_svg\$($map[$k])"
  New-Item -ItemType Directory -Force -Path $outdir | Out-Null
  $wmfs = Get-ChildItem "$indir\*.wmf" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
  if ($wmfs.Count -eq 0) { Write-Output "$k : no wmf"; continue }
  & $soffice "-env:UserInstallation=$prof" --headless --convert-to svg --outdir $outdir @wmfs *> $null
  $n = (Get-ChildItem "$outdir\*.svg" -ErrorAction SilentlyContinue).Count
  Write-Output ("$k -> $($map[$k]) : $($wmfs.Count) wmf -> $n svg")
}
Write-Output ("elapsed: {0:N1}s" -f $sw.Elapsed.TotalSeconds)
