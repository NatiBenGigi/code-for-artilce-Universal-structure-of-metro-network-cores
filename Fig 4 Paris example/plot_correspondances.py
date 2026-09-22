"""Plot Paris correspondances vs. number of lines.

Reads metro_correspondances.xlsx from the shared ../data directory.

Draws a scatter plot (black hexagonal markers) with a least-squares line,
in the style of the reference figure. Two fits are computed:
  - through the origin (used for the drawn line, so it starts at (0, 0))
  - ordinary least squares with a free intercept (reported in the console)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
XLSX_PATH = DATA_DIR / "metro_correspondances.xlsx"
OUTPUT_PATH = BASE_DIR / "correspondances_plot.png"

df = pd.read_excel(XLSX_PATH)
# drop the trailing source-note row, which carries no numeric data
df = df.dropna(subset=["number of lines", "correspondances"])

x = df["number of lines"].to_numpy(dtype=float)
y = df["correspondances"].to_numpy(dtype=float)

# Fit 1: least-squares line forced through the origin
slope_origin = np.sum(x * y) / np.sum(x * x)

# Fit 2: ordinary least squares with a free intercept
slope_ols, intercept_ols = np.polyfit(x, y, 1)

print(f"Through-origin fit:  y = {slope_origin:.3f} x")
print(f"Free-intercept fit:  y = {slope_ols:.3f} x + {intercept_ols:.3f}")

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, marker="h", s=80, color="black", zorder=3)

x_line = np.array([0, x.max() + 1])
ax.plot(x_line, slope_origin * x_line, color="black", linewidth=1.5,
        label=f"slope = {slope_origin:.2f}")

ax.set_xlim(0, x.max() + 1)
ax.set_ylim(0, y.max() + 2)
ax.set_xlabel("Number of lines")
ax.set_ylabel("New transfer stations")
ax.legend(frameon=False)

# Match the plain look of the reference figure
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=200)
plt.show()
