$j = Invoke-RestMethod -Uri "https://data.iana.org/rdap/dns.json" -TimeoutSec 25
foreach ($tld in 'dev','app','page','eu','it','xyz','info','com','org','net') {
  $svc = $j.services | Where-Object { $_[0] -contains $tld }
  $base = if ($svc) { ($svc[1] | Select-Object -First 1) } else { '(none)' }
  Write-Output ("{0,-5} -> {1}" -f $tld, $base)
}
