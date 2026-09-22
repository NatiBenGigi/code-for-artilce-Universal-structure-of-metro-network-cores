# Universal structure of metro network cores

Code and data for the article *"Universal structure of metro network cores"*.

Every figure in the article is produced by one of the four scripts below.
Running a script reads its data from `data/` and writes its PNGs into the
script's own folder. The figures themselves are not stored in this
repository — they are regenerated from the data on every run.

## Data

All three datasets live in [`data/`](data/):

| File | Contents |
|---|---|
| `metro_data_Derrible2010_Table3.xlsx` | The 33 metro systems of Table 3 of Derrible & Kennedy (2010), *Characterizing metro networks: state, form, and structure*. Columns: `City`, `Lines`, `Transfer_stations`. |
| `metro_data_self_collected.xlsx` | Metro systems collected independently by the authors. Same columns. London is recorded as the range `50-70`; the scripts use its midpoint. |
| `metro_correspondances.xlsx` | Historical growth of the Paris Metro, compiled from RATP and Wikipedia. Columns: `ligne`, `number of lines`, `correspondances`, `Ouverture`. `correspondances` is the number of *new* transfer stations created when that line opened. |

Each file ends with a row naming its source; the scripts drop it.

Throughout, **L** is the number of lines, **N** the number of transfer
stations (network nodes) and **E** the number of links.

## Scripts

| Folder | Script | Produces |
|---|---|---|
| `Fig 2_a_b The N_L relationship` | `plot_metro_NL.py` | Fig. 2a and 2b — N against L for each dataset, with the least-squares fit N = a·L². Only systems with L ≥ 3 are kept, since below three lines a metro cannot be described as a network. |
| `Fig 3_a_b The calculated N_L relationship` | `N_calculated_vs_observed.py` | Fig. 3a and 3b — N calculated from Eq. (1), N = 0.27·L², against the mean observed N. For each value of L the observed N is averaged over all systems with that many lines. |
| `Fig 4 Paris example` | `plot_correspondances.py` | Fig. 4 — new transfer stations against the number of lines, over the history of the Paris Metro. |
| `Fig 5_6_7 The E N L` | `The_E_N_L_relation.py` | Figs. 5, 6 and 7 — β = E/N and γ = E/3(N−2) against L, then the difference 2 − β against L and against N. Uses E from Eq. (3), E = 2N − L. Self-collected data. |

## Running

Requires Python 3 with:

```
pip install -r requirements.txt
```

Then run any script from anywhere; each locates `data/` relative to its own
file:

```
python3 "Fig 2_a_b The N_L relationship/plot_metro_NL.py"
python3 "Fig 3_a_b The calculated N_L relationship/N_calculated_vs_observed.py"
python3 "Fig 4 Paris example/plot_correspondances.py"
python3 "Fig 5_6_7 The E N L/The_E_N_L_relation.py"
```

Each script prints its fitted parameters to the console and opens the figures
in a window. To run without a display, set `MPLBACKEND=Agg`; the PNGs are
still written.

## Fitted values

Reproduced by the scripts above:

| Quantity | Value |
|---|---|
| Prefactor a in N = a·L², Derrible & Kennedy (2010) | 0.277 |
| Prefactor a in N = a·L², self-collected | 0.263 |
| Paris, new transfer stations per line (through origin) | 0.538 |
| k in Eq. (6), 2 − β = 3.7k/L | 0.81 |
| k in Eq. (7), 2 − β = k(3.7/N)^0.5 | 0.96 |

## Licence

Released under the GNU General Public License v3.0 — see [`LICENSE`](LICENSE).
