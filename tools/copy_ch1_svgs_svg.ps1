$t=[Diagnostics.Stopwatch]::StartNew()
$src = "diagrammi-dwg\01"
$map = @{ "FIG2.svg"="fig1.svg"; "FIG1.svg"="fig2.svg"; "FIG3.svg"="fig3.svg"; "FIG4.svg"="fig4.svg"; "PROGET~2.svg"="app3.svg"; "PROGETTO.svg"="app4.svg"; "PROGET~1.svg"="app5.svg"; "FIG5.svg"="app6.svg" }
$dest = "site\svg\img\pandoc_ch1"
foreach ($k in $map.Keys) { Copy-Item (Join-Path $src $k) (Join-Path $dest $map[$k]) -Force }
Write-Output "copied 8 -> $dest"
Write-Output "elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s"
