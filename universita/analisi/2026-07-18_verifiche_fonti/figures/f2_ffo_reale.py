"""F2 — FFO università 2019-2025: nominale vs reale (base 2019).
Legge data/b4_ffo_serie.csv, produce figures/f2_ffo_reale.png.
Fonte nominale: decreti MUR di riparto (DM 1059/2021, 581/2022, 809/2023, 1170/2024, 595/2025) + ADI.
Deflatore primario: deflatore del PIL (Eurostat nama_10_gdp, 2019=100); HICP come check.
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "b4_ffo_serie.csv")
anni, nom, real_pil, real_hicp = [], [], [], []
with open(DATA, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        anni.append(int(r["ANNO"]))
        nom.append(float(r["FFO_NOMINALE_MLD"]))
        real_pil.append(float(r["FFO_REALE_PIL_MLD_2019"]))
        real_hicp.append(float(r["FFO_REALE_HICP_MLD_2019"]))

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(anni, nom, "-o", color="#1f77b4", label="FFO nominale")
ax.plot(anni, real_pil, "-o", color="#d62728", label="FFO reale (deflatore PIL, base 2019)")
ax.plot(anni, real_hicp, "--o", color="#ff7f0e", label="FFO reale (deflatore alternativo HICP, base 2019)", alpha=0.8)
# livello reale medio 2021-2023 (plateau), etichettato
liv = sum(real_pil[2:5]) / 3
ax.axhline(liv, color="#d62728", ls=":", lw=1, alpha=0.6)
ax.text(2019.05, liv + 0.03, "livello reale 2021-23", color="#d62728", fontsize=7.5, va="bottom")
ax.annotate("massimo nominale 2025 (9,37 mld)\nma reale sotto il livello 2021-23",
            xy=(2025, nom[-1]), xytext=(2021.0, 9.55), fontsize=8,
            arrowprops=dict(arrowstyle="->", color="gray"))
# punto forte: taglio anche nominale nel 2024 (9,21 -> 9,03)
ax.annotate("taglio nominale 2024\n(9,21 → 9,03)", xy=(2024, nom[5]), xytext=(2024.05, 8.35),
            fontsize=8, color="#1f77b4",
            arrowprops=dict(arrowstyle="->", color="#1f77b4"))
ax.set_xlabel("Anno"); ax.set_ylabel("FFO (miliardi €)")
ax.set_title("FFO università statali 2019-2025: nominale vs reale (base 2019)")
ax.legend(fontsize=8, loc="lower right"); ax.grid(alpha=0.25)
ax.set_ylim(7, 9.8)
fig.text(0.01, 0.01,
         "Fonte: decreti MUR di riparto FFO + ADI (nominale); deflatore PIL ed HICP da Eurostat. "
         "Perimetro nominale con rumore (riclassifiche: +671M in base 2025, ADI).",
         fontsize=6, color="gray")
out = os.path.join(HERE, "f2_ffo_reale.png")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out, dpi=140)
print("saved", out)
