$roots = @(
  # "quantistica" resa internazionale (elegante, monoparola)
  'quantica','quantika','quantical','quantics','quantics','quantix','quantik','quantiq',
  'quantist','quantista','quantists','quantico','quantly','quantonic','quantonics',
  'quantia','quantora','quantessa','quantoria','quanton','quantea','quantera',
  # the-quantum / startup-style (facili per anglofoni)
  'thequantum','getquantum','tryquantum','myquantum','goquantum','quantumly','quantumish',
  'quantumkit','quantumroom','quantumnote','quantumdesk','quantumclass','quantumbasics',
  'quantumclear','quantumway','quantumlane','quantumhouse','quantumcore','quantumworld',
  # quant- brandable EN
  'quantwave','quantverse','quantworld','quantwise','quantable','quantful','quantcore',
  'quantlab','quantroom','quantkit','quantbook','quantnote','quantclass','quantbasics',
  # quanta- brandable EN
  'quantalab','quantahouse','quantakit','quantaverse','quantaroom','quantaworld','quantawave',
  # nove esperimenti in chiave EN
  'ninequantum','quantumnine','quantum9','ninequanta2'
) | Select-Object -Unique

$tlds = @('com','dev','org','xyz')
$out = foreach ($r in $roots) { foreach ($t in $tlds) { "$r.$t" } }
$out | Set-Content -Path "tools/domains/candidates4.txt" -Encoding ASCII
Write-Output "roots=$($roots.Count) candidates=$($out.Count)"
