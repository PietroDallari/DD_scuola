"""ORA driver — runs a corrected (dedup) scenario WITHOUT modifying Nazareno's repo.

Imports his util functions and passes:
 - a corrected edifici_base.csv (POP_ISTAT_ETA_CICLO_UNICO / 4, fixing the 4x POSAS dup)
 - per-scenario param overrides (never edits config/variabili_scenario.py)

Outputs go to output/simulazioni/<scenario>/ which is gitignored (only scenario_base is tracked).
Usage:  py run_scenario.py <scenario_name>
"""
from __future__ import annotations
import sys, csv, copy
from pathlib import Path
from collections import Counter

ROOT = Path(r"c:/Users/dallarip/Repos/DD_scuola/Ciclo_unico_scolastico")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "script"))

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

SCENARIOS = {
    "scenario_base_dedup": {},
    "scenario_orizzonte_9": {"param": {"orizzonte_analisi_anni": 9}},
    "scenario_contingenza_25": {"costi": {"quota_contingenza": 0.25}},
    "scenario_docenti_tempo_lungo": {
        "param": {"includi_docenti_extra_tempo_lungo": True},
        "costi": {"docenti_extra_tempo_lungo_studente_anno": 400},
    },
}

def write_corrected_edifici_base(dst: Path) -> tuple[int, int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(SRC_EB, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        hdr = next(r)
        idx = hdr.index("POP_ISTAT_ETA_CICLO_UNICO")
        n = fixed = 0
        with open(dst, "w", encoding="utf-8", newline="") as g:
            w = csv.writer(g)
            w.writerow(hdr)
            for row in r:
                n += 1
                v = row[idx]
                if v not in ("", None):
                    try:
                        row[idx] = str(round(int(float(v)) / 4))
                        fixed += 1
                    except ValueError:
                        pass
                w.writerow(row)
    return n, fixed

def count_rows(p: Path) -> int:
    if not p.exists():
        return -1
    with open(p, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1

def read_first(p: Path) -> dict:
    with open(p, encoding="utf-8") as f:
        return next(csv.DictReader(f))

def main() -> None:
    name = sys.argv[1]
    ov = SCENARIOS[name]
    param = copy.deepcopy(PARAMETRI_SCENARIO); param.update(ov.get("param", {}))
    costi = copy.deepcopy(COSTI_UNITARI); costi.update(ov.get("costi", {}))
    tab = SIM / name / "tabelle"
    tab.mkdir(parents=True, exist_ok=True)
    eb = tab / "edifici_base.csv"
    n, fixed = write_corrected_edifici_base(eb)
    print(f"[{name}] corrected edifici_base: {n} rows, {fixed} POP_ISTAT values /4")

    analizza_scenario(
        percorso_edifici_base=eb, percorso_output_file=tab, anno_cutoff=ANNO_CUTOFF,
        parametri=param, costi_unitari=costi, fattori_rischio_costi=FATTORI_RISCHIO_COSTI,
        tempi_realizzazione=TEMPI_REALIZZAZIONE_ANNI, parametri_riordino=PARAMETRI_RIORDINO_TERRITORIALE,
        percorso_dati_ufficiali=Path(config["paths"]["dati_ufficiali"]),
    )
    print(f"[{name}] analisi done")
    crea_output_timeline_realistica(
        config=config, percorso_tabelle=tab, anno_cutoff=ANNO_CUTOFF,
        costi_unitari=costi, fattori_rischio_costi=FATTORI_RISCHIO_COSTI,
        parametri_timeline=PARAMETRI_TIMELINE_REALISTICA, forza_download=False,
    )
    print(f"[{name}] timeline done")

    rr = read_first(tab / "spesa_riepilogo_realistico.csv")
    print(f"RESULT {name}")
    print(f"  SPESA_LORDA_BASE_EUR = {float(rr['SPESA_LORDA_BASE_EUR']):,.0f}")
    print(f"  SPESA_NETTA_BASE_EUR = {float(rr['SPESA_NETTA_BASE_EUR']):,.0f}")
    print(f"  SPESA_LORDA_MAX_EUR  = {float(rr['SPESA_LORDA_MAX_EUR']):,.0f}")
    print(f"  RISPARMI_CHIUSURE_BASE_EUR = {float(rr['RISPARMI_CHIUSURE_BASE_EUR']):,.0f}")
    print(f"  esito: chiudere={count_rows(tab/'sedi_chiudere.csv')} "
          f"da_valutare={count_rows(tab/'sedi_da_valutare.csv')} "
          f"tenere_aperte={count_rows(tab/'sedi_tenere_aperte.csv')}")

if __name__ == "__main__":
    main()
