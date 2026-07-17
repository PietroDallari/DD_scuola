# Fase 3 — calibrazione soglie + parametri e modello costo docente (2026-07-17)

Lavoro nostro (ORA) sul modello ciclo unico di Nazareno Lecis (pin `a9edf41`), su **dato POSAS corretto ÷4**.
Repo di Nazareno read-only: tutto prodotto da driver esterni che ne importano le funzioni.

## Contenuto
- `RISCONTRO_fase3_2026-07-17.md` — report completo (Task A/B/C, fonti, anomalie).
- `griglia_calibrazione/` — `run_grid.py` (driver 16 run) + `griglia_calibrazione_soglie.csv` (griglia soglia×concentrazione con chiusure, spesa, presidio-check).
- `parametri_modello_B/` — parametri sourced per il modello: RDS docenti/studenti, iscritti paritarie e statali per età, Eurostat ELET e partecipazione 16-17. (CSV grezzi MIM nel pacchetto brother, non in git.)
- `modello_costo_docente_C/` — `task_c_model.py` + `task_c_modello_costo_docente_teachers.csv` (componenti A/C in docenti, per regime e copertura).

## Headline
- **Calibrazione:** sul dato corretto, concentrazione ON = 46–50% chiusure (~25 mld), OFF = 4,5–12,4% (~38–40 mld). Il ~18% del committato non è riproducibile: era un artefatto della domanda ×4. La concentrazione è "tutto o niente" → per un target intermedio serve un meccanismo graduale.
- **Costo docente:** la compressione 13→12 leve libera ~18–33 mila docenti netti (> del trattenimento dell'obbligo a 18) → l'obbligo si **autofinanzia**, e il rilascio è **assorbito dal turnover** (rapporto 0,2–0,6 vs pensionamenti), senza licenziamenti. Euro in attesa di CDOC (RGS, B.2).
