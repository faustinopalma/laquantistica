"""Recreate the Millikan charge-measurement histogram (Fig. after the sample table)
matching the scanned original: red-outlined bars clustered at multiples of
1.6e-19 C, axes drawn as arrows (Origin style). Output SVG.
Usage: python tools/_histogram.py <out.svg>
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["svg.fonttype"] = "path"  # embed text as paths so it renders identically everywhere

# (charge q in 1e-19 C, frequency) — deduced from the scan; groups of 3,3,2,2,2; sums to 50
bars = [(1.35, 1), (1.55, 4), (1.75, 7),
        (3.00, 5), (3.20, 6), (3.40, 1),
        (4.55, 5), (4.75, 3),
        (6.25, 4), (6.45, 5),
        (7.85, 4), (8.05, 5)]
assert sum(f for _, f in bars) == 50

fig, ax = plt.subplots(figsize=(7.2, 3.1))
xs = [q for q, _ in bars]
hs = [f for _, f in bars]
ax.bar(xs, hs, width=0.13, facecolor="white", edgecolor="#7a1420", linewidth=1.3, zorder=3)

ax.set_xlim(0, 9.0)
ax.set_ylim(0, 8.2)
ax.set_xticks([0, 1.6, 3.2, 4.8, 6.4, 8.0])
ax.set_xticklabels(["0,0", "1,6", "3,2", "4,8", "6,4", "8,0"])
ax.set_yticks([0, 2, 4, 6, 8])
ax.tick_params(direction="out", length=4)

for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(1.1)
# axis arrowheads
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize=7)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize=7)

# axis labels placed like the original
ax.text(9.0, -1.35, r"Carica $q$ $(10^{-19}\,$C)", va="top", ha="right", fontsize=12, clip_on=False)
ax.text(-0.15, 8.3, "Frequenza", va="bottom", ha="left", fontsize=12)

fig.subplots_adjust(left=0.07, right=0.98, top=0.93, bottom=0.24)
fig.savefig(sys.argv[1])
print("saved", sys.argv[1])
