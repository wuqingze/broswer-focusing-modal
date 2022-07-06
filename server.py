import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        shutoffchrome = "powershell -command \"Get-Process chrome | ForEach-Object { $_.CloseMainWindow() | Out-Null}\""
        os.system(shutoffchrome)
        os.system("python lockwindow.py")
        print(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
