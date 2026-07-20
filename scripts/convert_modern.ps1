$env:PYTHONHOME = $null; $env:PYTHONPATH = $null; $env:PYTHONUTF8 = $null
$sw = [Diagnostics.Stopwatch]::StartNew()
$soffice = "C:\Program Files\LibreOffice\program\soffice.com"
$prof = "file:///" + ($PWD.Path -replace '\\', '/') + "/build/louser"
$dest = "originale-moderno"
$roots = @("originale-doc", "originale-docx")
$ok = 0; $fail = @()
$files = Get-ChildItem -Path $roots -Recurse -File -Include *.doc, *.docx -ErrorAction SilentlyContinue
Write-Output ("found {0} Word files" -f $files.Count)
foreach ($f in $files) {
  $rel = $f.FullName.Substring($PWD.Path.Length + 1)          # e.g. originale-docx\4. ...\X.docx
  $outdir = Join-Path $dest (Split-Path $rel -Parent)
  New-Item -ItemType Directory -Force -Path $outdir | Out-Null
  & $soffice "-env:UserInstallation=$prof" --headless --convert-to "docx:MS Word 2007 XML" --outdir $outdir $f.FullName *> $null
  $expected = Join-Path $outdir ([IO.Path]::GetFileNameWithoutExtension($f.Name) + ".docx")
  if (Test-Path -LiteralPath $expected) { $ok++ } else { $fail += $rel }
}
Write-Output ("converted OK: {0}" -f $ok)
Write-Output ("FAILED ({0}):" -f $fail.Count)
$fail | ForEach-Object { Write-Output ("  - $_") }
Write-Output ("elapsed: {0:N1}s" -f $sw.Elapsed.TotalSeconds)
