"""Build the mini-presentation, written for people outside computer science / data science."""
import pathlib
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

root = pathlib.Path(__file__).resolve().parents[1]
C, R = root / "figures" / "comparison", root / "figures" / "reproduced"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
LILAC, DEEP, GOLD, CREAM, INK = (RGBColor(0xF4, 0xEC, 0xFB), RGBColor(0x6A, 0x3F, 0xA0),
                                RGBColor(0xE8, 0xB9, 0x2E), RGBColor(0xFD, 0xF3, 0xCF), RGBColor(0x3E, 0x2F, 0x52))
FONT = "Segoe UI"

def base(title):
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = LILAC
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.3), prs.slide_width, Inches(0.2))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()
    if title:
        tf = s.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(1)).text_frame
        tf.word_wrap = True
        r = tf.paragraphs[0].add_run(); r.text = title
        r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(34), True, DEEP, FONT
    return s

def text(s, lines, x, y, w, h, size=22):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        bold, rest = (line.split("|", 1) if "|" in line else ("", line))
        if bold:
            rb = p.add_run(); rb.text = bold; rb.font.bold = True
            rb.font.size, rb.font.color.rgb, rb.font.name = Pt(size), DEEP, FONT
        rr = p.add_run(); rr.text = rest; rr.font.size, rr.font.color.rgb, rr.font.name = Pt(size), INK, FONT

def callout(s, msg, y=6.15):
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(y), Inches(12.1), Inches(0.95))
    box.fill.solid(); box.fill.fore_color.rgb = CREAM; box.line.color.rgb = GOLD; box.line.width = Pt(2)
    tf = box.text_frame; tf.word_wrap = True
    r = tf.paragraphs[0].add_run(); r.text = "\U0001F4A1  " + msg
    r.font.size, r.font.color.rgb, r.font.name, r.font.bold = Pt(19), INK, FONT, True

def pic(s, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Inches(w)
    if h: kw["height"] = Inches(h)
    return s.shapes.add_picture(str(path), Inches(x), Inches(y), **kw)

# 1 - Title
s = base("")
text(s, ["|\U0001F338 Can you trust a chart made from fuzzy data?"], 0.8, 2.0, 11.8, 1.2, size=44)
text(s, ["Re-creating the pictures from the research paper \u201cUncertainty-Aware PCA Revisited\u201d (IEEE VIS 2025)",
         "Karina Ponze \u00b7 CPS 5745 \u00b7 Week 9"], 0.8, 3.4, 11.8, 2, size=22)

# 2 - Big idea
s = base("The big idea, in everyday words")
text(s, [
    "Flattening data is like taking a photo. |A photo turns a 3D object into a flat 2D picture. "
    "A popular method called PCA does the same for data with many columns, so we can see it on a screen.",
    "Real data is fuzzy. |Measurements are never exact. A student\u2019s grade can vary from test to test, "
    "and two flowers of the same kind aren\u2019t identical.",
    "The question: |if the data is a little fuzzy, can we trust the flat picture? Or would it look totally "
    "different if the data wiggled a bit?",
], 0.6, 1.4, 12.1, 4.6)
callout(s, "Think of it like a group photo where people won\u2019t stand still. Is the photo still a fair picture of the group?")

# 3 - What researchers made
s = base("What the researchers came up with")
text(s, [
    "\U0001F52E  Picture 1: The \u201cstability blob.\u201d |A 3D shape that shows how steady the flattening is. "
    "Thin spikes mean steady. Wide, flat parts mean shaky.",
    "\U0001F3AF  Picture 2: The \u201crings.\u201d |The computer invents many slightly different versions of the data "
    "(they used one million) and takes a \u201cphoto\u201d of each. The rings show where each item usually lands, "
    "a bit like the bullseye rings on a dartboard.",
], 0.6, 1.4, 12.1, 4.4)
callout(s, "Small, separate rings mean you can trust the picture. Big, overlapping rings mean be careful.")

# 4 - What I did
s = base("What I did")
text(s, [
    "1. |Found the researchers\u2019 code, which they shared publicly on GitHub.",
    "2. |Followed their setup instructions on my Windows laptop.",
    "3. |Ran their code on the same three datasets from the paper:",
    "      \U0001F33A  Iris flowers (3 kinds)    \U0001F393  Student grades (6 students)    \U0001F438  Frog calls (4 frog families)",
    "4. |Put my pictures next to the paper\u2019s pictures to check if they match.",
], 0.6, 1.4, 12.1, 4.6)
callout(s, "Re-creating someone\u2019s results is how science checks itself. If it works for me, it\u2019s more believable.")

# 5 - Hiccups
s = base("Bumps along the way (and how I fixed them)")
text(s, [
    "\U0001F527  Wrong version. |The code needed a newer Python than I had, so one add-on wouldn\u2019t install. "
    "I used the closest version that works with my Python.",
    "\u23F3  Too slow. |One million versions would take about 2 hours per picture. I used 100,000. "
    "The paper itself shows this looks almost the same.",
    "\U0001F9E9  Missing piece. |The code made the 3D blob but had no way to show it, so I wrote my own viewer.",
    "\U0001F504  Sideways blob. |My blobs were tipped on their side. A line in the code marked \u201cTODO: ask if wanted\u201d "
    "fixes it, and turning it on made the blobs match the paper.",
    "\U0001F3F7\uFE0F  Mixed-up names. |The code labels the 3 iris flower types in the wrong order. The pictures are "
    "still right; only the name tags were off.",
], 0.6, 1.3, 12.1, 5.8, size=19)

# 6-9 - Results
s = base("\U0001F33A Iris flowers: the stability blob")
pic(s, C / "fig5_iris_glyph_comparison.png", 0.6, 1.3, w=12.1)
callout(s, "Left: the paper. Right: mine. Same long, flat shape, so the flower picture is less steady than it looks.", y=6.2)

s = base("\U0001F33A Iris flowers: where each kind lands")
pic(s, C / "fig5_iris_projection_comparison.png", 2.2, 1.2, h=4.9)
callout(s, "Blue (Setosa) sits alone, so it\u2019s easy to tell apart. Orange and green overlap, so those two kinds get mixed up.", y=6.2)

s = base("\U0001F393 Student grades")
pic(s, C / "fig8_students_comparison.png", 0.6, 1.4, w=12.1)
callout(s, "Thin spike plus a wide flat disc: the main pattern is steady, but the second one isn\u2019t. "
           "So the students\u2019 positions are shakier than older methods showed.", y=5.9)

s = base("\U0001F438 Frog calls")
pic(s, C / "fig9_anuran_comparison.png", 0.9, 1.2, h=4.9)
callout(s, "All the rings pile on top of each other. A normal flat chart of this data would be misleading!", y=6.2)

# 10 - Bonus interactive
s = base("\u2728 Bonus: I made it move")
text(s, [
    "The paper only has still pictures, so I built a website where you can:",
    "\U0001F504  |Spin the 3D blob with your mouse",
    "\U0001F3AC  |Watch the \u201cphoto\u201d change, one version of the data at a time. Steady items barely move, and shaky ones jump around.",
    "\U0001F517  |ponzek.github.io/CSP5745WK9AS2",
], 0.6, 1.4, 6.6, 4.6, size=21)
pic(s, R / "glyph_students_swapped.png", 7.4, 1.3, h=4.6)

# 11 - Takeaways
s = base("What I learned")
text(s, [
    "\u2705  |It worked. All 4 pictures I tried match the paper.",
    "\U0001F4CF  |The small differences came from using fewer versions (100,000 instead of 1,000,000) and a different 3D viewer.",
    "\U0001F9E0  |Big lesson: a chart can look sure of itself even when the data behind it is fuzzy. Showing the fuzziness helps people "
    "avoid wrong conclusions.",
    "\U0001F91D  |The researchers shared their code and data, which made this possible. That\u2019s what good science looks like.",
], 0.6, 1.4, 12.1, 4.6)
callout(s, "Thank you! \U0001F49C  Questions?")

out = root / "WK9AS2_presentation.pptx"
prs.save(out); print("saved", out)
