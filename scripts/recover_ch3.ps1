# Attempt to open & recover the corrupt chapter 3 .doc via Word COM
$ErrorActionPreference = 'Stop'
$src = "C:\code\TesiLaureaR2\3. Esperimenti con gli Elettroni\ESPERIMENTI CON GLI ELETTRONI.docx"
$outDir = "C:\code\TesiLaureaR2\build\recover"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$t=[Diagnostics.Stopwatch]::StartNew()

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0  # wdAlertsNone

$wdOpenFormatAuto = 0
$wdFormatXMLDocument = 12
$wdFormatFilteredHTML = 10
$wdFormatText = 2

try {
    # Open with repair
    $doc = $word.Documents.Open($src, $false, $true, $false, "", "", $false, "", "", $wdOpenFormatAuto, "", $false, $false, 0, $true)
    Write-Output "OPENED. Paragraphs: $($doc.Paragraphs.Count)  Chars: $($doc.Characters.Count)"
    $preview = $doc.Range(0, [Math]::Min(400, $doc.Characters.Count)).Text
    Write-Output "PREVIEW: $preview"
    $docxOut = Join-Path $outDir "cap3_recovered.docx"
    $doc.SaveAs2($docxOut, $wdFormatXMLDocument)
    $txtOut = Join-Path $outDir "cap3_recovered.txt"
    $doc.SaveAs2($txtOut, $wdFormatText)
    Write-Output "SAVED: $docxOut"
    $doc.Close($false)
} catch {
    Write-Output "OPEN FAILED: $($_.Exception.Message)"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s"