from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import json
import os
from datetime import datetime

class InvoicePDFGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4

    def format_currency(self, amount):
        """Format amount as currency string."""
        return f"€ {amount:.2f}".replace('.', ',')

    def generate_pdf(self, invoice_data, output_path):
        """Generate PDF invoice from JSON data."""
        c = canvas.Canvas(output_path, pagesize=A4)
        invoice = invoice_data['invoice']

        # Company details (seller)
        c.setFont("Helvetica", 12)
        company = invoice['company']
        c.drawString(20*mm, 280*mm, company['name'])
        c.drawString(20*mm, 275*mm, f"t.a.v. {company['contact']}")
        c.drawString(20*mm, 270*mm, company['address'])
        c.drawString(20*mm, 265*mm, f"{company['postal']} {company['city']}")

        # Customer details
        customer = invoice['customer']
        c.drawString(120*mm, 280*mm, customer['name'])
        # Add default contact person if not present
        contact_person = customer.get('contact_person', 'T.a.v. de administratie')
        c.drawString(120*mm, 275*mm, contact_person)
        c.drawString(120*mm, 270*mm, customer['address'])
        c.drawString(120*mm, 265*mm, f"{customer['postal_code']} {customer['city']}")

        # Invoice details
        c.setFont("Helvetica", 10)
        c.drawString(20*mm, 250*mm, "Factuurdatum:")
        c.drawString(60*mm, 250*mm, invoice['date'])
        c.drawString(20*mm, 245*mm, "Vervaldatum:")
        c.drawString(60*mm, 245*mm, invoice['due_date'])
        c.drawString(20*mm, 240*mm, "Factuurnummer:")
        c.drawString(60*mm, 240*mm, invoice['invoice_number'])
        c.drawString(20*mm, 235*mm, "Periode:")
        # Use order date for period
        order_date = datetime.strptime(invoice['date'], "%d-%m-%Y")
        period = f"01-{order_date.month:02d}-{order_date.year} t/m {order_date.day:02d}-{order_date.month:02d}-{order_date.year}"
        c.drawString(60*mm, 235*mm, period)

        # Company registration details
        c.drawString(20*mm, 220*mm, "Kvk:")
        c.drawString(60*mm, 220*mm, company['kvk'])
        c.drawString(20*mm, 215*mm, "Btw:")
        c.drawString(60*mm, 215*mm, company['btw'])
        c.drawString(20*mm, 210*mm, "Iban:")
        c.drawString(60*mm, 210*mm, company['iban'])

        # Contact details
        c.drawString(20*mm, 195*mm, "Contact:")
        c.drawString(20*mm, 190*mm, "Tel:")
        c.drawString(60*mm, 190*mm, company['phone'])
        c.drawString(20*mm, 185*mm, "Mobiel:")
        c.drawString(60*mm, 185*mm, company['mobile'])
        c.drawString(20*mm, 180*mm, "Mail:")
        c.drawString(60*mm, 180*mm, company['email'])
        c.drawString(20*mm, 175*mm, "Web:")
        c.drawString(60*mm, 175*mm, company['website'])

        # Table header
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20*mm, 160*mm, "Aantal")
        c.drawString(40*mm, 160*mm, "Eenheid")
        c.drawString(60*mm, 160*mm, "Omschrijving")
        c.drawString(120*mm, 160*mm, "Prijs")
        c.drawString(140*mm, 160*mm, "Btw")
        c.drawString(160*mm, 160*mm, "Totaal")

        # Table lines
        c.line(20*mm, 158*mm, 180*mm, 158*mm)
        c.line(20*mm, 155*mm, 180*mm, 155*mm)

        # Line items
        c.setFont("Helvetica", 10)
        y_pos = 145*mm
        for item in invoice['line_items']:
            c.drawString(20*mm, y_pos, str(item['quantity']))
            c.drawString(40*mm, y_pos, item['unit'])
            c.drawString(60*mm, y_pos, item['description'])
            c.drawString(120*mm, y_pos, self.format_currency(item['price_excl']))
            c.drawString(140*mm, y_pos, f"{item['vat_rate']}%")
            c.drawString(160*mm, y_pos, self.format_currency(item['total_incl']))
            y_pos -= 10*mm

        # Totals
        totals = invoice['totals']
        c.line(120*mm, 115*mm, 180*mm, 115*mm)
        c.drawString(120*mm, 105*mm, "Totaal excl. BTW:")
        c.drawString(160*mm, 105*mm, self.format_currency(totals['total_excl']))

        # VAT specifications
        y_pos = 95
        for rate, spec in totals['vat_specifications'].items():
            c.drawString(120*mm, y_pos*mm, f"BTW {rate}%:")
            c.drawString(160*mm, y_pos*mm, self.format_currency(spec['vat_amount']))
            y_pos -= 10

        # Final total
        c.line(120*mm, y_pos*mm + 5*mm, 180*mm, y_pos*mm + 5*mm)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(120*mm, y_pos*mm - 5*mm, "Totaal:")
        c.drawString(160*mm, y_pos*mm - 5*mm, self.format_currency(totals['total_incl']))

        c.save()

def process_invoices(input_dir, output_dir):
    """Process all invoice JSON files and generate PDFs."""
    # Create PDF output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    generator = InvoicePDFGenerator()
    
    # Process each JSON file
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            # Read invoice JSON
            with open(os.path.join(input_dir, filename), 'r') as f:
                invoice_data = json.load(f)
            
            # Generate PDF filename
            pdf_filename = f"{invoice_data['invoice']['invoice_number']}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            # Generate PDF
            generator.generate_pdf(invoice_data, pdf_path)
            print(f"Generated PDF: {pdf_path}")

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output directories
    invoice_json_dir = os.path.join(current_dir, "generated_invoices")
    pdf_output_dir = os.path.join(current_dir, "generated_pdfs")
    
    try:
        process_invoices(invoice_json_dir, pdf_output_dir)
        print("PDF generation completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")