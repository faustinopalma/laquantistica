$ErrorActionPreference = 'Stop'
$soffice = "C:\Program Files\LibreOffice\program\soffice.exe"
$src = "9. Spettri atomici di emissione\SPETTRI ATOMICI DI EMISSIONE.docx"
Write-Output ("exists: " + (Test-Path $src))
New-Item -ItemType Directory -Force -Path build\mmltest | Out-Null
& $soffice --headless --convert-to fodt --outdir build\mmltest $src 2>&1 | Out-String | Write-Output
& $soffice --headless --convert-to "docx:MS Word 2007 XML" --outdir build\mmltest $src 2>&1 | Out-String | Write-Output
Get-ChildItem build\mmltest | Select-Object Name, Length | Format-Table | Out-String | Write-Output
