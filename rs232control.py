#!/usr/bin/python
# -*- coding: cp1252 -*-
import config
import api
import logging
import rs232
import process
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
    config.init(logger)

    logger.info("Iniciando RS232control SB version " + config.VERSION)
    process.app_system(logger)

    if process.num_process_running('rs232control.exe') < 3:
        hilo1 = threading.Thread(target=rs232.init, args=[logger])
        hilo2 = threading.Thread(target=api.init, args=[logger])
        hilo1.start()
        hilo2.start()
        time.sleep(10)
        adviceMessage.init(logger)

    else:
        logger.error(u"No se puede iniciar, existe otro proceso 'rs232control.exe' en ejecucion.")
