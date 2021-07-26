import binascii
import sys

import config
import serial
import time
import os
import win32api
import webbrowser
import restartSession

from binascii import unhexlify
from serial.tools import list_ports

BAUD = 9600
SIZE = 8
PARITY = "N"
STOP = 1

REBOOTING = False
SYSTEM_ON = True
SER = None

'''
Clase que recibe los bytes de entrada en el puerto serie cuando hay botonera
'''


class RingBuffer:
    def __init__(self):
        self.data = ''

    '''
    Recibe los bytes de entrada y almecena el resultado en una variable de tipo string
    '''

    def append(self, x):
        converted = string_to_hex_botonera(x)
        '''
        Si el string devuelto cominza por 8D o 8C significa que es un nuevo comando y se reinicia la variable con los
         nuevos datos, si no empieza por uno de estos dos, los bytes recibidos pertenecen al mismo comando
        '''
        if converted.startswith(":8D") or converted.startswith(":8C"):
            self.data = converted
        else:
            self.data = self.data + converted


'''
Recibe los bytes y lo devuelve en un formato string
'''


def string_to_hex_botonera(asciiString):
    code = ""
    '''
    Se lee de byte en byte
    '''
    for c in asciiString:
        toHex = hex(c).upper()
        toHex = toHex[2:]
        if len(toHex) == 1:
            code = code + ":0" + toHex
        else:
            code = code + ":" + toHex
    return code


def string_to_hex(str_hex):
    return unhexlify(str_hex.replace(":", ""))

#Alternativa para detectar el monitor con powershell
'''
def check_monitor(logger):
    result = subprocess.run(["powershell", "-Command", "gwmi WmiMonitorID -Namespace root\wmi"],
                            capture_output=True).stdout.decode("utf-8", errors='ignore')
    if "SAM" in result:
        #config.MONITOR = "SAMSUNG"
        logger.info("Powershell -- SAMSUNG")
    elif "SNY" in result:
        #config.MONITOR = "SONY"
        logger.info("Powershell -- SONY")
    else:
        #config.MONITOR = "UNKNOW"
        logger.info("Powershell -- Desconocido")
'''

def configure_port_monitor(logger):
    # Recorremos todos los puertos COM del pc
    for port in list(list_ports.comports()):
        try:
            print(str(port).split(" ")[0])
            port = str(port).split(" ")[0]
            # Trata de abrir el puerto para iniciar la comunicación
            ser = serial.Serial(str(port), BAUD, SIZE, PARITY, STOP, timeout=None, write_timeout=0)

            if ser.isOpen():
                # probamos si hay comunicación con el monitor
                # al haber Samsung y Sony probamos con los dos y el que responda ese es

                ###########
                # SAMSUNG #
                ###########
                # Obtenemos el estado actual del monitor (apagado o encendido)
                ser.write(string_to_hex("AA:11:01:00:12"))
                time.sleep(1)
                ###########
                #  SONY   #
                ###########
                # Obtenemos el estado actual del monitor (apagado o encendido)
                ser.write(string_to_hex("8C:00:00:02:00:8F"))
                time.sleep(1)

                ###########
                # NEXCOM  #
                ###########
                # Obtenemos el estado actual del monitor (apagado o encendido)
                ser.write(string_to_hex("7F:08:99:A2:B3:C4:02:FF:01:00:CF"))
                time.sleep(1)

                bytes_to_read = ser.inWaiting()
                if bytes_to_read:
                    config.OPEN_PORT = True
                    config.PORT = str(port)
                    buff = RingBuffer()
                    buff.append(ser.read(bytes_to_read))
                    print(buff.data)
                    if buff.data.startswith(":AA:FF:01:"):
                        config.MONITOR = "SAMSUNG"
                        logger.info("Puerto " + port + " abierto, monitor Samsung")
                        return ser
                    elif buff.data.startswith(":70:00:"):
                        config.MONITOR = "SONY"
                        logger.info("Puerto " + port + " abierto, monitor Sony")
                        return ser
                    elif buff.data.startswith(":7F:09:99"):
                        config.MONITOR = "NEXCOM"
                        logger.info("Puerto " + port + " abierto, monitor Nexcom")
                        return ser
                    else:
                        config.MONITOR = "UNKNOW"
                        logger.info("Puerto " + port + " abierto, monitor desconocido")
                        return ser
        except binascii.Error as e:
            config.ERROR = True
            print(e)
        except serial.serialutil.SerialTimeoutException as e:
            config.ERROR = True
            print(e)
        except serial.serialutil.SerialException as e:
            config.ERROR = True
            print(e)
        except:
            config.ERROR = True
            logger.error(sys.exc_info()[0])

    logger.info("Control RS232 no configurado")
    return None


def init_reader(logger):
    logger.info("Iniciando lector RS232")
    if config.PORT:
        try:
            # Trata de abrir el puerto para iniciar la comunicación
            ser = serial.Serial(config.PORT, BAUD, SIZE, PARITY, STOP, timeout=None)

            if ser.isOpen():
                logger.info("Puerto " + config.PORT + " abierto")
                reader(logger, ser)
            else:
                logger.error("No se puede abrir el puerto " + config.PORT)
        except:
            config.ERROR = True
            logger.error("Error al abrir el puerto " + config.PORT)
    else:
        logger.error("Configurada botonera pero no el puerto")


def reader(logger, ser):
    buff = RingBuffer()
    try:
        while True:
            time.sleep(0.002)
            bytes_to_read = ser.inWaiting()
            # Si hay datos para leer se leen
            if bytes_to_read:
                buff.append(ser.read(bytes_to_read))
                print(buff.data)

                if buff.data.endswith("8D:00:04:01:92"):
                    logger.info("Pulsado ON en botonera")
                if buff.data.endswith("8D:00:04:02:93"):
                    logger.info("Pulsado OFF en botonera")
                    restartSession.restart(logger)
                if buff.data.endswith("8D:00:01:01:8F"):
                    logger.info("Pulsado VOL + en botonera")
                    win32api.keybd_event(0xAF, 0, 0, 0)
                if buff.data.endswith("8D:00:01:02:90"):
                    logger.info("Pulsado VOL - en botonera")
                    win32api.keybd_event(0xAE, 0, 0, 0)
                if buff.data.endswith("8D:00:03:01:91"):
                    logger.info("Pulsado WEBEX")

                    if os.path.isfile('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'):
                        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                    else:
                        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

                    try:
                        webbrowser.get(chrome_path).open("https://bbva.webex.com")
                        logger.info("Abriendo  Webex en el navegador")
                    except:
                        config.ERROR = True
                        logger.error("No se ha podido abrir el navegador")
    except:
        config.ERROR = True
        logger.error("Error al leer la botonera")


def init_sender(logger):
    global SER
    #check_monitor(logger)
    SER = configure_port_monitor(logger)


def send_on():
    if SER and config.MONITOR:
        if config.MONITOR == "SAMSUNG":
            print("Encendido Samsung")
            SER.write(string_to_hex("AA:11:01:01:01:14"))
        elif config.MONITOR == "SONY":
            print("Encendido SONY")
            SER.write(string_to_hex("8C:00:00:02:01:8F"))
        elif config.MONITOR == "NEXCOM":
            print("Encendido NEXCOM")
            SER.write(string_to_hex("7F 08 99 A2 B3 C4 02 FF 01 00 CF"))


def send_off():
    if SER and config.MONITOR:
        if config.MONITOR == "SAMSUNG":
            print("Apagado Samsung")
            SER.write(string_to_hex("AA:11:01:01:00:13"))
        elif config.MONITOR == "SONY":
            print("Apagado SONY")
            SER.write(string_to_hex("8C:00:00:02:00:8E"))
        elif config.MONITOR == "NEXCOM":
            print("Apagado NEXCOM")
            SER.write(string_to_hex("7F 08 99 A2 B3 C4 02 FF 01 01 CF"))
