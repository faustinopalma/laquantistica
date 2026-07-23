Write-Output "=== tools _ch2 sizes ==="
Get-ChildItem tools\_ch2_*.py, tools\_omml2mml.ps1 | ForEach-Object { "{0,8}  {1}" -f $_.Length, $_.Name }
Write-Output "=== key build artifacts ==="
$files = 'ch2_final_map.tsv','ch2_index.tsv','ch2_latex_index.txt','ch2_omml2mml.xml','ch2_imgmap.tsv','ch2_map2.tsv'
foreach($f in $files){ $p = Join-Path 'build' $f; if(Test-Path $p){ "{0,9}  {1}" -f (Get-Item $p).Length, $f } else { "MISSING  $f" } }
Write-Output "=== mml folders ==="
foreach($d in 'ch2_mml','ch2_mml2','ch2_overrides'){ $p = Join-Path 'build' $d; if(Test-Path $p){ "{0}: {1} file" -f $d, (Get-ChildItem $p -File | Measure-Object).Count } else { "MISSING $d" } }
