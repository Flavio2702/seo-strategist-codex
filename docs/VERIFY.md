# Verifiche

Data delle verifiche locali: 14 novembre 2026.

## Ambiente effettivo

- Windows 11, build 26200; CPython 3.14.0; Expat 2.7.3.
- Ambiente virtuale isolato; pacchetto costruito come wheel e installato.
- La suite è stata eseguita anche da una directory esterna al sorgente, con i soli
  test copiati, verificando l'import da `site-packages`.
- Playwright 1.65.2, greenlet 3.5.6, Chrome for Testing 159.0.8154.6 / Chromium
  build Playwright 1255. Browser installato nella directory di lavoro, fuori dal repository.

## Risultati locali

| Verifica | Esito |
|---|---|
| Installazione da pyproject in ambiente isolato | Superata |
| Suite completa contro pacchetto installato, browser abilitato | 36 test: 35 superati, 1 saltato |
| HTTP su server sintetico loopback | Superata: redirect, retry, timeout, errori, campione |
| Rendering iniziale/renderizzato su pagina JavaScript locale | Superata: titolo Prima → Dopo e confronto conservato |
| PDF da report HTML locale | Superata: esportazione Chromium e firma PDF verificata; non validazione tipografica di ogni possibile report |
| Assenza Playwright | Simulata esplicitamente e verificata; fallback senza perdere HTML iniziale |
| Reset normale e dry run | Superati; report esterno preservato |
| Reset con risoluzione fuori perimetro | Superato con filesystem simulato |
| Reset con symlink reale | Saltato su Windows per permessi di creazione; previsto su Linux in CI |
| Demo JSON/Markdown/HTML | Generata realmente; rigenerazione identica byte per byte |
| Gitleaks 8.30.1 sui file | Nessuna rilevazione; non garanzia assoluta di assenza di segreti |
| Procedure conversazionali | Revisione degli scenari in SCENARIOS.md; non prova end-to-end in nuova chat Codex |

La prima esecuzione nell'ambiente di accesso limitato non poteva raggiungere il
server locale né usare correttamente la cartella temporanea. Le prove riportate
sono quelle completate con accesso al loopback e directory temporanea dedicata.
Non sono state usate chiavi API o chiamate a pagamento. Nessun sito reale è stato
usato come fixture della suite o della demo.

## Controlli di pubblicazione

Workflow [Verify](https://github.com/Flavio2702/seo-strategist-codex/actions/workflows/verify.yml):
test offline su Python 3.11, 3.12, 3.13, 3.14; riproducibilità demo; collegamenti
locali; installazione; browser/PDF su Linux; Gitleaks su file e intera cronologia.
La preparazione degli strumenti in CI richiede rete pubblica; i test applicativi
usano soltanto dati locali. Nessuna credenziale personale configurata nei job.

Il risultato CI deve essere letto sul commit specifico nella pagina Actions; non
inferirlo dalla presenza del workflow. La ricevuta della pubblicazione con SHA e
run verificato viene consegnata separatamente per evitare attestazioni circolari.

## Limiti delle verifiche

Non misurate prestazioni su larga scala, accuratezza semantica GEO, ranking,
idoneità Google dei markup, uso reale dei crawler, sicurezza completa o diritti
terzi. Le fonti sono state consultate alla data indicata, non monitorate nel tempo.
Non sono stati effettuati un audit legale o una certificazione clean room.
