# Riscontro fase 3 — griglia di calibrazione, parametri modello, costo docente obbligo-18

**Data:** 2026-07-17 · **Esecutore:** Claude (analytical) · **Regole:** repo di Nazareno read-only (driver esterni `run_grid.py` e `task_c_model.py`), ogni numero con fonte/anno/URL. Base dati: scenario POSAS **corretto ÷4** (vedi [analisi_tecnica_duplicazione_posas_x4.md](../2026-07-17_verifica_scenario/analisi_tecnica_duplicazione_posas_x4.md)).

---

## Task A — Griglia di calibrazione delle soglie (dato corretto)

16 run = `usa_vincolo_concentrazione_superiori` {ON, OFF} × `soglia_domanda_minima_chiusura` (= `soglia_bacino_minimo_chiusura`) {30,60,90,120} × `studenti_minimi_sede_riferimento_superiori` {250,200}. `soglia_presidio_alunni` tenuta ferma a 120 per isolare l'effetto. **Presidio-check** = comuni con ≥1 residente 11-18 (`DOMANDA_ISTAT_ETA_COMUNE`>0) che perdono ogni sede locale (`SEDI_TENERE_APERTE`=0 e `SEDI_DA_VALUTARE`=0). Universo sedi medie-superiori = 16.770. File: [griglia_calibrazione/griglia_calibrazione_soglie.csv](griglia_calibrazione/griglia_calibrazione_soglie.csv).

**`RIFERIMENTO_SUP` 200 vs 250 dà risultati identici in ogni cella** → riporto le 8 combinazioni distinte:

| Conc. | Soglia | Chiudere | Da_val. | Tenere | % chius. | Lordo €mld | Netto €mld | Risparmi €mld | Comuni senza sede | Alunni |
|---|---|---|---|---|---|---|---|---|---|---|
| ON | 30 | 7.713 | 1.194 | 7.863 | 46,0 | 25,91 | 22,84 | 3,07 | 119 | 7.177 |
| ON | 60 | 8.004 | 1.073 | 7.693 | 47,7 | 25,66 | 22,54 | 3,12 | 287 | 27.571 |
| ON | 90 | 8.206 | 979 | 7.585 | 48,9 | 25,39 | 22,23 | 3,15 | 394 | 53.354 |
| ON | 120 | 8.367 | 912 | 7.491 | 49,9 | 25,19 | 22,00 | 3,20 | 486 | 82.083 |
| OFF | 30 | 754 | 4.244 | 11.772 | 4,5 | 40,13 | 39,87 | 0,25 | 117 | 6.431 |
| OFF | 60 | 1.285 | 3.949 | 11.536 | 7,7 | 39,53 | 39,18 | 0,35 | 280 | 25.667 |
| OFF | 90 | 1.697 | 3.698 | 11.375 | 10,1 | 38,85 | 38,41 | 0,43 | 375 | 47.797 |
| OFF | 120 | 2.073 | 3.481 | 11.216 | 12,4 | 38,21 | 37,65 | 0,55 | 457 | 74.475 |

(`ON,120` riproduce all'euro il base_dedup: 8.367 / 25,19 / 22,00 — check di consistenza.)

### 3 righe di lettura (intento prudenziale del committato ≈ 18% di chiusure sul dato corretto)
1. **Nessuna combinazione degli attuali parametri riproduce il ~18% del committato** sul dato corretto: concentrazione ON = 46–50% (troppo aggressiva), OFF = 4,5–12,4% (troppo conservativa). Il 17,9% del run buggato (3.001/16.770) era un **artefatto della domanda ×4**: la concentrazione era ON, ma con bacini gonfiati quasi nessuna sede risultava "eccedente".
2. **`studenti_minimi_sede_riferimento_superiori` (200 vs 250) non sposta nulla**: il vincolo di concentrazione è di fatto "tutto o niente" (salto da ≤12% a ≥46%). Per una calibrazione **intermedia ~18% serve un meccanismo graduale nuovo** (concentrazione parziale/pesata), non le soglie attuali.
3. La combinazione più vicina all'intento (dal basso) è **OFF, soglia 120 = 12,4%** chiusure, ma il costo resta ~38,2 mld (vicino al buggato) *per un motivo diverso* — poche chiusure, non domanda gonfiata. La concentrazione ON dimezza il costo (~25 mld) **e** chiude ~metà rete, lasciando fino a **82.083 alunni** in comuni senza sede locale (soglia 120): è il vero trade-off costo↔presidio da decidere.

---

## Task B — Parametri per il modello (fonte, anno, URL)

| # | Parametro | Valore | Anno | Fonte / dataset | URL |
|---|---|---|---|---|---|
| B.1 | RDS docenti/studenti sec. II statale | **0,107** (posto comune tit.+suppl.); 0,133 tutti i posti; 0,101 solo titolari | a.s. 2024/25 | MIM `DOCTIT` (252.367 tit.) + `DOCSUPXXV` (80.323 suppl.) sec. II ÷ `ALUCORSOETASTA` (2.506.430 alunni) | dati.istruzione.it/opendata → catalogo/elements1/`DOCTIT20242520250831.csv`, `DOCSUPXXV20242520250831.csv` |
| B.2 | Costo medio annuo docente **lordo Stato** | **NON estratto** — segnalato | 2023 | RGS Conto Annuale, Tabelle 12/13 (retrib.+oneri+IRAP). Non esposto nel testo indicizzato; serve il portale SICO / PDF | contoannuale.rgs.mef.gov.it → Spese e retribuzioni |
| B.3 | Iscritti paritarie sec. II per età | **97.437** (14→18 anni) | a.s. 2024/25 | MIM `ALUCORSOETAPAR` | dati.istruzione.it/opendata → `ALUCORSOETAPAR20242520250831.csv` |
| B.4 | Iscritti IeFP presso IF accreditate (esclusi IP in sussidiarietà) | **163.038** | a.f. 2023/24 | INAPP, XXIII Rapporto monitoraggio IeFP | oa.inapp.gov.it (XXIII Rapporto) |
| B.5 | ELET 18-24 / partecipazione età 16-17 | **ELET 8,2%** (2025); partecip. 97,1% (16) / 91,9% (17) | 2025 / 2024 | Eurostat `edat_lfse_14` (POP); `educ_uoe_enra02` (iscritti) ÷ POSAS | ec.europa.eu/eurostat API |
| B.6 | Pensionamenti annui docenti | **21.322** tutti ordini (di cui **8.536** sec. II) | 2024 | MIM (dati a OO.SS., ripresi da CISL Scuola) | tecnicadellascuola.it / cislscuola.it (dati MIM 1/9/2024) |

**Nota B.1:** il rapporto include titolari + supplenti (annuali e non separabili qui per durata); "solo titolari" 0,101 è il lower bound. **Nota B.2:** senza CDIC il modello resta in docenti; la conversione in euro è parametrica (vedi Task C). **Nota B.4:** distribuita `/3,5` anni → ~46.582/età (assunzione dichiarata).

File processati: [parametri_modello_B/](parametri_modello_B/). I CSV grezzi MIM (paritarie, docenti) sono nel pacchetto di staging per brother, non in git.

---

## Task C — Modello costo docente obbligo-18 (spec autosufficiente di console brother)

Ancore verificate: `COP_QUINTA` = 415.030/596.915 = **0,695**; `COPSTA` = 944.093/1.179.655 = **0,800** (= spec); `COPTOT` (statale+paritarie+IeFP) = 1.078.728/1.179.655 = **0,914**. Esenzione a regime 0,97 (segnaposto dichiarato). File: [modello_costo_docente_C/task_c_modello_costo_docente_teachers.csv](modello_costo_docente_C/task_c_modello_costo_docente_teachers.csv).

### Componenti A (trattenimento) e C (rilascio 13→12) — in DOCENTI, base RDS 0,107
| Regime R | Copertura | ΔDOC_A (trattenim.) | DOC_LIBERATI (leva 13) | **DOC_NETTI** |
|---|---|---|---|---|
| 2032/33 | totale (COPTOT) | +6.043 | 38.906 | **−32.863** |
| 2032/33 | prudente (solo statale) | +18.457 | 38.906 | **−20.449** |
| 2037/38 | totale | +5.099 | 33.905 | **−28.805** |
| 2037/38 | prudente | +15.575 | 33.905 | **−18.329** |

**Lettura:** in tutte le varianti il saldo docenti è **fortemente negativo** (la riforma *libera* ~18–33 mila docenti netti): la compressione 13→12 leve domina largamente il trattenimento dell'obbligo a 18. La Componente A (l'obbligo a 18) è **più che autofinanziata** dalla Componente C.

### Check turnover (base RDS)
- **2032/33:** 38.906 docenti liberati su 3 anni di transizione = 12.969/anno vs **21.322** pensionamenti docenti/anno → rapporto **0,61 → assorbito con margine**. (Contro i soli sec. II 8.536/anno il rapporto è 1,52: serve mobilità tra gradi, che il ciclo unico comunque abilita.)
- **2037/38:** 4.238/anno su 8 anni → rapporto **0,20** → assorbito ampiamente.
- **Conclusione:** il rilascio è assorbito dal turnover fisiologico, **senza licenziamenti**, come atteso.

### Check esterno
1 − COPTOT = **8,6%** fuori da ogni percorso a 16-17, vs non-partecipazione Eurostat media 16-17 **≈5,5%** ed ELET 18-24 **8,2%**. Divergenza **3,1 punti (>3 → segnalata)**: quasi certamente l'assunzione di distribuzione IeFP `/3,5` (spostando iscritti IeFP verso 16-17 la copertura sale e il gap si chiude). Stessa storia qualitativa: ~5–9% realmente fuori.

### Euro (SALDO) — parametrico, in attesa di B.2
`SALDO(R) = DOC_NETTI × CDOC + COSTO_B`. `DOC_NETTI` negativo ⇒ **la parte docenti è un risparmio**. `COSTO_B` (OPEX annua a regime dal run `scenario_docenti_tempo_lungo` − base, segnaposto 400 €/stud) = **2,02 mld €/anno**. Il valore assoluto in euro richiede **CDOC** (B.2, RGS): finché non è sourced non si consegna un numero. Intervalli previsti alla consegna di CDOC: RDS ±10% (0,096–0,118) e CDOC ±12,5%.

---

## Anomalie / da decidere
- **A (calibrazione):** il ~18% del committato non è riproducibile con gli attuali parametri sul dato corretto; la concentrazione è "tutto o niente". Serve un meccanismo graduale se si vuole un target intermedio. Trade-off costo↔presidio esplicito in tabella.
- **B.2 CDOC** manca (RGS non automatizzabile): è l'unico blocco per il SALDO in euro.
- **C:** risultato robusto e CDOC-indipendente in docenti — la riforma libera docenti netti e il turnover assorbe; l'obbligo a 18 si autofinanzia. Da promuovere: Componente B (400 €/stud → ore/cattedre reali) e distribuzione IeFP per età.
