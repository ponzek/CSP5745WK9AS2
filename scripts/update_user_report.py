"""Add the Iris-label bug + extra-credit line to Karina's own WK9AS2.docx (keeps her formatting)."""
import copy, pathlib, docx

root = pathlib.Path(__file__).resolve().parents[1]
doc = docx.Document(root / "WK9AS2.docx")
ps = doc.paragraphs
model = next(p for p in ps if p.text.startswith("The glyphs came out rotated"))

def clone_after(ref, bold, rest):
    new = copy.deepcopy(ref._p); ref._p.addnext(new)
    p = docx.text.paragraph.Paragraph(new, ref._parent)
    runs = p.runs
    for r in runs[2:]: r._r.getparent().remove(r._r)
    if len(runs) >= 2:
        runs[0].text, runs[1].text = bold, rest
        runs[0].bold, runs[1].bold = True, False
    else:
        runs[0].text = bold + rest
    return p

if not any("Mixed-up iris names" in p.text for p in ps):
    clone_after(model, "Mixed-up iris names (a bug in the authors\u2019 code). ",
        "When I printed the species names that the code attaches to the Iris data, they came out as \u201cVersicolor, "
        "Virginica, Virginica\u201d instead of \u201cSetosa, Versicolor, Virginica.\u201d The loader saves each group of "
        "flowers under the next species\u2019 name. The numbers are correct and in the right order, so the pictures are "
        "not affected; only the name labels are wrong. Change: I used the correct names on my interactive page and "
        "did not edit their code.")

last = next(p for p in doc.paragraphs if p.text.startswith("You can obtain extra points"))
if not any(p.text.startswith("Extra credit:") for p in doc.paragraphs):
    new = copy.deepcopy(last._p); last._p.addnext(new)
    p = docx.text.paragraph.Paragraph(new, last._parent)
    for r in p.runs[1:]: r._r.getparent().remove(r._r)
    p.runs[0].text = ("Extra credit: mini-presentation (WK9AS2_presentation.pdf) and an interactive website where you "
                      "can spin the 3D glyphs and watch the PCA picture change for each random version of the data: "
                      "https://ponzek.github.io/CSP5745WK9AS2/")

out = root / "WK9AS2_final.docx"
doc.save(out); print("saved", out)
