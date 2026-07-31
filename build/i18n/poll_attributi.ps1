$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/en/01-stern-gerlach' -UseBasicParsing -TimeoutSec 25
    $ok = ($r.Content -match 'An atom as a tiny magnet') -and ($r.Content -notmatch '-en="')
    Write-Output "[$ts] poll $n  http=$($r.StatusCode)  altEN=$ok  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
    if ($ok) { Write-Output "VERDICT: online dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0 }
  } catch {
    Write-Output "[$ts] poll $n  non ancora: $($_.Exception.Message.Split([char]10)[0])"
  }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
