$t = [Diagnostics.Stopwatch]::StartNew()
$fine = (Get-Date).AddMinutes(8)
$n = 0
while ((Get-Date) -lt $fine) {
  $n++
  $ts = Get-Date -Format 'HH:mm:ss'
  try {
    $r = Invoke-WebRequest -Uri 'https://laquantistica.com/sitemap.xml' -UseBasicParsing -TimeoutSec 25
    $conDate = ([regex]::Matches($r.Content, '<lastmod>')).Count
    $indirizzi = ([regex]::Matches($r.Content, '<loc>')).Count
    Write-Output "[$ts] poll $n  http=$($r.StatusCode)  indirizzi=$indirizzi  conData=$conDate  elapsed=$([math]::Round($t.Elapsed.TotalSeconds,1))s"
    if ($conDate -eq $indirizzi -and $indirizzi -gt 0) {
      Write-Output "VERDICT: sitemap online con le date dopo $([math]::Round($t.Elapsed.TotalSeconds,1))s"; exit 0
    }
  } catch {
    Write-Output "[$ts] poll $n  non ancora: $($_.Exception.Message.Split([char]10)[0])"
  }
  Start-Sleep -Seconds 20
}
Write-Output "VERDICT: non aggiornato entro il tempo previsto"
