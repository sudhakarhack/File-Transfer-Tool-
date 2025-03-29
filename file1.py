from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
from pyqrcode import QRCode

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

PORT = 8010
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')
os.chdir(desktop)

# Generate the IP address and QR code
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP
url = pyqrcode.create(link)
url.svg("myqr.svg", scale=8)
webbrowser.open('myqr.svg')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    return render_template('index.html')

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Override translate_path to serve files only from the 'uploads' directory
        path = super().translate_path(path)
        return os.path.join(desktop, UPLOAD_FOLDER, os.path.relpath(path, self.directory))

# Create the 'uploads' directory if it doesn't exist
uploads_path = os.path.join(desktop, UPLOAD_FOLDER)
os.makedirs(uploads_path, exist_ok=True)

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Serving at port", PORT)
    print("Type this in your Browser", IP)
    print("or Use the QRCode")
    app.run(port=PORT, threaded=True)
