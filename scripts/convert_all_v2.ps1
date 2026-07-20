# Master Word COM converter v2: copies OLE .doc(x) sources to a real .doc temp first,
# then converts each chapter source to clean .docx, filtered HTML, and TXT.
$ErrorActionPreference = 'Continue'
$repo = "C:\code\TesiLaureaR2"
$docxDir = Join-Path $repo "build\docx"
$htmlDir = Join-Path $repo "build\html_word"
$txtDir  = Join-Path $repo "build\text"
$tmpDir  = Join-Path $repo "build\tmp_src"
New-Item -ItemType Directory -Force -Path $docxDir,$htmlDir,$txtDir,$tmpDir | Out-Null
$log = Join-Path $repo "build\convert_log.txt"
"START $(Get-Date -Format o)" | Set-Content -Encoding utf8 $log
$t=[Diagnostics.Stopwatch]::StartNew()

$sources = [ordered]@{
  "00_introduzione"          = "Introduzione.docx"
  "01_stern_gerlach"         = "1. Esperimento di Stern-Gerlach\Esperimento di Stern-Gerlach.docx"
  "02_stern_gerlach_cascata" = "2. Esperimenti di Stern-Gerlach in cascata\Esperimenti di Stern-Gerlach in cascata.docx"
  "04_diffrazione"           = "4. Diffrazione degli Elettroni\DIFFRAZIONE DEGLI ELETTRONI.docx"
  "05_rutherford"            = "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD 2.docx"
  "05_rutherford_alt"        = "5. Esperimento di Rutherford\ESPERIMENTO DI RUTHERFORD.docx"
  "06_ulteriori_sviluppi"    = "6. Ulteriori sviluppi della Teoria\Ulteriori sviluppi della Teoria.docx"
  "07_franck_hertz"          = "7. Esperimento di Franck-Hertz\ESPERIMENTO DI FRANCK-HERTZ.docx"
  "08_effetto_fotoelettrico" = "8. Effetto Fotoelettrico\EFFETTO FOTOELETTRICO.docx"
  "09_spettri_atomici"       = "9. Spettri atomici di emissione\SPETTRI ATOMICI DI EMISSIONE.docx"
}

$wdFormatXMLDocument = 12
$wdFormatFilteredHTML = 10
$wdFormatText = 2

function Get-Sig($path) {
    $fs = [System.IO.File]::OpenRead($path)
    $b = New-Object byte[] 4
    [void]$fs.Read($b,0,4); $fs.Close()
    return ($b | ForEach-Object { $_.ToString('x2') }) -join ''
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

foreach ($id in $sources.Keys) {
    $src = Join-Path $repo $sources[$id]
    "==== $id ====" | Tee-Object -FilePath $log -Append
    if (-not (Test-Path $src)) { "  MISSING $src" | Tee-Object -FilePath $log -Append; continue }
    $sig = Get-Sig $src
    # With ExtensionHardening disabled, Word opens OLE-content .docx files directly.
    $openPath = $src
    "  sig=$sig open=$openPath" | Tee-Object -FilePath $log -Append
    try {
        $doc = $word.Documents.Open($openPath, $false, $true, $false, "", "", $false, "", "", 0, "", $false, $false, 0, $true)
        $pc = $doc.Paragraphs.Count; $cc = $doc.Characters.Count
        "  opened paragraphs=$pc chars=$cc" | Tee-Object -FilePath $log -Append
        $doc.SaveAs2((Join-Path $docxDir "$id.docx"), $wdFormatXMLDocument)
        $doc.SaveAs2((Join-Path $htmlDir "$id.htm"), $wdFormatFilteredHTML)
        $doc.SaveAs2((Join-Path $txtDir "$id.txt"), $wdFormatText, $false, "", $false, "", $false, $false, $false, $false, $false, 65001)
        $doc.Close($false)
        "  OK saved" | Tee-Object -FilePath $log -Append
    } catch {
        "  ERROR: $($_.Exception.Message)" | Tee-Object -FilePath $log -Append
        try { $doc.Close($false) } catch {}
    }
}

$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
"ALL DONE elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s" | Tee-Object -FilePath $log -Append