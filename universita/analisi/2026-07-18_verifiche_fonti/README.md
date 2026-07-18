# Verifiche fonti-primarie — batch 2026-07-18

Prima tornata di verifiche dei flag [C] del report `../../docs/Universita_e_Ricerca_ORA_v1.md`.
Stato complessivo e protocollo in `../../note/stato_verifiche.md`.

## Fatto in questo batch (Eurostat, fonte primaria via API)
- **B6 — spesa pubblica istruzione terziaria (% PIL).** IT **0,4%** vs EU27 **0,8%** (2023-24, stabile dal 2021). Risolve il [C] "0,3–0,4% vs ~0,8%": il valore è 0,4% (il 0,3 corrispondeva a un perimetro diverso). Fonte: Eurostat `gov_10a_exp`, COFOG GF0904 (istruzione terziaria), settore S13, spesa totale, % PIL. → `data/b6_spesa_terziaria_cofog.csv`
- **F1 — attainment terziario 25-34.** IT 30,6% / EU27 43,1% (2023) — coincide con i numeri del report §1.4. Ultimo disponibile 2025: IT 31,1% / EU 44,8%. Fonte: Eurostat `edat_lfse_03`, ISCED ED5-8. → `data/f1_attainment_25_34.csv`

## Cartelle
- `data/` — estrazioni verificate (CSV con fonte/anno per riga).
- `figures/` — script e output figure (da popolare: F1 usa `f1_attainment_25_34.csv`).

## Nota di metodo
Nessuna modifica al report: le verifiche stanno qui; le correzioni ai numeri del report si applicano in v2 dopo review di Pietro (protocollo di quarantena). Le voci [C] che richiedono decreti/GU/USTAT (B1, B2, B4, ...) comportano download e parsing di PDF: da fare a lotti nelle prossime sessioni.
