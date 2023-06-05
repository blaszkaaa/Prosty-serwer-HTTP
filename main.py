from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        message = "<html><body>Hello, World!</body></html>"
        self._send_response(message)

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            message = []
            for field in fields.keys():
                message.append("%s=%s" % (field, fields[field][0]))
        else:
            length = int(self.headers.get('content-length'))
            message = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        
        message = "<html><body>%s</body></html>" % "<br/>".join(message)
        self._send_response(message)

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Running server on port 8000...')
    httpd.serve_forever()
