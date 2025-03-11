from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Theracon Script</h1>
    <p>Klicke auf die Links, um die Dateien herunterzuladen:</p>
    <ul>
        <li><a href="/download/theracon_angebotsdaten.csv">Download Conrad-Angebots-CSV</a></li>
        <li><a href="/download/theracon_angebotsdaten_oci.csv">Download Conrad-Angebots-CSV (OCI)</a></li>
        <li><a href="/download/Theracon_Conrad_Feed.csv">Download Theracon-Feed-CSV</a></li>
    </ul>
    """

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('itscope_produkte', filename)
    if not os.path.exists(file_path):
        return f"Datei {filename} nicht gefunden.", 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)