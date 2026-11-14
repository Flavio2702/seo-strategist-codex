# Guida operativa

## Installazione

Python 3.11–3.14 è il perimetro supportato. Il motore non ha dipendenze obbligatorie
di runtime; il packaging usa setuptools. Dalla radice del repository:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install .
python -m seo_strategist --help
```

Per il browser opzionale:

```sh
python -m pip install '.[browser]'
python -m playwright install chromium
```

Apri il repository come progetto in Codex e chiedi `avvia seo strategist`.
[AGENTS.md](../AGENTS.md) contiene discovery, ripresa e comandi conversazionali.
La disponibilità delle istruzioni non garantisce che ogni ambiente Codex abbia
browser, ricerca web o permessi di esecuzione: l'operatore deve verificarli.

## Comandi locali

```sh
python -m seo_strategist status
python -m seo_strategist configure examples/profile.json
python -m seo_strategist audit https://example.org --sample 10 --render off --output reports/esempio
python -m seo_strategist audit https://example.org --render always --pdf --variant https://www.example.org
python -m seo_strategist keywords 'comprare scarpe' 'come scegliere scarpe'
python -m seo_strategist keywords --csv examples/keywords.csv
python -m seo_strategist brief 'Scelta delle scarpe' --audience 'principianti'
python -m seo_strategist schema Article examples/article.json
python -m seo_strategist validate-schema examples/article-built.json
python -m seo_strategist reset-runtime
python -m seo_strategist reset-runtime --apply
```

Questi URL sono esempi, non risultati di audit già eseguiti. Audit usa rete pubblica
solo su richiesta. Evita siti non autorizzati, servizi amministrativi e ambienti con
credenziali. Il client non è un servizio pubblico protetto contro SSRF: è uno
strumento locale per URL scelti dall'operatore. I redirect possono cambiare host.

`--project DIRECTORY` precede il sottocomando e seleziona dove mantenere il profilo.
Codice di uscita 0 indica esecuzione conclusa, non sito senza problemi; 2 indica
input o scrittura non validi. Esiti HTTP inconclusivi sono nel JSON. `--agent`
ripetibile sostituisce la lista predefinita GPTBot/OAI-SearchBot. `--variant`
controlla robots/sitemap/llms sulla variante richiesta, senza inventare equivalenze.

`auto` rende soltanto pagine con script e meno di 80 parole estratte: è un trigger
euristico, può non riconoscere tutte le applicazioni JavaScript. `always` prova
ogni pagina HTML del campione, `off` non avvia browser. I risultati statici restano
la base della matrice; quelli renderizzati sono separati con confronto esplicito.

## Contratti JSON-LD

| Tipo | Input minimo | Opzioni |
|---|---|---|
| Article | headline, author (nome) | url, datePublished, dateModified ISO |
| Product | name | description, sku, url, aggregateRating con rating_evidence |
| FAQPage | questions: lista question/answer | Nessun rich result Google promesso |
| LocalBusiness | name, address (testo) | url, telephone |
| Organization | name, url | description |
| BreadcrumbList | items: lista name/url | Posizioni generate da 1 |
| Person | name | url, jobTitle |

Campi sconosciuti sono rifiutati, non ignorati. Per Product `aggregateRating`
richiede ratingValue, ratingCount intero positivo; bestRating/worstRating sono
opzionali (5/1). `rating_evidence` richiede `visible_on_page: true`,
`genuine_product_ratings: true`, `source_url` http/https. È un'attestazione
dell'operatore, non una prova svolta dal software. I builder restituiscono oggetti
JSON, non blocchi HTML da incollare senza escaping.

## Stato e protezione dei risultati

`.seo-runtime/profile.json` contiene schema 1, answers con original/normalized/method,
ed env_names. Non inserirvi credenziali. L'esempio è sintetico. Le versioni sconosciute
vengono rifiutate: esporta le risposte e riconfigura esplicitamente, senza distruggere
il file esistente. `recent.json` registra il percorso dell'ultimo report.

Reset rifiuta collegamenti simbolici e junction e controlla i percorsi risolti;
non accetta pattern o directory arbitrarie da cancellare. Preserva file esterni a
`.seo-runtime`. Non collocare deliverable dentro quel percorso. Non eseguire reset
mentre un altro processo modifica la directory: non offre garanzie contro race
condition ostili sul filesystem locale.

I report contengono testo estratto dai siti e possono includere dati sensibili:
revisionarli prima di condividerli. JSON conserva i dati originali come stringhe;
HTML e Markdown li visualizzano come testo. PDF è derivato dall'HTML locale generato.

## Test e demo

```sh
python -m unittest discover -v
python scripts/demo.py
python scripts/demo.py --check
python scripts/check_links.py
```

Per includere le prove Chromium, imposta `SEO_BROWSER_TESTS=1` (PowerShell:
`$env:SEO_BROWSER_TESTS='1'`) e ripeti la suite. Tutti i test usano fixture locali;
l'installazione dei pacchetti/browser richiede rete, l'esecuzione della suite no.
La demo sostituisce soltanto origine loopback e header volatili per essere
riproducibile. Il dominio riservato `demo.example.invalid` non è stato visitato.
