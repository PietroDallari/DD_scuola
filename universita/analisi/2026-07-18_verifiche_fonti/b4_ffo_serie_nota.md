# B4 (T3, completamento) — FFO 2019-2025: serie nominale e reale

Completa il B4 (composizione/premiale già in `b4b5_ffo_gini_nota.md`). Dati: `data/b4_ffo_serie.csv`; figura `figures/f2_ffo_reale.png` (script `f2_ffo_reale.py`).

## Serie (miliardi €, base 2019)
| Anno | Nominale | Defl. PIL (2019=100) | **Reale (PIL)** | HICP (check) | Reale (HICP) | Decreto |
|---|---|---|---|---|---|---|
| 2019 | 7,43 | 100,0 | 7,43 | 100,0 | 7,43 | — |
| 2020 | 7,88 | 101,6 | 7,75 | 99,8 | 7,89 | DM riparto 2020 |
| 2021 | 8,38 | 102,9 | **8,15** | 101,7 | 8,24 | DM 1059/2021 |
| 2022 | 8,66 | 106,4 | 8,13 | 110,7 | 7,82 | DM 581/2022 |
| 2023 | 9,21 | 113,1 | 8,14 | 117,2 | 7,86 | DM 809/2023 |
| 2024 | 9,03 | 115,3 | **7,83** | 118,5 | 7,62 | DM 1170/2024 |
| 2025 | 9,37 | 117,6 | **7,96** | 120,4 | 7,78 | DM 595/2025 |

Deflatore PIL: Eurostat `nama_10_gdp` (nominale/volume concatenato). HICP: Eurostat `prc_hicp_aind`.

## Esito [V] — claim §1.1 "riduzioni reali 2024-25" confermato
In **termini reali** l'FFO cresce fino al picco 2021 (8,15), resta piatto 2021-2023 (~8,14), **cade nel 2024 (7,83, −3,8% reale)** e recupera solo parzialmente nel 2025 (7,96). **Il 2025, massimo storico nominale (9,37 mld), in termini reali resta SOTTO il livello 2021-2023.** L'HICP (che incorpora lo shock energetico 2022) dà un quadro anche peggiore (reale 2025 = 7,78, sotto il 2021). → il report §1.1 è supportato da entrambi i deflatori.

**Riclassifiche in quota base 2025 — verificato direttamente sul decreto [V].** Sommando le sotto-colonne "consolidamento" della quota base nel DM 595 TAB1 (nostra elaborazione): consolidamento scatti stipendiali **150,0M** + consolidamento risorse TA **50,0M** + consolidamento piani straordinari conclusi (residui reclutamento) **493,5M** = **693,5M** consolidati nella quota base 2025. Coerente (anzi leggermente superiore) con i ~671M dell'analisi ADI, ma ora è **nostra elaborazione su fonte primaria** [V]. Questo gonfia la crescita *apparente* della quota base 2025.
La lettura ADI per cui, *a perimetro costante, il 2025 sarebbe in calo anche nominale* è un passo ulteriore (richiede il diff composizione 2024 vs 2025 sui rispettivi decreti): resta **inciso attribuito ad ADI [C]**, non promosso. Il claim principale (reale 2025 < picco 2021-23) regge da solo.

## Caveat di perimetro (dichiarato)
I totali nominali annui hanno rumore di perimetro (con/senza vincolo di destinazione, riparti successivi, riclassifiche): il livello ha incertezza di ±0,1-0,3 mld tra fonti. La **conclusione qualitativa** (reale 2025 < picco 2021-2023) è **robusta a entrambi i deflatori** e al rumore. Per la v2 basta il messaggio in termini reali; se serve la serie all'euro, i totali vanno presi uno per uno dai singoli DM (link nel CSV).

**Confronto "programmato LdB 2022 vs effettivo"**: non ricostruito all'euro (richiederebbe la tabella di programmazione L.234/2021 per anno); l'ADI documenta lo scostamento — usabile come check secondario, non promosso a [V] qui.
