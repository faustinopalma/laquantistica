# Farsi trovare: Google Search Console e Bing Webmaster Tools

Guida operativa per **laquantistica.com**. Aggiornata al 31 luglio 2026.

Entrambi gli strumenti sono **gratuiti**, senza versioni a pagamento e senza limiti d'uso.
Non fanno salire il sito nei risultati: servono a *vedere* cosa i motori capiscono del sito,
e a segnalare loro le pagine nuove.

---

## 1. Google Search Console

### A cosa serve

| cosa vedi | perché conta |
|---|---|
| le ricerche che portano visitatori, con posizione media e numero di clic | scopri per quali domande la gente ti trova davvero, che spesso non sono quelle che immaginavi |
| quali pagine sono indicizzate e quali no, con il motivo dell'esclusione | se un capitolo non compare, qui trovi scritto perché |
| errori di scansione, problemi di `hreflang`, pagine duplicate | sono i guasti che altrimenti non noteresti mai |
| i dati strutturati riconosciuti | conferma che Google ha capito che si tratta di un corso |
| lo stato della sitemap | quante pagine ha letto e quante ne ha accettate |

### Come si attiva

1. Vai su **https://search.google.com/search-console** e accedi con un account Google.
2. Scegli il tipo di proprietà **«Dominio»** (la colonna di sinistra), non «Prefisso URL».
   Il tipo «Dominio» copre tutto insieme: `laquantistica.com`, `www.laquantistica.com`,
   `http` e `https`. È la scelta giusta e si fa una volta sola.
3. Inserisci `laquantistica.com`.
4. Google mostra una stringa da inserire nel DNS, del tipo
   `google-site-verification=xxxxxxxxxxxxxxxxxxxxxxxx`.
5. Vai su **Cloudflare** → il dominio `laquantistica.com` → **DNS** → **Add record**:
   - **Type**: `TXT`
   - **Name**: `@`
   - **Content**: la stringa che ti ha dato Google, per intero
   - **TTL**: Auto
6. Salva, torna su Search Console e premi **Verifica**. Di solito funziona subito; se dice
   di no, aspetta dieci minuti e riprova — il DNS ci mette un po' a propagarsi.

> **Non cancellare quel record TXT.** Google lo ricontrolla ogni tanto: se sparisce, perdi
> l'accesso alla proprietà. Nel DNS c'è già un altro TXT di validazione, quello di Azure:
> convivono senza problemi.

### Subito dopo la verifica

1. **Sitemaps** (menù di sinistra) → nel campo incolla questo indirizzo:

   ```
   https://laquantistica.com/sitemap.xml
   ```

   e premi **Invia**. Se il modulo mostra già `https://laquantistica.com/` come prefisso
   fisso, allora nel campo scrivi solo:

   ```
   sitemap.xml
   ```

   Si inserisce **una volta sola**: non si carica nessun file, si indica l'indirizzo. Google
   torna a rileggerlo da solo ogni tanto, e il file viene rigenerato a ogni ricostruzione del
   sito. Se aggiungi o togli una pagina, la sitemap la segue senza che tu debba fare nulla.

2. **Controllo URL** (in alto) → incolla `https://laquantistica.com/it/` → **Richiedi
   l'indicizzazione**. Fallo per l'indice italiano e per quello inglese. Non serve farlo
   per tutte le pagine: dall'indice Google raggiunge il resto da solo.

> La sitemap è anche dichiarata dentro `robots.txt`, quindi i motori la trovano comunque.
> Segnalarla a mano serve solo ad accorciare i tempi la prima volta.

### Cosa aspettarsi, onestamente

I primi dati compaiono dopo **qualche giorno**; un quadro leggibile dopo **due o tre
settimane**. All'inizio i numeri saranno bassissimi, ed è normale: il sito è nuovo e
nessuno lo collega ancora. Non è un segnale che qualcosa non funziona.

---

## 2. Bing Webmaster Tools

Copre Bing, Yahoo, DuckDuckGo e — cosa non ovvia — è la fonte che alimenta le risposte di
diversi assistenti conversazionali. Vale la mezz'ora anche se il traffico di Bing è minore.

1. Vai su **https://www.bing.com/webmasters**.
2. Accedi e scegli **«Importa da Google Search Console»**: se hai già fatto il punto 1,
   Bing prende da lì proprietà e verifica, e non devi toccare nulla.
3. Se preferisci non collegare i due account, puoi verificare anche qui con un record TXT
   su Cloudflare, con la stessa procedura.
4. Anche qui, alla voce **Sitemaps**, inserisci lo stesso indirizzo:

   ```
   https://laquantistica.com/sitemap.xml
   ```

---

## 3. Cosa è già stato fatto sul sito

Non serve rifarlo, ma è utile sapere che c'è.

- **Un indirizzo per lingua**: `/it/…` e `/en/…`, con `hreflang` reciproci. Google può
  mostrare la versione italiana a chi cerca in italiano.
- **`sitemap.xml`** con tutti i 52 indirizzi, le corrispondenze fra le due lingue e la data
  dell'ultima modifica di ogni pagina, così i motori sanno *cosa* è cambiato e non
  riscandagliano tutto alla cieca.
- **`robots.txt`** che apre tutto il sito e indica dove sta la sitemap.
- **Titolo e descrizione** su ogni pagina, distinti e scritti a mano.
- **Anteprima di condivisione** (Open Graph) su ogni pagina, con immagine di copertina
  1200×630 nelle due lingue: chi incolla il link su LinkedIn o WhatsApp vede titolo,
  descrizione e immagine invece di un rettangolo vuoto.
- **Dati strutturati** sull'indice e sui nove capitoli, che dichiarano l'opera come un
  *corso completo* con i suoi argomenti, l'autore, e la tesi del 1999 da cui deriva.
- **Rimandi 301** dai vecchi indirizzi, così i link già in circolazione non si rompono.
- **Pagina «non trovato»** nella lingua del lettore, con stato HTTP corretto.

---

## 4. Cosa sposta davvero l'ago

Questa è la parte che nessuno strumento può fare al posto tuo.

I motori di ricerca decidono la posizione soprattutto in base a **chi ti cita**. Un link da
un sito già autorevole vale più di qualunque accorgimento tecnico. Le strade praticabili,
in ordine di resa:

1. **La pagina di un docente o di un dipartimento.** Un corso di Istituzioni di Fisica
   Teorica che mette il link fra i materiali di supporto vale moltissimo, ed è plausibile:
   il sito offre laboratori simulati che un docente non ha.
2. **Wikipedia**, nelle voci *Esperimento di Stern-Gerlach*, *Esperimento di Franck-Hertz*,
   *Esperimento di Millikan*, nella sezione «Collegamenti esterni». Attenzione: aggiungere
   un link al proprio sito è formalmente un conflitto d'interessi. La via corretta è
   proporlo nella pagina di discussione della voce, spiegando cosa aggiunge.
3. **Comunità di fisica**: Physics Stack Exchange, r/PhysicsStudents, gruppi di didattica
   della fisica. Funziona solo se rispondi a una domanda vera e il link è pertinente.
4. **La Società Italiana di Fisica**, dove la tesi fu presentata nel 1999 (85° Congresso
   Nazionale, Pavia): un annuncio dell'edizione web ha una motivazione legittima.
5. **LinkedIn.** Ora che le anteprime funzionano, un post con il link mostra copertina e
   descrizione. Il valore per i motori è modesto, ma porta i primi lettori reali.

Una nota che vale più di tutte le altre: il vantaggio del sito non è tecnico, è il
**contenuto**. Una trattazione che ricava l'equazione di Schrödinger dagli esperimenti
invece di postularla, con laboratori che si possono usare, non è facile da trovare — e in
italiano non esiste altro di simile. È questo che, raccontato bene, fa venire i link.

---

## 5. Ogni tanto

- **Search Console → Prestazioni**: quali domande portano visitatori. Se scopri che
  arrivano cercando qualcosa che tratti solo di sfuggita, è un'indicazione su cosa
  approfondire.
- **Search Console → Indicizzazione delle pagine**: se qualche pagina risulta esclusa,
  qui trovi il motivo.
- Dopo modifiche importanti al sito, reinvia la sitemap.
