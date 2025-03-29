import fitz  # PyMuPDF
import argparse

# Argumente parsen
parser = argparse.ArgumentParser(description="PDF-Seitenbereiche extrahieren und neu anordnen.")
parser.add_argument("-alterName", type=str, default="adhs_ver.pdf", help="Name der Eingabedatei (PDF)")
parser.add_argument("-neuerName", type=str, default="neu.pdf", help="Name der Ausgabedatei (PDF)")
parser.add_argument("-x0", type=float, default=100.0, help="Linke Koordinate des Ausschnitts")
parser.add_argument("-y0", type=float, default=100.0, help="Obere Koordinate des Ausschnitts")
parser.add_argument("-x1", type=float, default=500.0, help="Rechte Koordinate des Ausschnitts")
parser.add_argument("-y1", type=float, default=380.0, help="Untere Koordinate des Ausschnitts")
parser.add_argument("-scale", type=float, default=2.0, help="Skalierungsfaktor")

args = parser.parse_args()

# PDF öffnen
doc = fitz.open(args.alterName)

# Neues PDF-Dokument erstellen
new_doc = fitz.open()

# Clip-Bereich und Zoom-Matrix
clip_rect = fitz.Rect(args.x0, args.y0, args.x1, args.y1)
zoom_matrix = fitz.Matrix(args.scale, args.scale)

# Immer zwei Seiten gleichzeitig verarbeiten
for i in range(0, len(doc), 2):
    page_width = clip_rect.width * args.scale
    page_height = clip_rect.height * args.scale * 2
    new_page = new_doc.new_page(width=page_width, height=page_height)

    for j in range(2):
        if i + j < len(doc):
            page = doc[i + j]
            pix = page.get_pixmap(matrix=zoom_matrix, clip=clip_rect)

            y_offset = j * clip_rect.height * args.scale
            rect = fitz.Rect(0, y_offset, pix.width, y_offset + pix.height)

            new_page.insert_image(rect, pixmap=pix)

# Neue PDF speichern
new_doc.save(args.neuerName)
new_doc.close()
doc.close()

