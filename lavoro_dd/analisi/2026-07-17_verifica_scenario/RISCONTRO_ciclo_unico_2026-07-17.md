# Riscontro — Ciclo Unico, verifica scenario + sensibilità + dati per modello obbligo-18

**Data lavoro:** 2026-07-17 · **Esecutore:** Claude (analytical) · **Regola rispettata:** nessun file/codice di Nazareno modificato (repo pinned pulito, `git status` clean, `config/variabili_scenario.py` pristine). Tutto prodotto via driver esterno che *importa* le sue funzioni e passa dati/parametri corretti.

---

## 0. Commit verificato
- **Hash:** `a9edf41706edd7a20c818c3ffed61d142ab27822`
- **Data commit:** Sat 4 Jul 2026 00:05 +0200
- L'output committato in `output/simulazioni/scenario_base/` è il run di questo pin.

## 1. Task A — verifica scenario base (file target `spesa_riepilogo_realistico.csv`)
| Campo | Valore committato |
|---|---|
| SPESA_LORDA_BASE_EUR | 36.823.844.889 |
| SPESA_NETTA_BASE_EUR | 35.975.489.589 |
| SPESA_LORDA_MAX_EUR | 50.643.098.637 |
| ORIZZONTE_ANALISI_ANNI | 4 (auto; config = 0) |
| ORIZZONTE_PRUDENTE_ANNI | 9 (regime 2037/2038) |

**Esito:** l'atteso ~36,7/35,8 è confermato in ordine di grandezza. **Nota:** esistono TRE "base" nell'output committato:
- `spesa_riepilogo.csv` (timeline da config): 37,87 / 37,02 mld
- `scenario_sintesi.md` (report): 36,57 / 35,73 mld
- `spesa_riepilogo_realistico.csv` (timeline OpenCoesione): 36,82 / 35,98 mld ← file target

**Anomalia A1:** `scenario_sintesi.md` non coincide con nessuno dei due CSV (250 M di scarto dal realistico): sembra generato da un run diverso/precedente rispetto ai CSV committati. Da confermare con Nazareno.

## 2. ANOMALIA CRITICA — POSAS duplicato ×4 (impatta il modello)
`estrai_popolazione_posas_zip` (download_utils.py:404) itera su *tutti* i CSV dentro lo zip ISTAT (4 file nazionali) e li concatena → **ogni riga (comune, età) compare 4 volte identica**.
- `popolazione_eta_comune_2026.csv` e `popolazione_bacino_11_18_2026.csv` sommano a **17,87 M** per 11–18; il vero è **4,47 M** (×4).
- La colonna finisce in `edifici_base.csv` come `POP_ISTAT_ETA_CICLO_UNICO` (build_utils.py:103); es. Roma = 834.024 = 4 × 208.506 (vero). Fattore ×4 **uniforme** su tutti i comuni → correzione esatta = ÷4.
- Propagazione: `domanda_istat_bacino` (riordino_utils.py:120) somma quel valore → `sedi_target = ceil(domanda/riferimento)` risulta ~4× troppo alto → il vincolo di concentrazione non segnala sedi in eccesso e le soglie di domanda (120) si superano troppo facilmente → **il modello sotto-chiude le sedi**.

### Impatto quantificato (rerun con dato corretto, ÷4)
Controllo di fedeltà: il driver sul dato **originale (gonfiato)** riproduce all'euro il committato (36.823.844.889 / 35.975.489.589; chiudere 3001 / da_valutare 3109 / tenere 10660). Quindi l'unica variabile è il ÷4.

| Metrica | Committato (buggy ×4) | Corretto (dedup ÷4) | Δ |
|---|---|---|---|
| Spesa lorda base (4 anni) | 36,82 mld | **25,19 mld** | −11,63 (−32%) |
| Spesa netta base (4 anni) | 35,98 mld | **22,00 mld** | −13,98 (−39%) |
| Spesa lorda MAX | 50,64 mld | **34,62 mld** | −16,02 |
| Risparmi chiusure | 0,85 mld | **3,20 mld** | ×3,8 |
| Sedi: chiudere | 3.001 | **8.367** | +5.366 |
| Sedi: da_valutare | 3.109 | **912** | −2.197 |
| Sedi: tenere_aperte | 10.660 | **7.491** | −3.169 |

**Lettura:** con la domanda corretta, molte più sedi piccole/eccedenti scendono sotto soglia → escono dal perimetro d'investimento (meno CAPEX) e generano più risparmio immobiliare. Il titolo pubblicato (~36,7 mld) è costruito su domanda gonfiata ×4.

**Attenzione (A2):** 8.367 chiusure sono >50% delle sedi medie-superiori: verosimilmente le soglie (`soglia_domanda_minima_chiusura`=120, vincolo concentrazione, `studenti_minimi_sede_riferimento_superiori`=250) andrebbero **ricalibrate** ora che la domanda è ~4× più piccola — erano di fatto tarate contro un bacino gonfiato. Decisione di scenario, non di dato.

**Fix definitivo (per Nazareno/console brother):** in `estrai_popolazione_posas_zip` leggere un solo CSV per (comune,età) o deduplicare, oppure filtrare la dimensione ripetuta nello zip ISTAT. Finché non è patchato a monte, ogni run va corretto ÷4.

## 3. Task C — sensibilità (su dato CORRETTO / dedup)
Base corretta (4 anni): **lordo 25,19 / netto 22,00 mld**. Esiti sedi identici in tutti i run (i 3 parametri non toccano la logica di chiusura).

| Scenario | Parametro | Lordo base (4a) | Netto base (4a) | Netto @9 anni |
|---|---|---|---|---|
| base_dedup | — | 25,19 | 22,00 | 28,30 |
| **orizzonte_9** | `orizzonte_analisi_anni=9` | 25,19* | 22,00* | **28,30** |
| **contingenza_25** | `quota_contingenza=0.25` | **26,89** | **23,70** | 30,00 |
| **docenti_tempo_lungo** | `includi_docenti_extra=True`, `400 €/stud/anno` | **29,23** | **26,03** | 42,43 |

*(**Anomalia A3**, attesa) `spesa_riepilogo_realistico.csv` usa un orizzonte auto derivato dalla timeline realistica, non `orizzonte_analisi_anni`: quindi il riepilogo realistico di orizzonte_9 = base. L'effetto 9 anni è nel file `spesa_confronto_orizzonti_realistico.csv` (riga 9 anni = netto 28,30 / lordo 36,82 mld). Il ×400 €/stud/anno è un **segnaposto** nostro, non sourced.

## 4. Task D — dati per il modello "costo docente obbligo a 18"
- **`posas_nazionale_eta_0_19.csv`** — ISTAT Demo POSAS, anno **2026**, popolazione residente per età singola 0–19, nazionale, **deduplicata** (÷ righe ×4). Totale 0–19 = 9.778.643. (Coorti 16/17 = 579.896 / 588.694.)
- **`posas_nazionale_eta_11_18_DEDUP.csv`** — stesso dato, sottoinsieme 11–18 (totale 4.467.855) per confronto diretto col bacino del modello.
- **`mim_studenti_superiori_per_anno_corso.csv`** — MIM `ALUCORSOETASTA` a.s. **2024/25**, SCUOLA SECONDARIA II GRADO, alunni per anno di corso: I 553.734 · II 513.675 · III 502.164 · IV 480.553 · V 456.022 (+282 corso 6 residuale) = 2.506.430.
- **`mim_studenti_superiori_per_anno_corso_eta.csv`** — stesso, dettagliato per FASCIAETA (per il confronto coorte-per-età).
- **Task D3 (candidati esterni/abbandoni/frequenza):** NON presenti nei dataset MIM scaricati (ALUCORSOETA ha solo scuola/corso/età/alunni). Per la dispersione useremo fonti pubblicate (ISTAT/MIM/Eurostat ELET) citate da noi.

## 5. File consegnati
**pacchetto 1** `tabelle_scenario_base.zip` (0,20 MB) — 13 tabelle come da Task B (nessuno split necessario).
**Task C** (8 file): `spesa_riepilogo_realistico__<scenario>.csv` + `spesa_confronto_orizzonti_realistico__<scenario>.csv` per i 4 scenari (base_dedup + 3).
**pacchetto 2 (dati modello):** `posas_nazionale_eta_0_19.csv`, `posas_nazionale_eta_11_18_DEDUP.csv`, `mim_studenti_superiori_per_anno_corso.csv`, `mim_studenti_superiori_per_anno_corso_eta.csv`.

## 6. Anomalie in sintesi
- **A0 (critica):** POSAS ×4 → modello sotto-chiude; totali corretti molto più bassi (25,2/22,0 vs 36,8/36,0). Serve patch a monte + ricalibrare le soglie di chiusura.
- **A1:** `scenario_sintesi.md` non coincide coi CSV committati (run disallineato).
- **A2:** con dato corretto le chiusure salgono a 8.367 (>50%): soglie da rivedere.
- **A3:** orizzonte_analisi_anni non muove il riepilogo realistico (usa orizzonte auto della timeline).
