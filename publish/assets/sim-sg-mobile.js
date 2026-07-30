/* Su schermo piccolo lo schema dell'apparato si apre a richiesta.
 *
 * Non tocca la simulazione: i due disegni erano gia' indipendenti e il
 * laboratorio si ridisegna da solo quando la finestra cambia. Qui si cambia
 * soltanto che cosa e' visibile, e poi si annuncia un ridimensionamento: al
 * disegno basta quello per riadattarsi allo spazio che ha trovato.
 */
(function () {
  'use strict';

  var schema = document.querySelector('#cApp');
  if (!schema) return;
  var box = schema.closest('.panelbox');
  var vetrino = document.querySelector('#cPlate');
  if (!box || !vetrino) return;

  function bottone(id, testo, etichetta) {
    var b = document.createElement('button');
    b.id = id;
    b.type = 'button';
    b.textContent = testo;
    b.setAttribute('aria-label', etichetta);
    return b;
  }

  var apri = bottone('apri-schema', '▦ Schema dell\'apparato',
                     'mostra lo schema dell\'apparato a schermo intero');
  var chiudi = bottone('chiudi-schema', 'Chiudi', 'chiudi lo schema');

  vetrino.closest('.panelbox').insertBefore(apri, vetrino.closest('.panelbox').firstChild);
  document.body.appendChild(chiudi);

  // Da dove viene lo schema, per rimettercelo alla chiusura.
  var casa = box.parentElement, posto = box.nextSibling;

  function mostra(aperto) {
    // Lo schema si sposta davvero in fondo alla pagina invece di limitarsi a
    // salire di livello: su Safari di iPhone un elemento a posizione fissa puo'
    // restare comunque sotto ai vicini, e nessun z-index lo salva.
    if (aperto) document.body.appendChild(box);
    else casa.insertBefore(box, posto);

    document.body.classList.toggle('schema-aperto', aperto);
    (aperto ? chiudi : apri).focus();
    // il laboratorio ridisegna gia' su questo evento, e ogni disegno rilegge
    // da solo lo spazio del proprio contenitore
    window.dispatchEvent(new Event('resize'));
  }

  apri.addEventListener('click', function () { mostra(true); });
  chiudi.addEventListener('click', function () { mostra(false); });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && document.body.classList.contains('schema-aperto')) {
      mostra(false);
    }
  });
})();
