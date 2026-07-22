$roots = @(
  # --- Italiano elegante (nel solco di quantessenza/quantiverso) ---
  'quantessenza','quantiverso','quantoscopio','quantoteca','quantonauta','quantoverso',
  'universoquanto','saltoquantico','quantosalto','ilsalto','isalti','saltinquanto',
  'ondaquanta','quantaonda','ondamateria','materiaonda','quantomateria','materiaquanta',
  'quantaluce','luceonda','ondaluce','quantidiluce','quantalume','lumequanto',
  'spettroteca','spettronova','quantonova','ondanova',
  'essenzaquanta','quantavia','viaquanta','sentieroquanto','orizzontequanto',
  'sogliaquanta','quantosoglia','nodoquanto','faseonda','ondafase',
  'pacchettodonda','collassoonda','coerenzaquanta','quantocoerente',
  'intreccioquanto','sovrapposto','superposto','granoquanto','granodiquanto',
  'quantomoto','motoquanto','ondaviva','quantaviva','quantaluna',
  'quantoria','quantura','quantalia','quantessa',
  # --- Coniati brevi (stile psiqm) ---
  'quanton','quantica','quantico','quantly','quantia','quantara','quantera','quantivo',
  'quantnova','quantcore','quantflux','quantphase','quantspin','quantwave','quantverso',
  'quanture','quantico2','quanticalab','quanticaverse','quantumverse',
  'psinova','psiphase','psiflux','psicore','psispin','psimatter','psiflow','psiluce',
  'psilume','psimoto','psionda','psiflow2',
  'qmcore','qmnova','qmphase','qmwave','qmverso','qmlab','qmnote','qmbook','qmatlas','qmnine',
  # --- Inglese fresco (senza braket) ---
  'wavepacket','wavecore','wavephase','waveflux','wavenova','coherentwave','phasewave',
  'discretewave','quantumleap','quantleap','qleap','ninewave','wavenine','superposed'
) | Select-Object -Unique

$tlds = @('com','dev','org','xyz')
$out = foreach ($r in $roots) { foreach ($t in $tlds) { "$r.$t" } }
$out | Set-Content -Path "tools/domains/candidates3.txt" -Encoding ASCII
Write-Output "roots=$($roots.Count) candidates=$($out.Count)"
