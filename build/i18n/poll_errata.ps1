$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  $sparita = $false
  try {
    Invoke-WebRequest -Uri 'https://laquantistica.com/it/errata' -UseBasicParsing -TimeoutSec 20 | Out-Null
  } catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 404) { $sparita = $true }
  }
  $viva = $false
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/it/01-stern-gerlach' -UseBasicParsing -TimeoutSec 20
    $viva = ($r.StatusCode -eq 200)
  } catch {}
  Write-Output "[$ts] poll $n  errataSparita=$sparita  sitoVivo=$viva  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
  if ($sparita -and $viva) { Write-Output "VERDICT: fatto dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0 }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
