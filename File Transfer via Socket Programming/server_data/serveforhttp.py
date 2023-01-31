from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class FileServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # check if the requested file exists
            if os.path.isfile(self.path[1:]):
                # open the file in binary mode
                with open(self.path[1:], 'rb') as f:
                    # read the file content
                    file_content = f.read()
                # send the file content to the client
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', 'attachment; filename=' + self.path[1:])
                self.end_headers()
                self.wfile.write(file_content)
            else:
                # send a 404 error if the file is not found
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
      