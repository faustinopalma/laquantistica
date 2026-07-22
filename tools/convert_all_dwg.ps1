# Batch: converte TUTTI i DWG delle schede (originale-docx/N. ...) in SVG puliti.
# Output: diagrammi-dwg/NN/  (SVG vettoriali + PNG anteprima)
# Pipeline: DWG -> DXF (ODA File Converter) -> SVG+PNG (ezdxf).
$ErrorActionPreference = 'Continue'
$env:PYTHONHOME = $null; $env:PYTHONPATH = $null
$oda = "C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"
$py = ".\.venv\Scripts\python.exe"
$src = "originale-docx"

$dirs = Get-ChildItem $src -Directory | Where-Object { $_.Name -match '^\d\.\s' -and $_.Name -notmatch 'ricostruito' }
foreach ($d in $dirs) {
    $nn = ('{0:00}' -f [int]($d.Name.Substring(0, 1)))
    $dwgs = Get-ChildItem $d.FullName -Filter *.dwg -File -ErrorAction SilentlyContinue
    if (-not $dwgs -or $dwgs.Count -eq 0) { Write-Output "SKIP $nn ($($d.Name)) : 0 dwg"; continue }
    $indwg = "scansioni\_dwg\$nn"; $outdxf = "scansioni\_dxf\$nn"; $outsvg = "diagrammi-dwg\$nn"
    Remove-Item $indwg -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $outdxf -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $indwg, $outdxf, $outsvg | Out-Null
    Copy-Item "$($d.FullName)\*.dwg" $indwg -Force
    $ai = (Resolve-Path $indwg).Path; $ao = (Resolve-Path $outdxf).Path
    $t = [Diagnostics.Stopwatch]::StartNew()
    $p = Start-Process -FilePath $oda -ArgumentList "`"$ai`"", "`"$ao`"", "ACAD2018", "DXF", "0", "1", "*.DWG" -PassThru -Wait
    & $py tools\dxf2svg.py $outdxf $outsvg 2>&1 | Out-Null
    $svgn = (Get-ChildItem $outsvg -Filter *.svg -ErrorAction SilentlyContinue).Count
    Write-Output ("DONE {0} : {1} dwg -> {2} svg  ({3}s)" -f $nn, $dwgs.Count, $svgn, [math]::Round($t.Elapsed.TotalSeconds, 1))
}
Write-Output "=== ALBERO diagrammi-dwg ==="
Get-ChildItem "diagrammi-dwg" -Directory | ForEach-Object { "{0}: {1} svg" -f $_.Name, (Get-ChildItem $_.FullName -Filter *.svg).Count }
