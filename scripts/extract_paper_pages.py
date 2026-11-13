"""Render every page of the paper PDF to PNG so the original figures can be cropped/compared."""
import fitz, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
out = root / "figures" / "original"
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(root / "Friesecke_2026_VIS.pdf")
for i, page in enumerate(doc):
    page.get_pixmap(dpi=110).save(out / f"page_{i+1:02d}.png")
    for line in page.get_text().splitlines():
        if line.strip().startswith("Fig"):
            print(i + 1, line.strip()[:110])

