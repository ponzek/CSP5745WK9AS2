"""Export the completed .docx and .pptx to PDF using Microsoft Office (COM automation)."""
import pathlib, win32com.client  # pywin32

root = pathlib.Path(__file__).resolve().parents[1]
word = win32com.client.DispatchEx("Word.Application"); word.Visible = False
d = word.Documents.Open(str(root / "WK9AS2_final.docx"), ReadOnly=True)
d.SaveAs(str(root / "WK9AS2.pdf"), FileFormat=17); d.Close(False); word.Quit()
print("saved WK9AS2.pdf")

ppt = win32com.client.DispatchEx("PowerPoint.Application")
p = ppt.Presentations.Open(str(root / "WK9AS2_presentation.pptx"), WithWindow=False)
p.SaveAs(str(root / "WK9AS2_presentation.pdf"), 32); p.Close(); ppt.Quit()
print("saved WK9AS2_presentation.pdf")

