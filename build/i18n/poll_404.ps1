$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  $stato = 0; $corpo = ''
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/indirizzo-che-non-esiste' -UseBasicParsing -TimeoutSec 20
    $stato = $r.StatusCode; $corpo = $r.Content
  } catch {
    $stato = $_.Exception.Response.StatusCode.value__
    try { $corpo = (New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())).ReadToEnd() } catch {}
  }
  $ok = ($stato -eq 404) -and ($corpo -match 'Page not found')
  Write-Output "[$ts] poll $n  stato=$stato  paginaGiusta=$ok  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
  if ($ok) { Write-Output "VERDICT: 404 online dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0 }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
