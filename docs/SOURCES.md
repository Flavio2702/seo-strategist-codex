# Fonti primarie e decisioni

Consultazione: 14 novembre 2026. Le fonti sono riferimenti concettuali; codice,
test, fixture e testi del progetto vengono scritti per questa implementazione.
Nessun esempio di codice delle fonti è incorporato. Le pagine possono cambiare.

| Fonte | Decisione di implementazione |
|---|---|
| https://developers.google.com/search/docs/appearance/title-link | Rilevare title e heading; soglie editoriali esplicitamente euristiche, nessun limite ufficiale in caratteri. |
| https://developers.google.com/search/docs/appearance/snippet | Rilevare description; non equipararla allo snippet effettivamente mostrato. |
| https://developers.google.com/search/docs/crawling-indexing/robots/intro | Separare crawling e indicizzazione; robots non garantisce esclusione dall'indice. |
| https://www.rfc-editor.org/rfc/rfc9309.html | Interpretazione dichiarativa delle regole per agenti, con precedenza della regola più specifica. |
| https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | Leggere URL e indici XML, lastmod è una dichiarazione da verificare; ignorare priority e changefreq per il ranking. |
| https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data | Distinguere controlli locali e idoneità ai risultati avanzati. |
| https://developers.google.com/search/updates | FAQ rich results dismessi dal 7 maggio 2026; relativa documentazione rimossa. Conservare FAQPage come vocabolario, senza promessa di rich result. |
| https://developers.google.com/search/blog/2023/08/howto-faq-changes | HowTo rich results dismessi nel settembre 2023; nessun builder HowTo. |
| https://web.dev/articles/inp | INP richiede misure di interazioni; non stimarlo dal parsing HTML. |
| https://schema.org/Article | Builder con headline e autore forniti. |
| https://schema.org/Product | Product con dati dichiarati; rating soltanto annidato e attestato dall'operatore. |
| https://schema.org/AggregateRating | Verificare intervallo del voto e numero positivo di valutazioni. |
| https://schema.org/FAQPage | Domande e risposte fornite, nessuna invenzione. |
| https://schema.org/LocalBusiness | Nome e indirizzo forniti. |
| https://schema.org/Organization | Nome e URL forniti. |
| https://schema.org/BreadcrumbList | Posizioni sequenziali e URL validi. |
| https://schema.org/Person | Nome fornito. |
| https://llmstxt.org/ | Proposta v2, aggiornata il 10 agosto 2026; analisi della struttura Markdown, stato sperimentale, nessun effetto SEO/GEO garantito. |
| https://developers.openai.com/api/docs/bots | GPTBot e OAI-SearchBot hanno scopi diversi; ChatGPT-User è attivato dall'utente, robots può non applicarsi. Nessuna deduzione sull'uso effettivo dei contenuti. |
| https://playwright.dev/python/docs/intro | Dipendenza opzionale, Chromium installato separatamente; errori espliciti e fallback statico. |
| https://docs.python.org/3/library/ | Libreria standard per CLI, parsing, HTTP, test e persistenza. |
| https://docs.python.org/3.14/library/urllib.request.html | Timeout, redirect controllati, errori HTTP separati da errori di trasporto. |
| https://docs.python.org/3.14/library/xml.html | Limite dimensionale, rifiuto DTD/entità, nessun recupero di risorse XML esterne. |
| https://www.apache.org/licenses/LICENSE-2.0.txt | Testo della licenza originale, conservato integralmente. |
| https://github.com/gitleaks/gitleaks | CLI git/dir con redazione output; release 8.30.1 e checksum ufficiale verificati. |
| https://github.com/actions/checkout | Checkout della cronologia completa per scansione, azione fissata a commit. |
| https://github.com/actions/setup-python | Matrice Python supportata, azione fissata a commit. |
| https://playwright.dev/python/docs/api/class-page#page-pdf | Esportazione PDF attraverso Chromium da HTML locale generato. |

La pagina Schema.org consultata si identifica come versione di sviluppo: i
controlli di questo progetto sono un contratto locale ristretto, non un validatore
completo del vocabolario. Verificare nuovamente fonti e requisiti prima di applicare
una raccomandazione su un sito reale.
