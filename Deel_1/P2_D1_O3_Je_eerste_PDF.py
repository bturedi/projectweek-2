from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def create_pdf(text):
    # Definieer de map waar de PDF wordt opgeslagen
    directory = 'PDF_INVOICE'
    
    # Als de map niet bestaat, maak deze dan aan
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Bestandsnaam voor de PDF
    filename = os.path.join(directory, 'invoice.pdf')
    
    # Maak een PDF canvas object
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Stel het lettertype in
    c.setFont("Helvetica", 12)
    
    # Voeg de tekst toe aan de PDF
    c.drawString(100, 750, text)
    
    # Sla de PDF op
    c.save()
    
    print(f"PDF is opgeslagen als {filename}")

if __name__ == '__main__':
    # Vraag de gebruiker om een stukje tekst in te voeren
    user_input = input("Voer de tekst in die je in de PDF wilt zetten: ")
    
    # Maak de PDF aan met de ingevoerde tekst
    create_pdf(user_input)

