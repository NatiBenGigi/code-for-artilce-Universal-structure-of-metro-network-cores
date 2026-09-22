"""The E, N, L relation
======================

Produces three figures, all from the self-collected dataset:

  fig_beta_gamma_self_collected.png
      Fig. 5 - beta = E/N (black triangles) and gamma = E/3(N-2)
      (red circles) versus the number of lines L, with E from Eq. (3):
      E = 2N - L. A dotted reference line marks beta = 2.
  fig6_two_minus_beta_vs_L.png
      Fig. 6 - the difference 2 - beta versus the number of lines L.
  fig7_two_minus_beta_vs_N.png
      Fig. 7 - the difference 2 - beta versus the number of nodes N.

Data file, read from the shared ../data directory:
  - metro_data_self_collected.xlsx      (self-collected dataset)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
SELF_XLSX = "metro_data_self_collected.xlsx"


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


def beta_gamma(L, N):
    """E from Eq. (3), then beta = E/N and gamma = E/3(N-2)."""
    E = 2 * N - L
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = np.where(N > 0, E / N, np.nan)
        gamma = np.where(N > 2, E / (3 * (N - 2)), np.nan)
    return E, beta, gamma


def set_window_title(fig, title):
    """Name the figure window (falls back silently on non-GUI backends)."""
    manager = fig.canvas.manager
    if manager is not None:
        manager.set_window_title(title)


def make_figure(L, N, source_label, out_path, window_title):
    """Fig. 5: beta and gamma versus L.

    Black triangle = beta, red circle = gamma; the source is named
    in the legend.
    """
    _, beta, gamma = beta_gamma(L, N)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    set_window_title(fig, window_title)

    ax.scatter(L, beta, marker=">", s=70, color="black",
               label=rf"$\beta = E/N$ - {source_label}")
    ax.scatter(L, gamma, marker="o", s=50, color="red",
               label=rf"$\gamma = E/3(N-2)$ - {source_label}")

    ax.axhline(2.0, color="gray", linewidth=0.8, linestyle=":")
    ax.set_xlim(0, np.nanmax(L) + 1)
    ax.set_ylim(0, 2.1)
    ax.set_title(f"Fig. 5  Parameters $\\gamma$ and $\\beta$ versus the number "
                 f"of lines\n{source_label}", fontsize=10)
    ax.set_xlabel("Number of lines  L")
    ax.set_ylabel(r"Network parameters  $\beta$, $\gamma$")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    print(f"Saved: {out_path}")


# ----------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------
selfc = pd.read_excel(resolve_input_file(SELF_XLSX))
selfc = selfc.dropna(subset=["Lines", "Transfer_stations"])
selfc["N"] = selfc["Transfer_stations"].apply(parse_transfer_stations)


# ----------------------------------------------------------------------
# Fig. 5: beta and gamma versus L, self-collected cities
# ----------------------------------------------------------------------
make_figure(
    selfc["Lines"].to_numpy(dtype=float),
    selfc["N"].to_numpy(dtype=float),
    "self-collected (this work)",
    BASE_DIR / "fig_beta_gamma_self_collected.png",
    "Fig. 5 - beta, gamma vs L - self-collected",
)

# ----------------------------------------------------------------------
# Figs. 6 and 7: the difference 2 - beta versus L and versus N
# (self-collected data only)
# ----------------------------------------------------------------------
# From Eq. (3), 2 - beta = L/N. With Eq. (1), N = 0.27 L^2, one expects
#   2 - beta = 3.7 k / L          (Eq. 6, since 1/0.27 = 3.7)
#   2 - beta = k (3.7 / N)^0.5    (Eq. 7)
# We fit A/L and B/sqrt(N) and convert: k = 0.27*A and k = sqrt(0.27)*B.
C1 = 0.27          # coefficient of Eq. (1): N = 0.27 L^2
COEF = 1.0 / C1    # = 3.7

L_s = selfc["Lines"].to_numpy(dtype=float)
N_s = selfc["N"].to_numpy(dtype=float)
two_minus_beta = L_s / N_s   # = 2 - beta, exact from Eq. (3)


def r_squared(y, y_hat):
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1.0 - ss_res / ss_tot


# --- Fig. 6: 2 - beta versus L, fit A/L ------------------------------
A = np.sum(two_minus_beta / L_s) / np.sum(1.0 / L_s**2)   # LSQ for A/L
k6 = C1 * A
r2_6 = r_squared(two_minus_beta, A / L_s)
print(f"Fig. 6 fit: 2 - beta = {A:.2f}/L  ->  k = {k6:.2f}  (R^2 = {r2_6:.2f})")

fig6, ax6 = plt.subplots(figsize=(6, 4.5))
set_window_title(fig6, "Fig. 6 - 2 - beta vs L - self-collected")
ax6.scatter(L_s, two_minus_beta, marker="h", s=80, color="black", zorder=3)
L_line = np.linspace(2, L_s.max() + 1, 200)
ax6.plot(L_line, A / L_line, color="black", linewidth=1.5,
         label=rf"Eq. (6): $2-\beta = {COEF:.1f}\,k/L$,  $k = {k6:.2f}$")
ax6.set_xlim(0, L_s.max() + 1)
ax6.set_ylim(0, 1.4)
ax6.set_title("Fig. 6  The difference $2-\\beta$ versus the number of lines\n"
              "self-collected data (this work)", fontsize=10)
ax6.set_xlabel("Number of lines  L")
ax6.set_ylabel(r"$2 - \beta$")
ax6.legend(frameon=False)
ax6.spines["top"].set_visible(False)
ax6.spines["right"].set_visible(False)
fig6.tight_layout()
fig6.savefig(BASE_DIR / "fig6_two_minus_beta_vs_L.png", dpi=200)
print(f"Saved: {BASE_DIR / 'fig6_two_minus_beta_vs_L.png'}")

# --- Fig. 7: 2 - beta versus N, fit B/sqrt(N) ------------------------
B = np.sum(two_minus_beta / np.sqrt(N_s)) / np.sum(1.0 / N_s)  # LSQ for B/sqrt(N)
k7 = np.sqrt(C1) * B
r2_7 = r_squared(two_minus_beta, B / np.sqrt(N_s))
print(f"Fig. 7 fit: 2 - beta = {B:.2f}/sqrt(N)  ->  k = {k7:.2f}  (R^2 = {r2_7:.2f})")

fig7, ax7 = plt.subplots(figsize=(6, 4.5))
set_window_title(fig7, "Fig. 7 - 2 - beta vs N - self-collected")
ax7.scatter(N_s, two_minus_beta, marker="h", s=80, color="black", zorder=3)
N_line = np.linspace(2, N_s.max() + 5, 300)
ax7.plot(N_line, B / np.sqrt(N_line), color="black", linewidth=1.5,
         label=rf"Eq. (7): $2-\beta = k\,({COEF:.1f}/N)^{{0.5}}$,  $k = {k7:.2f}$")
ax7.set_xlim(0, N_s.max() + 5)
ax7.set_ylim(0, 1.4)
ax7.set_title("Fig. 7  The difference $2-\\beta$ versus the number of nodes\n"
              "self-collected data (this work)", fontsize=10)
ax7.set_xlabel("Number of nodes  N")
ax7.set_ylabel(r"$2 - \beta$")
ax7.legend(frameon=False)
ax7.spines["top"].set_visible(False)
ax7.spines["right"].set_visible(False)
fig7.tight_layout()
fig7.savefig(BASE_DIR / "fig7_two_minus_beta_vs_N.png", dpi=200)
print(f"Saved: {BASE_DIR / 'fig7_two_minus_beta_vs_N.png'}")

plt.show()
