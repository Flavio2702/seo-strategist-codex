# Dipendenze e attribuzioni

Nessuna dipendenza Python obbligatoria di runtime. Python e la sua libreria standard
restano soggetti alla [licenza PSF](https://docs.python.org/3/license.html); non sono
redistribuiti nel repository. Richiesto Python 3.11–3.14; usare patch di sicurezza
aggiornate, specialmente per Expat/XML e networking.

| Componente | Uso | Licenza / fonte |
|---|---|---|
| setuptools >=77 | Costruzione del pacchetto, non runtime | MIT — https://github.com/pypa/setuptools |
| Playwright Python >=1.49,<2 | Rendering e PDF opzionali; verificato 1.65.2 | Apache-2.0 — https://github.com/microsoft/playwright-python |
| greenlet | Dipendenza transitiva di Playwright; verificato 3.5.6 | MIT/PSF secondo i file di licenza upstream — https://github.com/python-greenlet/greenlet |
| Chromium / Chrome for Testing | Browser installato separatamente da Playwright | Licenze BSD e componenti terzi — https://chromium.googlesource.com/chromium/src/+/main/LICENSE |
| Gitleaks 8.30.1 | Scansione di file e cronologia, solo sviluppo/CI | MIT — https://github.com/gitleaks/gitleaks |
| actions/checkout, actions/setup-python | Preparazione CI; commit fissati nel workflow | MIT — https://github.com/actions/checkout e https://github.com/actions/setup-python |

Pacchetti, browser e strumenti non sono vendorizzati. Gli strumenti conservano i
propri avvisi e licenze nei rispettivi download; questo progetto non rivendica la
loro titolarità. I componenti opzionali possono cambiare entro gli intervalli:
la versione effettivamente verificata è registrata in [VERIFY.md](VERIFY.md).

Il workflow scarica release Gitleaks fissata e verifica il checksum pubblicato.
Il checksum controlla integrità rispetto alla release, non costituisce una prova
indipendente dell'identità dell'autore. Nessun segreto personale richiesto dai job.
