param(
  [Parameter(Mandatory=$true)][string]$num,      # es. "05"
  [Parameter(Mandatory=$true)][string]$folder,   # es. "05_rutherford"
  [Parameter(Mandatory=$true)][string]$pairs     # "DWG=TGT;DWG=TGT" (senza estensione)
)
$ErrorActionPreference = 'Stop'
$editions = @('publish\leggi','site\mathml','site\svg')
$src = "diagrammi-dwg\$num"
$report = @()
foreach($p in ($pairs -split ';' | Where-Object { $_ -ne '' })){
  $kv = $p -split '='
  $dwg = $kv[0]; $tgt = $kv[1]
  $svgSrc = Join-Path $src "$dwg.svg"
  if(-not (Test-Path $svgSrc)){ $report += "MISSING dwg: $svgSrc"; continue }
  foreach($ed in $editions){
    $imgDir = Join-Path $ed "img\$folder"
    if(-not (Test-Path $imgDir)){ New-Item -ItemType Directory -Force $imgDir | Out-Null }
    Copy-Item $svgSrc (Join-Path $imgDir "$tgt.svg") -Force
    $html = Get-ChildItem "$ed\$num-*.html" | Select-Object -First 1
    $c = Get-Content $html.FullName -Raw
    $old = "img/$folder/$tgt.png"
    $new = "img/$folder/$tgt.svg"
    if($c -match [regex]::Escape($old)){
      $c = $c.Replace($old,$new)
      Set-Content -Path $html.FullName -Value $c -NoNewline -Encoding UTF8
      $report += "OK  $ed  $tgt.png -> $tgt.svg"
    } else {
      $report += "NOsrc $ed  $old (non trovato)"
    }
  }
}
$report | ForEach-Object { Write-Output $_ }
