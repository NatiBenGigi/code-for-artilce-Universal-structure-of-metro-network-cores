"""Calculated N versus observed N
================================

Produces two figures comparing the number of transfer stations
calculated from Eq. (1),

    N = 0.27 L^2 ,

with the mean observed values of N. For every value of L the observed N
is averaged over all systems having that number of lines, following the
reading of Eq. (1) as giving the mean value of N for systems with the
same number of lines.

Each point corresponds to one value of L. Values of L represented by a
single system cannot be averaged and are expected to scatter more; the
script reports how many such values occur in each dataset.

Output:
  fig3a_N_calculated_vs_observed_self_collected.png
  fig3b_N_calculated_vs_observed_Derrible2010.png

Data files are read from the shared ../data directory,
both with columns City, Lines, Transfer_stations:
  - metro_data_self_collected.xlsx      (self-collected dataset)
  - metro_data_Derrible2010_Table3.xlsx (Table 3 of Derrible & Kennedy
                                         2010)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
SELF_XLSX = "metro_data_self_collected.xlsx"
ARTICLE_XLSX = "metro_data_Derrible2010_Table3.xlsx"

C1 = 0.27      # prefactor of Eq. (1): N = 0.27 L^2


def resolve_input_file(filename):
    """Locate a data file in the shared ../data directory."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Could not find {filename!r} in {DATA_DIR}")
    return path


def parse_transfer_stations(value):
    """Parse a transfer-station count; ranges like '50-70' -> midpoint."""
    if isinstance(value, str) and "-" in value:
        lo, hi = value.split("-")
        return (float(lo) + float(hi)) / 2
    return float(value)


def set_window_title(fig, title):
    """Name the figure window (falls back silently on non-GUI backends)."""
    manager = fig.canvas.manager
    if manager is not None:
        manager.set_window_title(title)


def r_squared(y, y_hat):
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1.0 - ss_res / ss_tot


def load_dataset(filename):
    df = pd.read_excel(resolve_input_file(filename))
    df = df.dropna(subset=["Lines", "Transfer_stations"])
    df["N"] = df["Transfer_stations"].apply(parse_transfer_stations)
    return df


def make_figure(df, source_label, out_path, window_title):
    """Calculated N (Eq. 1) versus the mean observed N, grouped by L."""
    grouped = df.groupby("Lines")["N"].agg(["mean", "size"])
    L = grouped.index.to_numpy(dtype=float)
    N_obs = grouped["mean"].to_numpy(dtype=float)
    n_systems = grouped["size"].to_numpy(dtype=int)
    N_calc = C1 * L**2

    n_single = int(np.sum(n_systems == 1))

    # Slope of calculated vs. observed, forced through the origin
    slope = np.sum(N_obs * N_calc) / np.sum(N_obs**2)
    r2 = r_squared(N_calc, slope * N_obs)
    print(f"{source_label}: slope = {slope:.2f}, R^2 = {r2:.2f}, "
          f"{n_single} of {len(L)} values of L are represented by a "
          f"single system")

    fig, ax = plt.subplots(figsize=(6, 4.5))
    set_window_title(fig, window_title)

    lim = max(N_obs.max(), N_calc.max()) * 1.15
    ax.plot([0, lim], [0, lim], color="red", linewidth=1.2,
            label="equality, slope 1")
    ax.scatter(N_obs, N_calc, marker="*", s=150, facecolors="none",
               edgecolors="black", linewidths=1.1, zorder=3,
               label=r"$\langle N \rangle$ averaged over systems with "
                     r"the same $L$")

    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_title(source_label, fontsize=11)
    ax.set_xlabel(r"$\langle N \rangle$  observed")
    ax.set_ylabel(r"$N$ calculated from Eq. (1)")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    print(f"Saved: {out_path}")


# ----------------------------------------------------------------------
# Fig. 3a: self-collected data
# ----------------------------------------------------------------------
make_figure(
    load_dataset(SELF_XLSX),
    "self-collected dataset",
    BASE_DIR / "fig3a_N_calculated_vs_observed_self_collected.png",
    "Fig. 3a - calculated vs observed N - self-collected",
)

# ----------------------------------------------------------------------
# Fig. 3b: Derrible & Kennedy (2010), Table 3
# ----------------------------------------------------------------------
make_figure(
    load_dataset(ARTICLE_XLSX),
    "Derrible & Kennedy (2010), Table 3",
    BASE_DIR / "fig3b_N_calculated_vs_observed_Derrible2010.png",
    "Fig. 3b - calculated vs observed N - Derrible & Kennedy 2010",
)

plt.show()
