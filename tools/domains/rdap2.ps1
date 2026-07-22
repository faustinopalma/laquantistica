param(
  [string]$InFile,
  [string]$OutFile = "tools/domains/results.csv",
  [int]$Throttle = 6
)

# Authoritative RDAP base per TLD (query the registry directly; 404 = truly unregistered)
$baseMap = @{
  'com'  = 'https://rdap.verisign.com/com/v1/domain/'
  'net'  = 'https://rdap.verisign.com/net/v1/domain/'
  'org'  = 'https://rdap.publicinterestregistry.org/rdap/domain/'
  'info' = 'https://rdap.identitydigital.services/rdap/domain/'
  'xyz'  = 'https://rdap.centralnic.com/xyz/domain/'
  'dev'  = 'https://pubapi.registry.google/rdap/domain/'
  'app'  = 'https://pubapi.registry.google/rdap/domain/'
  'page' = 'https://pubapi.registry.google/rdap/domain/'
}

$all = Get-Content $InFile | Where-Object { $_.Trim() -ne '' } | ForEach-Object { $_.Trim().ToLower() } | Select-Object -Unique
Write-Output "checking $($all.Count) domains, throttle=$Throttle"

function Invoke-Pass {
  param([string[]]$Domains, [int]$Throttle, [hashtable]$BaseMap)
  $Domains | ForEach-Object -Parallel {
    $d = $_
    $map = $using:BaseMap
    $tld = ($d -split '\.')[-1]
    $base = $map[$tld]
    if (-not $base) { return [pscustomobject]@{ Domain=$d; Code=0; State='NO_RDAP_BASE' } }
    $uri = "$base$d"
    try {
      $r = Invoke-WebRequest -Uri $uri -Method Get -TimeoutSec 25 -MaximumRedirection 5 -ErrorAction Stop
      [pscustomobject]@{ Domain=$d; Code=[int]$r.StatusCode; State='REGISTERED' }
    } catch {
      $resp = $_.Exception.Response
      $sc = $null
      if ($resp -and $resp.StatusCode) { $sc = [int]$resp.StatusCode.value__ }
      if ($sc -eq 404)     { [pscustomobject]@{ Domain=$d; Code=404; State='AVAILABLE' } }
      elseif ($sc -eq 429) { [pscustomobject]@{ Domain=$d; Code=429; State='RETRY' } }
      elseif ($sc)         { [pscustomobject]@{ Domain=$d; Code=$sc;  State="HTTP$sc" } }
      else                 { [pscustomobject]@{ Domain=$d; Code=0;    State='RETRY' } }
    }
  } -ThrottleLimit $Throttle
}

$final = @{}
$pending = [System.Collections.Generic.List[string]]::new()
$all | ForEach-Object { $pending.Add($_) }
for ($p = 1; $p -le 5 -and $pending.Count -gt 0; $p++) {
  $thr = if ($p -eq 1) { $Throttle } else { 2 }
  Write-Output "pass $p : $($pending.Count) (throttle $thr)"
  $res = Invoke-Pass -Domains $pending.ToArray() -Throttle $thr -BaseMap $baseMap
  $next = [System.Collections.Generic.List[string]]::new()
  foreach ($r in $res) { if ($r.State -eq 'RETRY') { $next.Add($r.Domain) } else { $final[$r.Domain] = $r } }
  $pending = $next
}
foreach ($d in $pending) { $final[$d] = [pscustomobject]@{ Domain=$d; Code=429; State='RETRY' } }
$results = $final.Values

$results | Sort-Object State, Domain | Export-Csv -Path $OutFile -NoTypeInformation -Encoding UTF8
$results | Group-Object State | Sort-Object Name | ForEach-Object { Write-Output ("{0}: {1}" -f $_.Name, $_.Count) }
Write-Output "written: $OutFile"
