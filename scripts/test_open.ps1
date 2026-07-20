# Set Trust Center overrides in BOTH user and policy hives, then test opening one OLE .doc
$ErrorActionPreference = 'Continue'
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 300

$hives = @(
  "HKCU:\Software\Microsoft\Office\16.0\Word\Security",
  "HKCU:\Software\Policies\Microsoft\Office\16.0\Word\Security"
)
foreach ($sec in $hives) {
  New-Item -Path $sec -Force | Out-Null
  New-ItemProperty -Path $sec -Name "ExtensionHardening" -Value 0 -PropertyType DWord -Force | Out-Null
  $fv = "$sec\FileValidation"; New-Item -Path $fv -Force | Out-Null
  New-ItemProperty -Path $fv -Name "EnableOnLoad" -Value 0 -PropertyType DWord -Force | Out-Null
  $fb = "$sec\FileBlock"; New-Item -Path $fb -Force | Out-Null
  foreach ($k in "Word2Files","Word60Files","Word95Files","Word97Files","Word2000Files","Word2003Files","Word2007Files","Word2007FilesForReadWrite","Word2003FilesForReadWrite","BinaryFiles") {
    New-ItemProperty -Path $fb -Name $k -Value 0 -PropertyType DWord -Force | Out-Null
  }
  New-ItemProperty -Path $fb -Name "OpenInProtectedView" -Value 0 -PropertyType DWord -Force | Out-Null
}
Write-Output "registry set in both hives"

# Prepare a .doc copy of the OLE intro
$repo = "C:\code\TesiLaureaR2"
$tmp = Join-Path $repo "build\tmp_src"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$src = Join-Path $repo "Introduzione.docx"
$copyDoc  = Join-Path $tmp "intro_test.doc"
Copy-Item -LiteralPath $src -Destination $copyDoc -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
Write-Output "Word started, version $($word.Version)"

foreach ($path in @($copyDoc, $src)) {
  Write-Output "--- trying: $path ---"
  try {
    $doc = $word.Documents.Open($path, $false, $true, $false, "", "", $false, "", "", 0, "", $false, $false, 0, $true)
    Write-Output "  OPENED paragraphs=$($doc.Paragraphs.Count) chars=$($doc.Characters.Count)"
    Write-Output ("  preview: " + $doc.Range(0,[Math]::Min(150,[int]$doc.Characters.Count)).Text)
    $doc.Close($false)
    Write-Output "  CLOSED ok"
  } catch {
    Write-Output "  FAILED: $($_.Exception.Message)"
  }
}
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Output "TEST DONE"