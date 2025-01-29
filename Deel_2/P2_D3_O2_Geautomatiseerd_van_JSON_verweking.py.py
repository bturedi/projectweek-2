import os
import json
import shutil
from datetime import datetime

def setup_directories():
    """Create required directories if they don't exist."""
    directories = ['JSON_ORDER', 'JSON_PROCESSED', 'JSON_INVOICE']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def process_order_file(filename):
    """Process a single order JSON file and create an invoice JSON."""
    try:
        # Read the order file
        with open(os.path.join('JSON_ORDER', filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create invoice filename based on original order number
        invoice_number = data['factuur']['factuurnummer']
        invoice_filename = f"invoice_{invoice_number}.json"
        
        # Save the invoice JSON
        invoice_path = os.path.join('JSON_INVOICE', invoice_filename)
        with open(invoice_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Move original file to processed folder
        shutil.move(
            os.path.join('JSON_ORDER', filename),
            os.path.join('JSON_PROCESSED', filename)
        )
        
        print(f"Processed {filename} -> Created {invoice_filename}")
        return True
    
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        return False

def main():
    """Main function to process all JSON files in the ORDER directory."""
    print("Starting JSON order processing...")
    
    # Setup directories
    setup_directories()
    
    # Get list of JSON files in ORDER directory
    order_files = [f for f in os.listdir('JSON_ORDER') if f.endswith('.json')]
    
    if not order_files:
        print("No JSON files found in JSON_ORDER directory")
        return
    
    # Process each file
    successful = 0
    failed = 0
    
    for filename in order_files:
        if process_order_file(filename):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print("\nProcessing complete!")
    print(f"Successfully processed: {successful}")
    print(f"Failed to process: {failed}")

if __name__ == "__main__":
    main()