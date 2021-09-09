#!/usr/bin/python
# -*- coding: cp1252 -*-
import config
import api
import logging
import rs232
import process
import restartSession
import adviceMessage

import threading
import time

from logging.handlers import RotatingFileHandler

frame = None

if __name__ == "__main__":

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('rs232control.log', maxBytes=10485760, backupCount=0)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    hilo2 = threading.Thread(target=api.init, args=[logger])

    #Siempre tiene que haber un proceso minimo, el de la API
    # Si no esta significa que no se ha iniciado el programa
    if process.num_process_running(logger, 'rs232control.exe') < 3:
        hilo2.start()
        #Si devuelve True el fichero de configuración se ha leido correctamente, iniciamos todos los servicios
        # Si hay algun error solo iniciamos la parte de la API para tener comunicacion con la web
        if config.init(logger):
            logger.info("Iniciando RS232control version " + config.VERSION)
            if config.KEYPAD:
                logger.info("Tipo sala: Con botonera")
                #Al estar configurada la botonera necesitamos iniciar el lector RS232
                hilo3 = threading.Thread(target=rs232.init_reader, args=[logger])
                hilo3.start()
            else:
                logger.info("Tipo sala: Sin botonera")
                rs232.init_sender(logger)
            process.app_system(logger)
            hilo1 = threading.Thread(target=restartSession.init, args=[logger])
            hilo1.start()
            adviceMessage.init(logger)

        time.sleep(10)
