$env:PYTHONHOME = $null; $env:PYTHONPATH = $null; $env:PYTHONUTF8 = $null
$sw = [Diagnostics.Stopwatch]::StartNew()
$soffice = "C:\Program Files\LibreOffice\program\soffice.com"
$prof = "file:///" + ($PWD.Path -replace '\\', '/') + "/build/louser"
$keys = Get-ChildItem build\eqimg -Directory | Select-Object -ExpandProperty Name
foreach ($k in $keys) {
  $indir = "build\eqimg\$k"
  $outdir = "build\eqsvg\$k"
  New-Item -ItemType Directory -Force -Path $outdir | Out-Null
  $wmfs = Get-ChildItem "$indir\*.wmf" | Select-Object -ExpandProperty FullName
  if ($wmfs.Count -eq 0) { continue }
  & $soffice "-env:UserInstallation=$prof" --headless --convert-to svg --outdir $outdir @wmfs *> $null
  $n = (Get-ChildItem "$outdir\*.svg" -ErrorAction SilentlyContinue).Count
  Write-Output ("$k : $($wmfs.Count) wmf -> $n svg")
}
Write-Output ("elapsed: {0:N1}s" -f $sw.Elapsed.TotalSeconds)
