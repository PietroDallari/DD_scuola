# B4/B5 — FFO 2025: composizione, % premiale, Gini per componente

Fonte primaria: **DM 595 del 07/08/2025**, TABELLA 1 "quadro generale" (per-ateneo), scaricata in `../../sources/DM595_TAB1_quadro_generale.pdf` (+ TAB 2/3/4). Parsing con pdfplumber. Dati: `data/b4b5_ffo2025_per_ateneo.csv` (68 atenei statali) e `data/b5_gini_stress.csv`.

## B4 — Composizione FFO 2025 e quota premiale [V]
Prima ripartizione (8,28 mld distribuiti; ulteriori 1,1 mld ripartiti dopo → **9,4 mld totali [V]**):

| Componente | € | % del distribuito |
|---|---|---|
| Quota base | 4.845.086.674 | 58,5% |
| **Quota premiale** | **2.500.000.000** | **30,2%** |
| Perequativo | 141.000.000 | 1,7% |
| Piani straordinari | 648.103.894 | 7,8% |
| **FFO 2025 (I riparto)** | **8.284.190.568** | (2024: 8.044.203.136, +3,0% nom.) |

**Esito:** la quota premiale è **€2,5 mld = 30,2%** del FFO distribuito (26,6% del totale 9,4 mld). Conferma il **30% nominale**; **la "23% effettivo" citata nel report (§1.1, da PP Finanziamento) NON è supportata** dai dati DM 595/2025. → flag correzione v2: usare 30% (o 26,6% sul totale), non 23%.

*(Serie reale 2019-2024 con deflatore ISTAT: da completare — servono i totali FFO dei singoli anni; qui abbiamo solo 2024→2025 = +3,0% nominale.)*

## B5 — Gini per componente: **CONTRADDIZIONE con il report** (3 stress test)
Il report §1.1 afferma: *"l'indice di concentrazione della componente premiale risulta inferiore a quello della quota base … distribuisce a pioggia"* [C] (claim Boeri-Perotti via lavoce.info). **Ricalcolo diretto dalle tabelle: il contrario.**

| Componente | Gini (sort) | Gini (MAD) |
|---|---|---|
| Quota base (costo std 36%) | 0,413 | 0,413 |
| Quota base (totale) | 0,450 | 0,450 |
| **Quota premiale** | **0,471** | **0,471** |
| FFO totale | 0,456 | 0,456 |

La premiale è **più** concentrata della base (0,471 > 0,450), non meno.

**Protocollo di quarantena — 3 stress test indipendenti (tutti confermano la contraddizione):**
1. **Due stimatori Gini** (ordinamento vs differenza media assoluta): identici → non è artefatto di calcolo.
2. **Tre definizioni di base** (costo standard 0,413; base totale 0,450; base+integrazione 0,450): la premiale (0,471) è più concentrata di **tutte**.
3. **Test diretto "a pioggia":** corr(premiale, FFO) = **0,997**, corr(premiale, base) = 0,993 → la premiale segue quasi perfettamente la dimensione dell'ateneo; ma il rapporto premiale/FFO varia in banda 18,6–34,2% (media 29,4%, CV 0,10).

**Conclusione (per issue, non per edit diretto):** il claim specifico "Gini premiale < Gini base / a pioggia" **è falso sui dati 2025**. Verosimile origine: dato Boeri-Perotti su annata precedente (premiale allora ~18-20% e criteri diversi) o normalizzazione differente. **Il punto sostanziale resta ma va riformulato:** la premiale *segue quasi perfettamente la dimensione* (r=0,997) e differenzia solo entro una banda stretta (19-34% dell'FFO di ateneo) → **poco selettiva**, ma non "meno concentrata della base". Proposta v2: sostituire l'argomento-Gini con l'argomento-correlazione ("la premiale replica la ripartizione per dimensione: r=0,99 con l'FFO, banda 19-34%"), più forte perché è nostra elaborazione su fonte primaria.

**Da decidere (Pietro):** applicare la riformulazione B4 (23%→30%) e B5 (Gini→correlazione) in v2.
