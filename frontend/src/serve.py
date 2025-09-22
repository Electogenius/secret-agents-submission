#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.parse

HOST = "0.0.0.0"
PORT = 8000
INDEX_FILE = "index.html"  # served for "/"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            if not os.path.isfile(INDEX_FILE):
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"index.html not found")
                return
            try:
                with open(INDEX_FILE, "rb") as f:
                    content = f.read()
                self.send_response(200)
                # basic content-type detection by extension
                if INDEX_FILE.lower().endswith(".html"):
                    ctype = "text/html; charset=utf-8"
                else:
                    ctype = "application/octet-stream"
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except OSError:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"error reading index.html")
        elif path == "/health":
            body = b"healthy"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            # other paths
            if not os.path.isfile(path[1:]):
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"index.html not found")
                return
            try:
                with open(path[1:], "rb") as f:
                    content = f.read()
                self.send_response(200)
                # basic content-type detection by extension
                d = {
                    'css':'css',
                    'js': 'javascript'
				}
                if path[1:].lower().endswith(".html"):
                    ctype = "text/html; charset=utf-8"
                else:
                    ctype = f"text/{d[path.split('.')[-1]]}; charset=utf-8"
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except OSError:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"error reading index.html")

    def log_message(self, format, *args):
        # override to reduce console spam; comment this out to enable logs
        pass

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f"Serving on http://{HOST}:{PORT} (press Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down")
        server.server_close()