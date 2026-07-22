param([string]$ch, [string]$prefix)
$env:PYTHONHOME=$null; $env:PYTHONPATH=$null
$t=[Diagnostics.Stopwatch]::StartNew()
$f="publish\leggi\$ch.html"
(Get-Content $f -Raw) -replace "<figure id=""fig-$prefix-", "<figure class=""fig-inline"" id=""fig-$prefix-" | Set-Content $f -NoNewline -Encoding utf8
& .\.venv\Scripts\python.exe tools\bilingualize.py $f "tools\tr\$ch.json"
& .\.venv\Scripts\python.exe tools\verify_bilingual.py $f
Write-Output "elapsed: $([math]::Round($t.Elapsed.TotalSeconds,1))s"
