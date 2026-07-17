"""Task A — calibration grid on CORRECTED POSAS data (÷4). Repo read-only.

For each (concentration on/off) x (soglia demand in 30/60/90/120) x (riferimento 250/200):
  - run analizza_scenario + timeline on corrected edifici_base with param overrides
  - record closures, realistic spend, savings, and a presidio-check from sintesi comunale
Writes an incremental CSV so partial results survive interruption.
Reuses one working folder to keep disk usage minimal.
"""
from __future__ import annotations
import sys, csv, copy, math
from pathlib import Path

ROOT = Path(r"c:/Users/dallarip/Repos/DD_scuola/Ciclo_unico_scolastico")
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "script"))
from config.dati_ufficiali import crea_config_base
from config.variabili_scenario import (
    ANNO_CUTOFF, PARAMETRI_SCENARIO, COSTI_UNITARI, FATTORI_RISCHIO_COSTI,
    TEMPI_REALIZZAZIONE_ANNI, PARAMETRI_RIORDINO_TERRITORIALE, PARAMETRI_TIMELINE_REALISTICA,
)
from utils.scenario_utils import analizza_scenario
from utils.timeline_utils import crea_output_timeline_realistica

config = crea_config_base(ROOT)
SIM = ROOT / "output" / "simulazioni"
SRC_EB = SIM / "scenario_base" / "tabelle" / "edifici_base.csv"
WORK = SIM / "grid_work" / "tabelle"
WORK.mkdir(parents=True, exist_ok=True)
OUT_CSV = Path(sys.argv[1])

def corrected_edifici_base(dst: Path) -> None:
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

def count_rows(p: Path) -> int:
    with open(p, encoding="utf-8") as f: return sum(1 for _ in f) - 1

def presidio_check(tab: Path):
    """comuni with 11-18 residents that keep NO local sede (all closed)."""
    comuni_dom_pos = 0; senza_sede = 0; alunni_senza = 0
    with open(tab / "sintesi_comunale_chiusure.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try: dom = int(float(r.get("DOMANDA_ISTAT_ETA_COMUNE") or 0))
            except ValueError: dom = 0
            if dom <= 0: continue
            comuni_dom_pos += 1
            tot = int(float(r.get("SEDI_TOTALI") or 0))
            tenere = int(float(r.get("SEDI_TENERE_APERTE") or 0))
            valut = int(float(r.get("SEDI_DA_VALUTARE") or 0))
            if tot > 0 and tenere == 0 and valut == 0:
                senza_sede += 1
                try: alunni_senza += int(float(r.get("ALUNNI_TOTALI") or 0))
                except ValueError: pass
    return comuni_dom_pos, senza_sede, alunni_senza

# corrected edifici_base once, reused for every cell (only riordino params change)
EB = WORK / "edifici_base.csv"
corrected_edifici_base(EB)

FIELDS = ["CONCENTRAZIONE","SOGLIA_DOMANDA","RIFERIMENTO_SUP","CHIUDERE","DA_VALUTARE",
          "TENERE_APERTE","TOTALE_SEDI","QUOTA_CHIUSURE_PCT","SPESA_LORDA_BASE_EUR",
          "SPESA_NETTA_BASE_EUR","RISPARMI_CHIUSURE_BASE_EUR","COMUNI_DOMANDA_POS",
          "COMUNI_SENZA_SEDE_LOCALE","ALUNNI_IN_COMUNI_SENZA_SEDE"]
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(FIELDS)

for conc in (True, False):
    for soglia in (30, 60, 90, 120):
        for rifer in (250, 200):
            rio = copy.deepcopy(PARAMETRI_RIORDINO_TERRITORIALE)
            rio["usa_vincolo_concentrazione_superiori"] = conc
            rio["soglia_domanda_minima_chiusura"] = soglia
            rio["soglia_bacino_minimo_chiusura"] = soglia
            rio["studenti_minimi_sede_riferimento_superiori"] = rifer
            param = copy.deepcopy(PARAMETRI_SCENARIO)
            param["soglia_domanda_minima_chiusura"] = soglia  # sede-level gate also reads scenario param path
            analizza_scenario(
                percorso_edifici_base=EB, percorso_output_file=WORK, anno_cutoff=ANNO_CUTOFF,
                parametri=param, costi_unitari=copy.deepcopy(COSTI_UNITARI),
                fattori_rischio_costi=FATTORI_RISCHIO_COSTI, tempi_realizzazione=TEMPI_REALIZZAZIONE_ANNI,
                parametri_riordino=rio, percorso_dati_ufficiali=Path(config["paths"]["dati_ufficiali"]),
            )
            crea_output_timeline_realistica(
                config=config, percorso_tabelle=WORK, anno_cutoff=ANNO_CUTOFF,
                costi_unitari=copy.deepcopy(COSTI_UNITARI), fattori_rischio_costi=FATTORI_RISCHIO_COSTI,
                parametri_timeline=PARAMETRI_TIMELINE_REALISTICA, forza_download=False,
            )
            ch = count_rows(WORK/"sedi_chiudere.csv"); dv = count_rows(WORK/"sedi_da_valutare.csv")
            ta = count_rows(WORK/"sedi_tenere_aperte.csv"); tot = ch+dv+ta
            with open(WORK/"spesa_riepilogo_realistico.csv", encoding="utf-8") as f:
                rr = next(csv.DictReader(f))
            cdp, senza, alsz = presidio_check(WORK)
            row = [conc, soglia, rifer, ch, dv, ta, tot, round(100*ch/tot,1) if tot else 0,
                   int(float(rr["SPESA_LORDA_BASE_EUR"])), int(float(rr["SPESA_NETTA_BASE_EUR"])),
                   int(float(rr["RISPARMI_CHIUSURE_BASE_EUR"])), cdp, senza, alsz]
            with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)
            print(f"conc={conc} soglia={soglia} rif={rifer} -> ch={ch} dv={dv} ta={ta} "
                  f"({row[7]}%) lordo={row[8]:,} netto={row[9]:,} senza_sede={senza}/{cdp}", flush=True)
print("GRID DONE ->", OUT_CSV)
