"""Build side-by-side 'original vs reproduced' comparison images."""
import sys, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

root = pathlib.Path(__file__).resolve().parents[1]
O, R, C = root / "figures/original", root / "figures/reproduced", root / "figures/comparison"
C.mkdir(parents=True, exist_ok=True)
U = sys.argv[1] if len(sys.argv) > 1 else "100000"

PAIRS = {
    "fig5_iris_glyph":      ("Fig. 5 (left) – IRIS covariance stability glyph", O / "fig5_iris_glyph.png", R / "glyph_iris_swapped.png"),
    "fig5_iris_projection": ("Fig. 5 (right) – IRIS sampling-based projection", O / "fig5_iris_projections.png", R / f"projection_iris_U{U}.png"),
    "fig8_students":        ("Fig. 8 – STUDENT glyph (left) and projection (right)", O / "fig8_students.png", [R / "glyph_students_swapped.png", R / f"projection_students_U{U}.png"]),
    "fig9_anuran":          ("Fig. 9 (right) – ANURAN CALLS sampling-based projection", O / "fig9_anuran.png", R / f"projection_anuran_U{U}.png"),
}

for key, (title, orig, rep) in PAIRS.items():
    reps = rep if isinstance(rep, list) else [rep]
    fig, axes = plt.subplots(1, 1 + len(reps), figsize=(5.5 * (1 + len(reps)), 4.6),
                             gridspec_kw={"width_ratios": [1.6 if key == "fig8_students" else 1] + [1] * len(reps)})
    axes[0].imshow(mpimg.imread(orig)); axes[0].set_title("Original (paper PDF)", fontsize=12)
    for ax, r in zip(axes[1:], reps):
        ax.imshow(mpimg.imread(r)); ax.set_title(f"Reproduced ({r.stem})", fontsize=10)
    for ax in axes: ax.axis("off")
    fig.suptitle(title, fontsize=14, weight="bold")
    fig.tight_layout()
    fig.savefig(C / f"{key}_comparison.png", dpi=150)
    print("saved", key)

