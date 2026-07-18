# Simulazione premiale al 50% (§2.1) — ISSUE con 3 stress test

**Contesto:** §2.1 del report propone di portare la quota premiale dell'FFO dal 30% al 50%, e afferma — riprendendo la simulazione del PP Finanziamento su dati 2022 — che *"tra i beneficiari netti figurano grandi atenei del Mezzogiorno e delle isole, mentre alcuni atenei settentrionali perderebbero risorse … la riforma non è una redistribuzione Nord-Sud"* [C: rifare sui dati DM 595/2025]. **Verifica su dati 2025: il claim non regge.**

**Metodo (statico, criteri invariati):** dal per-ateneo del DM 595/2025 (TAB1), si porta la premiale nazionale al 50% dell'FFO e si riduce simmetricamente la base (perequativo e piani straordinari invariati). Ogni ateneo mantiene la propria quota *dentro* la premiale (VQR-driven) e *dentro* la base (costo standard); i pool nazionali vengono riscalati (base ×0,692, premiale ×1,657). `delta_i = 0,657·premiale_i − 0,308·base_i`. Dati: `data/sim_premiale50_delta_per_ateneo.csv`.

## Risultato — a livello di macro-area il Sud perde
| Macro-area | Δ (M€) | Δ % del suo FFO |
|---|---|---|
| **Nord** | **+15,4** | **+0,42%** |
| Centro | −1,1 | −0,05% |
| **Sud** | **−13,1** | **−0,74%** |
| Isole | −1,2 | −0,16% |

È una redistribuzione **verso il Nord**, non "dalla rendita alla qualità ovunque" in senso geograficamente neutro. Meccanismo intuitivo: la premiale è VQR/merito, e la premiale-intensità media è più alta negli atenei di ricerca del Centro-Nord.

## I "grandi atenei del Sud/isole" — vince solo una minoranza
Napoli Federico II **+8,0M (+2,0%)**, Cagliari +2,3M, Messina +0,8M **vincono**; ma **Bari −1,4M, Palermo −3,2M, Catania −2,9M, Salerno −1,6M, Vanvitelli −1,3M perdono**. Tra i 7 grandi atenei Sud/isole (FFO>140M), **vincono 2** (Federico II, Messina).

## Tre stress test (protocollo di quarantena) — tutti confermano
1. **Premiale 40% (tappa intermedia):** Nord +0,19% / Sud −0,34% / Isole −0,05% — stessa direzione, monotòna.
2. **Escludendo scuole speciali/piccole** (Normale, Sant'Anna, SSM2, GSSI, IUSS, SISSA, IMT, Foro Italico, Stranieri, Trento): Nord +0,32% / Sud −0,52% / Isole −0,41% — non è un artefatto degli outlier.
3. **Conteggio vincitori:** Nord 11/24, Centro 8/19, Sud 6/20, Isole 3/5; grandi Sud/isole 2/7.

→ Contraddizione **confermata e robusta**: il claim "Sud tra i beneficiari netti" è falso sul 2025.

## Riformulazione proposta per la v2 (§2.1) — non rimozione, ma verità difendibile
Il punto politico va tenuto ma reso onesto:
- **Togliere** l'affermazione che il Sud sia beneficiario netto / "non è redistribuzione Nord-Sud".
- **Tenere e usare** il fatto verificato che **i migliori atenei di ricerca del Sud vincono** (Napoli Federico II +8M/+2%, Cagliari, Messina): la riforma premia la *qualità della ricerca ovunque si trovi*, e al Sud c'è eccellenza che oggi non è premiata a sufficienza.
- **Ancorare l'argomento anti-divergenza ai presìdi già nel testo**, non alla simulazione grezza: criterio della **traiettoria** (premia il miglioramento da condizioni svantaggiate), **perequativo**, **"campioni per macroregione"**. È *questo* che rende la riforma compatibile con la coesione, non un (inesistente) guadagno netto del Sud.
- Formula difendibile: *"a criteri invariati, il 50% premiale sposterebbe modestamente risorse verso gli atenei più intensi in ricerca (Δ Nord +0,4%, Sud −0,7% dell'FFO); per questo la proposta accoppia alla premialità la traiettoria, il perequativo e i campioni per macroregione — e già oggi i migliori atenei del Sud, come Federico II, ne sarebbero beneficiari."*

**Stato:** issue per la v2 (correzione §2.1), penna a Claude-chat. Nostra elaborazione su fonte primaria (DM 595/2025), 3 stress test superati.
