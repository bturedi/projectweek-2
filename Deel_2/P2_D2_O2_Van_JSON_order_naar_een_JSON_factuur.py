import json
from datetime import datetime, timedelta
import os
from decimal import Decimal, ROUND_HALF_UP

class OrderToInvoiceConverter:
    def __init__(self):
        self.company_info = {
            "name": "XYZ Services",
            "contact": "Lisa de Vries",
            "address": "Hoofdstraat 45",
            "postal": "5678 CD",
            "city": "Rotterdam",
            "kvk": "12345678",
            "btw": "NL123456789B01",
            "iban": "NL91ABNA0123456789",
            "phone": "010-1234567",
            "mobile": "06-12345678",
            "email": "info@xyzservices.nl",
            "website": "www.xyzservices.nl"
        }

    def calculate_due_date(self, order_date, payment_term):
        """Calculate due date based on order date and payment term."""
        date_obj = datetime.strptime(order_date, "%d-%m-%Y")
        days = int(payment_term.split("-")[0])
        due_date = date_obj + timedelta(days=days)
        return due_date.strftime("%d-%m-%Y")

    def round_amount(self, amount):
        """Round amount according to Belastingdienst rules."""
        return Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def calculate_vat_amount(self, base_amount, vat_percentage):
        """Calculate VAT amount and round according to Belastingdienst rules."""
        vat_rate = Decimal(str(vat_percentage)) / Decimal('100')
        vat_amount = base_amount * vat_rate
        return self.round_amount(vat_amount)

    def process_order(self, order_data):
        order = order_data["order"]
        
        # Calculate totals and VAT amounts per rate
        vat_totals = {}  # To store totals per VAT rate
        total_excl = Decimal('0')
        
        line_items = []
        for product in order["producten"]:
            quantity = Decimal(str(product["aantal"]))
            price_excl = Decimal(str(product["prijs_per_stuk_excl_btw"]))
            vat_rate = Decimal(str(product["btw_percentage"]))
            
            line_total_excl = quantity * price_excl
            vat_amount = self.calculate_vat_amount(line_total_excl, vat_rate)
            line_total_incl = line_total_excl + vat_amount
            
            # Add to VAT totals
            if vat_rate not in vat_totals:
                vat_totals[vat_rate] = {"base": Decimal('0'), "vat": Decimal('0')}
            vat_totals[vat_rate]["base"] += line_total_excl
            vat_totals[vat_rate]["vat"] += vat_amount
            
            total_excl += line_total_excl
            
            line_items.append({
                "description": product["productnaam"],
                "quantity": int(quantity),
                "unit": "stuks",
                "price_excl": float(self.round_amount(price_excl)),
                "vat_rate": float(vat_rate),
                "total_excl": float(self.round_amount(line_total_excl)),
                "vat_amount": float(self.round_amount(vat_amount)),
                "total_incl": float(self.round_amount(line_total_incl))
            })
        
        # Calculate total VAT and invoice total
        total_vat = sum(rate_info["vat"] for rate_info in vat_totals.values())
        total_incl = total_excl + total_vat

        # Create invoice data structure
        invoice_data = {
            "invoice": {
                "invoice_number": f"F{order['ordernummer']}",
                "order_number": order["ordernummer"],
                "date": order["orderdatum"],
                "due_date": self.calculate_due_date(order["orderdatum"], order["betaaltermijn"]),
                
                "company": self.company_info,
                
                "customer": {
                    "name": order["klant"]["naam"],
                    "address": order["klant"]["adres"],
                    "postal_code": order["klant"]["postcode"],
                    "city": order["klant"]["stad"],
                    "kvk": order["klant"]["KVK-nummer"]
                },
                
                "line_items": line_items,
                
                "totals": {
                    "total_excl": float(self.round_amount(total_excl)),
                    "vat_specifications": {
                        str(float(rate)): {
                            "base_amount": float(self.round_amount(info["base"])),
                            "vat_amount": float(self.round_amount(info["vat"]))
                        }
                        for rate, info in vat_totals.items()
                    },
                    "total_vat": float(self.round_amount(total_vat)),
                    "total_incl": float(self.round_amount(total_incl))
                }
            }
        }
        
        return invoice_data

    def convert_order_file(self, input_file, output_dir="generated_invoices"):
        """Convert a single order file to an invoice file."""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Read order file
        with open(input_file, 'r') as f:
            order_data = json.load(f)
        
        # Process order to invoice
        invoice_data = self.process_order(order_data)
        
        # Generate output filename
        output_filename = os.path.join(
            output_dir, 
            f"invoice_{invoice_data['invoice']['invoice_number']}.json"
        )
        
        # Write invoice file
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(invoice_data, f, indent=2, ensure_ascii=False)
        
        return output_filename

    def process_directory(self, input_dir, output_dir="generated_invoices"):
        """Process all JSON files in a directory."""
        processed_files = []
        for filename in os.listdir(input_dir):
            if filename.endswith('.json'):
                input_path = os.path.join(input_dir, filename)
                output_file = self.convert_order_file(input_path, output_dir)
                processed_files.append(output_file)
        return processed_files

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the input and output directories
    input_dir = os.path.join(current_dir, "test_set_softwareleverancier")
    output_dir = os.path.join(current_dir, "generated_invoices")
    
    # Create converter instance
    converter = OrderToInvoiceConverter()
    
    try:
        # Process all files in the test_set_softwareleverancier directory
        results = converter.process_directory(input_dir, output_dir)
        
        # Print results
        print("Generated invoices:")
        for result in results:
            print(f"- {result}")
            
    except FileNotFoundError as e:
        print(f"Error: Could not find directory or file: {e}")
        print(f"Current directory: {current_dir}")
        print(f"Looking for input directory: {input_dir}")
    except Exception as e:
        print(f"Error occurred: {e}")