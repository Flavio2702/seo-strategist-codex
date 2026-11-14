# SEO Strategist — versione Codex

Un progetto portfolio di **Flavio2702**: strumenti Python per audit SEO su campione
e procedure in italiano per lavorare con Codex su contenuti, ricerca e strategia.
Ogni raccomandazione distingue ciò che è stato osservato da ciò che è inferito o
rimane da verificare.

**Guarda subito la [demo Markdown](demo/report.md)** oppure scarica e apri la
[demo HTML](demo/report.html). Sono risultati realmente generati su un sito
sintetico locale, consultabili senza installazione. I [dati JSON](demo/report.json)
permettono di controllare tutte le evidenze.

## Competenze mostrate

- Traduzione di requisiti SEO in contratti, strumenti e verifiche riproducibili.
- Gestione di HTTP, redirect, sitemap, canonical, indicizzabilità e limiti di campionamento.
- Distinzione fra misure, segnali strutturali GEO e ipotesi editoriali.
- Progettazione di procedure Codex, persistenza locale, fallback e protezione dei report.
- Test offline, rendering opzionale, documentazione della provenienza e controlli CI.

## Cosa contiene

Audit di title, description, heading, testo, immagini/alt, canonical, robots,
hreflang e JSON-LD; risorse robots.txt/sitemap/llms.txt; matrice per pagina;
link interni sul campione; confronto statico/renderizzato con Playwright;
regole dichiarate per crawler AI; cluster lessicali, intent e brief; sette builder
JSON-LD; roadmap e report JSON/Markdown/HTML/PDF opzionale.

Le attività strategiche rimangono assistite da Codex: discovery in otto domande,
ricerca SERP/competitor con fonti, content audit, gap, decay con dati storici,
pianificazione e proposta llms.txt. Non sono connettori API automatici.

```sh
python -m pip install .
python -m seo_strategist audit https://example.org --render off
python -m unittest discover -v
python scripts/demo.py --check
```

Per usare le procedure, apri il repository in Codex e scrivi **avvia seo strategist**.
Python supportato: 3.11–3.14. Nessuna dipendenza obbligatoria di runtime;
Playwright/Chromium sono opzionali. L'esecuzione dei test non richiede chiavi o rete
esterna; il download degli strumenti di sviluppo sì.

## Documentazione e verificabilità

- [Guida operativa e contratti](docs/GUIDE.md)
- [Matrice di copertura di tutte le capacità](docs/COVERAGE.md)
- [Architettura, regole e limiti](docs/ARCHITECTURE.md)
- [Esiti e ambiente delle verifiche](docs/VERIFY.md)
- [Scenari conversazionali revisionati](docs/SCENARIOS.md)
- [Fonti primarie e decisioni](docs/SOURCES.md)
- [Provenienza](docs/PROVENANCE.md) e [dipendenze](docs/DEPENDENCIES.md)

## Limiti e attribuzione

Questo è un progetto dimostrativo, non una certificazione di idoneità alla
produzione. Nessuna promessa di ranking, traffico o citazioni AI; nessun INP
dedotto dall'HTML. La validazione JSON-LD è locale e limitata, non una validazione
completa Schema.org né una prova di idoneità Google. llms.txt è sperimentale.

Sviluppato con assistenza AI (OpenAI Codex) da requisiti funzionali e fonti pubbliche
primarie, con implementazione e test nuovi. Nessuna certificazione giuridica di
indipendenza o assenza di rischi. [Apache License 2.0](LICENSE) per i contributi
originali concedibili, copyright 2026 Flavio2702. Vedi [NOTICE](NOTICE).
