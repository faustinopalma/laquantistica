$roots = @(
  # braket family
  'braket','brakets','thebraket','braketlab','braketbook','braketnote','braketnotes',
  'braketqm','qmbraket','braketpsi','psibraket','braketphysics','braketry','braketto',
  'braketti','braketta','braketspace','braketwave','openbraket','mybraket','braketverse',
  'braketup','ketbraket','braketize','braketed','getbraket','braket9','braketnine',
  # ket family
  'ket','ketpsi','psiket','ketbra','ketlab','ketnote','ketbook','ketqm','qmket','ketspace',
  'ketvector','ketwave','ketphysics','ketverse','ketra','ketology','ketand','ketbox',
  # bra family
  'bralab','bravector','braqm','brapsi','psibra',
  # dirac family
  'dirac','diracnotation','diracket','diraclab','diracnote','diracqm','diracpsi','diracbook',
  'diracbra','diracspace','diracverse','diracnotes','diracbraket',
  # psi + qm terse (stile psiqm)
  'qmpsi','psiq','qpsi','psiqbit','psiamp','psiqm2','qm-psi','psi-qm','psinet','psihub',
  # notazione / prodotto interno
  'notationpsi','quantumnotation','amplitudepsi','innerbraket','braketstudio','braketclub'
) | Select-Object -Unique

$tlds = @('com','dev','org','xyz')
$out = foreach ($r in $roots) { foreach ($t in $tlds) { "$r.$t" } }
$out | Set-Content -Path "tools/domains/candidates2.txt" -Encoding ASCII
Write-Output "roots=$($roots.Count) candidates=$($out.Count)"
