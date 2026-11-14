# Verifica delle procedure conversazionali

Revisione delle istruzioni svolta il 14 novembre 2026, confrontando ciascuno
scenario con AGENTS.md e con i contratti Python. **Non è una prova effettiva di
un'intera sessione in una nuova chat Codex**, né un benchmark di comportamento
del modello. I passaggi di persistenza hanno prove automatiche distinte.

| Scenario | Input sintetico | Comportamento verificato nelle istruzioni | Evidenza e limite |
|---|---|---|---|
| Configurazione nuova | avvia seo strategist; nessun profilo | Una domanda per messaggio, otto aree, numeri e testo libero | Revisione AGENTS: tutte le otto aree presenti; ProfileTests verifica profilo vuoto/completo |
| Risposta libera | ruolo: Ricercatore; strumenti: Fogli locali | Conserva originale e normalizzazione testuale, non inventa classificazione | test_custom_and_complete; non prova la qualità del dialogo |
| Nessun sito | scelta 2 alla domanda sito | Salva original=2 e normalized=null; audit richiede URL, keyword/brief disponibili | test_no_site_and_geography; procedura revisionata |
| Strumento assente | nessun Playwright o ricerca web | Statico con esito unavailable; SERP diventa piano di raccolta | MissingBrowserTests più revisione procedura SERP |
| Dati insufficienti | richiesta decay senza storico | Nessun calo numerico; richiede finestre, metrica e fonte | Revisione procedura decay; non test statistico |
| Ripresa | profilo parziale già salvato | status mostra campi mancanti; riparte dalla prima domanda mancante | ProfileTests e test_resume_and_recent |
| Profilo corrotto | JSON non valido/versione ignota | Errore, conservazione del file, riconfigurazione esplicita | test_corrupt_profile_preserved e test_invalid_schema_and_answers |
| Pulizia | clean-runtime | Dry run, applicazione autorizzata, report esterni preservati | Test reset reale/simulato; prove symlink su Linux in CI |
| Richiesta schema non incluso | schema Review | Spiega i sette tipi disponibili, non improvvisa il builder | test_rating_evidence_and_invalid |

Per una prova reale futura: aprire un nuovo progetto Codex su questo repository,
eseguire gli scenari senza contesto precedente, conservare trascrizione depurata
da dati personali e annotare esiti effettivi. Non convertire questa revisione in
una dichiarazione di validazione end-to-end conversazionale.
