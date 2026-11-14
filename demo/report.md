# Rapporto SEO Strategist

Analisi sul campione; segnali e priorità non garantiscono risultati.

**DEMO: dati sintetici generati localmente. Nessun sito reale analizzato.**

## Matrice delle pagine

| URL richiesta | URL finale | HTTP finale | Redirect | Noindex | Canonical | Sitemap |
|---|---|---|---|---|---|---|
| https://demo.example.invalid/ | https://demo.example.invalid/ | 200 | — | No | https://demo.example.invalid/ | Sì |
| https://demo.example.invalid/article | https://demo.example.invalid/article | 200 | — | No | https://demo.example.invalid/article | Sì |
| https://demo.example.invalid/old | https://demo.example.invalid/article | 200 | 301 | No | https://demo.example.invalid/article | Sì |
| https://demo.example.invalid/private | https://demo.example.invalid/private | 200 | — | Sì | https://demo.example.invalid/article | Sì |
| https://demo.example.invalid/missing | https://demo.example.invalid/missing | 404 | — | Non verificato | — | Sì |

## Roadmap

- P1: Direttiva noindex osservata; verificare intenzione prima di modificarla — &#91;'https://demo.example.invalid/private'&#93;
- P1: Pagina non analizzabile come HTML — &#91;'https://demo.example.invalid/missing'&#93;
- P2: Canonical dichiarato diverso dall'URL finale; scelta Google non verificata — &#91;'https://demo.example.invalid/private'&#93;
- P2: Link a un target non canonico noto nel campione — &#91;'https://demo.example.invalid/'&#93;
- P2: Immagini senza attributo alt; verificare funzione e contenuto — &#91;'https://demo.example.invalid/'&#93;
- P2: Title assente nell'HTML iniziale — &#91;'https://demo.example.invalid/private'&#93;
- P3: Description fuori fascia editoriale interna 50–170; non limite Google — &#91;'https://demo.example.invalid/'&#93;
- P3: Meta description assente; snippet effettivo non verificato — &#91;'https://demo.example.invalid/article', 'https://demo.example.invalid/old', 'https://demo.example.invalid/private'&#93;
- P3: Nessun H1 rilevato — &#91;'https://demo.example.invalid/private'&#93;

## Evidenze complete

Tutti i campi, inclusi errori e limiti, sono riportati di seguito come testo.

<pre>{
  &quot;schema_version&quot;: 1,
  &quot;scope&quot;: &quot;sample&quot;,
  &quot;requested_url&quot;: &quot;https://demo.example.invalid/&quot;,
  &quot;sample&quot;: {
    &quot;selected&quot;: [
      &quot;https://demo.example.invalid/&quot;,
      &quot;https://demo.example.invalid/article&quot;,
      &quot;https://demo.example.invalid/old&quot;,
      &quot;https://demo.example.invalid/private&quot;,
      &quot;https://demo.example.invalid/missing&quot;
    ],
    &quot;available_candidates&quot;: 5,
    &quot;limit&quot;: 10,
    &quot;selection&quot;: &quot;URL iniziale, poi ordine sitemap&quot;
  },
  &quot;resources&quot;: {
    &quot;robots&quot;: {
      &quot;requested_url&quot;: &quot;https://demo.example.invalid/robots.txt&quot;,
      &quot;final_url&quot;: &quot;https://demo.example.invalid/robots.txt&quot;,
      &quot;status&quot;: 200,
      &quot;state&quot;: &quot;present&quot;,
      &quot;headers&quot;: {
        &quot;content-type&quot;: &quot;text/plain&quot;
      },
      &quot;redirects&quot;: [],
      &quot;attempts&quot;: 1,
      &quot;error&quot;: null
    },
    &quot;llms&quot;: {
      &quot;requested_url&quot;: &quot;https://demo.example.invalid/llms.txt&quot;,
      &quot;final_url&quot;: &quot;https://demo.example.invalid/llms.txt&quot;,
      &quot;status&quot;: 200,
      &quot;state&quot;: &quot;present&quot;,
      &quot;headers&quot;: {
        &quot;content-type&quot;: &quot;text/plain&quot;
      },
      &quot;redirects&quot;: [],
      &quot;attempts&quot;: 1,
      &quot;error&quot;: null
    },
    &quot;llms_quality&quot;: {
      &quot;state&quot;: &quot;observed&quot;,
      &quot;experimental&quot;: true,
      &quot;checks&quot;: {
        &quot;h1&quot;: true,
        &quot;summary&quot;: true,
        &quot;sections&quot;: true,
        &quot;markdown_links&quot;: true,
        &quot;not_html&quot;: true
      },
      &quot;note&quot;: &quot;Indicatori di struttura della proposta llms.txt v2; qualità semantica e utilizzo non verificati.&quot;
    },
    &quot;sitemap&quot;: {
      &quot;entries&quot;: [
        {
          &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
          &quot;lastmod&quot;: &quot;2025-01-10&quot;,
          &quot;issues&quot;: []
        },
        {
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;lastmod&quot;: &quot;2025-01-10&quot;,
          &quot;issues&quot;: []
        },
        {
          &quot;url&quot;: &quot;https://demo.example.invalid/old&quot;,
          &quot;lastmod&quot;: &quot;2025-01-10&quot;,
          &quot;issues&quot;: []
        },
        {
          &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
          &quot;lastmod&quot;: &quot;2025-01-10&quot;,
          &quot;issues&quot;: []
        },
        {
          &quot;url&quot;: &quot;https://demo.example.invalid/missing&quot;,
          &quot;lastmod&quot;: &quot;2025-01-10&quot;,
          &quot;issues&quot;: []
        }
      ],
      &quot;checks&quot;: [
        {
          &quot;requested_url&quot;: &quot;https://demo.example.invalid/sitemap.xml&quot;,
          &quot;final_url&quot;: &quot;https://demo.example.invalid/sitemap.xml&quot;,
          &quot;status&quot;: 200,
          &quot;state&quot;: &quot;present&quot;,
          &quot;headers&quot;: {
            &quot;content-type&quot;: &quot;application/xml&quot;
          },
          &quot;redirects&quot;: [],
          &quot;attempts&quot;: 1,
          &quot;error&quot;: null
        },
        {
          &quot;requested_url&quot;: &quot;https://demo.example.invalid/pages.xml&quot;,
          &quot;final_url&quot;: &quot;https://demo.example.invalid/pages.xml&quot;,
          &quot;status&quot;: 200,
          &quot;state&quot;: &quot;present&quot;,
          &quot;headers&quot;: {
            &quot;content-type&quot;: &quot;application/xml&quot;
          },
          &quot;redirects&quot;: [],
          &quot;attempts&quot;: 1,
          &quot;error&quot;: null
        }
      ],
      &quot;warnings&quot;: [],
      &quot;complete&quot;: true,
      &quot;limits&quot;: {
        &quot;documents&quot;: 10,
        &quot;depth&quot;: 3,
        &quot;urls&quot;: 1000
      }
    },
    &quot;declared_sitemaps&quot;: [
      &quot;https://demo.example.invalid/sitemap.xml&quot;
    ],
    &quot;host_variants&quot;: [],
    &quot;variant_note&quot;: &quot;Solo varianti esplicitamente richieste; URL iniziale e finale sempre conservati.&quot;
  },
  &quot;pages&quot;: [
    {
      &quot;http&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/&quot;,
        &quot;status&quot;: 200,
        &quot;state&quot;: &quot;present&quot;,
        &quot;headers&quot;: {
          &quot;content-type&quot;: &quot;text/html; charset=utf-8&quot;
        },
        &quot;redirects&quot;: [],
        &quot;attempts&quot;: 1,
        &quot;error&quot;: null
      },
      &quot;initial&quot;: {
        &quot;title&quot;: &quot;Laboratorio SEO sintetico&quot;,
        &quot;descriptions&quot;: [
          &quot;Pagina dimostrativa di un audit locale.&quot;
        ],
        &quot;headings&quot;: [
          {
            &quot;level&quot;: 1,
            &quot;text&quot;: &quot;Laboratorio&quot;
          }
        ],
        &quot;text&quot;: &quot;Laboratorio clicca qui Guida sintetica Dati inventati per verificare il funzionamento del software.&quot;,
        &quot;images&quot;: [
          {
            &quot;src&quot;: &quot;/photo.png&quot;,
            &quot;alt&quot;: null,
            &quot;decorative_candidate&quot;: false
          }
        ],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/&quot;
        ],
        &quot;robots&quot;: [],
        &quot;hreflang&quot;: [],
        &quot;jsonld&quot;: [],
        &quot;jsonld_errors&quot;: [],
        &quot;links&quot;: [
          {
            &quot;href&quot;: &quot;/old&quot;,
            &quot;text&quot;: &quot;clicca qui&quot;,
            &quot;rel&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;https://demo.example.invalid/old&quot;,
            &quot;navigable&quot;: true,
            &quot;generic_anchor&quot;: true
          },
          {
            &quot;href&quot;: &quot;/article&quot;,
            &quot;text&quot;: &quot;Guida sintetica&quot;,
            &quot;rel&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
            &quot;navigable&quot;: true,
            &quot;generic_anchor&quot;: false
          }
        ],
        &quot;dates&quot;: [],
        &quot;script_count&quot;: 0,
        &quot;geo&quot;: {
          &quot;signals&quot;: {
            &quot;headings&quot;: true,
            &quot;question_headings&quot;: false,
            &quot;citation_markup&quot;: false,
            &quot;date_markup&quot;: false,
            &quot;lists&quot;: false,
            &quot;structured_data&quot;: false
          },
          &quot;heuristic_score&quot;: 1,
          &quot;scale&quot;: &quot;0–6, euristica interna; non misura citazioni o ranking&quot;,
          &quot;evidence&quot;: &quot;observed_markup&quot;,
          &quot;limitations&quot;: &quot;Citazioni, date e JSON-LD rilevati non sono verificati quanto a verità o qualità.&quot;
        }
      },
      &quot;rendering&quot;: {
        &quot;state&quot;: &quot;off&quot;
      },
      &quot;rendered&quot;: null,
      &quot;schema_validation&quot;: [],
      &quot;matrix&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/&quot;,
        &quot;http_status&quot;: 200,
        &quot;redirects&quot;: [],
        &quot;noindex&quot;: false,
        &quot;robots_directives&quot;: [
          &quot;&quot;
        ],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/&quot;
        ],
        &quot;in_sitemap&quot;: true,
        &quot;indexability&quot;: &quot;potentially_indexable_not_verified&quot;
      },
      &quot;ai_crawlers&quot;: [
        {
          &quot;agent&quot;: &quot;GPTBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;no_matching_rule&quot;
        },
        {
          &quot;agent&quot;: &quot;OAI-SearchBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/&quot;
        }
      ],
      &quot;internal_links&quot;: [
        {
          &quot;href&quot;: &quot;/old&quot;,
          &quot;text&quot;: &quot;clicca qui&quot;,
          &quot;rel&quot;: &quot;&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/old&quot;,
          &quot;navigable&quot;: true,
          &quot;generic_anchor&quot;: true,
          &quot;known_noncanonical_target&quot;: true
        },
        {
          &quot;href&quot;: &quot;/article&quot;,
          &quot;text&quot;: &quot;Guida sintetica&quot;,
          &quot;rel&quot;: &quot;&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;navigable&quot;: true,
          &quot;generic_anchor&quot;: false,
          &quot;known_noncanonical_target&quot;: false
        }
      ]
    },
    {
      &quot;http&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;status&quot;: 200,
        &quot;state&quot;: &quot;present&quot;,
        &quot;headers&quot;: {
          &quot;content-type&quot;: &quot;text/html; charset=utf-8&quot;
        },
        &quot;redirects&quot;: [],
        &quot;attempts&quot;: 1,
        &quot;error&quot;: null
      },
      &quot;initial&quot;: {
        &quot;title&quot;: &quot;Guida sintetica alla ricerca&quot;,
        &quot;descriptions&quot;: [],
        &quot;headings&quot;: [
          {
            &quot;level&quot;: 1,
            &quot;text&quot;: &quot;Come verificare le fonti?&quot;
          }
        ],
        &quot;text&quot;: &quot;Come verificare le fonti? Leggi la fonte primaria Fonte dimostrativa 10 gennaio&quot;,
        &quot;images&quot;: [],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;robots&quot;: [],
        &quot;hreflang&quot;: [],
        &quot;jsonld&quot;: [
          {
            &quot;@context&quot;: &quot;https://schema.org&quot;,
            &quot;@type&quot;: &quot;Article&quot;,
            &quot;headline&quot;: &quot;Guida sintetica&quot;,
            &quot;author&quot;: {
              &quot;@type&quot;: &quot;Person&quot;,
              &quot;name&quot;: &quot;Autore di esempio&quot;
            }
          }
        ],
        &quot;jsonld_errors&quot;: [],
        &quot;links&quot;: [],
        &quot;dates&quot;: [
          &quot;2025-01-10&quot;
        ],
        &quot;script_count&quot;: 1,
        &quot;geo&quot;: {
          &quot;signals&quot;: {
            &quot;headings&quot;: true,
            &quot;question_headings&quot;: true,
            &quot;citation_markup&quot;: true,
            &quot;date_markup&quot;: true,
            &quot;lists&quot;: true,
            &quot;structured_data&quot;: true
          },
          &quot;heuristic_score&quot;: 6,
          &quot;scale&quot;: &quot;0–6, euristica interna; non misura citazioni o ranking&quot;,
          &quot;evidence&quot;: &quot;observed_markup&quot;,
          &quot;limitations&quot;: &quot;Citazioni, date e JSON-LD rilevati non sono verificati quanto a verità o qualità.&quot;
        }
      },
      &quot;rendering&quot;: {
        &quot;state&quot;: &quot;off&quot;
      },
      &quot;rendered&quot;: null,
      &quot;schema_validation&quot;: [
        {
          &quot;valid_local_contract&quot;: true,
          &quot;errors&quot;: [],
          &quot;scope&quot;: &quot;Campi e coerenza locali; non validazione completa Schema.org, autenticità rating o idoneità Google.&quot;
        }
      ],
      &quot;matrix&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;http_status&quot;: 200,
        &quot;redirects&quot;: [],
        &quot;noindex&quot;: false,
        &quot;robots_directives&quot;: [
          &quot;&quot;
        ],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;in_sitemap&quot;: true,
        &quot;indexability&quot;: &quot;potentially_indexable_not_verified&quot;
      },
      &quot;ai_crawlers&quot;: [
        {
          &quot;agent&quot;: &quot;GPTBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;no_matching_rule&quot;
        },
        {
          &quot;agent&quot;: &quot;OAI-SearchBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/&quot;
        }
      ],
      &quot;internal_links&quot;: []
    },
    {
      &quot;http&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/old&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;status&quot;: 200,
        &quot;state&quot;: &quot;present&quot;,
        &quot;headers&quot;: {
          &quot;content-type&quot;: &quot;text/html; charset=utf-8&quot;
        },
        &quot;redirects&quot;: [
          {
            &quot;from&quot;: &quot;https://demo.example.invalid/old&quot;,
            &quot;to&quot;: &quot;https://demo.example.invalid/article&quot;,
            &quot;status&quot;: 301
          }
        ],
        &quot;attempts&quot;: 2,
        &quot;error&quot;: null
      },
      &quot;initial&quot;: {
        &quot;title&quot;: &quot;Guida sintetica alla ricerca&quot;,
        &quot;descriptions&quot;: [],
        &quot;headings&quot;: [
          {
            &quot;level&quot;: 1,
            &quot;text&quot;: &quot;Come verificare le fonti?&quot;
          }
        ],
        &quot;text&quot;: &quot;Come verificare le fonti? Leggi la fonte primaria Fonte dimostrativa 10 gennaio&quot;,
        &quot;images&quot;: [],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;robots&quot;: [],
        &quot;hreflang&quot;: [],
        &quot;jsonld&quot;: [
          {
            &quot;@context&quot;: &quot;https://schema.org&quot;,
            &quot;@type&quot;: &quot;Article&quot;,
            &quot;headline&quot;: &quot;Guida sintetica&quot;,
            &quot;author&quot;: {
              &quot;@type&quot;: &quot;Person&quot;,
              &quot;name&quot;: &quot;Autore di esempio&quot;
            }
          }
        ],
        &quot;jsonld_errors&quot;: [],
        &quot;links&quot;: [],
        &quot;dates&quot;: [
          &quot;2025-01-10&quot;
        ],
        &quot;script_count&quot;: 1,
        &quot;geo&quot;: {
          &quot;signals&quot;: {
            &quot;headings&quot;: true,
            &quot;question_headings&quot;: true,
            &quot;citation_markup&quot;: true,
            &quot;date_markup&quot;: true,
            &quot;lists&quot;: true,
            &quot;structured_data&quot;: true
          },
          &quot;heuristic_score&quot;: 6,
          &quot;scale&quot;: &quot;0–6, euristica interna; non misura citazioni o ranking&quot;,
          &quot;evidence&quot;: &quot;observed_markup&quot;,
          &quot;limitations&quot;: &quot;Citazioni, date e JSON-LD rilevati non sono verificati quanto a verità o qualità.&quot;
        }
      },
      &quot;rendering&quot;: {
        &quot;state&quot;: &quot;off&quot;
      },
      &quot;rendered&quot;: null,
      &quot;schema_validation&quot;: [
        {
          &quot;valid_local_contract&quot;: true,
          &quot;errors&quot;: [],
          &quot;scope&quot;: &quot;Campi e coerenza locali; non validazione completa Schema.org, autenticità rating o idoneità Google.&quot;
        }
      ],
      &quot;matrix&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/old&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/article&quot;,
        &quot;http_status&quot;: 200,
        &quot;redirects&quot;: [
          {
            &quot;from&quot;: &quot;https://demo.example.invalid/old&quot;,
            &quot;to&quot;: &quot;https://demo.example.invalid/article&quot;,
            &quot;status&quot;: 301
          }
        ],
        &quot;noindex&quot;: false,
        &quot;robots_directives&quot;: [
          &quot;&quot;
        ],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;in_sitemap&quot;: true,
        &quot;indexability&quot;: &quot;potentially_indexable_not_verified&quot;
      },
      &quot;ai_crawlers&quot;: [
        {
          &quot;agent&quot;: &quot;GPTBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;no_matching_rule&quot;
        },
        {
          &quot;agent&quot;: &quot;OAI-SearchBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/&quot;
        }
      ],
      &quot;internal_links&quot;: []
    },
    {
      &quot;http&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/private&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/private&quot;,
        &quot;status&quot;: 200,
        &quot;state&quot;: &quot;present&quot;,
        &quot;headers&quot;: {
          &quot;content-type&quot;: &quot;text/html; charset=utf-8&quot;
        },
        &quot;redirects&quot;: [],
        &quot;attempts&quot;: 1,
        &quot;error&quot;: null
      },
      &quot;initial&quot;: {
        &quot;title&quot;: &quot;&quot;,
        &quot;descriptions&quot;: [],
        &quot;headings&quot;: [
          {
            &quot;level&quot;: 2,
            &quot;text&quot;: &quot;Pagina riservata dimostrativa&quot;
          }
        ],
        &quot;text&quot;: &quot;Pagina riservata dimostrativa&quot;,
        &quot;images&quot;: [],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;robots&quot;: [
          {
            &quot;agent&quot;: &quot;robots&quot;,
            &quot;value&quot;: &quot;noindex&quot;
          }
        ],
        &quot;hreflang&quot;: [],
        &quot;jsonld&quot;: [],
        &quot;jsonld_errors&quot;: [],
        &quot;links&quot;: [],
        &quot;dates&quot;: [],
        &quot;script_count&quot;: 0,
        &quot;geo&quot;: {
          &quot;signals&quot;: {
            &quot;headings&quot;: true,
            &quot;question_headings&quot;: false,
            &quot;citation_markup&quot;: false,
            &quot;date_markup&quot;: false,
            &quot;lists&quot;: false,
            &quot;structured_data&quot;: false
          },
          &quot;heuristic_score&quot;: 1,
          &quot;scale&quot;: &quot;0–6, euristica interna; non misura citazioni o ranking&quot;,
          &quot;evidence&quot;: &quot;observed_markup&quot;,
          &quot;limitations&quot;: &quot;Citazioni, date e JSON-LD rilevati non sono verificati quanto a verità o qualità.&quot;
        }
      },
      &quot;rendering&quot;: {
        &quot;state&quot;: &quot;off&quot;
      },
      &quot;rendered&quot;: null,
      &quot;schema_validation&quot;: [],
      &quot;matrix&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/private&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/private&quot;,
        &quot;http_status&quot;: 200,
        &quot;redirects&quot;: [],
        &quot;noindex&quot;: true,
        &quot;robots_directives&quot;: [
          &quot;noindex&quot;,
          &quot;&quot;
        ],
        &quot;canonical&quot;: [
          &quot;https://demo.example.invalid/article&quot;
        ],
        &quot;in_sitemap&quot;: true,
        &quot;indexability&quot;: &quot;noindex_observed&quot;
      },
      &quot;ai_crawlers&quot;: [
        {
          &quot;agent&quot;: &quot;GPTBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
          &quot;declared_access&quot;: false,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/private&quot;
        },
        {
          &quot;agent&quot;: &quot;OAI-SearchBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/&quot;
        }
      ],
      &quot;internal_links&quot;: []
    },
    {
      &quot;http&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/missing&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/missing&quot;,
        &quot;status&quot;: 404,
        &quot;state&quot;: &quot;absent&quot;,
        &quot;headers&quot;: {
          &quot;content-type&quot;: &quot;text/html; charset=utf-8&quot;
        },
        &quot;redirects&quot;: [],
        &quot;attempts&quot;: 1,
        &quot;error&quot;: null
      },
      &quot;initial&quot;: null,
      &quot;rendering&quot;: {
        &quot;state&quot;: &quot;off&quot;
      },
      &quot;rendered&quot;: null,
      &quot;matrix&quot;: {
        &quot;requested_url&quot;: &quot;https://demo.example.invalid/missing&quot;,
        &quot;final_url&quot;: &quot;https://demo.example.invalid/missing&quot;,
        &quot;http_status&quot;: 404,
        &quot;redirects&quot;: [],
        &quot;noindex&quot;: null,
        &quot;robots_directives&quot;: [
          &quot;&quot;
        ],
        &quot;canonical&quot;: [],
        &quot;in_sitemap&quot;: true,
        &quot;indexability&quot;: &quot;inconclusive&quot;
      },
      &quot;ai_crawlers&quot;: [
        {
          &quot;agent&quot;: &quot;GPTBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/missing&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;no_matching_rule&quot;
        },
        {
          &quot;agent&quot;: &quot;OAI-SearchBot&quot;,
          &quot;url&quot;: &quot;https://demo.example.invalid/missing&quot;,
          &quot;declared_access&quot;: true,
          &quot;state&quot;: &quot;declared&quot;,
          &quot;actual_use&quot;: &quot;Non deducibile: accesso, indicizzazione e citazioni non verificati.&quot;,
          &quot;reason&quot;: &quot;/&quot;
        }
      ],
      &quot;internal_links&quot;: []
    }
  ],
  &quot;findings&quot;: [
    {
      &quot;code&quot;: &quot;description_editorial_review&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Description fuori fascia editoriale interna 50–170; non limite Google&quot;,
      &quot;evidence&quot;: &quot;heuristic&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_alt&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Immagini senza attributo alt; verificare funzione e contenuto&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_description&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/article&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Meta description assente; snippet effettivo non verificato&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_description&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/old&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Meta description assente; snippet effettivo non verificato&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_title&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Title assente nell&#x27;HTML iniziale&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_description&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Meta description assente; snippet effettivo non verificato&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_h1&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Nessun H1 rilevato&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;noindex_review&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
      &quot;priority&quot;: 1,
      &quot;reason&quot;: &quot;Direttiva noindex osservata; verificare intenzione prima di modificarla&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [
        &quot;Conferma obiettivo di indicizzazione&quot;
      ],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;canonical_other&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/private&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Canonical dichiarato diverso dall&#x27;URL finale; scelta Google non verificata&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [
        &quot;Verifica equivalenza contenuti&quot;
      ],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;page_unavailable&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/missing&quot;,
      &quot;priority&quot;: 1,
      &quot;reason&quot;: &quot;Pagina non analizzabile come HTML&quot;,
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: [
        &quot;HTML analizzabile&quot;
      ]
    },
    {
      &quot;code&quot;: &quot;internal_noncanonical&quot;,
      &quot;url&quot;: &quot;https://demo.example.invalid/&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Link a un target non canonico noto nel campione&quot;,
      &quot;evidence&quot;: &quot;sample_observation&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    }
  ],
  &quot;roadmap&quot;: [
    {
      &quot;code&quot;: &quot;noindex_review&quot;,
      &quot;priority&quot;: 1,
      &quot;reason&quot;: &quot;Direttiva noindex osservata; verificare intenzione prima di modificarla&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/private&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [
        &quot;Conferma obiettivo di indicizzazione&quot;
      ],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;page_unavailable&quot;,
      &quot;priority&quot;: 1,
      &quot;reason&quot;: &quot;Pagina non analizzabile come HTML&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/missing&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: [
        &quot;HTML analizzabile&quot;
      ]
    },
    {
      &quot;code&quot;: &quot;canonical_other&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Canonical dichiarato diverso dall&#x27;URL finale; scelta Google non verificata&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/private&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [
        &quot;Verifica equivalenza contenuti&quot;
      ],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;internal_noncanonical&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Link a un target non canonico noto nel campione&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/&quot;
      ],
      &quot;evidence&quot;: &quot;sample_observation&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_alt&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Immagini senza attributo alt; verificare funzione e contenuto&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_title&quot;,
      &quot;priority&quot;: 2,
      &quot;reason&quot;: &quot;Title assente nell&#x27;HTML iniziale&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/private&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;description_editorial_review&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Description fuori fascia editoriale interna 50–170; non limite Google&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/&quot;
      ],
      &quot;evidence&quot;: &quot;heuristic&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_description&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Meta description assente; snippet effettivo non verificato&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/article&quot;,
        &quot;https://demo.example.invalid/old&quot;,
        &quot;https://demo.example.invalid/private&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    },
    {
      &quot;code&quot;: &quot;missing_h1&quot;,
      &quot;priority&quot;: 3,
      &quot;reason&quot;: &quot;Nessun H1 rilevato&quot;,
      &quot;urls&quot;: [
        &quot;https://demo.example.invalid/private&quot;
      ],
      &quot;evidence&quot;: &quot;observed&quot;,
      &quot;dependencies&quot;: [],
      &quot;missing_data&quot;: []
    }
  ],
  &quot;limitations&quot;: [
    &quot;Risultati limitati al campione&quot;,
    &quot;Nessuna misura INP, ranking, traffico o citazioni AI&quot;,
    &quot;robots è una dichiarazione; utilizzo reale dei crawler non verificato&quot;,
    &quot;Nessuna analisi di competitor eseguita&quot;
  ],
  &quot;synthetic&quot;: true,
  &quot;demo_method&quot;: &quot;HTTP reale su server sintetico loopback; origine sostituita da dominio riservato, header volatili rimossi. Rendering off.&quot;,
  &quot;keyword_example&quot;: {
    &quot;clusters&quot;: [
      {
        &quot;id&quot;: 1,
        &quot;seed_tokens&quot;: [
          &quot;comprare&quot;,
          &quot;rosse&quot;,
          &quot;scarpe&quot;
        ],
        &quot;keywords&quot;: [
          {
            &quot;keyword&quot;: &quot;comprare scarpe rosse&quot;,
            &quot;intent&quot;: &quot;transactional&quot;,
            &quot;evidence&quot;: &quot;rule_based_inference&quot;,
            &quot;opportunity&quot;: &quot;specifica_da_validare&quot;,
            &quot;volume&quot;: null,
            &quot;difficulty&quot;: null
          },
          {
            &quot;keyword&quot;: &quot;prezzo scarpe rosse&quot;,
            &quot;intent&quot;: &quot;transactional&quot;,
            &quot;evidence&quot;: &quot;rule_based_inference&quot;,
            &quot;opportunity&quot;: &quot;specifica_da_validare&quot;,
            &quot;volume&quot;: null,
            &quot;difficulty&quot;: null
          }
        ]
      },
      {
        &quot;id&quot;: 2,
        &quot;seed_tokens&quot;: [
          &quot;scarpe&quot;,
          &quot;scegliere&quot;
        ],
        &quot;keywords&quot;: [
          {
            &quot;keyword&quot;: &quot;come scegliere scarpe&quot;,
            &quot;intent&quot;: &quot;informational&quot;,
            &quot;evidence&quot;: &quot;rule_based_inference&quot;,
            &quot;opportunity&quot;: &quot;ampia_da_esplorare&quot;,
            &quot;volume&quot;: null,
            &quot;difficulty&quot;: null
          }
        ]
      }
    ],
    &quot;method&quot;: &quot;Jaccard &gt;= 0.5 rispetto al primo elemento del cluster; dipende dall&#x27;ordine di input. Intent per parole chiave, nessuna misura SERP.&quot;,
    &quot;missing_data&quot;: [
      &quot;volumi misurati&quot;,
      &quot;difficoltà misurata&quot;,
      &quot;SERP verificata&quot;
    ]
  },
  &quot;brief_example&quot;: {
    &quot;status&quot;: &quot;bozza_da_revisionare&quot;,
    &quot;topic&quot;: &quot;Scelta delle scarpe&quot;,
    &quot;audience&quot;: &quot;lettori di esempio&quot;,
    &quot;intent&quot;: &quot;informational&quot;,
    &quot;working_title&quot;: &quot;Scelta delle scarpe: guida per lettori di esempio&quot;,
    &quot;outline&quot;: [
      &quot;Problema del lettore e risposta iniziale&quot;,
      &quot;Concetti e criteri di scelta&quot;,
      &quot;Esempio verificabile&quot;,
      &quot;Limiti e prossimi passi&quot;
    ],
    &quot;evidence_supplied&quot;: [],
    &quot;competitor_analysis&quot;: &quot;non_eseguita&quot;,
    &quot;requirements&quot;: [
      &quot;Verificare ogni dato e fonte&quot;,
      &quot;Aggiungere esperienza o esempi originali&quot;,
      &quot;Controllare che il titolo rispecchi il contenuto&quot;
    ],
    &quot;missing_data&quot;: [
      &quot;SERP corrente&quot;,
      &quot;differenziazione verificata&quot;,
      &quot;dati proprietari e revisione esperta&quot;
    ]
  }
}</pre>
