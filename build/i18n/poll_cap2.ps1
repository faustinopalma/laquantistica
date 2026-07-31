$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/v2/en/02-stern-gerlach-cascata' -UseBasicParsing -TimeoutSec 20
    $ok = $r.Content -match '<title>Cascaded Stern'
    Write-Output "[$ts] poll $n  http=$($r.StatusCode)  titoloEN=$ok  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
    if ($ok) { Write-Output "VERDICT: capitolo 2 online dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0 }
  } catch {
    Write-Output "[$ts] poll $n  non ancora: $($_.Exception.Message.Split([char]10)[0])"
  }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
