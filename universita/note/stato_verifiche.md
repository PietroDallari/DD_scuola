# Stato verifiche fonti-primarie — workstream Università ORA

Tracker vivo dei flag **[C]** del report `docs/Universita_e_Ricerca_ORA_v1.md`, secondo il protocollo di quarantena delle istruzioni di brother: ogni [C] va promosso a **[V]** solo su fonte primaria; un [C] che *contraddice* un numero già nel report richiede tre stress test indipendenti e una issue (correzione applicata in v2 dopo review di Pietro, non direttamente nel report).

Convenzione file: dati verificati in `analisi/<data>_.../data/*.csv` con fonte/anno per riga; PDF fonti in `sources/` (naming `AAAA_ente_titolo.pdf`).

## Stato (aggiornato 2026-07-18)

| ID | Oggetto | Stato | Valore verificato | Fonte |
|---|---|---|---|---|
| B6 | Spesa pubblica terziaria % PIL | **[V]** | IT **0,4%** vs EU27 **0,8%** (2023-24); il "0,3" era altro perimetro | Eurostat `gov_10a_exp` COFOG GF0904, S13/TE, PC_GDP → `analisi/2026-07-18_verifiche_fonti/data/b6_spesa_terziaria_cofog.csv` |
| F1 | Attainment terziario 25-34 | **[V]** | IT 30,6% / EU 43,1% (2023, = report); ultimo 2025: IT 31,1% / EU 44,8% | Eurostat `edat_lfse_03` ED5-8 → `.../data/f1_attainment_25_34.csv` |
| B1 | Legge Bernini reclutamento (AC 2735) | [C] | testo definitivo in attesa di GU; mappa modifiche L.240/2010 da fare | Gazzetta Ufficiale (da scaricare) |
| B2 | PTR 2026-28 / FPR (perimetro 259 vs 409M) | [C] | — | DM 150/2026 (PDF mur.gov.it) |
| B3 | Serie FIS (FIS2 importo; esiti FIS3) | [C] | FIS1 50M, FIS3 475M [V da report]; FIS2 330M da confermare | DD istitutivi; graduatorie fis-submission.mur.gov.it |
| B4 | FFO serie storica reale + % premiale | [C] | FFO 2025 = 9,4 mld [V]; serie 2019-25 e premiale da tabelle | DM 595/2025 + allegati (PDF) |
| B5 | Gini quota premiale vs base | [C] | ricalcolo diretto da tabelle DM 595/2025 | dipende da B4 |
| B7 | N. atenei statali (57/66/67) | [C] | — | USTAT/MUR anagrafe |
| B8 | Cons. Stato 3043/2016 e 8516/2024 | [C] | estremi da verificare + testi | giustizia-amministrativa.it |
| B9 | Piano straordinario ricercatori LdB 2026 | [C] | ~50M/2 anni, comma esatti | Legge di Bilancio 2026 |
| B10 | Semestre filtro medicina (numeri 1° ciclo) | [C] | ~54.300 / 22.700 / 17.278 posti da fonte MUR | L.26/2025, D.Lgs.71/2025, DM 941/2026, Universitaly |
| B11 | Contribuzione (gettito 1,5 mld; esonerati 37,8%) | [C] | + tetto 20% FFO (DPR 306/97) e no tax area | USTAT focus contribuzione |
| B12 | RTT anticipo passaggio PA (3° o 4° anno) | [C] | testo vigente art.24 L.240/2010 + modifica Bernini | Normattiva |
| F4 | Bandi competitivi IT vs DFG/ANR/SNSF/NWO/UKRI | **[V]** | budget agenzie verificati; gap "4-6x" difendibile ma conservativo (a regime, per ab., vs DE); fino a ~10x vs CH/NL | report agenzie (DFG/ANR/SNSF/NWO/UKRI) → `analisi/2026-07-18_verifiche_fonti/data/f4_bandi_competitivi_confronto.csv` + `f4_..._nota.md` |
| F2,F3,F5,F6 | Figure (FFO reale, Gini, successo FIS, precariato) | [C] | dipendono da B3/B4/B5 + ANVUR/USTAT | — |
| D | Tabella costi §8 | [C] | dopo B4/B6/B11; NO coperture (→ fiscal framework) | — |

## Prossimi passi (ordine E delle istruzioni)
Bloccanti: **B1, B2, B4** (richiedono download PDF decreti + parsing tabelle). Poi **B5, B6→fatto** e figure chiave **F4** (bandi competitivi IT vs DFG/ANR/SNSF/NWO/UKRI, gap 4-6x). Le verifiche Eurostat/API sono immediate; quelle su GU/decreti/USTAT richiedono fetch+parsing di PDF (fattibile ma più lento) — da fare a lotti.
