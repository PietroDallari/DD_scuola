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
x, y, escl = [], [], 0
with open(os.path.join(DATA, "b4b5_ffo2025_per_ateneo.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            ffo = float(r["FFO_2025"]); prem = float(r["QUOTA_PREMIALE"])
        except (ValueError, KeyError):
            continue
        if ffo > 0 and prem > 0:
            x.append(ffo / 1e6); y.append(100 * prem / ffo)
        elif ffo > 0:
            escl += 1  # atenei senza quota premiale 2025 (SSM2, Trento2)
fig, ax = plt.subplots(figsize=(8, 5))
ax.axhspan(18.6, 34.2, color="#1f77b4", alpha=0.08, label="banda 18,6–34,2% (min–max tra gli atenei con quota premiale)")
ax.scatter(x, y, s=18, color="#d62728", alpha=0.7)
ax.set_xscale("log")
ax.set_xlabel("FFO 2025 per ateneo (milioni €, scala log)")
ax.set_ylabel("Quota premiale / FFO (%)")
ax.set_title(f"Quota premiale come % dell'FFO, per ateneo (2025; {len(x)} atenei con premiale)")
ax.annotate("corr(premiale, quota base) = 0,99\nla premiale modula ai margini\nuna ripartizione dimensionale",
            xy=(0.97, 0.05), xycoords="axes fraction", ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.8))
ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.25); ax.set_ylim(0, 36)
fig.text(0.01, 0.01, f"Fonte: DM 595/2025, TABELLA 1 (nostra elaborazione). Esclusi {escl} atenei di nuova istituzione/ordinamento speciale senza quota premiale 2025 (SSM2, Trento2).", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f3_premiale_ffo.png"), dpi=140); plt.close(fig)

# ---------- F5 — tassi di successo FIS vs ERC ----------
labels = ["FIS1\n(2021)", "FIS2\n(2023)", "FIS3\n(2024)", "ERC CoG\n(2024)"]
vals = [2.46, 4.63, 6.52, 14.2]
colors = ["#d62728", "#d62728", "#d62728", "#1f77b4"]
fig, ax = plt.subplots(figsize=(7.5, 5))
bars = ax.bar(labels, vals, color=colors, alpha=0.85)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.2, f"{v}%", ha="center", fontsize=9)
ax.set_ylabel("Tasso di successo (%)")
ax.set_title("Tassi di successo: bandi FIS (Italia) vs ERC Consolidator")
ax.set_ylim(0, 16); ax.grid(alpha=0.25, axis="y")
fig.text(0.01, 0.01, "Fonte: MUR (FIS1 47/1.912; FIS2 106/2.289; FIS3 326/oltre 5.000, graduatorie iniziali, revoche a parte); "
         "ERC 2024 Consolidator Grant Statistics (328/2.313 = 14,2%).", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f5_successo_fis_erc.png"), dpi=140); plt.close(fig)

# ---------- F6 — precarizzazione (quota TD sul TOTALE docenti, perimetro identico) ----------
labels = ["2012", "2022"]
vals = [4.1, 21.1]        # TD (RTD a+b) / totale docenti; denominatore identico
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(labels, vals, color="#d62728", alpha=0.85, width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v}%", ha="center", fontsize=10)
ax.text(1, 10.1, "(soli RTD-a: 10,1%)", ha="center", fontsize=7, color="gray")
ax.set_ylabel("Docenti a tempo determinato (RTD a+b) sul totale del personale docente (%)")
ax.set_title("Precarizzazione del corpo docente: quota a tempo determinato")
ax.set_ylim(0, 24); ax.grid(alpha=0.25, axis="y")
fig.text(0.01, 0.01, "Fonte: ANVUR. Numeratore = RTD a+b; denominatore = totale docenti (ruolo a t.i. + TD), perimetro identico nei due anni "
         "(2012: 2.356/57.285; 2022: 12.728/60.333). Con i soli RTD-a il 2022 = 10,1% (misura prudente).", fontsize=6, color="gray")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(HERE, "f6_precariato.png"), dpi=140); plt.close(fig)

print("saved F3, F5, F6")
