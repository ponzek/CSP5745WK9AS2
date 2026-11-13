"""Reproduce the covariance stability glyphs (Fig. 5 left, Fig. 8 left).

The authors' code only exports an .OFF mesh (they rendered it in an external 3D tool that is not
part of the repo).  This script computes the glyph with their `Glyph` class (91 x 181 samples,
as recommended in the README), saves the .off, and renders it with matplotlib (viridis colormap
by distance from origin, similar to the paper).
"""
import sys, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "repo" / "src"))
from uapcar import Glyph, dataset_iris, dataset_students_grades

out_dir = root / "figures" / "reproduced"
out_dir.mkdir(parents=True, exist_ok=True)

def render(glyph, name, elev, azim):
    V, F = glyph._vertices, glyph._faces
    tris = V[F]
    r = np.linalg.norm(tris, axis=2).mean(axis=1)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=cm.viridis(r / r.max()), edgecolor="none"))
    lim = np.abs(V).max()
    for i, lab in enumerate("xyz"):  # thin axes like in the paper
        e = np.zeros(3); e[i] = lim * 1.2
        ax.plot(*zip(-e, e), color="k", lw=0.8); ax.text(*(e * 1.05), lab)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    fig.savefig(out_dir / f"glyph_{name}.png", dpi=150, bbox_inches="tight")
    print("rendered", name, flush=True)

for name, loader in [("iris", dataset_iris), ("students", dataset_students_grades)]:
    g = Glyph(loader(), 91, 181, False)
    g.save_off(str(out_dir / f"glyph_{name}"))
    render(g, name, elev=12, azim=45)
    # Variant: glyph.py contains a commented-out "idx = [2, 1, 0]  # TODO: ask if wanted" that
    # reverses the eigenvector order so the FIRST major eigenvector maps to the z-axis, as the
    # paper's text describes.  Reversing U's columns is equivalent to swapping x and z of the
    # final vertices, so we do that here instead of modifying the authors' code.
    g._vertices = g._vertices[:, [2, 1, 0]]
    g.save_off(str(out_dir / f"glyph_{name}_swapped"))
    render(g, name + "_swapped", elev=12, azim=45)
