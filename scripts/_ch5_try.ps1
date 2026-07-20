$env:PYTHONHOME = $null; $env:PYTHONPATH = $null; $env:PYTHONUTF8 = $null
$prof = "file:///" + ($PWD.Path -replace '\\', '/') + "/build/louser"
$soffice = "C:\Program Files\LibreOffice\program\soffice.com"
$src = "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD 2.docx"
foreach ($flt in @("MS Word 97", "MS Word 2007 XML")) {
  New-Item -ItemType Directory -Force -Path build\fodt\v2try | Out-Null
  & $soffice "-env:UserInstallation=$prof" --headless --infilter="$flt" --convert-to fodt --outdir build\fodt\v2try $src 2>&1 | Out-String | Write-Output
  $ok = Test-Path "build\fodt\v2try\ESPERIMENTO DI RUTHERFORD 2.fodt"
  Write-Output ("filter [$flt] -> $ok")
  if ($ok) { break }
}
