"""
Plot N (transfer stations) versus L (metro lines) for two datasets,
both read from the shared ../data directory:
  1. metro_data_Derrible2010_Table3.xlsx  - Table 3 of Derrible & Kennedy (2010),
     "Characterizing metro networks: state, form, and structure"
  2. metro_data_self_collected.xlsx       - dataset collected by ourselves

Only systems with L >= 3 are retained, since below L = 3 a metro system
cannot be described as a network.

For each dataset one standalone figure is produced:
  Fig. 2a  -  the data points and the least-squares fit N = a L^2

Requires: pandas, numpy, scipy, matplotlib, openpyxl
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

FILES = [
    ("metro_data_Derrible2010_Table3.xlsx",
     "Derrible & Kennedy (2010), Table 3"),
    ("metro_data_self_collected.xlsx",
     "Self-collected dataset"),
]

X_LABEL = "L  (number of lines in the city's metro system)"
Y_LABEL = "N  (number of transfer stations)"


def parse_n(value):
    """Return a numeric N. A range such as '50-70' becomes its midpoint."""
    if isinstance(value, (int, float)):
        return float(value)
    m = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", str(value))
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return (lo + hi) / 2.0
    return float(value)


def load_table(path):
    df = pd.read_excel(DATA_DIR / path)
    df = df.dropna(subset=["City"])
    # drop any trailing source-note rows that lack numeric data
    df = df[pd.to_numeric(df["Lines"], errors="coerce").notna()]
    df = df[df["Lines"].astype(float) >= 3]  # keep only systems with L >= 3
    L = df["Lines"].astype(float).to_numpy()
    N = df["Transfer_stations"].map(parse_n).to_numpy()
    return L, N


def fit_prefactor(L, N):
    """Least-squares fit of N = a L^2 (exponent fixed at 2). Returns a."""
    quad = lambda x, a: a * x ** 2
    (a_fit,), _ = curve_fit(quad, L, N)
    return a_fit


def make_plot(L, N, a_fit, title, outfile):
    """Fig. 2a: N versus L, with the fitted quadratic curve."""
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    ax.plot(L, N, "o", color="black", markersize=6, label="data")

    xs = np.linspace(0, max(L) * 1.15, 300)
    ax.plot(xs, a_fit * xs ** 2, "-", color="red", linewidth=1.5,
            label=rf"$N = {a_fit:.2f}\,L^2$ (fit)")

    ax.set_xlabel(X_LABEL, fontsize=11)
    ax.set_ylabel(Y_LABEL, fontsize=11)
    ax.set_title(title, fontsize=11)
    ax.set_xlim(0, max(L) * 1.2)
    ax.set_ylim(0, max(N) * 1.2)
    ax.tick_params(direction="in")
    ax.legend(fontsize=9, frameon=False)
    fig.tight_layout()
    fig.savefig(outfile, dpi=200)
    print(f"{title}:  fitted prefactor a = {a_fit:.3f}  ->  saved {outfile}")
    plt.show()
    plt.close(fig)


def main():
    for fname, title in FILES:
        L, N = load_table(fname)
        a_fit = fit_prefactor(L, N)

        make_plot(L, N, a_fit, title,
                  BASE_DIR / fname.replace(".xlsx", "_plot.png"))


if __name__ == "__main__":
    main()
