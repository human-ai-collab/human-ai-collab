import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = 'static'

# Call http://localhost:8000/ for the main page
# Call http://localhost:8000/api/complete to complete a drawing

class MyHandler(http.server.SimpleHTTPRequestHandler):
  def translate_path(self, path: str) -> str:
    print(f"Path Before: {path}")
    path = super().translate_path(path)
    if os.path.isdir(path):
      path = os.path.join(path, DIRECTORY, 'index.html')
      print(f"Path After: {path}")
    return path
    
  def do_GET(self):
    if self.path.startswith("/api"):
      if self.path.startswith("/api/complete"):
        print(f"do_GET path: {self.path}")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # with open(filename, '')
        self.wfile.write(b'{"completed": "dajodajwiodjwai"}')
      else:
        super().do_GET()
    else:
      super().do_GET()

Handler = MyHandler

try:
  with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.daemon_threads = True
    httpd.allow_reuse_address = True
    Handler.directory = DIRECTORY
    httpd.serve_forever()
except KeyboardInterrupt:
  httpd.server_close()