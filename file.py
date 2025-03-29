import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
from pyqrcode import QRCode
import os

PORT = 8010
UPLOADS_DIR = "uploads"

# Change the current working directory to the user's desktop
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')
os.chdir(desktop)

# Handler for serving files from the 'uploads' directory
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Override translate_path to serve files only from the 'uploads' directory
        path = super().translate_path(path)
        return os.path.join(desktop, UPLOADS_DIR, os.path.relpath(path, self.directory))

# Create the 'uploads' directory if it doesn't exist
uploads_path = os.path.join(desktop, UPLOADS_DIR)
os.makedirs(uploads_path, exist_ok=True)

# Generate the IP address and QR code
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP
url = pyqrcode.create(link)
url.svg("myqr.svg", scale=8)
webbrowser.open('myqr.svg')

# Start the HTTP server
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Serving at port", PORT)
    print("Type this in your Browser", IP)
    print("or Use the QRCode")
    httpd.serve_forever()
