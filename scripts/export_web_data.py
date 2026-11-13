"""Export data for the interactive web page (docs: index.html).

1. Glyph meshes (from the authors' Glyph class, x/z-swapped like the paper) -> vertices + faces.
2. Per-realization PCA projections using the SAME pipeline as the authors' plot_projection_2D
   (sample all distributions, PCA per realization, align eigenvector signs, project, scale).
   Instead of collapsing them into contour lines, each realization becomes one animation frame.
"""
import sys, json, pathlib
import numpy as np

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "repo" / "src"))
from uapcar import (Glyph, dataset_iris, dataset_students_grades, dataset_anuran_calls,
                    colors_contour_iris, colors_contour_students, colors_contour_anuran)
from uapcar.utils.pca import align_direction_eigenvecs, projection_onto_subspace
from uapcar.utils.sampling import samples_from_distributions

def hexcol(c):
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])

data = {"glyphs": {}, "projections": {}}

# ---- glyphs
for name, loader in [("iris", dataset_iris), ("students", dataset_students_grades)]:
    g = Glyph(loader(), 61, 121, False)          # slightly coarser mesh for the browser
    V = g._vertices[:, [2, 1, 0]]                # same x<->z swap as reproduce_glyphs.py
    data["glyphs"][name] = {"v": np.round(V, 4).T.tolist(), "f": g._faces.T.tolist()}
    print("glyph", name, flush=True)

# ---- realizations
CFG = {
    "iris":     (dataset_iris, colors_contour_iris, np.array([[-1., 0.], [0., 2.]]), 4.0,
                 ["Setosa", "Versicolor", "Virginica"]),
    "students": (dataset_students_grades, colors_contour_students, np.array([[-1., 0.], [0., 1.]]), 15.0,
                 [f"Student {i+1}" for i in range(6)]),
    "anuran":   (dataset_anuran_calls, colors_contour_anuran, np.identity(2), 1.5,
                 ["Bufonidae", "Dendrobatidae", "Hylidae", "Leptodactylidae"]),
}
U = 300
for name, (loader, cols, scale, lim, labels) in CFG.items():
    dists = loader()
    sl, sm = samples_from_distributions(dists, U, 849273076560029784)
    smR = sm.reshape(U, len(dists), dists[0].dim(), order="F")
    mR = smR.mean(axis=1); smRc = smR - mR[:, None, :]
    C = [smRc[i].T @ smRc[i] / smRc.shape[1] for i in range(U)]
    ev = align_direction_eigenvecs([np.linalg.svd(c)[0] for c in C])
    proj = [np.stack([projection_onto_subspace(ev[i][:, :2], (s - mR)[i]) for i in range(U)]) @ scale for s in sl]
    data["projections"][name] = {
        "labels": [str(getattr(d, "name", lab)).replace("Iris-", "").title() if name == "anuran" else lab for d, lab in zip(dists, labels)], "colors": [hexcol(cols[i % len(cols)]) for i in range(len(dists))], "lim": lim,
        "frames": np.round(np.stack(proj, 1), 3).tolist(),   # [U][N][2]
    }
    print("projection", name, flush=True)

out = root / "viz_data.js"
out.parent.mkdir(exist_ok=True)
out.write_text("const VIZ = " + json.dumps(data, separators=(",", ":")) + ";")
print("saved", out, round(out.stat().st_size / 1e6, 2), "MB")
