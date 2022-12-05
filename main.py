from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

address = ('localhost', 8080)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_OPTIONS(self):
    # preflight request対応
    print( "options" )
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
    self.send_header('Access-Control-Allow-Headers', '*')
    self.end_headers()

  def do_GET(self):
    self.process("get")

  def do_POST(self):
    self.process("post")

  def process(self, msg):
    print(f"recv {msg}")

    ######### httpのボディを受信してコンソール出力 ここから ==>
    length = self.headers.get('content-length')
    if length is not None:
      nbytes = int(length)
      rawPostData = self.rfile.read(nbytes)
      print(f"post body: {rawPostData}")
    ######### httpのボディを受信してコンソール出力 <== ここまで

    enc = sys.getfilesystemencoding()
    encoded = "hello".encode(enc, 'surrogateescape')
    self.send_response(200)
    self.send_header("Content-type", "text/html; charset=%s" % enc)
    self.send_header("Content-Length", str(len(encoded)))
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
    self.send_header('Access-Control-Allow-Headers', '*')
    self.end_headers()

    self.wfile.write(encoded)

with HTTPServer(address, MyHTTPRequestHandler) as server:
    server.serve_forever()