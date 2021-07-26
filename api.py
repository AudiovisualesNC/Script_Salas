import config
import json
import info
import os
import restartSession

from http.server import BaseHTTPRequestHandler, HTTPServer


LOGGER = None


class HTTPRequestHandler(BaseHTTPRequestHandler):
    # handle GET command
    def do_GET(self):

        global LOGGER

        try:
            if self.path == '/roomdata.json':
                # send response code:
                self.send_response(200)
                # send headers:
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                BaseHTTPRequestHandler.end_headers(self)
                strVal = json.dumps(info.room_info(LOGGER))
                self.wfile.write(bytes(strVal, 'utf-8'))

            if self.path == '/getmeet':
                # send response code:

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                BaseHTTPRequestHandler.end_headers(self)
                strVal = json.dumps(config.MEETING)
                self.wfile.write(bytes(strVal, 'utf-8'))

            if self.path == '/geterror':
                # send response code:

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                BaseHTTPRequestHandler.end_headers(self)
                strVal = json.dumps(config.ERROR)
                self.wfile.write(bytes(strVal, 'utf-8'))

            if self.path == '/poweroff':
                # send response code:
                LOGGER.info("El usuario ha pulsado el boton apagado")
                restartSession.restart(LOGGER)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))

            if self.path == '/restartpc':
                LOGGER.info("Reinicio del pc por el usuario")
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))
                os.system(r"shutdown /r")

        except IOError:
            config.ERROR = True
            self.send_error(404, 'file not found')


def init(logger):
    try:
        global LOGGER
        LOGGER = logger
        logger.info("Iniciando servidor JSON en el puerto 8080")
        server_address = ('127.0.0.1', 8080)
        httpd = HTTPServer(server_address, HTTPRequestHandler)
        httpd.serve_forever()
    except:
        config.ERROR = True
        logger.error("No se ha podido iniciar el servidor JSON")
