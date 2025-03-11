import os
import requests
import zipfile

# API-URL für die ZIP-Datei
zip_api_url = "https://m107169:18qoqNzeLLsNchLOpHim7dUIuFqhRt7bzUIcjHwPU2I@api.itscope.com/2.1/products/exports/eae5a00f-e62d-470f-920a-ed53c7a4c2f9"

# Zielordner im aktuellen Verzeichnis (relativer Pfad)
target_folder = os.path.join(os.getcwd(), "itscope_produkte")

# Erstelle den Zielordner, falls er nicht existiert
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# ZIP-Datei herunterladen und nur bestimmte Dateien entpacken
zip_file_name = "Theracon_standard.zip"
zip_file_path = os.path.join(target_folder, zip_file_name)

# ZIP-Datei herunterladen
response = requests.get(zip_api_url)
if response.status_code == 200:
    # Speichere die ZIP-Datei
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)
    print(f"ZIP-Datei wurde erfolgreich heruntergeladen und unter {zip_file_path} gespeichert.")

    # Entpacke nur die benötigten Dateien aus der ZIP-Datei
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Liste der Dateien, die entpackt werden sollen
        files_to_extract = ["product.csv", "supplierItem.csv"]
        for file in zip_ref.namelist():
            if file in files_to_extract:
                zip_ref.extract(file, target_folder)
                print(f"Datei {file} wurde erfolgreich entpackt.")
            else:
                print(f"Datei {file} wird ignoriert.")

    # Lösche die ZIP-Datei nach dem Entpacken
    os.remove(zip_file_path)
    print(f"Die ZIP-Datei {zip_file_name} wurde gelöscht.")
else:
    print(f"Fehler beim Herunterladen der ZIP-Datei. Statuscode: {response.status_code}")