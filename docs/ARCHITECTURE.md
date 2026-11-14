# Architettura e limiti

Il flusso è CLI → audit → client HTTP/parser → evidenze → roadmap → report.
`runtime.py` gestisce separatamente profilo e reset. `editorial.py` e `schema.py`
sono funzioni locali utilizzabili anche senza sito o browser.

- `network.py`: risposte strutturate con URL richiesta/finale, stato, redirect,
  tentativi e errore. 2 MB per corpo, massimo 5 redirect, 2 retry su trasporto e
  429/500/502/503/504. Timeout 10 secondi per operazione di socket, non deadline
  globale. Non interpreta Retry-After; il backoff breve è limitato, non pensato per
  scansioni massive. Charset sconosciuti hanno fallback UTF-8 con sostituzione.
- `html.py`: HTMLParser, nessuna esecuzione. Estrae markup, non layout o accessibilità
  completa. Non ricostruisce tutte le correzioni DOM di un browser. Alt vuoto è un
  possibile intento decorativo da verificare, distinto da attributo assente.
- `sitemap.py`: XML urlset/sitemapindex; rifiuta DTD ed entità; 10 documenti,
  profondità 3, 1000 URL. Non supporta gzip, RSS e sitemap testuali. Segnala formato
  non supportato come non concluso. Segue il primo Sitemap same-host dichiarato in
  robots, oppure /sitemap.xml; conserva tutte le dichiarazioni per revisione.
- `robots.py`: gruppi per token agente, fallback *, regola più specifica, Allow a
  parità, wildcard e fine percorso. Non è una certificazione completa RFC; non
  interpreta Crawl-delay. Errori/mancanza robots restano inconclusivi per la
  dichiarazione d'accesso, senza simulare il comportamento specifico dei bot.
- `audit.py`: campione deterministico nell'ordine sitemap, esclusi host esterni;
  matrice basata sull'HTML iniziale. Non controlla tutti i link: identifica target
  non canonici già noti nel campione. Una canonical dichiarata non è quella scelta
  da Google. X-Robots-Tag con scope agente resta conservato, senza applicarlo a tutti.
- `browser.py`: Chromium opzionale in contesto effimero; JS del sito solo qui.
  Nessun login. Non è un ambiente di isolamento per codice ostile certificato.
  Gli errori diventano stati unavailable/inconclusive. PDF usa HTML locale,
  JavaScript disabilitato e risorse HTTP bloccate.
- `report.py`: JSON integrale, Markdown con contenuti codificati, HTML con escaping
  e CSP senza script. Nessuna libreria di templating o CDN. I file report esistenti
  nella directory di output scelta vengono sostituiti: scegli cartelle distinte
  per conservare più esecuzioni.
- `schema.py`: sette builder con campi delimitati e validatore del medesimo
  contratto. Non risolve @graph, contesti remoti o l'intero vocabolario. Tipi validi
  fuori contratto possono essere segnalati come non supportati, non come errore SEO.

## Regole qualitative

GEO: sei segnali booleani con peso uguale (heading, domande nei heading, markup di
citazione, date, liste, JSON-LD). La somma 0–6 misura presenza strutturale, non
qualità, affidabilità, visibilità AI o probabilità di citazione.

Keyword: Jaccard >= 0.5 rispetto ai token del primo elemento del cluster, con
stopword limitate italiane/inglesi. Ordine input determinante; nessuna semantica
multilingue o SERP reale. Intent: transazionale → commerciale → navigazionale →
informativo secondo indicatori lessicali. Opportunità: almeno tre token utili
significa "specifica da validare", altrimenti "ampia da esplorare"; non classifica
facilità di posizionamento o valore economico.

Roadmap: raggruppamento per codice rilievo e ordinamento per priorità, poi codice.
P1 condizioni che richiedono chiarimento sull'accesso/indicizzazione; P2 coerenza,
accessibilità delle immagini o verifica browser mancante; P3 cura editoriale.
Ogni gruppo conserva evidenza, URL, motivazione, dipendenze e dati mancanti.

## Confini dichiarati

Non pronto per la produzione senza ulteriore revisione. Nessuna misura INP,
nessun connettore a piattaforme commerciali, nessun dato storico implicito, nessun
crawl esaustivo, nessuna prova di ranking/citazione. Nessuna garanzia giuridica o
di sicurezza assoluta. Il progetto è una dimostrazione professionale verificabile.
