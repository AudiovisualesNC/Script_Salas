import sys

import config
import info
import serial
import time
import os
import process
import statsServer
import adviceMessage
import win32api
import webbrowser

from binascii import unhexlify

REBOOTING = False
SYSTEM_ON = True

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


def Vol_UP():
    win32api.keybd_event(0xAF, 0, 0, 0)


def Vol_DOWN():
    win32api.keybd_event(0xAE, 0, 0, 0)


def Vol_MUTE():
    win32api.keybd_event(0xAD, 0, 0, 0)


def clean_pc():
    os.system(r"taskkill /f /im chrome.exe")
    os.system(r"reg delete HKEY_CURRENT_USER\Software\WebEx\ProdTools\ /f")

    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Downloads\*.*")
    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Documents\*.*")
    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Desktop\*.*")
    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Pictures\*.*")
    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Videos\*.*")
    os.system(r"del /S /Q C:\Users\usr_salas_autolog\Music\*.*")
    os.system(r"taskkill /f /im chrome.exe")
    os.system(r"taskkill /f /im atmgr.exe")
    process.delete_app_user()


def shutdown_process(ser):
    global SYSTEM_ON
    global REBOOTING

    if not config.BOTONERA:
        ser.write(string_to_hex(config.OFF))

    statsServer.sendStatus(config.ID, "roomPower", "off")
    clean_pc()
    SYSTEM_ON = False
    REBOOTING = False
    config.BUTTON_OFF = False


def init(logger):
    global SYSTEM_ON
    global REBOOTING

    logger.info("Iniciando control RS232")

    try:
        ser = serial.Serial(config.PORT, config.BAUD, config.SIZE, config.PARITY, config.STOP, timeout=None)
        # open the serial port
        if ser.isOpen():
            logger.info("Puerto " + config.PORT + " abierto")
            config.OPEN_PORT = True
    except:
        logger.error("No se puede abrir el puerto " + config.PORT)
        config.OPEN_PORT = False

    t = time.time()

    webex_open = False
    if config.BOTONERA:
        buff = RingBuffer()

    while True:
        try:
            if info.get_idle_time() < 3 and not SYSTEM_ON:
                logger.info("El usuario ha encendido la sala al mover el ratÃ³n")
                SYSTEM_ON = True
                REBOOTING = False
                cont = 0
                while cont <= 2:
                    if not config.BOTONERA:
                        ser.write(string_to_hex(config.ON))
                    time.sleep(5)
                    cont = cont + 1
                statsServer.sendStatus(config.ID, "roomPower", "on")

            elif SYSTEM_ON and not REBOOTING:
                if (info.get_idle_time() > config.REBOOT_TIME * 60) and not config.MEETG and not config.WEBEXS:
                    logger.info("Iniciando reinicio por inactividad")
                    adviceMessage.show()
                    REBOOTING = True
                elif config.BUTTON_OFF:
                    logger.info("El usuario ha apagado la sala")
                    shutdown_process(ser)

            elif SYSTEM_ON and REBOOTING:
                if info.get_idle_time() < config.REBOOT_TIME * 60:
                    logger.info("Reinicio cancelado por el usuario")
                    adviceMessage.hide()
                    REBOOTING = False
                elif info.get_idle_time() > ((config.REBOOT_TIME * 60) + 23):
                    logger.info("Reinicio")
                    adviceMessage.hide()
                    shutdown_process(ser)
                elif config.BUTTON_OFF:
                    logger.info("El usuario ha apagado la sala")
                    adviceMessage.hide()
                    shutdown_process(ser)

            # Check every 10 seconds
            if time.time() - t > 10:
                if process.process_running("chrome.exe"):
                    if config.STATUS == "START MEET" and (config.MEETG == True):
                        config.STATUS = ""
                        logger.info("Conectado a sesion Google Meets")
                        statsServer.sendStatus(config.ID, "vcInCall", "yes")
                    elif config.STATUS == "END MEET" and (config.MEETG == True):
                        config.MEETG = False
                        config.STATUS = ""
                        logger.info("Desconectado de una sesion Google Meets")
                        statsServer.sendStatus(config.ID, "vcInCall", "no")
                elif config.MEETG:
                    config.STATUS = ""
                    config.MEETG = False
                    logger.info("Desconectado de una sesion Google Meets")
                    statsServer.sendStatus(config.ID, "vcInCall", "no")
            if time.time() - t > 10:
                if process.process_running("chrome.exe"):
                    if config.STATUSF == "START WEBEX" and (config.WEBEXS == True):
                        config.STATUSF = ""
                        logger.info("Conectado a sesion Webex")
                        statsServer.sendStatus(config.ID, "vcInCall", "yes")
                    elif config.STATUSF == "END WEBEX" and (config.WEBEXS == True):
                        config.WEBEXS = False
                        config.STATUSF = ""
                        logger.info("Desconectado de una sesion Webex")
                        statsServer.sendStatus(config.ID, "vcInCall", "no")
                elif config.WEBEXS:
                    config.STATUSF = ""
                    config.WEBEXS = False
                    logger.info("Desconectado de una sesion Google Webex")
                    statsServer.sendStatus(config.ID, "vcInCall", "no")

                    # Check every 10 seconds
            if time.time() - t > 10:
                t = time.time()
                if process.process_running(config.EXE):
                    if not webex_open:
                        logger.info("Conectado a sesiÃ³n Webex")
                        webex_open = True
                        statsServer.sendStatus(config.ID, "vcInCall", "yes")
                else:
                    if webex_open:
                        logger.info("Desconectado de sesiÃ³n Webex")
                        os.system(r"reg delete HKEY_CURRENT_USER\Software\WebEx\ProdTools\ /f")
                        webex_open = False
                        statsServer.sendStatus(config.ID, "vcInCall", "no")

            '''
            Si la sala tiene botonera
            Se lee si la botonera ha enviado algún comando RS232
            '''
            if config.BOTONERA:
                bytes_to_read = ser.inWaiting()
                '''
                Si hay datos para leer se leen
                '''
                if bytes_to_read:
                    buff.append(ser.read(bytes_to_read))
                    if buff.data.endswith(config.ON):
                        logger.info("Pulsado ON en botonera")
                        statsServer.sendStatus(config.ID, "roomPower", "on")
                    if buff.data.endswith(config.OFF):
                        logger.info("Pulsado OFF en botonera")
                        config.BUTTON_OFF = True
                    if buff.data.endswith(config.VOLUP):
                        logger.info("Pulsado VOL + en botonera")
                        Vol_UP()
                    if buff.data.endswith(config.VOLDOWN):
                        logger.info("Pulsado VOL - en botonera")
                        Vol_DOWN()
                    if buff.data.endswith(config.WEBEX):
                        logger.info("Pulsado WEBEX")

                        if os.path.isfile('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'):
                            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                        else:
                            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

                        try:
                            webbrowser.get(chrome_path).open(config.URL)
                            logger.info("Abriendo " + config.URL + " en el navegador")
                        except:
                            logger.error("No se ha podido abrir el navegador")
                    if buff.data.endswith(config.HDMI):
                        logger.info("Pulsado HDMI en botonera")
                    if buff.data.endswith(config.VGA):
                        logger.info("Pulsado VGA en botonera")
                    if buff.data.endswith(config.PCSALA):
                        logger.info("Pulsado PC DE SALA en botonera")

            time.sleep(0.002)
        except TypeError as e:
            print(e)
        except UnicodeError as e:
            print(e)
        except:
            logger.error("Error en hilo RS232")
            print(sys.exc_info()[0])
            time.sleep(0.002)
