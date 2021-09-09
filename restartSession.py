import sys

import win32api
from win32con import VK_NUMLOCK, KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP

import rs232
import info
import config
import adviceMessage
import time
import os
import process
import subprocess

import winreg

global SYSTEM_ON
global REBOOTING


# El uso del microfono se queda guardado en variables de registro, por lo tanto si se comprueban estas variables se
# puede determinar si el usuario esta en una videoconferencia o no, aunque este en mute el microfono sigue en uso.
# El resultado del comando es:
# C:#Program Files#Google#Chrome#Application#chrome.exe
#    LastUsedTimeStop    REG_QWORD    0x1d77d4453a732d4
# Si termina en 0x0 significa que esta en uso

def videconference():
    access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

    primary_access_key = winreg.OpenKey(access_registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged")
    # accessing the key to open the registry directories under
    for n in range(30):
        try:
            x = winreg.EnumKey(primary_access_key, n)
            secondary_access_key = winreg.OpenKey(access_registry,r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged\\" + x)
            if winreg.EnumValue(secondary_access_key, 1)[1] == 0:
                return True
        except:
            return False


def restart(logger):
    global SYSTEM_ON
    SYSTEM_ON = False
    global REBOOTING
    REBOOTING = False

    rs232.send_off()

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

    process.delete_app_user(logger)


def init(logger):
    logger.info("Iniciando hilo restartSession")

    global SYSTEM_ON
    SYSTEM_ON = True
    global REBOOTING
    REBOOTING = False
    # Time sleep para que se inicien los demas procesos
    time.sleep(10)

    while True:

        try:
            update_meeting_started = videconference()
            # Cuando se termina una videoconferencia necesitamos borrar la clave de registro por si se ha usado webex
            # y necesitamos reiniciar el idle time a si que simulamos una pulsacion de teclas, si no reiniciamos el
            # idle time if (info.get_idle_time() > config.REBOOT_TIME * 60) and not meeting_started and
            # config.REBOOT_TIME > 0 esta condicion seria cierta probablemente (depende del tiempo de reinicio
            # configurado), entraria en tiempo de reinicio inmediatamente pero en el siguiente ciclo elif
            # info.get_idle_time() > ((config.REBOOT_TIME * 60) + 23): seria cierto seguramente e inmediatamente
            # haria el reinicio con lo cual no damos tiempo al usuario a reaccionar, por eso es necesario reiniciar
            # el idle time
            if not config.MEETING and update_meeting_started:
                logger.info("Videoconferencia iniciada")
                config.MEETING = True
            elif config.MEETING and not update_meeting_started:
                config.MEETING = False
                logger.info("Videoconferencia terminada")
                os.system(r"reg delete HKEY_CURRENT_USER\Software\WebEx\ProdTools\ /f")
                win32api.keybd_event(VK_NUMLOCK, 0x45, KEYEVENTF_EXTENDEDKEY | 0, 0)
                win32api.keybd_event(VK_NUMLOCK, 0x45, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

            if info.get_idle_time() < 3 and not SYSTEM_ON:
                logger.info("El usuario ha encendido la sala al mover el ratÃ³n")
                SYSTEM_ON = True
                REBOOTING = False
                if not config.KEYPAD:
                    rs232.send_on()
                    time.sleep(5)
                    rs232.send_on()

            elif SYSTEM_ON and not REBOOTING:
                if (info.get_idle_time() > config.REBOOT_TIME * 60) and not config.MEETING and config.REBOOT_TIME > 0:
                    logger.info("Iniciando reinicio por inactividad")
                    adviceMessage.show()
                    REBOOTING = True

            elif SYSTEM_ON and REBOOTING:
                if info.get_idle_time() < config.REBOOT_TIME * 60:
                    logger.info("Reinicio cancelado por el usuario")
                    adviceMessage.hide()
                    REBOOTING = False
                #Damos 23s al usuario para que cancele el reinicio
                elif info.get_idle_time() > ((config.REBOOT_TIME * 60) + 23):
                    logger.info("Reinicio")
                    adviceMessage.hide()
                    restart(logger)

        except TypeError as e:
            config.ERROR = True
            logger.error("Error en hilo restartSession" + str(e))
        except OSError as e:
            config.ERROR = True
            logger.error("Error en hilo restartSession" + str(e))
        except subprocess.CalledProcessError as e:
            config.ERROR = True
            logger.error("Error en hilo restartSession" + str(e))
        except:
            config.ERROR = True
            logger.error("Error en hilo restartSession " + str(sys.exc_info()[0]))

        time.sleep(1)
