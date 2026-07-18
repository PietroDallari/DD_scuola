# Fase 3 — calibrazione soglie + parametri e modello costo docente (2026-07-17)

Lavoro nostro (ORA) sul modello ciclo unico di Nazareno Lecis (pin `a9edf41`), su **dato POSAS corretto ÷4**.
Repo di Nazareno read-only: tutto prodotto da driver esterni che ne importano le funzioni.

## Contenuto
- `RISCONTRO_fase3_2026-07-17.md` — report fase 3 (Task A/B/C, fonti, anomalie).
- `RISCONTRO_fase3b_saldo_euro_e_concentrazione.md` — addendum che chiude i due punti aperti (SALDO in euro con CDOC validato + proposta concentrazione graduale).
- `griglia_calibrazione/` — `run_grid.py` (driver 16 run) + `griglia_calibrazione_soglie.csv` (griglia soglia×concentrazione con chiusure, spesa, presidio-check).
- `concentrazione_graduale/` — proposta della tolleranza di ridondanza τ per Nazareno: `proposta_concentrazione_graduale_tau.md`, `run_tau.py`, `curva_tau_concentrazione.csv`, e le righe complete degli endpoint τ=1,5 / τ=2,0.
- `parametri_modello_B/` — parametri sourced: RDS docenti/studenti, iscritti paritarie e statali per età, Eurostat ELET e partecipazione 16-17. (CSV grezzi MIM nel pacchetto brother, non in git.)
- `modello_costo_docente_C/` — `task_c_model.py`, componenti A/C in docenti (`task_c_modello_costo_docente_teachers.csv`) e SALDO in euro (`task_c_saldo_euro.csv`).

## Headline
- **Calibrazione:** sul dato corretto, concentrazione ON = 46–50% chiusure (~25 mld), OFF = 4,5–12,4% (~38–40 mld). Il ~18% del committato non è riproducibile: era un artefatto della domanda ×4. La concentrazione è "tutto o niente" → proposta di un parametro di tolleranza graduale **τ** (curva monotòna; τ≈2,0 → 19% chiusure ≈ le 3.001 del committato, su dato corretto; presidio ortogonale a τ).
- **Costo docente:** la compressione 13→12 leve libera ~18–33 mila docenti netti (> del trattenimento dell'obbligo a 18) → l'obbligo si **autofinanzia**, e il rilascio è **assorbito dal turnover** (rapporto 0,2–0,6 vs pensionamenti), senza licenziamenti. Con CDOC 44.000 € [RGS Conto Annuale 2024]: parte docenti = risparmio 0,8–1,45 mld €/anno; saldo totale +0,57/+1,21 mld €/anno = interamente arricchimento B (segnaposto).
