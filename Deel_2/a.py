import json
import os
from P2_D2_O2_Van_JSON_order_naar_een_JSON_factuur import OrderToInvoiceConverter
from P2_D3_O1_Gebruikt_de_data_uit_de_factuur_JSON_file_voor_je_PDF import InvoicePDFGenerator  # Importeer de class

def bulk_genereer_pdf_facturen(input_map, output_map, error_map):
    """Genereert PDF-facturen van JSON-orderbestanden."""

    converter = OrderToInvoiceConverter()
    pdf_generator = InvoicePDFGenerator()  # Maak een instantie van de PDF-generator

    for filename in os.listdir(input_map):
        if filename.endswith(".json"):
            filepath = os.path.join(input_map, filename)
            try:
                with open(filepath, 'r') as f:
                    order_data = json.load(f)
                factuur_data = converter.process_order(order_data)
                
                # Gebruik de instantie om de methode aan te roepen
                pdf_generator.generate_pdf(factuur_data, os.path.join(output_map, filename[:-5] + ".pdf"))  
            except Exception as e:
                print(f"Fout bij het verwerken van {filename}: {e}")
                os.makedirs(error_map, exist_ok=True)
                with open(os.path.join(error_map, filename), 'w') as f:
                    json.dump(order_data, f, indent=4)

if __name__ == "__main__":
    input_map = "P2_D4_O1"
    output_map = "P2_D4_O1_PDF_FACTUREN"
    error_map = "P2_D4_O1_JSON_ORDER_ERROR"
    bulk_genereer_pdf_facturen(input_map, output_map, error_map)