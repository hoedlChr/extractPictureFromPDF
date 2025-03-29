import fitz  # PyMuPDF

# PDF öffnen
doc = fitz.open("adhs_ver.pdf")

# Neues PDF-Dokument erstellen
new_doc = fitz.open()

# Bereich definieren (x0, y0, x1, y1)
clip_rect = fitz.Rect(100, 100, 500, 380)

# Skalierungsfaktor – z. B. 2 = doppelte Auflösung
scale = 2.0
zoom_matrix = fitz.Matrix(scale, scale)

# Immer zwei Seiten gleichzeitig verarbeiten
for i in range(0, len(doc), 2):
    # Neue Seite erstellen: doppelte Breite, Höhe bleibt gleich
    page_width = clip_rect.width * scale 
    page_height = clip_rect.height * scale * 2
    new_page = new_doc.new_page(width=page_width, height=page_height)

    for j in range(2):
        if i + j < len(doc):
            page = doc[i + j]
            pix = page.get_pixmap(matrix=zoom_matrix, clip=clip_rect)

            # Bild einfügen: erste links, zweite rechts
            y_offset = j * clip_rect.height * scale
            rect = fitz.Rect(0, y_offset, pix.width, y_offset + pix.height)

            new_page.insert_image(rect, pixmap=pix)

# Neue PDF speichern
new_doc.save("neu.pdf")
new_doc.close()
doc.close()

