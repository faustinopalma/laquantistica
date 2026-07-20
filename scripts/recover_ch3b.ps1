# Attempt to open & recover the corrupt chapter 3 .doc via Word COM (multiple strategies)
$ErrorActionPreference = 'Continue'
$src = "C:\code\TesiLaureaR2\3. Esperimenti con gli Elettroni\ESPERIMENTI CON GLI ELETTRONI.docx"
$outDir = "C:\code\TesiLaureaR2\build\recover"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$t=[Diagnostics.Stopwatch]::StartNew()

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$wdFormatXMLDocument = 12
$wdFormatText = 2

# Strategy 1: OpenAndRepair = true (13th positional arg)
Write-Output "--- Strategy 1: OpenAndRepair=true ---"
try {
    $doc = $word.Documents.Open($src, $false, $true, $false, "", "", $false, "", "", 0, "", $false, $true, 0, $true)
    Write-Output "  OPENED. Paragraphs: $($doc.Paragraphs.Count)  Chars: $($doc.Characters.Count)"
    $n = [Math]::Min(400, [int]$doc.Characters.Count)
    if ($n -gt 0) { Write-Output ("  PREVIEW: " + $doc.Range(0,$n).Text) }
    $doc.SaveAs2((Join-Path $outDir "cap3_recovered.docx"), $wdFormatXMLDocument)
    $doc.SaveAs2((Join-Path $outDir "cap3_recovered.txt"), $wdFormatText)
    $doc.Close($false)
    Write-Output "  SUCCESS"
} catch {
    Write-Output "  FAILED: $($_.Exception.Message)"
    # Strategy 2: Recover Text from Any File converter
    Write-Output "--- Strategy 2: RecoverText converter ---"
    try {
        $doc = $word.Documents.OpenNoRepairDialog($src, $false, $true, $false, "", "", $false, "", "", "Recover Text from Any File", "", $false, $false, 0, $true)
        Write-Output "  OPENED via RecoverText. Chars: $($doc.Characters.Count)"
        $doc.SaveAs2((Join-Path $outDir "cap3_recovered.txt"), $wdFormatText)
        $doc.Close($false)
    } catch {
        Write-Output "  FAILED: $($_.Exception.Message)"
    }
}

$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Output "elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s"