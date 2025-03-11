import subprocess
import sys
import os
import time

def run_script(script_name):
    """Führt ein Python-Skript aus und gibt eine Fehlermeldung aus, falls etwas schiefgeht."""
    try:
        print(f"Starte {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"{script_name} erfolgreich abgeschlossen.")
        print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Fehler:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von {script_name}: {e}")
        sys.exit(1)

def main():
    while True:
        # Skripte in der richtigen Reihenfolge ausführen
        scripts = [
            "theracon_download.py",  # Läd die Dateien herunter und entpackt sie
            "theracon_conrad.py",    # Erstellt die Conrad-Angebots-CSV
            "theracon_feed.py"       # Erstellt die Theracon-Feed-CSV
        ]

        for script in scripts:
            run_script(script)

        print("Alle Skripte wurden erfolgreich ausgeführt!")
        print("Warte 3 Stunden bis zum nächsten Durchlauf...")
        time.sleep(3 * 60 * 60)  # 3 Stunden warten

if __name__ == "__main__":
    main()