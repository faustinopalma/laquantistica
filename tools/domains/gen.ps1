$roots = @(
  # Psi / QM wordmark
  'psiqm','qmpsi','psiquanta','psiwave','psilab','psibook','psinote','psinotes','psiket',
  'psifield','psiphysics','psiquantum','psiqubit','psionika','psiverse','psiology',
  # quantum / quanti / quanto
  'quantabook','quantanote','quantanotes','quantalab','quantaidea','quantaidee','quantafisica',
  'quantario','quantoteca','quantessenza','quantessence','quantoscopio','quantiverso','quantesimo',
  'quantumfoundations','quantumfromexperiments','quantumintuition','intuitivequantum','quantumfirst',
  'firstquantum','purequantum','plainquantum','cleanquantum','quantumessentials','essentialquantum',
  'ninequanta','quantumnine','quantcraft','quantidea','quantnotes','quantbook','quantlab','quantcasa',
  'quantica','quantika','quantora','quantaria','quantalia','quantessa','quantevo','evoquanta',
  'quantavia','viaquanta','quantoria','quantopia','quantaverse','quantatlas','atlasquantum',
  'quantummap','quantumpath','pathtoquanta','quantaroad','quantaway','quantazero','zeroquanta',
  # meccanica quantistica (IT)
  'meccanicaquantistica','laquantistica','quantisticamente','esperimentiquantistici','esperimentimq',
  'novesperimenti','capirequanti','capirelaquantistica','quantisticadanewton','fisicaquantistica',
  # fisici / esperimenti
  'schrodingerlab','schrodingernote','schrodingernotes','deriveschrodinger','deducingschrodinger',
  'newtontoquanta','fromnewtontoquanta','debrogliewave','planckstep','sterngerlachlab','franckhertzlab',
  # onda / ampiezza / probabilita
  'ondaquanta','ampiezzaonda','complexwave','complexpsi','linearwave','thewavefunction',
  'complexamplitude','probabilityamplitude','waveandprobability',
  # autore
  'faustinopalma','palmaquantum','palmaphysics',
  # tesi
  'tesiquantistica','quantumthesis','thequantumthesis',
  # coined brandable
  'quantora','quantoria','quantessa','quantalia','qbitlab','qubitnote','braketlab','braketnote',
  'braketbook','ketbra','spinhalf','halfspin','hbarlab','hbarnote','planckbar','quantaquila'
) | Select-Object -Unique

$tlds = @('com','org','dev','xyz')
$out = foreach ($r in $roots) { foreach ($t in $tlds) { "$r.$t" } }
$out | Set-Content -Path "tools/domains/candidates.txt" -Encoding ASCII
Write-Output "roots=$($roots.Count) candidates=$($out.Count)"
