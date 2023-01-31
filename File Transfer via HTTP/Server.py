from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(tmp):
        tmp.send_response(200)
        tmp.send_header('Content-type', 'text/html')
        tmp.end_headers()

    def do_GET(tmp):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(tmp.path), str(tmp.headers))
        file_path = tmp.path[1:]  
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()

        except FileNotFoundError:
            logging.error("File not found: %s", file_path)
            tmp.send_error(404, "File not found")
            return
        nam=f.name.encode("utf-8")
        tmp._set_response()
        tmp.wfile.write(file_content)

    def do_POST(tmp):
        content_length = int(tmp.headers['Content-Length']) 
        post_data = tmp.rfile.read(content_length) 
        print("hello", tmp.responses)
        with open('output.in', 'wb') as local_file:
            for chunk in post_data.iter_content(chunk_size=content_length):
                local_file.write(chunk)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(tmp.path), str(tmp.headers), post_data.decode('utf-8'))

        tmp._set_response()
        tmp.wfile.write("POST request for {}".format(tmp.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()