"""Build the mini-presentation (PowerPoint) for the reproduced visualizations."""
import pathlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

root = pathlib.Path(__file__).resolve().parents[1]
C = root / "figures" / "comparison"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def slide(title, bullets=None, img=None, img_top=1.3, img_h=5.9):
    s = prs.slides.add_slide(BLANK)
    tb = s.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.9)).text_frame
    tb.text = title; tb.paragraphs[0].runs[0].font.size = Pt(32); tb.paragraphs[0].runs[0].font.bold = True
    tb.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    if bullets:
        left = 0.6 if not img else 0.5
        box = s.shapes.add_textbox(Inches(left), Inches(1.3), Inches(12.2 if not img else 4.3), Inches(5.8)).text_frame
        box.word_wrap = True
        for i, b in enumerate(bullets):
            p = box.paragraphs[0] if i == 0 else box.add_paragraph()
            p.text = "• " + b; p.runs[0].font.size = Pt(20 if not img else 16); p.space_after = Pt(10)
    if img:
        if bullets:
            s.shapes.add_picture(str(img), Inches(4.9), Inches(img_top), width=Inches(8.1))
        else:
            pic = s.shapes.add_picture(str(img), Inches(0.5), Inches(img_top), height=Inches(img_h))
            if pic.width > Inches(12.3):
                ratio = Inches(12.3) / pic.width; pic.width = Inches(12.3); pic.height = int(pic.height * ratio)
    return s

slide("Reproducing \u201cUncertainty-Aware PCA Revisited\u201d", [
    "Friesecke, Braune, R\u00f6ssl, Theisel \u2013 IEEE VIS 2025",
    "Problem: classic PCA ignores uncertainty in data points; prior uncertainty-aware PCA (G\u00f6rtler et al. 2019) "
    "ignored the uncertainty of the global covariance itself",
    "Contributions: (1) covariance stability glyph \u2013 shows how stable the top-3 eigenvectors are; "
    "(2) sampling-based projection \u2013 run PCA on U random realizations and draw density contours",
    "Code: github.com/lfriesecke/uncertainty-aware-pca-revisited",
])
slide("Setup & what broke", [
    "README: python -m venv venv_uapcar \u2192 pip install -r requirements.txt \u2192 python example_*.py",
    "Error: numpy==2.3.1 requires Python \u2265 3.11 (I have 3.10.10) \u2192 pinned numpy 2.2.6, no code changes needed",
    "Runtime: U = 1,000,000 \u2248 2 h per dataset on my laptop \u2192 used U = 100,000 (paper\u2019s Fig. 10 shows this is close)",
    "Glyph code only exports an .OFF mesh \u2192 wrote my own matplotlib 3D renderer",
    "Glyph axes didn\u2019t match the paper \u2192 found commented-out \u201cidx = [2,1,0]  # TODO: ask if wanted\u201d in glyph.py; "
    "applying it (x\u2194z swap) reproduces the paper exactly",
])
slide("Fig. 5 \u2013 IRIS glyph", ["Long flat lobes and only small bumps: the eigenvectors are fairly unstable in the xy-plane",
                                "Shape matches the original; only the shading differs"],
      img=C / "fig5_iris_glyph_comparison.png", img_top=1.6)
slide("Fig. 5 \u2013 IRIS projection", None, img=C / "fig5_iris_projection_comparison.png")
slide("Fig. 8 \u2013 STUDENT glyph + projection", None, img=C / "fig8_students_comparison.png", img_top=1.6, img_h=4.5)
slide("Fig. 9 \u2013 ANURAN CALLS projection", None, img=C / "fig9_anuran_comparison.png")
slide("Takeaways", [
    "All 4 visualizations reproduced: same structure, clusters, orientation",
    "Differences: noisier contours (U=100k vs 1M), different 3D renderer, x/z axis order in released glyph code",
    "Lesson: pinned requirements can block older Pythons; check for leftover TODOs when results look \u201crotated\u201d",
    "Reproducibility score: high \u2013 public code + bundled datasets + fixed random seeds",
])
out = root / "WK9AS2_presentation.pptx"
prs.save(out); print("saved", out)

