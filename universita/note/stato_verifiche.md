# Stato verifiche fonti-primarie — workstream Università ORA

Tracker vivo dei flag **[C]** del report `docs/Universita_e_Ricerca_ORA_v1.md`, secondo il protocollo di quarantena delle istruzioni di brother: ogni [C] va promosso a **[V]** solo su fonte primaria; un [C] che *contraddice* un numero già nel report richiede tre stress test indipendenti e una issue (correzione applicata in v2 dopo review di Pietro, non direttamente nel report).

Convenzione file: dati verificati in `analisi/<data>_.../data/*.csv` con fonte/anno per riga; PDF fonti in `sources/` (naming `AAAA_ente_titolo.pdf`).

## Stato (aggiornato 2026-07-18)

| ID | Oggetto | Stato | Valore verificato | Fonte |
|---|---|---|---|---|
| B6 | Spesa pubblica terziaria % PIL | **[V]** | IT **0,4%** vs EU27 **0,8%** (2023-24); il "0,3" era altro perimetro | Eurostat `gov_10a_exp` COFOG GF0904, S13/TE, PC_GDP → `analisi/2026-07-18_verifiche_fonti/data/b6_spesa_terziaria_cofog.csv` |
| F1 | Attainment terziario 25-34 | **[V]** | IT 30,6% / EU 43,1% (2023, = report); ultimo 2025: IT 31,1% / EU 44,8% | Eurostat `edat_lfse_03` ED5-8 → `.../data/f1_attainment_25_34.csv` |
| B1 | Legge Bernini reclutamento (AC 2735) | [C] | testo definitivo in attesa di GU; mappa modifiche L.240/2010 da fare | Gazzetta Ufficiale (da scaricare) |
| B2 | PTR/FPR perimetro 259 vs 409M | **[V]** | 259 = FPR base; 409 = base + 150M incremento PRIN (c.533 L.199/2025); linee dentro il 409. Baseline F4 IT 2026 = 0,41 mld; regime 0,67 (665,9M) | DM 150/2026 → `.../data/b2_fpr_perimetro.csv`, `sources/2026_MUR_DM150_PTR.pdf` |
| B3 | FIS budget/schema + esiti | **[V] parz.** | budget/schema [V]: Starting 40/48,5/**50%** → critica "riparto penalizza i giovani" è **FALSA**; successo FIS1 2,46% / FIS2 4,63%; FIS2=338M (DD 1236/2023). FIS3 esiti+revoche da graduatorie [C] | `.../b3_fis_esiti_nota.md` |
| B4 | FFO composizione, % premiale, serie reale | **[V]** | premiale = 2,5 mld = **30,2%** del distribuito (il "23%" NON supportato); serie 2019-25: reale 2025 (7,96 mld base 2019) **sotto il picco 2021-23** nonostante il massimo nominale → claim "riduzioni reali 2024-25" confermato (defl. PIL e HICP) | DM 595/2025 + serie → `.../b4_ffo_serie_nota.md`, `data/b4_ffo_serie.csv`, `figures/f2_ffo_reale.png` |
| B5 | Gini premiale vs base | **⚠ CONTRADDIZIONE** (3 stress test) | Gini premiale **0,471** > base **0,450**: il claim "a pioggia / premiale<base" (report §1.1) è FALSO sul 2025. Argomento v2 (arbitrato): **corr(premiale, quota base) = 0,9929** (ricontrollato su TUTTI i 68 atenei, base esclude la premiale; invariato vs 0,993) + banda 19-34% dell'FFO, CV 0,10 | DM 595/2025 TAB1 → `.../b4b5_ffo_gini_nota.md` |
| B7 | N. atenei statali | **[V]** | ~**67** università statali (di cui alcune scuole a ordinamento speciale); TAB1 DM595 = 68 righe FFO (coerente). 57/66 dei vecchi PP erano perimetri datati | USTAT + coerenza TAB1 → `.../b7_atenei_e_figure_nota.md` |
| B8 | Cons. Stato 3043/2016 e 8516/2024 | **[V]** | 8516/2024 (sez VII): illegittimo subordinare la Commissione al Consiglio di Dip. (riformulare "terne" §4.1). 3043/2016 (**sez VI**, 11/7/2016): nozione funzionale di ente pubblico → conferma §2.3/§9 | `.../b8_b12_giuridiche_nota.md`, `.../b7_atenei_e_figure_nota.md` |
| B9 | Piano straordinario ricercatori LdB 2026 | **[V]** | L.199/2025 art.1 **commi 305-315** (c.307: 11,3M dal 2026 + 38,7M dal 2027 = 50M); cofin 50%, PA 0,2 po; ~1.600 posti; DM 193/2026. Flag: "0,45 po" del report non riscontrato | `.../b9_piano_straordinario_nota.md` |
| B10 | Semestre filtro medicina | **[V]** | confermati: ~54.300 iscritti / **22.700** (tutti e 3 esami) / 17.278 posti; dichiarare def. "idonei". DM 1115/2025 | MUR esiti dic.2025 → `.../b10_semestre_filtro_nota.md` |
| B11 | Contribuzione + scenari gratuità | **[V] parz.** | esonerati **38,0%** (2022/23) e gettito **~1,5 mld** confermati; tetto 20% FFO (DPR 306/97) [V]. Gratuità: **0,9-1,5 mld** (flat 500/200/0€ su ~1,20M in-corso statali) → rivede il "1,5-2 mld [C]" del §8 verso il basso. Iscritti in-corso statali esatti [C] | USTAT Focus 2022/23 + ANS → `.../b11_contribuzione_nota.md` |
| B12 | RTT passaggio PA: 3° o 4° anno | **[V]** | art.24 c.5 L.240/2010: **TERZO anno** (post L.79/2022: dal 3° e successivi); c.5-bis anticipo dopo il 1° con prova didattica. Report "quarto"→**terzo** | `.../b8_b12_giuridiche_nota.md` |
| F4 | Bandi competitivi IT vs DFG/ANR/SNSF/NWO/UKRI | **[V]** | budget agenzie verificati; gap "4-6x" difendibile ma conservativo (a regime, per ab., vs DE); fino a ~10x vs CH/NL | report agenzie (DFG/ANR/SNSF/NWO/UKRI) → `analisi/2026-07-18_verifiche_fonti/data/f4_bandi_competitivi_confronto.csv` + `f4_..._nota.md` |
| F2 | FFO reale 2019-25 | **[V]** | figura resa | `.../figures/f2_ffo_reale.png` (+ `.py`) |
| F3,F5,F6 | Figure premiale / successo FIS / precariato | **[V]** (F5 parz.) | F3 scatter premiale/FFO [V]; F5 FIS 2,46/4,63% vs **ERC CoG 14,2%** [ancorato] (FIS3 in corso); F6 RTD 4,1%→11,2% (ANVUR) | `figures/f3_*,f5_*,f6_*.png` |
| D | Tabella costi §8 | **[V parz.]** | assemblata: baseline bandi 0,41 (B2), gratuità **1,2-1,3** (B11, era 1,5-2), spesa terziaria gap ~8,8 mld (B6); totale ~12-14. NO coperture (R-Z1) | `.../data/tabella_costi.csv` |

## Prossimi passi (ordine E delle istruzioni)
Bloccanti: **B1, B2, B4** (richiedono download PDF decreti + parsing tabelle). Poi **B5, B6→fatto** e figure chiave **F4** (bandi competitivi IT vs DFG/ANR/SNSF/NWO/UKRI, gap 4-6x). Le verifiche Eurostat/API sono immediate; quelle su GU/decreti/USTAT richiedono fetch+parsing di PDF (fattibile ma più lento) — da fare a lotti.
