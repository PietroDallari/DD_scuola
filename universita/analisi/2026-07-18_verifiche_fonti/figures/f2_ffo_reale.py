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
ax.plot(anni, real_hicp, "--o", color="#ff7f0e", label="FFO reale (HICP, base 2019) — check", alpha=0.8)
ax.axhspan(min(real_pil), real_pil[2], color="#d62728", alpha=0.05)
ax.annotate("massimo nominale 2025 (9,37 mld)\nma reale sotto il picco 2021-23",
            xy=(2025, nom[-1]), xytext=(2021.2, 9.5), fontsize=8,
            arrowprops=dict(arrowstyle="->", color="gray"))
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
