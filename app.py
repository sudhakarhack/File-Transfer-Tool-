from flask import Flask, render_template, request, redirect, url_for
import os
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
from pyqrcode import QRCode

app = Flask(__name__)

UPLOADS_DIR = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR
PORT = 8010

# Change the current working directory to the user's desktop
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')
os.chdir(desktop)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

    # List the uploaded files
    uploaded_files = os.listdir(os.path.join(desktop, UPLOADS_DIR))
    
    # Generate the IP address and QR code
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
    link = IP
    url = pyqrcode.create(link)
    url.svg("myqr.svg", scale=8)
    webbrowser.open('myqr.svg')

    return render_template('index.html', uploaded_files=uploaded_files, link=link)

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Serving at port", PORT)
        app.run(port=PORT, debug=True)
