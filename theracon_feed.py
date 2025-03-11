import csv
import os

# Pfade zu den Eingabedateien und der Ausgabedatei
input_file = os.path.join('itscope_produkte', 'product.csv')  # Pfad zur product.csv
supplier_item_file = os.path.join('itscope_produkte', 'supplierItem.csv')  # Pfad zur supplierItem.csv
output_file = 'Theracon_Conrad_Feed.csv'  # Ausgabedatei

# Spaltenüberschriften für die Ausgabedatei
header = [
    "Product.SellerProductID", "Product.Category", "Product.EAN.Main_MP", "ATT.GLOBAL.Brandname",
    "ATT.GLOBAL.ManufacturerAID", "ATT.GLOBAL.ManufacturerTypeDesc", "Product.BaseUnit", "ATT.GLOBAL.NoCUperOU",
    "ATT.GLOBAL.NoCUperOU_UNIT", "Product.ArticleStatus", "Product.WarrantyTime", "Product.TaxIndicator",
    "Product.Hazmat.Relevancy", "SHOP.PRODUCT.TITLE", "ATT.Text.ProductHeadline", "ATT.Text.ProductFeatures",
    "ATT.Text.ProductTextLong", "ATT.Text.ProductFacts", "ATT.Text.ProductDelivery", "ATT.Text.ProductSysReq",
    "ATT.Text.ProductSpecialAdd", "Product.DetailpageVariantGroup_MP", "Product.DetailpageVariantValue_MP",
    "ATT.CPCS.ArticleKeywords", "ATT.GLOBAL.ProductSpecifications", "Product.PrimaryImageURL_MP", "Product.Image02URL_MP",
    "Product.Image03URL_MP", "Product.Image04URL_MP", "Product.Image05URL_MP", "Product.ImageIllustration01URL_MP",
    "Product.ImageIllustration02URL_MP", "Product.ImageSymbol01URL_MP", "Product.ImageSymbol02URL_MP",
    "Product.ImageSymbol03URL_MP", "Product.ImageSymbol04URL_MP", "Product.ImageSymbol05URL_MP",
    "Product.ImageAward01URL_MP", "Product.ImageAward02URL_MP", "Product.ImageEnergyEfficiencyLabelURL_MP",
    "Product.DocumentManual01URL_MP", "Product.DocumentDatasheet01URL_MP", "Product.DocumentCertificate01URL_MP",
    "Product.DocumentCertificate02URL_MP", "Product.DocumentCertificate03URL_MP", "Product.DocumentSecurityAdvisory01URL_MP",
    "Product.DocumentEnergyEfficiencyFicheURL_MP", "Product.HideInCommonSearches", "Product.InvalidationFlag",
    "eClass", "Produktkategorien", "EEK Datenblatt", "EEK Label", "Energieeffizienzklasse", "weeeRegNo"
]

# Einlesen der supplierItem.csv, um weeeRegNo und price zu extrahieren
weee_reg_no_map = {}  # Dictionary, um productId auf weeeRegNo und price abzubilden

try:
    with open(supplier_item_file, 'r', encoding='utf-8') as supplier_file:
        supplier_reader = csv.DictReader(supplier_file, delimiter='\t')  # Annahme: Tabulator als Trennzeichen

        for row in supplier_reader:
            product_id = row.get('productId')  # Spalte "productId" in supplierItem.csv
            weee_reg_no = row.get('weeeRegNo', '')  # Leerstring, falls weeeRegNo fehlt
            try:
                price = float(row.get('price', 0.0))  # Falls price fehlt, setzen wir es auf 0.0
            except ValueError:
                price = 0.0  # Falls price kein gültiger Wert ist, setzen wir es auf 0.0

            # Überspringe Einträge mit einem Preis von 0
            if price == 0:
                continue

            if product_id:
                # Wenn das Produkt schon im Dictionary ist, prüfen wir, ob der aktuelle Preis günstiger ist
                if product_id not in weee_reg_no_map:
                    weee_reg_no_map[product_id] = {'weee_reg_no': weee_reg_no, 'price': price}
                else:
                    # Wenn der aktuelle Preis günstiger ist, wird er gespeichert
                    if price < weee_reg_no_map[product_id]['price']:
                        weee_reg_no_map[product_id] = {'weee_reg_no': weee_reg_no, 'price': price}
                    
except FileNotFoundError:
    print(f"Fehler: Die Datei {supplier_item_file} wurde nicht gefunden.")
    exit()

except Exception as e:
    print(f"Fehler beim Lesen der supplierItem.csv: {e}")
    exit()

# Funktion zur Formatierung der Attribut-Werte
def format_attributes(row):
    formatted_attributes = []
    
    for i in range(1, 6):  # Durchlaufe die Attribute von 1 bis 5 (attributeTypeName1 bis attributeValue5)
        attribute_name = row.get(f'attributeTypeName{i}')
        attribute_value = row.get(f'attributeValue{i}')
        
        if attribute_name and attribute_value:
            formatted_attributes.append(f'{attribute_name}: {attribute_value}')
        elif attribute_name:  # Falls es nur den Namen gibt
            formatted_attributes.append(attribute_name)

    # Verbinde die formatierten Attribute mit <br> als Trennzeichen
    return '<br>'.join(formatted_attributes)

# Einlesen der Produktdaten aus der CSV-Datei
try:
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='\t')

        # Überprüfen, ob die CSV korrekt eingelesen wurde
        if reader.fieldnames:
            print("Die folgenden Spalten wurden aus der product.csv eingelesen:", reader.fieldnames)
        else:
            print("Die Eingabedatei scheint leer zu sein oder keine gültigen Spalten zu haben.")
            exit()

        # Öffnen der Ausgabedatei im Schreibmodus mit dem richtigen Trennzeichen (Semikolon)
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=header, delimiter=';')  # Verwende Semikolon als Trennzeichen

            # Schreibe die Header-Zeile
            writer.writeheader()

            # Iteriere durch jede Zeile der Eingabedatei
            for row in reader:
                # Wenn einige Spalten fehlen, gebe eine Warnung aus
                if not all(col in row for col in ['puid', 'ean', 'manufacturerSKU', 'productName', 'longDescription', 'shortDescription', 'imageHighRes1', 'image2', 'image3', 'image4', 'image5', 'standardHtmlDatasheet', 'eClass', 'productTypeName']):
                    print(f"Warnung: Einige Spalten fehlen für das Produkt: {row}")
                    continue  # Überspringe diese Zeile, wenn wichtige Daten fehlen

                # Hole weeeRegNo aus der supplierItem.csv basierend auf der puid und wähle den günstigsten Preis
                puid = row['puid']  # Spalte "puid" in product.csv
                weee_reg_no_data = weee_reg_no_map.get(puid, {'weee_reg_no': '', 'price': float('inf')})  # Leerstring und unendlich, falls keine Übereinstimmung
                weee_reg_no = weee_reg_no_data['weee_reg_no']  # Die weeeRegNo mit dem günstigsten Preis

                # Erstellen einer neuen Zeile mit den entsprechenden Werten
                new_row = {
                    "Product.SellerProductID": puid,  # puid wird zu Product.SellerProductID
                    "Product.Category": row['productTypeGroupName'],
                    "Product.EAN.Main_MP": row['ean'],
                    "ATT.GLOBAL.Brandname": row['manufacturerName'],
                    "ATT.GLOBAL.ManufacturerAID": row['manufacturerSKU'],
                    "ATT.GLOBAL.ManufacturerTypeDesc": "",  # Leer lassen
                    "Product.BaseUnit": "Stück",  # Immer "Stück"
                    "ATT.GLOBAL.NoCUperOU": "1",  # Immer "1"
                    "ATT.GLOBAL.NoCUperOU_UNIT": "St.",  # Immer "St."
                    "Product.ArticleStatus": "neu",  # Immer "neu"
                    "Product.WarrantyTime": "",  # Leer lassen
                    "Product.TaxIndicator": "19",  # Immer "19"
                    "Product.Hazmat.Relevancy": "",  # Leer lassen
                    "SHOP.PRODUCT.TITLE": row['productName'],
                    "ATT.Text.ProductHeadline": "",  # Leer lassen
                    "ATT.Text.ProductFeatures": "",  # Leer lassen
                    "ATT.Text.ProductTextLong": row['longDescription'],
                    "ATT.Text.ProductFacts": format_attributes(row),  # Hier wird die formatierte Zeichenkette gesetzt
                    "ATT.Text.ProductDelivery": "",  # Leer lassen
                    "ATT.Text.ProductSysReq": "",  # Leer lassen
                    "ATT.Text.ProductSpecialAdd": "",  # Leer lassen
                    "Product.DetailpageVariantGroup_MP": "",  # Leer lassen
                    "Product.DetailpageVariantValue_MP": "",  # Leer lassen
                    "ATT.CPCS.ArticleKeywords": "",  # Leer lassen
                    "ATT.GLOBAL.ProductSpecifications": "",  # Leer lassen
                    "Product.PrimaryImageURL_MP": row['imageHighRes1'],
                    "Product.Image02URL_MP": row['image2'] if row['image2'] else "",  # Leer lassen wenn leer
                    "Product.Image03URL_MP": row['image3'] if row['image3'] else "",  # Leer lassen wenn leer
                    "Product.Image04URL_MP": row['image4'] if row['image4'] else "",  # Leer lassen wenn leer
                    "Product.Image05URL_MP": row['image5'] if row['image5'] else "",  # Leer lassen wenn leer
                    "Product.ImageIllustration01URL_MP": "",  # Leer lassen
                    "Product.ImageIllustration02URL_MP": "",  # Leer lassen
                    "Product.ImageSymbol01URL_MP": "",  # Leer lassen
                    "Product.ImageSymbol02URL_MP": "",  # Leer lassen
                    "Product.ImageSymbol03URL_MP": "",  # Leer lassen
                    "Product.ImageSymbol04URL_MP": "",  # Leer lassen
                    "Product.ImageSymbol05URL_MP": "",  # Leer lassen
                    "Product.ImageAward01URL_MP": "",  # Leer lassen
                    "Product.ImageAward02URL_MP": "",  # Leer lassen
                    "Product.ImageEnergyEfficiencyLabelURL_MP": "",  # Leer lassen
                    "Product.DocumentManual01URL_MP": "",  # Leer lassen
                    "Product.DocumentDatasheet01URL_MP": row['standardHtmlDatasheet'],
                    "Product.DocumentCertificate01URL_MP": "",  # Leer lassen
                    "Product.DocumentCertificate02URL_MP": "",  # Leer lassen
                    "Product.DocumentCertificate03URL_MP": "",  # Leer lassen
                    "Product.DocumentSecurityAdvisory01URL_MP": "",  # Leer lassen
                    "Product.DocumentEnergyEfficiencyFicheURL_MP": "",  # Leer lassen
                    "Product.HideInCommonSearches": "",  # Leer lassen
                    "Product.InvalidationFlag": "",  # Leer lassen
                    "eClass": row['eClass'],
                    "Produktkategorien": row['productTypeName'],
                    "EEK Datenblatt": "",  # Leer lassen
                    "EEK Label": row['energyLabel'],  # Hier den Wert für EEK Label einfügen
                    "Energieeffizienzklasse": row['energyEfficiencyClass'],  # Hier den Wert für Energieeffizienzklasse einfügen
                    "weeeRegNo": weee_reg_no,  # weeeRegNo aus der supplierItem.csv
                }

                # Schreibe die neue Zeile in die Ausgabedatei
                writer.writerow(new_row)

    print("Die Datei 'Theracon_Conrad_Feed.csv' wurde erfolgreich erstellt.")

except FileNotFoundError:
    print(f"Fehler: Die Datei {input_file} wurde nicht gefunden.")

except Exception as e:
    print(f"Es ist ein Fehler aufgetreten: {e}")