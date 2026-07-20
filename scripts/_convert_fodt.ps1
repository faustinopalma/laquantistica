$ErrorActionPreference = 'Stop'
$sw = [Diagnostics.Stopwatch]::StartNew()
$soffice = "C:\Program Files\LibreOffice\program\soffice.exe"
$docs = @(
  "Introduzione.docx",
  "1. Esperimento di Stern-Gerlach\Esperimento di Stern-Gerlach.docx",
  "2. Esperimenti di Stern-Gerlach in cascata\Esperimenti di Stern-Gerlach in cascata.docx",
  "4. Diffrazione degli Elettroni\DIFFRAZIONE DEGLI ELETTRONI.docx",
  "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD 2.docx",
  "6. Ulteriori sviluppi della Teoria\Ulteriori sviluppi della Teoria.docx",
  "7. Esperimento di Franck-Hertz\ESPERIMENTO DI FRANCK-HERTZ.docx",
  "8. Effetto Fotoelettrico\EFFETTO FOTOELETTRICO.docx",
  "9. Spettri atomici di emissione\SPETTRI ATOMICI DI EMISSIONE.docx"
)
New-Item -ItemType Directory -Force -Path build\fodt | Out-Null
foreach ($d in $docs) {
  & $soffice --headless --convert-to fodt --outdir build\fodt $d 2>&1 | Out-Null
  Write-Output ("converted: " + [IO.Path]::GetFileName($d))
}
Write-Output ("elapsed: {0:N1}s" -f $sw.Elapsed.TotalSeconds)
Get-ChildItem build\fodt\*.fodt | ForEach-Object { $c=(Get-Content $_.FullName -Raw).Split('<math').Length - 1; Write-Output ("{0}: {1} math" -f $_.Name, $c) }
