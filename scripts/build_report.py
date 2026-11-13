"""Fill in Part 3 of WK9AS2.docx with the reproduction write-up and export it to PDF via Word."""
import re, pathlib, copy
import docx
from docx.shared import Inches, Pt

root = pathlib.Path(__file__).resolve().parents[1]
doc = docx.Document(root / "WK9AS2.docx")
anchor = next(p for p in doc.paragraphs if p.text.startswith("50 points"))

def timing(log, name):
    m = re.search(rf"{name}: U=\d+ done in ([\d.]+)s", (root / log).read_text(errors="ignore"))
    return f"{float(m.group(1))/60:.1f} min" if m else "n/a"

def para(text="", style="Normal", bold_prefix=None):
    p = anchor.insert_paragraph_before("", style=style)
    if bold_prefix:
        p.add_run(bold_prefix).bold = True
    p.add_run(text)
    return p

def image(path, width=6.3, caption=None):
    p = anchor.insert_paragraph_before("")
    p.add_run().add_picture(str(path), width=Inches(width))
    if caption:
        c = anchor.insert_paragraph_before("")
        r = c.add_run(caption); r.italic = True; r.font.size = Pt(9)

def table(rows, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    from docx.oxml import parse_xml
    t._tbl.tblPr.append(parse_xml(
        '<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
        "".join(f'<w:{b} w:val="single" w:sz="4" w:color="808080"/>' for b in
                ["top", "left", "bottom", "right", "insideH", "insideV"]) + "</w:tblBorders>"))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j); cell.text = val
            for r in cell.paragraphs[0].runs:
                r.font.size = Pt(9); r.bold = (i == 0)
    anchor._p.addprevious(t._tbl)
    para()

# ---------------------------------------------------------------- content
para(bold_prefix="Reproduction write-up")
para("I cloned the repository and followed the README: create a virtual environment called venv_uapcar, "
     "activate it, run pip install -r requirements.txt, then run the example scripts from the src folder. "
     "The repository has two kinds of examples. The glyph examples write a 3D covariance stability glyph to an .off "
     "mesh file, and the projection examples save the sampling-based PCA projection as a PDF. I reproduced four "
     "visualizations: Fig. 5 (IRIS glyph and projection), Fig. 8 (STUDENT glyph and projection), and the right "
     "panel of Fig. 9 (ANURAN CALLS projection). My scripts, logs, and figures are in my repository.",
     bold_prefix="Setup. ")

para(bold_prefix="Dependencies")
table([
    ["Item", "Authors (README / requirements.txt)", "My machine"],
    ["OS", "Not stated", "Windows 11, PowerShell"],
    ["Python", "3.13.5", "3.10.10"],
    ["numpy", "2.3.1", "2.2.6 (changed, see errors)"],
    ["matplotlib", "3.10.3", "3.10.3"],
    ["contourpy / pillow / others", "pinned in requirements.txt", "same versions"],
    ["Extra (mine)", "-", "pymupdf (crop figures from PDF), python-docx, python-pptx"],
])

para(bold_prefix="Errors and changes")
for b, t in [
    ("Error 1: numpy 2.3.1 would not install. ",
     "pip stopped with \"Could not find a version that satisfies the requirement numpy==2.3.1\" because numpy 2.3.x "
     "requires Python 3.11 or newer and I have Python 3.10. Change: I made requirements_py310.txt, which is the same "
     "file except numpy==2.2.6, the last release that supports 3.10. Everything else installed at the pinned versions, "
     "and the code ran without any code changes."),
    ("Issue 2: Runtime. ",
     "The paper and the example scripts use U = 1,000,000 realizations, and the authors say this takes up to an hour "
     "per figure. On my laptop U = 10,000 already took about 1.3 minutes for IRIS, so 1,000,000 would have taken "
     "around 2 hours per dataset. Change: I used U = 100,000 and kept every other parameter from their examples "
     "(bins = 250, R = 0.2, the same axis limits, scale matrices, colors, and random seed). Their own parameter study "
     "(Fig. 10) shows U = 100,000 looks close to 1,000,000, with slightly noisier contour lines."),
    ("Issue 3: No glyph renderer. ",
     "The glyph example only writes an .off mesh. The 3D renderer the authors used for the paper figures is not in "
     "the repository. Change: I wrote reproduce_glyphs.py, which runs their Glyph class (91 x 181 samples, as the "
     "README recommends) and draws the mesh with matplotlib using the viridis colormap and a similar camera angle."),
    ("Issue 4: Glyph axes in the wrong order. ",
     "My first render did not match the paper. The IRIS glyph was stretched along z instead of lying flat. In "
     "glyph.py there is a commented-out line, \"idx = np.array([2, 1, 0]) # TODO: ask if wanted\", that reverses the "
     "order of the eigenvectors. The paper says the first major eigenvector should map to the z-axis, but the "
     "released code maps it to x. Reversing the eigenvector order is the same as swapping the x and z coordinates of "
     "the finished mesh, so I did that in my script and did not edit their code. After the swap, both glyphs match the "
     "paper. I kept both versions (glyph_*.png and glyph_*_swapped.png)."),
    ("Issue 5: Iris species names shifted by one (bug in the authors' code). ",
     "When I built the interactive page I printed the names that dataset_iris() gives each distribution. They came out as "
     "\"Versicolor, Virginica, Virginica\" instead of \"Setosa, Versicolor, Virginica\". The loader reads iris.csv and, when "
     "the species changes, saves the finished group of flowers under the new species name instead of the old one. The "
     "numbers (means and covariances) are correct and in the right order, so the figures are not affected. Only the "
     "labels are wrong. Change: my interactive page uses the correct names, and I did not edit their code. The ANURAN "
     "loader does not have this problem."),
    ("Minor: ",
     "Matplotlib warned that C:\\Users\\...\\.matplotlib was not writable. Setting MPLCONFIGDIR to a local folder fixed it."),
]:
    para(t, style="List Paragraph", bold_prefix=b)

para(bold_prefix="Results")
table([
    ["Figure", "Script", "Runtime (U = 100,000)", "Match"],
    ["Fig. 5 left – IRIS glyph", "reproduce_glyphs.py", "< 1 min", "Yes, after the x/z swap"],
    ["Fig. 5 right – IRIS projection", "reproduce_projections.py iris", timing("logs_proj_100k.txt", "iris"), "Yes, same clusters, shapes, and orientation"],
    ["Fig. 8 left – STUDENT glyph", "reproduce_glyphs.py", "< 1 min", "Yes, after the x/z swap"],
    ["Fig. 8 right – STUDENT projection", "reproduce_projections.py students", timing("logs_proj_100k.txt", "students"), "Yes, same layout"],
    ["Fig. 9 right – ANURAN projection", "reproduce_projections.py anuran", timing("logs_proj_100k.txt", "anuran"), "Yes, overall shape matches, contours a bit noisier"],
])
para("Overall, the reproduction worked. Every figure I tried shows the same structure as the paper. The differences "
     "are small: the contour lines are slightly wobblier because I used fewer samples, the 3D shading differs because I "
     "used a different renderer, and the glyph axes had to be swapped because of the TODO line in the code.")

para(bold_prefix="Original versus reproduced")
C = root / "figures" / "comparison"
for f, cap in [("fig5_iris_glyph_comparison.png", "Fig. 5 (left): IRIS covariance stability glyph."),
               ("fig5_iris_projection_comparison.png", "Fig. 5 (right): IRIS sampling-based projection."),
               ("fig8_students_comparison.png", "Fig. 8: STUDENT glyph and sampling-based projection."),
               ("fig9_anuran_comparison.png", "Fig. 9 (right): ANURAN CALLS sampling-based projection.")]:
    image(C / f, caption=cap)

para("Mini-presentation: WK9AS2_presentation.pdf in my repository. Website with an interactive version "
     "(rotatable 3D glyphs and an animation of PCA on each random version of the data): "
     "https://ponzek.github.io/CSP5745WK9AS2/ (code: https://github.com/ponzek/CSP5745WK9AS2).", bold_prefix="Extra credit. ")

out = root / "WK9AS2_completed.docx"
doc.save(out)
print("saved", out)
