# Riscontro fase 3b — SALDO in euro (CDOC validato) + concentrazione graduale τ

**Data:** 2026-07-17 · Chiude i due punti aperti della fase 3. Repo di Nazareno read-only.

## 1. Task C — SALDO in euro (CDOC [V])
**CDOC = 44.000 €** [V — RGS Conto Annuale 2024, cruscotto SICO, categoria *docenti a tempo indeterminato / laureati* ≈ secondaria: retribuzione media 2024 ≈ 33.200 × 1,3247 oneri+IRAP]; intervallo 41.500–46.000. (Il 2023 a 34.000 include arretrati CCNL → non usato. Gerarchia verificata: laureati 33,2k > media TI 32,9k > comparto ~31,6k.) `COSTO_B` = 2,02 mld €/anno (OPEX arricchimento, segnaposto 400 €/stud). File: [modello_costo_docente_C/task_c_saldo_euro.csv](modello_costo_docente_C/task_c_saldo_euro.csv).

| Regime | Copertura | Docenti A+C €mld/anno | **SALDO tot €mld/anno** | intervallo |
|---|---|---|---|---|
| 2032/33 | totale | −1,45 | **+0,57** | +0,36 / +0,79 |
| 2032/33 | prudente (solo statale) | −0,90 | **+1,12** | +0,98 / +1,26 |
| 2037/38 | totale | −1,27 | **+0,75** | +0,56 / +0,94 |
| 2037/38 | prudente | −0,81 | **+1,21** | +1,09 / +1,33 |

**Lettura:** la parte docenti (obbligo-18 trattenimento **A** + rilascio 13→12 **C**) è sempre un **risparmio di 0,8–1,45 mld €/anno**. Il saldo totale positivo (+0,57/+1,21 mld/anno) è **interamente** l'arricchimento **B** (segnaposto 400 €/stud, da promuovere a ore/cattedre reali). Quindi: **l'obbligo a 18 si autofinanzia con margine; il costo netto della riforma "a regime docenti" dipende solo da quanto arricchimento tempo-lungo si decide di finanziare.**

## 2. Concentrazione graduale — proposta τ + curva di calibrazione
Disegno completo (per Nazareno, come proposta): [concentrazione_graduale/proposta_concentrazione_graduale_tau.md](concentrazione_graduale/proposta_concentrazione_graduale_tau.md).

Un solo parametro nuovo (tolleranza di ridondanza τ) rende continua la scelta oggi binaria: `sedi_da_mantenere = min(ceil(sedi_target × (1+τ)), sedi_attive)` — una riga in `riordino_utils.py:182`, riusando la graduatoria tecnica già presente. τ=0 = `ON` attuale; τ→∞ = `OFF`. Curva ottenuta via monkeypatch a runtime (repo non toccato), τ=0 riproduce all'euro il run ON.

**Risultati chiave (dato corretto, soglia domanda 120):**
- Curva monotòna 49,9% (τ=0) → 12,4% (τ→∞); niente più salto 12%↔46%.
- **τ ≈ 2,0 → 19,1% di chiusure (3.205 sedi ≈ le 3.001 del committato), 35,6/34,6 mld:** riproduce l'ordine di grandezza originale **su dato corretto**, con parametro dichiarabile, non per domanda gonfiata.
- **Presidio ortogonale:** i comuni senza sede locale (~457–486) sono governati dalla soglia domanda, non da τ → si calibra la quota di razionalizzazione senza toccare il presidio.

## Stato parametri modello (aggiornato)
Tutti i [B] ora sourced: RDS 0,107 · CDOC **44.000 [V]** · paritarie 97.437 · IeFP 163.038 · ELET 8,2% · pensioni 21.322. Da promuovere: Componente **B** (400 €/stud → ore/cattedre) e distribuzione IeFP per età (chiude i 3,1 punti del check esterno).
