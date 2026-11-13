"""Reproduce the sampling-based projections (Fig. 5 right, Fig. 8 right, Fig. 9 right).

Uses the authors' `plot_projection_2D` with the exact parameters from their example scripts,
except that the number of realizations U can be lowered (paper: U = 1,000,000) to keep runtime
reasonable on a laptop.  Usage:  python reproduce_projections.py <iris|students|anuran|all> [U]
"""
import sys, time, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "repo" / "src"))
from uapcar import (dataset_iris, dataset_students_grades, dataset_anuran_calls, plot_projection_2D,
                    colors_contour_iris, colors_contour_students, colors_contour_anuran)

# Parameters copied from the authors' example_projection_*.py files
CONFIGS = {
    "iris":     (dataset_iris, colors_contour_iris, 4.0, np.array([[-1., 0.], [0., 2.]])),
    "students": (dataset_students_grades, colors_contour_students, 15.0, np.array([[-1., 0.], [0., 1.]])),
    "anuran":   (dataset_anuran_calls, colors_contour_anuran, 1.5, np.identity(2)),
}

def run(name, U):
    loader, colors, lim, scale = CONFIGS[name]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim((-lim, lim)); ax.set_ylim((-lim, lim))
    t = time.time()
    plot_projection_2D(loader(), ax, num_realizations=U, bins=250, R=0.2, colors=colors,
                       scale_matrix=scale, modify_ax=True, display_progress=False)
    out = root / "figures" / "reproduced" / f"projection_{name}_U{U}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight"); fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"{name}: U={U} done in {time.time()-t:.1f}s -> {out.name}", flush=True)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    U = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
    for n in (CONFIGS if which == "all" else [which]):
        run(n, U)

