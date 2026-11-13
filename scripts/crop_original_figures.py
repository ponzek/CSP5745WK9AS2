"""Crop the original figures out of the paper PDF at high resolution (coordinates in PDF points)."""
import pymupdf, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
out = root / "figures" / "original"
doc = pymupdf.open(root / "Friesecke_2026_VIS.pdf")
CROPS = {  # name: (page index, x0, y0, x1, y1)
    "fig5_iris_glyph":          (6, 312, 50, 452, 112),
    "fig5_iris_projections":    (6, 450, 48, 568, 110),
    "fig8_students":            (8, 54, 305, 306, 372),
    "fig9_anuran":              (8, 315, 49, 568, 134),
}
for name, (p, *r) in CROPS.items():
    doc[p].get_pixmap(dpi=300, clip=pymupdf.Rect(*r)).save(out / f"{name}.png")
    print("saved", name)

