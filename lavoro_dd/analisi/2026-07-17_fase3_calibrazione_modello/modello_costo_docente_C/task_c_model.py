"""Task C — Modello costo docente obbligo-18, per la spec autosufficiente di console brother.
Componenti A (trattenimento) e C (rilascio 13->12) in DOCENTI (robusto, CDOC-indipendente);
euro come funzione di CDOC (non sourced -> parametrico). Turnover + external check.
"""
import csv, io, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
DEL = Path(r"C:/Users/dallarip/AppData/Local/Temp/claude/c--Users-dallarip-Repos-DD-scuola/0f94d9fd-a5fd-4d15-9d12-7367bb213014/scratchpad/deliverables")

# ---- [D] POP(eta) POSAS 2026 dedup ----
POP = {}
for r in csv.DictReader(open(DEL/"posas_nazionale_eta_0_19.csv", encoding="utf-8")):
    POP[int(r["ETA"])] = int(r["POPOLAZIONE"])

# ---- [D] STU_STA(MIM age), [B.3] STU_PAR(MIM age) ----
def by_age(path, col):
    d = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        d[int(r["ETA_MIM_31_12_2024"])] = int(r[col])
    return d
STU_STA = by_age(DEL/"mim_studenti_superiori_statali_per_eta.csv", "ALUNNI_STATALI")
STU_PAR = by_age(DEL/"mim_studenti_superiori_paritarie_per_eta.csv", "ALUNNI_PARITARIE")

# ---- [B.4] IeFP: 163038 IF accreditate a.f.2023/24 (INAPP XXIII); spread /3.5 anni ----
IEFP_TOT = 163038
IEFP_PER_ETA = round(IEFP_TOT / 3.5)   # ~46582; assumption flagged
def IEFP(mim_age): return IEFP_PER_ETA if 14 <= mim_age <= 18 else 0

# ---- [B.1] RDS docenti/studenti sec II statale ----
RDS_BASE = 0.107   # titolari+supplenti posto comune (268315/2506430)
RDS_MIN, RDS_MAX = round(RDS_BASE*0.9, 4), round(RDS_BASE*1.1, 4)  # +/-10% per spec
# alt all-posts = 0.133 (riportato a parte)

# ---- [B.6] PENS ----
PENS_DOC = 21322      # docenti tutti gli ordini, 2024 (MIM/CISL)
PENS_SEC2 = 8536      # solo secondaria II grado

# ---- copertura statale quinta = STU_STA(18)/POP(19) ----
COP_QUINTA = STU_STA[18] / POP[19]
# ---- COPTOT e COPSTA a 16-17 (MIM 16,17 <-> POSAS 17,18) ----
den = POP[17] + POP[18]
num_sta = STU_STA[16] + STU_STA[17]
num_tot = num_sta + STU_PAR[16] + STU_PAR[17] + IEFP(16) + IEFP(17)
COPSTA = num_sta / den
COPTOT = num_tot / den
ESENZIONE = 0.97  # obbligo con esenzioni fisiologiche (segnaposto dichiarato)

COORTE = {  # COORTE_1617(R)
    "2032/33": POP[10] + POP[11],
    "2037/38": POP[5] + POP[6],
}
LEVA_POP = {"2032/33": POP[12], "2037/38": POP[7]}   # coorte anno-13 eliminato
ANNI_TRANS = {"2032/33": 2032 - 2029, "2037/38": 2037 - 2029}  # da avvio 2029/30

print(f"COP_QUINTA = {STU_STA[18]:,}/{POP[19]:,} = {COP_QUINTA:.3f}")
print(f"COPSTA = {num_sta:,}/{den:,} = {COPSTA:.3f}   COPTOT = {num_tot:,}/{den:,} = {COPTOT:.3f}")
print(f"IEFP per età (assunta) = {IEFP_PER_ETA:,}\n")

rows = []
for R in ("2032/33", "2037/38"):
    for varname, COP in (("base_totale", COPTOT), ("prudente_solo_statale", COPSTA)):
        controf = COORTE[R] * COP
        conrif = COORTE[R] * ESENZIONE
        dSTUD_A = conrif - controf
        LEVA = LEVA_POP[R] * COP_QUINTA
        for lvl, rds in (("min", RDS_MIN), ("base", RDS_BASE), ("max", RDS_MAX)):
            dDOC_A = dSTUD_A * rds
            DOC_LIB = LEVA * rds
            net = dDOC_A - DOC_LIB   # + = docenti in più; - = docenti liberati netti
            rows.append({
                "R": R, "COPERTURA": varname, "LIVELLO_RDS": lvl, "RDS": rds,
                "COORTE_1617": round(COORTE[R]), "COP": round(COP,3),
                "DELTA_STUD_A": round(dSTUD_A), "LEVA_ELIMINATA": round(LEVA),
                "DELTA_DOC_A": round(dDOC_A), "DOC_LIBERATI": round(DOC_LIB),
                "DOC_NETTI": round(net),
            })

# write CSV
cols = list(rows[0].keys())
with open(DEL/"task_c_modello_costo_docente_teachers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

print("=== Componenti A/C in DOCENTI (base RDS=0.107) ===")
for r in rows:
    if r["LIVELLO_RDS"] != "base": continue
    print(f"R={r['R']} {r['COPERTURA']:22s} ΔDOC_A={r['DELTA_DOC_A']:>7,}  DOC_LIBERATI={r['DOC_LIBERATI']:>7,}  DOC_NETTI={r['DOC_NETTI']:>8,}")

print("\n=== CHECK TURNOVER (base RDS) ===")
for R in ("2032/33", "2037/38"):
    lib = LEVA_POP[R]*COP_QUINTA*RDS_BASE
    per_anno = lib / ANNI_TRANS[R]
    print(f"R={R}: DOC_LIBERATI={lib:,.0f} su {ANNI_TRANS[R]} anni transizione = {per_anno:,.0f}/anno")
    print(f"   vs PENS docenti tutti ordini {PENS_DOC:,}/anno -> rapporto {per_anno/PENS_DOC:.2f}  (assorbito: {'SI' if per_anno<PENS_DOC else 'NO'})")
    print(f"   vs PENS solo sec II {PENS_SEC2:,}/anno -> rapporto {per_anno/PENS_SEC2:.2f}")

print("\n=== CHECK ESTERNO (1-COPTOT vs Eurostat) ===")
part = {}
for r in csv.DictReader(open(DEL/"eurostat_partecipazione_eta_16_17.csv", encoding="utf-8")):
    part[r["AGE"]] = float(r["PARTECIPAZIONE_PCT"])
noncov = 1 - COPTOT
euro_noncov = 1 - (part.get("Y16",0)+part.get("Y17",0))/200
print(f"1-COPTOT = {noncov*100:.1f}%   |  Eurostat non-part media 16-17 = {euro_noncov*100:.1f}%  |  ELET 18-24 = 8.2%")
print(f"   divergenza = {abs(noncov-euro_noncov)*100:.1f} punti  ({'>3: SEGNALARE' if abs(noncov-euro_noncov)*100>3 else 'coerente'})")

# COSTO_B annuale a regime dal run docenti - base
def opex(path):
    r = next(csv.DictReader(open(path, encoding="utf-8"))); return float(r["OPEX_ANNUO_A_REGIME_EUR"])
try:
    b = opex(DEL/"spesa_riepilogo_realistico__scenario_base_dedup.csv")
    d = opex(DEL/"spesa_riepilogo_realistico__scenario_docenti_tempo_lungo.csv")
    print(f"\nCOSTO_B (OPEX annua a regime, docenti_tempo_lungo - base) = {d-b:,.0f} €/anno (segnaposto 400€/stud)")
except Exception as e:
    print("COSTO_B n/d:", e)
print("\nEURO: SALDO(R) = DOC_NETTI × CDOC + COSTO_B.  CDOC NON sourced (RGS Conto Annuale, Tab.12/13) -> vedi riscontro.")
