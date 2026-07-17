"""Concentrazione graduale (proposta ORA per Nazareno) — curva tau.
Repo di Nazareno READ-ONLY: la tolleranza tau e' iniettata via monkeypatch a runtime
di applica_vincolo_concentrazione_superiori (i file su disco non sono toccati).
tau=0 -> comportamento ON attuale; tau grande -> concentrazione inattiva (solo soglia domanda).
"""
from __future__ import annotations
import sys, csv, copy
from pathlib import Path

ROOT = Path(r"c:/Users/dallarip/Repos/DD_scuola/Ciclo_unico_scolastico")
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "script"))
from config.dati_ufficiali import crea_config_base
from config.variabili_scenario import (
    ANNO_CUTOFF, PARAMETRI_SCENARIO, COSTI_UNITARI, FATTORI_RISCHIO_COSTI,
    TEMPI_REALIZZAZIONE_ANNI, PARAMETRI_RIORDINO_TERRITORIALE, PARAMETRI_TIMELINE_REALISTICA,
)
import utils.riordino_utils as ru
from utils.scenario_utils import analizza_scenario
from utils.timeline_utils import crea_output_timeline_realistica

# ---- monkeypatch: applica_vincolo con tolleranza tau (copia della logica upstream + 1 riga) ----
def patched_vincolo(righe_sedi, parametri):
    tau = getattr(ru, "_TAU_OVERRIDE", 0.0)
    riferimento_studenti = ru.calcola_studenti_riferimento_superiori(righe_sedi, parametri)
    gruppi = ru.defaultdict(list)
    for indice, riga in enumerate(righe_sedi):
        if riga.get("RUOLO_TARGET") == "fuori_perimetro":
            continue
        gruppi[riga.get("BACINO_ID", "BACINO_NON_DEFINITO")].append((indice, riga))
    risultato = [dict(r) for r in righe_sedi]
    for bacino_id, elementi in gruppi.items():
        if not elementi:
            continue
        if any(r.get("SIGLAPROVINCIA", "") in {"AO", "TN", "BZ"} for _, r in elementi):
            ru.annota_vincolo_concentrazione(risultato, elementi, riferimento_studenti, "", "NO",
                "autonomia speciale: dati da integrare"); continue
        domanda_bacino = (ru.converti_intero(elementi[0][1].get("DOMANDA_TOTALE_BACINO"))
                          or ru.domanda_istat_bacino([r for _, r in elementi])
                          or ru.domanda_mim_unica_bacino([r for _, r in elementi]))
        if domanda_bacino <= 0:
            ru.annota_vincolo_concentrazione(risultato, elementi, riferimento_studenti, "", "NO",
                "domanda bacino assente"); continue
        riferimento_bacino = ru.calcola_studenti_riferimento_superiori_bacino(elementi, riferimento_studenti)
        sedi_target_base = max(1, ru.ceil(domanda_bacino / riferimento_bacino))
        sedi_target = min(ru.ceil(sedi_target_base * (1.0 + tau)), len(elementi))  # <-- tolleranza tau
        eccedenza = max(len(elementi) - sedi_target, 0)
        ru.annota_vincolo_concentrazione(risultato, elementi, riferimento_studenti, sedi_target,
            "SI" if eccedenza else "NO", f"tolleranza ridondanza tau={tau:.2f} (proposta ORA)")
        if eccedenza <= 0:
            continue
        ordinati = sorted(elementi, key=lambda e: ru.punteggio_concentrazione_sede(e[1]), reverse=True)
        mant = {r.get("CODICEEDIFICIO", "") for _, r in ordinati[:sedi_target]}
        for indice, riga in ordinati[sedi_target:]:
            if riga.get("CODICEEDIFICIO", "") in mant:
                continue
            if riga.get("DECISIONE_OPERATIVA_SEDE") == "mantenere_autonomia_dati_da_integrare":
                continue
            domanda = max(ru.converti_intero(riga.get("DOMANDA_TARGET")), ru.converti_intero(riga.get("ALUNNI_TOTALI")))
            posti = ru.converti_intero(riga.get("POSTI_ALTERNATIVI_USATI"))
            dist = ru.converti_float(riga.get("DISTANZA_KM_ALTERNATIVA_USATA"), valore_default=-1)
            dmax = ru.converti_float(riga.get("DISTANZA_MAX_AMMISSIBILE_KM"), valore_default=-1)
            vicina = posti >= domanda and (dist < 0 or dmax < 0 or dist <= dmax)
            risultato[indice]["DECISIONE_OPERATIVA_SEDE"] = "chiudere_o_accorpare" if vicina else "chiudere_condizionato_verifica_capienza"
            risultato[indice]["MOTIVAZIONE_DECISIONE"] = "sede eccedente oltre tolleranza ridondanza (proposta ORA)"
    return risultato

ru.applica_vincolo_concentrazione_superiori = patched_vincolo

config = crea_config_base(ROOT)
SIM = ROOT / "output" / "simulazioni"
SRC_EB = SIM / "scenario_base" / "tabelle" / "edifici_base.csv"
WORK = SIM / "tau_work" / "tabelle"; WORK.mkdir(parents=True, exist_ok=True)
OUT_CSV = Path(sys.argv[1])

def corrected_eb(dst):
    with open(SRC_EB, encoding="utf-8", newline="") as f:
        r = csv.reader(f); hdr = next(r); idx = hdr.index("POP_ISTAT_ETA_CICLO_UNICO")
        with open(dst, "w", encoding="utf-8", newline="") as g:
            w = csv.writer(g); w.writerow(hdr)
            for row in r:
                v = row[idx]
                if v not in ("", None):
                    try: row[idx] = str(round(int(float(v)) / 4))
                    except ValueError: pass
                w.writerow(row)
def cnt(p): return sum(1 for _ in open(p, encoding="utf-8")) - 1
def presidio(tab):
    dp = ss = 0
    for r in csv.DictReader(open(tab / "sintesi_comunale_chiusure.csv", encoding="utf-8")):
        try: dom = int(float(r.get("DOMANDA_ISTAT_ETA_COMUNE") or 0))
        except ValueError: dom = 0
        if dom <= 0: continue
        dp += 1
        if int(float(r.get("SEDI_TOTALI") or 0)) > 0 and int(float(r.get("SEDI_TENERE_APERTE") or 0)) == 0 and int(float(r.get("SEDI_DA_VALUTARE") or 0)) == 0:
            ss += 1
    return dp, ss

EB = WORK / "edifici_base.csv"; corrected_eb(EB)
rio = copy.deepcopy(PARAMETRI_RIORDINO_TERRITORIALE)
rio["usa_vincolo_concentrazione_superiori"] = True
rio["soglia_domanda_minima_chiusura"] = 120; rio["soglia_bacino_minimo_chiusura"] = 120
param = copy.deepcopy(PARAMETRI_SCENARIO); param["soglia_domanda_minima_chiusura"] = 120

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["TAU","CHIUDERE","DA_VALUTARE","TENERE_APERTE","TOTALE","QUOTA_CHIUSURE_PCT",
                            "SPESA_LORDA_BASE_EUR","SPESA_NETTA_BASE_EUR","RISPARMI_CHIUSURE_EUR",
                            "COMUNI_DOMANDA_POS","COMUNI_SENZA_SEDE_LOCALE"])
for tau in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0):
    ru._TAU_OVERRIDE = tau
    analizza_scenario(percorso_edifici_base=EB, percorso_output_file=WORK, anno_cutoff=ANNO_CUTOFF,
        parametri=param, costi_unitari=copy.deepcopy(COSTI_UNITARI), fattori_rischio_costi=FATTORI_RISCHIO_COSTI,
        tempi_realizzazione=TEMPI_REALIZZAZIONE_ANNI, parametri_riordino=rio,
        percorso_dati_ufficiali=Path(config["paths"]["dati_ufficiali"]))
    crea_output_timeline_realistica(config=config, percorso_tabelle=WORK, anno_cutoff=ANNO_CUTOFF,
        costi_unitari=copy.deepcopy(COSTI_UNITARI), fattori_rischio_costi=FATTORI_RISCHIO_COSTI,
        parametri_timeline=PARAMETRI_TIMELINE_REALISTICA, forza_download=False)
    ch = cnt(WORK/"sedi_chiudere.csv"); dv = cnt(WORK/"sedi_da_valutare.csv"); ta = cnt(WORK/"sedi_tenere_aperte.csv")
    tot = ch+dv+ta; rr = next(csv.DictReader(open(WORK/"spesa_riepilogo_realistico.csv", encoding="utf-8")))
    dp, ss = presidio(WORK)
    row = [tau, ch, dv, ta, tot, round(100*ch/tot,1), int(float(rr["SPESA_LORDA_BASE_EUR"])),
           int(float(rr["SPESA_NETTA_BASE_EUR"])), int(float(rr["RISPARMI_CHIUSURE_BASE_EUR"])), dp, ss]
    with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)
    print(f"tau={tau:>4} -> ch={ch} ({row[5]}%) lordo={row[6]:,} netto={row[7]:,} senza_sede={ss}", flush=True)
print("TAU CURVE DONE")
