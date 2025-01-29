from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def maak_factuur(bestandsnaam):
    """
    Genereert een PDF factuur met de opgegeven lay-out en data.
    """
    c = canvas.Canvas(bestandsnaam, pagesize=A4)

    # Bedrijfsgegevens
    c.setFont("Helvetica", 12)
    c.drawString(20*mm, 280*mm, "XYZ Services")
    c.drawString(20*mm, 275*mm, "t.a.v. Lisa de Vries")
    c.drawString(20*mm, 270*mm, "Hoofdstraat 45")
    c.drawString(20*mm, 265*mm, "5678 CD Rotterdam")

    # Klantgegevens
    c.drawString(120*mm, 280*mm, "ABC Bedrijf B.V.")
    c.drawString(120*mm, 275*mm, "t.a.v. Jan Jansen")
    c.drawString(120*mm, 270*mm, "Lindelaan 12")
    c.drawString(120*mm, 265*mm, "1234 AB Amsterdam")

    # Factuurgegevens
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, 250*mm, "Factuurdatum:")
    c.drawString(60*mm, 250*mm, "29-01-2025")
    c.drawString(20*mm, 245*mm, "Vervaldatum:")
    c.drawString(60*mm, 245*mm, "28-02-2025")
    c.drawString(20*mm, 240*mm, "Factuurnummer:")
    c.drawString(60*mm, 240*mm, "12345")
    c.drawString(20*mm, 235*mm, "Periode:")
    c.drawString(60*mm, 235*mm, "01-01-2025 t/m 31-01-2025")

    # Overige gegevens
    c.drawString(20*mm, 220*mm, "Kvk:")
    c.drawString(60*mm, 220*mm, "12345678")
    c.drawString(20*mm, 215*mm, "Btw:")
    c.drawString(60*mm, 215*mm, "NL123456789B01")
    c.drawString(20*mm, 210*mm, "Iban:")
    c.drawString(60*mm, 210*mm, "NL91ABNA0123456789")

    # Contactgegevens
    c.drawString(20*mm, 195*mm, "Contact:")
    c.drawString(20*mm, 190*mm, "Tel:")
    c.drawString(60*mm, 190*mm, "010-1234567")
    c.drawString(20*mm, 185*mm, "Mobiel:")
    c.drawString(60*mm, 185*mm, "06-12345678")
    c.drawString(20*mm, 180*mm, "Mail:")
    c.drawString(60*mm, 180*mm, "info@xyzservices.nl")
    c.drawString(20*mm, 175*mm, "Web:")
    c.drawString(60*mm, 175*mm, "www.xyzservices.nl")

    # Factuurtabel header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, 160*mm, "Aantal")
    c.drawString(40*mm, 160*mm, "Eenheid")
    c.drawString(60*mm, 160*mm, "Omschrijving")
    c.drawString(120*mm, 160*mm, "Prijs")
    c.drawString(140*mm, 160*mm, "Btw")
    c.drawString(160*mm, 160*mm, "Totaal")

    # Lijnen voor de tabel
    c.line(20*mm, 158*mm, 180*mm, 158*mm) # Horizontale lijn boven tabel
    c.line(20*mm, 155*mm, 180*mm, 155*mm) # Horizontale lijn onder header

    # Factuurregels
    c.setFont("Helvetica", 10)
    y_pos = 145*mm
    factuur_regels = [
        ("1", "uur", "Arbeid", "€ 50,00", "21%", "€ 60,50"),
        ("1", "stuks", "Product", "€ 25,00", "21%", "€ 30,25"),
        ("1", "km", "Reiskosten", "€ 0,30", "21%", "€ 0,36")
    ]
    for regel in factuur_regels:
        c.drawString(20*mm, y_pos, regel[0])
        c.drawString(40*mm, y_pos, regel[1])
        c.drawString(60*mm, y_pos, regel[2])
        c.drawString(120*mm, y_pos, regel[3])
        c.drawString(140*mm, y_pos, regel[4])
        c.drawString(160*mm, y_pos, regel[5])
        y_pos -= 10*mm

    # Totalen
    c.line(120*mm, 115*mm, 180*mm, 115*mm)  # Lijn boven totalen
    c.drawString(120*mm, 105*mm, "Totaal excl. BTW:")
    c.drawString(160*mm, 105*mm, "€ 105,11")
    c.drawString(120*mm, 95*mm, "BTW 21%:")
    c.drawString(160*mm, 95*mm, "€ 22,07")
    c.line(120*mm, 90*mm, 180*mm, 90*mm)  # Lijn boven totaal
    c.setFont("Helvetica-Bold", 10)
    c.drawString(120*mm, 80*mm, "Totaal:")
    c.drawString(160*mm, 80*mm, "€ 127,18")

    c.save()

if __name__ == "__main__":
    bestandsnaam = "PDF_INVOICE/factuur.pdf"
    maak_factuur(bestandsnaam)
    print(f"PDF gegenereerd: {bestandsnaam}")