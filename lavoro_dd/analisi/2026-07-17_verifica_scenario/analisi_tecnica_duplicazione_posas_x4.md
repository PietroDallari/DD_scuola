# Duplicazione ×4 della popolazione ISTAT POSAS nella pipeline dati — analisi tecnica e correzione

**Repo analizzato:** `NazarenoLecis/Ciclo_unico_scolastico` — commit `a9edf41`
**Data analisi:** 2026-07-17
**Gravità:** alta — il dato di popolazione ISTAT entra nel modello moltiplicato ×4, con effetti materiali su chiusure sedi e stima di spesa.
**Ambito:** solo dati (nessun input errato dell'utente); riproducibile da pipeline pulita.

---

## 1. Sintesi

Il downloader ISTAT POSAS scarica e concatena **più zip che contengono gli stessi comuni** (i file per-provincia, l'aggregato nazionale `..._Comuni.zip` e il bundle `..._Tutti_i_file.zip` che li ricontiene entrambi). Il risultato è che **ogni riga `(comune, età)` viene ripetuta esattamente 4 volte, identica**. La popolazione nazionale 11–18 risulta 17,87 M invece dei reali ~4,47 M.

Il valore gonfiato ×4 si propaga in `popolazione_bacino_*.csv`, poi in `edifici_base.csv` (colonna `POP_ISTAT_ETA_CICLO_UNICO`) e infine nella logica di riordino territoriale, dove **sovrastima la domanda di bacino ×4** e porta il modello a **sotto-chiudere le sedi**.

Correggendo il dato (÷4, fattore uniforme e verificato), lo scenario base passa da **36,8 / 36,0 mld** (lordo/netto) a **25,2 / 22,0 mld**, e le chiusure da **3.001 a 8.367**.

---

## 2. Sintomo osservato

Nei file prodotti dalla pipeline in `output/dati_ufficiali/istat/posas/`:

- `popolazione_eta_comune_2026.csv`: 252.672 righe = 7.896 comuni × 8 età (11–18) × **4**.
- Ogni chiave `(CODICECOMUNE, ETA)` compare **4 volte, byte-identica**. Esempio comune `001001` (Agliè), età 11: 4 righe uguali `POP_TOTALE=20`.
- Somma nazionale 11–18: **17.871.420** (atteso ~4,47 M). Anche `popolazione_bacino_11_18_2026.csv` somma a 17,87 M perché aggregato dagli stessi dati.
- Controprova su comune grande: Roma (`058091`), 11–18 = **834.024** = 4 × 208.506 (valore vero).

Il fattore ×4 è **uniforme su tutti i comuni**, quindi la correzione esatta è la divisione per 4 (o, meglio, la rimozione della causa a monte).

---

## 3. Causa radice

### 3.1 Selezione dei link zip — `script/utils/download_utils.py:323`

```python
def trova_link_zip_posas(html_pagina: str, anno: int) -> list[str]:
    pattern = rf"""href\s*=\s*["']([^"']*POSAS_{anno}_it_[^"']+\.zip)["']"""
    link_trovati = re.findall(pattern, html_pagina, flags=re.IGNORECASE)
    link_puliti = []
    for link in link_trovati:
        link_pulito = html.unescape(link).strip()
        if link_pulito not in link_puliti:
            link_puliti.append(link_pulito)
    return link_puliti
```

Il pattern `POSAS_{anno}_it_*.zip` intercetta **tutti** i link della pagina ISTAT, che pubblica:

- 107 zip per-provincia — `POSAS_2026_it_001_Torino.zip` … `POSAS_2026_it_111_Sud_Sardegna.zip`
- 4 aggregati — `POSAS_2026_it_Comuni.zip`, `..._Province.zip`, `..._Regioni.zip`, `..._Ripartizioni.zip`
- 1 bundle onnicomprensivo — `POSAS_2026_it_Tutti_i_file.zip` (ricontiene i file precedenti)

Vengono restituiti e scaricati **tutti**.

### 3.2 Estrazione — `script/utils/download_utils.py:395` (loop righe 402–404)

```python
def estrai_popolazione_posas_zip(percorso_zip, anno, eta_minima, eta_massima):
    righe = []
    with zipfile.ZipFile(percorso_zip) as archivio:
        nomi_csv = [nome for nome in archivio.namelist() if nome.lower().endswith(".csv")]
        for nome_csv in nomi_csv:          # <-- legge OGNI csv nello zip
            ...
            for riga in lettore:
                ...
                righe.append({...})        # <-- e le accoda tutte
    return righe
```

Il chiamante (`scarica_dati_istat_posas`, righe 354–377) itera su **tutti** i link e fa `righe_popolazione.extend(...)` per ciascuno zip, senza deduplica.

### 3.3 Meccanismo esatto della moltiplicazione ×4 (evidenza)

Conteggio delle occorrenze della riga `(comune 001001, età 11)` tra gli zip scaricati:

| Sorgente scaricata | Copie di `(001001, 11)` |
|---|---|
| `POSAS_2026_it_001_Torino.zip` (file provincia) | 1 |
| `POSAS_2026_it_Comuni.zip` (aggregato nazionale comuni) | 1 |
| `POSAS_2026_it_Tutti_i_file.zip` (bundle: provincia **+** comuni) | 2 |
| **Totale** | **4** |

Ogni comune è quindi contato: 1× dal suo file provincia standalone, 1× dall'aggregato `_Comuni` standalone, 2× dentro `_Tutti_i_file` (che include sia il file provincia sia il file comuni). Struttura identica per tutti i comuni ⇒ ×4 uniforme.

---

## 4. Propagazione nel modello

1. `aggrega_popolazione_posas` (`download_utils.py:431`) somma `POP_TOTALE` per comune ⇒ `POP_ETA_BACINO` ×4.
2. `carica_popolazione_istat_bacino` / `popolazione_istat_per_edificio` (`build_utils.py:56`, `:103`) scrivono il valore in `edifici_base.csv` come `POP_ISTAT_ETA_CICLO_UNICO` ×4.
3. `domanda_istat_bacino` (`riordino_utils.py:116-123`) somma per comune quel valore:

```python
def domanda_istat_bacino(righe: list[dict]) -> int:
    valori_per_comune = {}
    for riga in righe:
        codice = riga.get("CODICECOMUNE", "")
        valore = converti_intero(riga.get("POP_ISTAT_ETA_CICLO_UNICO"))
        if codice and valore > 0:
            valori_per_comune[codice] = max(valori_per_comune.get(codice, 0), valore)
    return sum(valori_per_comune.values())
```

4. `sedi_target = max(1, ceil(domanda_bacino / riferimento_studenti_sede))` risulta **~4× troppo alto** ⇒ il vincolo di concentrazione (`usa_vincolo_concentrazione_superiori`) non segnala sedi in eccesso, e le soglie di domanda (`soglia_domanda_minima_chiusura`, `soglia_presidio_alunni` = 120) vengono superate troppo facilmente. **Effetto netto: il modello sotto-chiude le sedi.**

---

## 5. Impatto quantificato

Metodo: rerun via driver esterno che **importa** `analizza_scenario` + `crea_output_timeline_realistica` senza modificare il repo, sostituendo solo `POP_ISTAT_ETA_CICLO_UNICO` con il valore corretto (÷4). **Controllo di fedeltà:** lo stesso driver, sul dato *gonfiato*, riproduce all'euro l'output committato (36.823.844.889 / 35.975.489.589; chiusure 3001/3109/10660). Quindi l'unica variabile è la correzione.

| Metrica (orizzonte 4 anni, realistico) | Committato (×4) | Corretto (÷4) | Δ |
|---|---|---|---|
| Spesa lorda base | 36,82 mld | **25,19 mld** | −11,63 (−32%) |
| Spesa netta base | 35,98 mld | **22,00 mld** | −13,98 (−39%) |
| Spesa lorda MAX | 50,64 mld | **34,62 mld** | −16,02 |
| Risparmi da chiusure | 0,85 mld | **3,20 mld** | ×3,8 |
| Sedi: chiudere | 3.001 | **8.367** | +5.366 |
| Sedi: da_valutare | 3.109 | **912** | −2.197 |
| Sedi: tenere_aperte | 10.660 | **7.491** | −3.169 |

---

## 6. Correzione proposta

### 6.1 Fix primario — selezionare una sola sorgente (`trova_link_zip_posas`)

Tenere unicamente l'aggregato nazionale dei comuni ed evitare province + bundle. Corregge la causa **e** elimina il download ridondante di 100+ MB di zip provinciali:

```python
def trova_link_zip_posas(html_pagina: str, anno: int) -> list[str]:
    pattern = rf"""href\s*=\s*["']([^"']*POSAS_{anno}_it_[^"']+\.zip)["']"""
    link_trovati = re.findall(pattern, html_pagina, flags=re.IGNORECASE)
    link_puliti = []
    for link in link_trovati:
        link_pulito = html.unescape(link).strip()
        if link_pulito not in link_puliti:
            link_puliti.append(link_pulito)

    # ISTAT pubblica file per-provincia + aggregati (_Comuni, _Province, ...) +
    # bundle _Tutti_i_file che li ricontiene: scaricarli tutti duplica ogni comune.
    # Tenere solo l'aggregato nazionale dei comuni.
    def nome(l): return l.rsplit("/", 1)[-1].lower()
    solo_comuni = [l for l in link_puliti if nome(l) == f"posas_{anno}_it_comuni.zip"]
    return solo_comuni[:1] if solo_comuni else link_puliti
```

### 6.2 Difesa in profondità — deduplica in estrazione

Anche mantenendo il fix 6.1, conviene rendere idempotente l'estrazione (protegge da bundle o file ridondanti dentro un singolo zip):

```python
# in estrai_popolazione_posas_zip, prima di append:
chiave = (codice_comune.zfill(6), eta)
if chiave in viste:
    continue
viste.add(chiave)
```

(con `viste = set()` inizializzato a inizio funzione). In alternativa, deduplica su `(CODICECOMUNE, ETA)` in `aggrega_popolazione_posas`.

---

## 7. Raccomandazione aggiuntiva — ricalibrare le soglie

Con il dato corretto le chiusure salgono a **8.367 (>50% delle sedi medie-superiori)**. Le soglie (`soglia_domanda_minima_chiusura`=120, `soglia_presidio_alunni`=120, `studenti_minimi_sede_riferimento_superiori`=250 e il vincolo di concentrazione) erano di fatto tarate contro un bacino gonfiato ×4: vanno **riviste** ora che la domanda è ~4× più piccola. È una scelta di scenario, non un difetto del dato, ma senza ricalibrazione il modello potrebbe chiudere troppo.

---

## 8. Come riprodurre

1. Eseguire il solo download POSAS (`scarica_dati_istat_posas`, età 11–18).
2. `wc -l output/dati_ufficiali/istat/posas/popolazione_eta_comune_2026.csv` → 252.673 (header incluso).
3. Verificare che `(CODICECOMUNE, ETA)` non sia univoca: 189.504 righe duplicate su 252.672.
4. Somma `POP_TOTALE` 11–18 = 17.871.420 (atteso ~4,47 M).
5. Confronto per zip: la riga `(001001, 11)` compare in `_001_Torino.zip` (1), `_Comuni.zip` (1) e `_Tutti_i_file.zip` (2) → 4.
