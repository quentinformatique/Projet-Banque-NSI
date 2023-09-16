from http.server import HTTPServer
import http.server
import socketserver
import logging
import cgi

from RequestManager import do_request


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-request_type', 'text/html')
        self.end_headers()

        logging.error(self.headers)
        self.wfile.write(bytes('GET REQUEST', 'utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-request_type', 'text/html')
        self.end_headers()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type']})
        contents = do_request(form, self.address_string())

        self.wfile.write(bytes(str(contents), 'utf-8'))

        return


handler = MyHttpRequestHandler

address = "192.168.1.26"
port = 2555
server = socketserver.TCPServer((address, port), handler)

print("Le serveur est lancé sur l'adresse locale {} port {}".format(address, port))
server.serve_forever()
