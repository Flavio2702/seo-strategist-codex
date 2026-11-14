# Contratti e matrice di copertura

Stato: implementazione completata; evidenze locali in [VERIFY.md](VERIFY.md).
Le procedure assistite sono disponibili e revisionate, non provate end-to-end in
una nuova sessione Codex. "Verifica" sotto indica test automatico o revisione,
secondo l'area; non implica verifica di servizi esterni.
Tutti gli output usano chiavi tecniche inglesi e spiegazioni italiane. Un valore
non osservato è null o accompagnato da uno stato esplicito, mai uno zero inventato.

| Capacità | Implementazione e interfaccia | Verifica ed evidenza |
|---|---|---|
| Avvio/ripresa | AGENTS.md, CLI status | SCENARIOS.md; test_resume_and_recent |
| Discovery | Otto domande singole in AGENTS.md | Revisione SCENARIOS.md; test_no_site_and_geography |
| Configurazione | runtime.py; config con original/normalized, schema_version | ProfileTests: default, personalizzata, incompleta, invalida |
| Capacità | runtime.py; moduli e nomi env configurati, mai valori | test_presence_not_connection_and_no_values; MissingBrowserTests |
| HTML | html.py; analyze_html(text, url) | ParserTests; test_malformed_href_retained_not_navigable |
| Risorse dominio | audit.py e network.py; audit URL | HTTPTests; risorse ed esiti nella demo JSON |
| Sitemap | sitemap.py; URL/index, limiti e campione | test_xml_limits_and_dates; test_sitemap_cycle_and_bad_location |
| Canonical/indice | audit.py; matrice pagina | test_audit_matrix_and_links; test_header_noindex_and_agent_scope |
| Link interni | audit.py; campione di link | test_html_semantics; test_audit_matrix_and_links |
| Rendering | browser.py; auto/always/off | BrowserTests con Chromium locale; fallback testato |
| GEO | html.py; segnali osservati, score euristico | test_html_semantics; evidenze complete nella demo |
| Crawler AI | robots.py; agenti configurabili | test_robots_precedence; test_robots_merged_groups_and_ties |
| Keyword | editorial.py; manuale/CSV | test_keywords_and_brief; esempio generato nella demo |
| Brief | editorial.py; topic/audience/intent/evidence | test_keywords_and_brief; bozza della demo |
| JSON-LD | schema.py; sette builder | test_all_builders_roundtrip; test_rating_evidence_and_invalid |
| Validazione | schema.py; contratto locale | test_schema_coherence; test_all_builders_roundtrip |
| Roadmap | audit.py; priorità e dipendenze | test_audit_matrix_and_links; regole in ARCHITECTURE.md |
| Report | report.py; JSON/MD/HTML/PDF opzionale | test_report_injection_and_files; test_local_pdf; demo --check |
| llms.txt | audit.py e AGENTS.md | test_llms_unknown_not_absent; demo; procedura revisionata |
| Strategia | AGENTS.md e guida | SCENARIOS.md: revisione SERP, competitor, gap, decay e piano |
| Stato/reset | runtime.py; status/reset-runtime e alias | ProfileTests/EdgeTests: dry run, reale, file/link e fuori perimetro |

## Confini degli input/output

- HTTP: soli URL http/https senza credenziali. 10 secondi per operazione, massimo
  2 retry, 5 redirect e 2 MB per risposta. Ogni tentativo ha un esito esplicito.
- Audit: massimo 10 pagine per default, 100 consentite; sitemap fino a 10 documenti,
  profondità 3, 1000 URL. Nessuna conclusione estesa oltre il campione.
- Configurazione: schema 1, campi mancanti conservati come tali; versioni sconosciute
  rifiutate senza riscrittura automatica. Nessun segreto nei file del profilo.
- Runtime: soltanto `.seo-runtime` sotto la directory di progetto esplicitamente
  scelta. Report e demo sono esterni al runtime e sopravvivono al reset.
- Rendering: confronto separato; il parser statico non esegue script. Il browser
  opzionale esegue il JavaScript del sito in un contesto isolato, senza profilo
  personale. Non esegue mai HTML scaricato come programma Python o shell.
- Report: dati del sito trattati come testo; nessun HTML remoto incorporato.
