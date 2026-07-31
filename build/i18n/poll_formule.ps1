$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/v2/en/05-rutherford' -UseBasicParsing -TimeoutSec 25
    $ok = ($r.Content -match 'Particles per unit of time in') -and ($r.Content -notmatch 'Particelle per unit')
    Write-Output "[$ts] poll $n  http=$($r.StatusCode)  formuleEN=$ok  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
    if ($ok) { Write-Output "VERDICT: formule online dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0 }
  } catch {
    Write-Output "[$ts] poll $n  non ancora: $($_.Exception.Message.Split([char]10)[0])"
  }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
