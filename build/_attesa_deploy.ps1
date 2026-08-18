param(
  [string]$Url = 'https://laquantistica.com/it/lab-05-rutherford.html',
  [string]$Marker = 'drawChain',
  [int]$IntervalSec = 20,
  [int]$BudgetSec = 420
)
$sw = [Diagnostics.Stopwatch]::StartNew()
while ($sw.Elapsed.TotalSeconds -lt $BudgetSec) {
  $cb = [guid]::NewGuid().ToString('N')
  try {
    $r = Invoke-WebRequest -Uri "$Url`?cb=$cb" -UseBasicParsing -TimeoutSec 15
    $hit = $r.Content -match [regex]::Escape($Marker)
  } catch { $hit = $false }
  $t = [math]::Round($sw.Elapsed.TotalSeconds, 0)
  Write-Output ("{0}  +{1,4}s  marcatore presente: {2}" -f (Get-Date -Format 'HH:mm:ss'), $t, $hit)
  if ($hit) { Write-Output "VERDICT: online dopo ${t}s"; exit 0 }
  Start-Sleep -Seconds $IntervalSec
}
Write-Output "VERDICT: NON comparso entro ${BudgetSec}s"
exit 1
