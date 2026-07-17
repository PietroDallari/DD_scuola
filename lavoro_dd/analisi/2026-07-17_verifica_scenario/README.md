# Verifica scenario base + sensibilità + dati modello obbligo-18 — 2026-07-17

Lavoro nostro (ORA) sul modello ciclo unico di Nazareno Lecis, pin upstream `a9edf41`.
**Nessun file di Nazareno è stato modificato o ridistribuito qui.** I run corretti sono
prodotti da `run_scenario.py`, che *importa* le sue funzioni e passa dati/parametri corretti;
gli output di scenario vanno in cartelle gitignored del clone e NON sono in questo repo.

## Contenuto
- `RISCONTRO_ciclo_unico_2026-07-17.md` — report completo (verifica, bug, sensibilità, dati).
- `analisi_tecnica_duplicazione_posas_x4.md` — analisi tecnica standalone del bug POSAS ×4:
  causa nel codice (file/riga), evidenza, propagazione, impatto e fix proposto (linkabile).
- `run_scenario.py` — driver esterno per i rerun corretti (dedup POSAS + override parametri).
- `risultati_sensibilita_corretta/` — nostri risultati calcolati (4 scenari × 2 file):
  `spesa_riepilogo_realistico__*` e `spesa_confronto_orizzonti_realistico__*`.
- `dati_modello_obbligo18/` — nostre estrazioni da fonti ufficiali (ISTAT POSAS 2026, MIM ALUCORSOETA 2024/25).

## Headline
Bug POSAS ×4 (popolazione ISTAT duplicata) nell'estrattore di Nazareno. Con dato corretto (÷4)
lo scenario base passa da **36,8/36,0 mld** (lordo/netto committati) a **25,2/22,0 mld**, e le
chiusure da **3.001 a 8.367**. Il fix va fatto a monte nel repo di Nazareno; dettagli e proposta
nel RISCONTRO.
