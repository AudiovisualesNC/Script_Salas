import configparser
import re
import os.path

CONFIG_FILE = "config.ini"


def init(logger):
    try:
        # RS232 variables
        global KEYPAD
        KEYPAD = False
        global PORT
        PORT = None

        # ROOM DATA
        global NAME
        NAME = "EMPTY"
        global ID
        ID = "00000"

        # RESTART TIME
        global REBOOT_TIME
        REBOOT_TIME = 5

        # LOCATION
        global ZONE
        ZONE = None
        global PROVINCE
        PROVINCE = None
        global OFFICE
        OFFICE = False
        global BUILDING_NAME
        BUILDING_NAME = None


        #OTHER VARIABLES
        global OPEN_PORT
        global VERSION
        global HTTP_PORT
        global MONITOR
        global MEETING
        global ERROR

        MEETING = False
        OPEN_PORT = False
        VERSION = "4.2"
        MONITOR = None
        ERROR = False

        # Comprobamos si existe el fichero de configuración, si no existe se dejan los valores por defecto
        if os.path.isfile('./config.ini'):

            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)

            # Comprobamos si existe el campo KEYPAD y obtenemos su valor
            # En caso de que no exista consideramos que las salas no tienen botonera
            if config.has_option("ROOM_TYPE", "KEYPAD"):
                if config.get("ROOM_TYPE", "KEYPAD") == "True":
                    KEYPAD = True
                    # Si tiene botonera necesitamos conocer el puerto COM, ya que la botonera
                    # no responde a comandos y no podemos averiguarlo
                    if config.has_option("RS232", "PORT"):
                        # El puerto com siempre es COM1, COM2, COM3.... Si no es asi esta mal configurado
                        if re.search("^COM\d", config.get("RS232", "PORT")):
                            PORT = str(config.get("RS232", "PORT"))
                            print(PORT)
                        else:
                            logger.error("Puerto COM mal configurado")

            if config.has_option("ROOM_DATA", "NAME"):
                NAME = str(config.get("ROOM_DATA", "NAME"))

            if config.has_option("ROOM_DATA", "ID"):
                ID = str(config.get("ROOM_DATA", "ID"))

            # AUTOMATIC CLOSE SESSION

            if config.has_option("RESTART", "TIME"):
                try:
                    REBOOT_TIME = int(config.get("RESTART", "TIME"))
                except:
                    REBOOT_TIME = 5

            # LOCATION INFORMATION

            if config.has_option("LOCATION", "ZONE"):
                ZONE = str(config.get("LOCATION", "ZONE"))
            if config.has_option("LOCATION", "PROVINCE"):
                PROVINCE = str(config.get("LOCATION", "PROVINCE"))
            if config.has_option("LOCATION", "OFFICE"):
                OFFICE = str(config.get("LOCATION", "OFFICE"))
            if config.has_option("LOCATION", "BUILDING_NAME"):
                BUILDING_NAME = str(config.get("LOCATION", "BUILDING_NAME"))

        return True

    except configparser.Error as e:
        logger.error("Error al leer los datos del fichero config.ini " + e.message)
        ERROR = True
        return False
    except TypeError as e:
        logger.error("Error al leer los datos del fichero config.ini " + str(e))
        ERROR = True
        return False
    except:
        logger.error("Error al leer los datos del fichero config.ini")
        ERROR = True
        return False
