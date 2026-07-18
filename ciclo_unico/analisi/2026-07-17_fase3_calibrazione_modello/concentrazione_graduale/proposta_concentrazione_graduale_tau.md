# Concentrazione graduale con tolleranza di ridondanza τ — proposta di disegno

**Da:** ORA (analisi) · 2026-07-17 · **Natura:** proposta di metodo per l'autore del modello, non una modifica al repo. Il disegno finale è dell'autore. Verificato su dato POSAS **corretto ÷4**.

## Problema
Il vincolo di concentrazione attuale è **binario**. Sul dato corretto:
- `usa_vincolo_concentrazione_superiori = True` → **46–50%** di sedi chiuse (~25 mld);
- `= False` → **4,5–12,4%** (~38–40 mld);
- e `studenti_minimi_sede_riferimento_superiori` (200 vs 250) **non modula** il risultato.

Manca quindi qualunque punto intermedio: non è possibile calibrare su un target prudenziale (es. ~15–20% di chiusure), che era l'ordine di grandezza del run originale (prima della correzione ×4 della popolazione).

## Proposta: un solo parametro nuovo, τ (tolleranza di ridondanza)
Il codice attuale (`applica_vincolo_concentrazione_superiori`) **già** ordina le sedi eccedenti per un punteggio di ridondanza (`punteggio_concentrazione_sede`: domanda, stato tecnico, ferrovia, ruolo) e chiude solo l'eccesso oltre `sedi_target`. La proposta cambia **una riga**: si mantiene una fascia di tolleranza sopra il fabbisogno teorico.

1. Per ogni bacino, fabbisogno teorico invariato: `sedi_target = ceil(domanda_bacino / riferimento_bacino)`.
2. **Tolleranza:** `sedi_da_mantenere = min(ceil(sedi_target × (1 + τ)), sedi_attive)`.
3. `eccedenza = max(0, sedi_attive − sedi_da_mantenere)`; si chiudono solo le prime `eccedenza` sedi **in coda alla graduatoria** già esistente (le meno "difendibili").
4. Regola dell'alternativa capiente/vicina e presidio **invariate**, applicate dopo (come oggi).

**Proprietà:** τ=0 riproduce esattamente l'attuale `ON`; τ→∞ (fascia che copre tutte le sedi) equivale all'attuale `OFF`. In mezzo, la % di chiusure degrada **con continuità e in modo monotòno**. Un solo parametro, dichiarabile nel metodo: *"tolleranza di ridondanza del X% oltre il fabbisogno teorico del bacino"*.

**Diff concettuale (riordino_utils.py:182):**
```python
# attuale
sedi_target = min(sedi_target, len(elementi))
eccedenza  = max(len(elementi) - sedi_target, 0)
# proposta (τ = "tolleranza_ridondanza_bacino", default 0.0 = comportamento attuale)
sedi_target = min(ceil(sedi_target * (1 + tau)), len(elementi))
eccedenza  = max(len(elementi) - sedi_target, 0)
```
(la graduatoria e la chiusura del solo eccesso sono già nel codice, righe 195–225.)

## Curva di calibrazione (dato corretto, soglia domanda fissa = 120)
Ottenuta iniettando τ a runtime (repo non modificato); τ=0 riproduce all'euro il run ON attuale (8.367 chiusure, 25,19/22,00 mld) — check di consistenza superato.

| τ | % chiusure | Chiudere | Lordo €mld | Netto €mld | Comuni senza sede |
|---|---|---|---|---|---|
| 0,00 | 49,9 | 8.367 | 25,19 | 22,00 | 486 |
| 0,25 | 39,1 | 6.558 | 27,71 | 25,17 | 459 |
| 0,50 | 35,5 | 5.947 | 29,19 | 26,88 | 459 |
| 0,75 | 30,9 | 5.188 | 30,94 | 29,06 | 458 |
| 1,00 | 28,7 | 4.808 | 31,88 | 30,16 | 458 |
| 1,50 | 22,2 | 3.719 | 34,34 | 33,16 | 457 |
| **2,00** | **19,1** | **3.205** | **35,57** | **34,63** | **457** |
| 3,00 | 15,1 | 2.532 | 37,10 | 36,37 | 457 |
| 5,00 | 12,9 | 2.156 | 38,00 | 37,41 | 457 |
| 8,00 | 12,4 | 2.079 | 38,19 | 37,63 | 457 |

File: [curva_tau_concentrazione.csv](curva_tau_concentrazione.csv) · driver: [run_tau.py](run_tau.py).

## Lettura
- La quota di chiusure degrada **con continuità e in modo monotòno** da 49,9% (τ=0, = `ON` attuale) a 12,4% (τ→∞, = `OFF` attuale, pavimento dato dalla sola soglia domanda). Niente più salto 12%↔46%.
- **Il target ~18% dell'intento prudenziale del committato è a τ ≈ 2,0–2,2:** a τ=2,0 → 19,1% di chiusure, **3.205 sedi** (≈ le 3.001 del run originale) e 35,6/34,6 mld. Cioè si **riproduce l'ordine di grandezza originale su dato CORRETTO**, ma con un parametro dichiarabile ("tolleranza di ridondanza ~200% oltre il fabbisogno"), non come artefatto della domanda ×4.
- **I comuni senza sede locale restano ~457–486 su tutta la curva:** sono governati dalla **soglia domanda** (qui 120), non da τ. Quindi τ (quota chiusure / ridondanza) e `soglia_domanda_minima_chiusura` (presidio) sono **due leve ortogonali**: si calibra la quota di razionalizzazione senza peggiorare il presidio, e viceversa. Questo è il vantaggio pratico principale rispetto al vincolo binario odierno.

## Vantaggi da esplicitare
- **Un solo parametro nuovo**, con default 0.0 retro-compatibile (nessun cambiamento per chi usa `ON` oggi).
- **Degrada con continuità** tra i due regimi attuali: niente più salto 12%↔46%.
- **Riusa il punteggio tecnico** già costruito (`punteggio_concentrazione_sede`): le sedi chiuse restano le meno difendibili.
- Trasforma il **trade-off costo↔presidio in una curva leggibile** invece di una scelta binaria: si sceglie τ sul target politico (~15–20%) e lo si dichiara nel metodo.
