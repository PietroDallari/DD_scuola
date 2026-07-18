# Handoff fine lotto 2 — verifiche università (per la v2)

**Data:** 2026-07-18. Tutte le verifiche su fonte primaria; PDF in `../../sources/`, dati in `data/`, figure in `figures/`, dettagli nelle note `b*_nota.md`. Tracker vivo: `../../note/stato_verifiche.md`.

## 1. Esito per task (una riga)
| Task | Esito |
|---|---|
| B2 (FPR) | **Confermato**: 259=base, 409=base+150 PRIN; baseline bandi 0,41 mld, regime 0,67 |
| B3 (FIS) | **Corretto/additivo**: Starting ~50% (no "anti-giovani"); tassi 2,46%/4,63%; FIS2=338M; FIS3 esiti [C] |
| B4 (FFO) | **Corretto**: premiale 30,2% (non 23%); serie reale 2025 < picco 2021-23; riclassifiche 693,5M [V] |
| B5 (Gini) | **Contraddizione risolta**: Gini premiale>base; sostituito con corr(premiale,base)=0,99 |
| B6 (spesa terz.) | **Corretto**: 0,4% (non 0,3-0,4) vs 0,8% UE |
| B7 (atenei) | **Confermato**: ~67 statali |
| B8 (Cons. Stato) | **Confermato con riformulazione**: 8516/2024 (no "terne"), 3043/2016 (sez VI) |
| B9 (piano straord.) | **Corretto**: L.199/2025 c.305-315; 50M/anno, ~1.600 posti |
| B10 (medicina) | **Confermato**: 54.300/22.700/17.278 |
| B11 (contribuzione) | **Corretto**: esonerati 38,0%; gratuità 1,2-1,3 mld (non 1,5-2) |
| B12 (RTT) | **Corretto**: terzo anno (non quarto) |
| F1 (attainment) | **Confermato**: IT 30,6% / EU 43,1% (2023) |
| F2 (FFO reale) | **Resa** (+ritocchi) |
| F3 (premiale/FFO) | **Resa** (sostituisce Gini) |
| F4 (bandi vs EU) | **Confermato conservativo**: gap 4-6x a regime vs DE, fino a ~10x |
| F5 (successo FIS) | **Resa parz.** (FIS1/2 + ERC 14,2%; FIS3 in corso) |
| F6 (precariato) | **Resa**: RTD 4,1%→11,2% |
| D (tabella costi) | **Assemblata**: totale ~12-14; no coperture |
| B1 (Bernini) | **Bloccato**: attesa GU |

## 2. Numeri da cambiare nel report v1 (vecchio → nuovo, fonte)
1. **§1.1 spesa terziaria** — "0,3–0,4%" → **0,4%** (UE 0,8%). *Eurostat COFOG GF0904.* [B6]
2. **§1.1 premiale** — "≈30% nominale ma effettivo poco selettivo / 23%" → **30,2%** del distribuito (26,6% del totale 9,4 mld). *DM 595/2025 TAB1.* [B4]
3. **§1.1 Gini** — "concentrazione premiale < quota base / a pioggia" → **corr(premiale, quota base) = 0,99; premiale in banda 19–34% dell'FFO di ateneo**. *DM 595/2025, ns. elaborazione (3 stress test).* [B5]
4. **§1.1 FFO** — rafforzare: **"massimo nominale di sempre (9,37 mld 2025) ma in termini reali sotto il livello 2021-23"** (deflatore PIL+HICP); **693,5M** consolidati in quota base 2025 [ns. V]; lettura "a perimetro costante calo anche nominale" = inciso ADI [C]. [T3]
5. **§1.3 piano straordinario** — "circa 50M in due anni [C: estremi]" → **50M/anno a regime (11,3 dal 2026 + 38,7 dal 2027), L. 199/2025 art.1 c.305-315; ~1.600 posizioni RTT su >30.000 precari** (sproporzione in *posti*). [B9] *(il "0,45 punti organico" è riconciliato, non entra.)*
6. **§1.3 precariato** — "quasi triplicata dal 2008" → ancorare: **RTD 4,1% (2012) → 11,2% (2022), ANVUR** (perimetro: docenti di ruolo); dichiarare la base 2012. [F6]
7. **§1.4 e §5.1 esonerati** — "37,8% (2022)" → **38,0% (a.a. 2022/23)** ovunque, anno dichiarato. *USTAT Focus.* [B11]
8. **§1.4/5.4 medicina** — togliere [C]; **~54.300 iscritti / ~22.700 con tutti e tre gli esami / 17.278 posti** (DM 1115/2025); dichiarare la definizione di "idonei". [B10]
9. **§2.2 atenei** — "67 istituzioni statali [C]" → **~67 università statali** (di cui alcune scuole a ordinamento speciale). [B7]
10. **§2.3 e §9 Cons. Stato 3043/2016** — [C] → **[V] Sez. VI, 11/07/2016** (nozione funzionale di ente pubblico). [B8]
11. **§3.2 baseline bandi** — "259M FPR / 409M linee [C]" → **409M = 259 base + 150 incremento PRIN (c.533 L.199/2025); "Italia oggi ≈ 0,41 mld"; a regime 0,67 mld dal 2029**. [B2]
12. **§3.2 gap bandi** — "4-6x" → **"4-6x a regime, per abitante, vs Germania; fino a ~10x vs i migliori sistemi piccoli (CH/NL)"** (UKRI fuori perimetro). [F4]
13. **§3.2 FIS** — **additivo, nessuna rimozione**: aggiungere **"tassi di successo 2,46% (FIS1) e 4,63% (FIS2) contro il 14,2% dell'ERC Consolidator 2024"**; FIS2 "oltre 330M" → **338M**. [B3/F5]
14. **§4.1 Cons. Stato 8516/2024** — riformulare togliendo "terne di idonei": *"illegittimo il regolamento che sottrae alla Commissione la valutazione per assegnarla al Consiglio di Dipartimento"*. [B8]
15. **§4 (nota storica) RTT** — "dal quarto anno" → **dal terzo anno** (c.5; anticipo dopo il primo, c.5-bis). [B12]
16. **§8 gratuità** — "~1,5–2 mld [C]" → **"~1,2–1,3 mld (contributo flat 200€; intervallo 0,9–1,5 secondo il livello) [V parz.]"** + caveat statico (una riga): non modella il ricavo dell'addizionale fuoricorso (↓ costo) né l'aumento di iscrizioni indotto dalla gratuità (↑ costo a valle su FFO/DSU) — quest'ultimo è l'obiettivo, da rivendicare come successo atteso a costo dichiarato. [B11]
17. **§8 tabella costi** — baseline bandi 0,41 (B2), gap spesa terziaria ~8,8 mld (B6): **totale ~12–14 mld confermato**; nessuna copertura (R-Z1). [D]

## 3. Ancora aperto
- **B1 (legge Bernini):** attesa pubblicazione in GU → mappa modifiche L.240/2010 + 3 domande (platea sorteggio, profilatura bandi, transitorio).
- **F5/FIS3:** domande/finanziati per macrosettore (DD 18008/18010/18169) + conteggio revoche 2026 (a parte).
- **Minori [C]:** gettito contribuzione statali all'euro + iscritti in-corso *statali* esatti; scelta editoriale flat (registrata: 200€).
