import config
import json
import info
import os

from http.server import BaseHTTPRequestHandler, HTTPServer


LOGGER = None


class HTTPRequestHandler(BaseHTTPRequestHandler):
    # handle GET command
    def do_GET(self):

        global LOGGER

        try:
            if self.path == ('/roomdata.json'):
                # send response code:
                self.send_response(200)
                # send headers:
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                BaseHTTPRequestHandler.end_headers(self)

                strVal = json.dumps(info.room_info(LOGGER))

                self.wfile.write(bytes(strVal, 'utf-8'))

            if self.path == ('/poweroff'):
                # send response code:
                config.BUTTON_OFF = True

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))
                LOGGER.info("El usuario ha pulsado el boton apagado -- true")

            if self.path == ('/startGmeets'):
                config.STATUS = "START MEET"
                config.MEETG = True
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))

            if self.path == ('/endGmeets'):
                config.STATUS = "END MEET"
                config.MEETG = True
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))

            if self.path == ('/startwebexS'):
                config.STATUSF = "START WEBEX"
                config.WEBEXS = True
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))

            if self.path == ('/endwebexS'):
                config.STATUSF = "END WEBEX"
                config.WEBEXS = True
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))

            if self.path == ('/restartpc'):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes('OK', 'utf-8'))
                os.system(r"shutdown /r")

        except IOError:
            self.send_error(404, 'file not found')


def init(logger):
    try:
        global LOGGER
        logger = logger
        logger.info("Iniciando servidor JSON en el puerto " + str(config.HTTP_PORT))
        server_address = ('127.0.0.1', config.HTTP_PORT)
        httpd = HTTPServer(server_address, HTTPRequestHandler)
        httpd.serve_forever()
    except:
        logger.error("No se ha podido iniciar el servidor JSON en el puerto " + str(config.HTTP_PORT))
