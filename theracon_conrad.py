import csv
import os

# Pfade zu den Eingabedateien und der Ausgabedatei
input_file_product = os.path.join('itscope_produkte', 'product.csv')  # Pfad zur product.csv
output_file_theracon = 'theracon_angebotsdaten.csv'  # Ausgabedatei 1
output_file_oci = 'theracon_angebotsdaten_oci.csv'  # Ausgabedatei 2

# **Erstellen der 'theracon_angebotsdaten.csv' Datei**
with open(output_file_theracon, mode='w', encoding='utf-8', newline='') as outfile_theracon:
    fieldnames_theracon = [
        'sku', 'product-id', 'product-id-type', 'price', 'quantity', 'state', 
        'logistic-class', 'leadtime-to-ship', 'reversecharge', 'warehouse'
    ]
    
    writer_theracon = csv.DictWriter(outfile_theracon, fieldnames=fieldnames_theracon, delimiter=';')
    writer_theracon.writeheader()

    try:
        with open(input_file_product, mode='r', encoding='utf-8') as infile_product:
            reader_product = csv.DictReader(infile_product, delimiter='\t')  # Tabulator als Trenner
            
            for row in reader_product:
                try:
                    price_with_tax = round(float(row['priceCalc']) * 1.19, 2)  # Berechnung mit 19% MwSt
                except ValueError:
                    price_with_tax = 0.0  # Wenn ein Fehler auftritt, setze den Preis auf 0.0

                new_row = {
                    'sku': row['puid'],
                    'product-id': row['puid'],
                    'product-id-type': 'SHOP_SKU',
                    'price': price_with_tax,
                    'quantity': row['stock'],
                    'state': '11',
                    'logistic-class': 'SM3',
                    'leadtime-to-ship': '3',
                    'reversecharge': 'false',
                    'warehouse': '1'
                }
                writer_theracon.writerow(new_row)

    except FileNotFoundError:
        print(f"Die Datei '{input_file_product}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist beim Verarbeiten der 'product.csv' Datei aufgetreten: {e}")


# **Erstellen der 'theracon_angebotsdaten_oci.csv' Datei**
with open(output_file_oci, mode='w', encoding='utf-8', newline='') as outfile_oci:
    fieldnames_oci = [
        'sku', 'product-id', 'product-id-type', 'price', 'quantity', 'state', 
        'logistic-class', 'leadtime-to-ship', 'reversecharge', 'warehouse', 'price_calc'
    ]
    
    writer_oci = csv.DictWriter(outfile_oci, fieldnames=fieldnames_oci, delimiter=';')
    writer_oci.writeheader()

    try:
        with open(input_file_product, mode='r', encoding='utf-8') as infile_product:
            reader_product = csv.DictReader(infile_product, delimiter='\t')  # Tabulator als Trenner
            
            for row in reader_product:
                try:
                    price_with_tax = round(float(row['priceCalc']) * 1.19, 2)
                    price_after_discount = round(price_with_tax * 0.85, 2)  # 15% Rabatt
                except ValueError:
                    price_with_tax = 0.0
                    price_after_discount = 0.0

                new_row_oci = {
                    'sku': f"OCI_{row['puid']}",  # Prefix "OCI_" hinzufügen
                    'product-id': row['puid'],
                    'product-id-type': 'SHOP_SKU',
                    'price': round(price_after_discount, 2),  # Preis mit 15% Rabatt auf 2 Dezimalstellen runden
                    'quantity': row['stock'],
                    'state': '11',
                    'logistic-class': 'oci',
                    'leadtime-to-ship': '3',
                    'reversecharge': 'false',
                    'warehouse': '1',
                    'price_calc': round(price_with_tax, 2)  # Preis mit 19% Mehrwertsteuer, auf 2 Dezimalstellen gerundet
                }
                writer_oci.writerow(new_row_oci)

    except FileNotFoundError:
        print(f"Die Datei '{input_file_product}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist beim Verarbeiten der 'product.csv' Datei aufgetreten: {e}")

print(f'Die Dateien {output_file_theracon} und {output_file_oci} wurden erfolgreich erstellt.')