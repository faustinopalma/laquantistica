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
& "$PSScriptRoot\lo_convert.ps1" -Fmt fodt -OutDir build\fodt -Docs $docs
Get-ChildItem build\fodt\*.fodt | ForEach-Object { $c = (Get-Content $_.FullName -Raw).Split('<math').Length - 1; Write-Output ("{0}: {1} math" -f $_.Name, $c) }
