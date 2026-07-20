# Master Word COM converter: converts each chapter source to clean .docx, filtered HTML, and TXT.
$ErrorActionPreference = 'Continue'
$repo = "C:\code\TesiLaureaR2"
$docxDir = Join-Path $repo "build\docx"
$htmlDir = Join-Path $repo "build\html_word"
$txtDir  = Join-Path $repo "build\text"
New-Item -ItemType Directory -Force -Path $docxDir,$htmlDir,$txtDir | Out-Null
$t=[Diagnostics.Stopwatch]::StartNew()

# id => source relative path
$sources = [ordered]@{
  "00_introduzione"        = "Introduzione.docx"
  "01_stern_gerlach"       = "1. Esperimento di Stern-Gerlach\Esperimento di Stern-Gerlach.docx"
  "02_stern_gerlach_cascata" = "2. Esperimenti di Stern-Gerlach in cascata\Esperimenti di Stern-Gerlach in cascata.docx"
  "04_diffrazione"         = "4. Diffrazione degli Elettroni\DIFFRAZIONE DEGLI ELETTRONI.docx"
  "05_rutherford"          = "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD 2.docx"
  "05_rutherford_alt"      = "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD.docx"
  "06_ulteriori_sviluppi"  = "6. Ulteriori sviluppi della Teoria\Ulteriori sviluppi della Teoria.docx"
  "07_franck_hertz"        = "7. Esperimento di Franck-Hertz\ESPERIMENTO DI FRANCK-HERTZ.docx"
  "08_effetto_fotoelettrico" = "8. Effetto Fotoelettrico\EFFETTO FOTOELETTRICO.docx"
  "09_spettri_atomici"     = "9. Spettri atomici di emissione\SPETTRI ATOMICI DI EMISSIONE.docx"
}

$wdFormatXMLDocument = 12
$wdFormatFilteredHTML = 10
$wdFormatText = 2

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try { $word.Options.SaveInterval = 0 } catch {}

foreach ($id in $sources.Keys) {
    $src = Join-Path $repo $sources[$id]
    Write-Output "==== $id ===="
    if (-not (Test-Path $src)) { Write-Output "  MISSING $src"; continue }
    try {
        $doc = $word.Documents.Open($src, $false, $true, $false, "", "", $false, "", "", 0, "", $false, $false, 0, $true)
        $pc = $doc.Paragraphs.Count; $cc = $doc.Characters.Count
        Write-Output "  opened paragraphs=$pc chars=$cc"
        $doc.SaveAs2((Join-Path $docxDir "$id.docx"), $wdFormatXMLDocument)
        $doc.SaveAs2((Join-Path $htmlDir "$id.htm"), $wdFormatFilteredHTML)
        $doc.SaveAs2((Join-Path $txtDir "$id.txt"), $wdFormatText, $false, "", $false, "", $false, $false, $false, $false, $false, 65001)
        $doc.Close($false)
        Write-Output "  saved docx/html/txt"
    } catch {
        Write-Output "  ERROR: $($_.Exception.Message)"
        try { $doc.Close($false) } catch {}
    }
}

$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Output "ALL DONE elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s"