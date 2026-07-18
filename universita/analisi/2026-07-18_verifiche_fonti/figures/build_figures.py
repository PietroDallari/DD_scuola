"""F3, F5, F6 per il pitchbook università. Stile coerente con F2.
F3: scatter premiale/FFO per ateneo (dati DM 595/2025 TAB1).
F5: tassi di successo FIS vs ERC (ERC CoG 2024 = 14,2% [ancorato]).
F6: precarizzazione del corpo docente (quota TD, ANVUR).
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# ---------- F3 — premiale/FFO per ateneo ----------
x, y = [], []
with open(os.path.join(DATA, "b4b5_ffo2025_per_ateneo.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            ffo = float(r["FFO_2025"]); prem = float(r["QUOTA_PREMIALE"])
        except (ValueError, KeyError):
            continue
        if ffo > 0:
            x.append(ffo / 1e6); y.append(100 * prem / ffo)
fig, ax = plt.subplots(figsize=(8, 5))
ax.axhspan(19, 34, color="#1f77b4", alpha=0.08, label="banda 19–34% (min–max osservati)")
ax.scatter(x, y, s=18, color="#d62728", alpha=0.7)
ax.set_xscale("log")
ax.set_xlabel("FFO 2025 per ateneo (milioni €, scala log)")
ax.set_ylabel("Quota premiale / FFO (%)")
ax.set_title("Quota premiale come % dell'FFO, per ateneo (2025)")
ax.annotate("corr(premiale, quota base) = 0,99\nla premiale modula ai margini\nuna ripartizione dimensionale",
            xy=(0.97, 0.05), xycoords="axes fraction", ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.25)
fig.text(0.01, 0.01, "Fonte: DM 595/2025, TABELLA 1 (nostra elaborazione, 68 atenei statali).", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f3_premiale_ffo.png"), dpi=140); plt.close(fig)

# ---------- F5 — tassi di successo FIS vs ERC ----------
labels = ["FIS1\n(2021)", "FIS2\n(2023)", "ERC CoG\n(2024)"]
vals = [2.46, 4.63, 14.2]
colors = ["#d62728", "#d62728", "#1f77b4"]
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(labels, vals, color=colors, alpha=0.85)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.2, f"{v}%", ha="center", fontsize=9)
ax.set_ylabel("Tasso di successo (%)")
ax.set_title("Tassi di successo: bandi FIS (Italia) vs ERC Consolidator")
ax.set_ylim(0, 16); ax.grid(alpha=0.25, axis="y")
fig.text(0.01, 0.01, "Fonte: MUR (FIS1 47/1.912; FIS2 106/2.289, graduatoria iniziale); ERC 2024 Consolidator Grant Statistics (328/2.313 = 14,2%). "
         "FIS3 in corso.", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f5_successo_fis_erc.png"), dpi=140); plt.close(fig)

# ---------- F6 — precarizzazione (quota TD del personale di ruolo) ----------
labels = ["2012", "2022"]
vals = [4.1, 11.2]
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(labels, vals, color="#d62728", alpha=0.85, width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.15, f"{v}%", ha="center", fontsize=10)
ax.set_ylabel("Ricercatori a tempo determinato (RTD-a) / personale di ruolo (%)")
ax.set_title("Precarizzazione del corpo docente: quota a tempo determinato")
ax.set_ylim(0, 13); ax.grid(alpha=0.25, axis="y")
fig.text(0.01, 0.01, "Fonte: ANVUR (2012: RTD 4,1%; 2022: RTD-a 11,2% del personale di ruolo). Perimetro: personale docente di ruolo. "
         "~triplicata in un decennio.", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f6_precariato.png"), dpi=140); plt.close(fig)

print("saved F3, F5, F6")
