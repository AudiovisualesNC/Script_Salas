import configparser

CONFIG_FILE = "config.ini"


def init(logger):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        # RS232 variables

        global PORT
        global BAUD
        global SIZE
        global PARITY
        global STOP

        PORT = str(config.get("RS232", "PORT"))
        BAUD = int(config.get("RS232", "BAUD"))
        SIZE = int(config.get("RS232", "SIZE"))
        PARITY = str(config.get("RS232", "PARITY"))
        STOP = int(config.get("RS232", "STOP"))

        # RS232 MONITOR COMMANDS

        global ON
        global OFF
        global BOTONERA

        ON = str(config.get("TV_COMMANDS", "ON"))
        OFF = str(config.get("TV_COMMANDS", "OFF"))
        BOTONERA = False

        if config.get("TIPO_SALA", "SALA") == "SALA CON BOTONERA":
            global VOLUP
            global VOLDOWN
            global REBOOT
            global WEBEX
            global HDMI
            global VGA
            global PCSALA

            BOTONERA = True
            VOLUP = str(config.get("COMMANDS", "VOL_UP"))
            VOLDOWN = str(config.get("COMMANDS", "VOL_DOWN"))
            REBOOT = str(config.get("COMMANDS", "REBOOT"))
            WEBEX = str(config.get("COMMANDS", "WEBEX"))
            HDMI = str(config.get("TV_COMMANDS", "HDMI"))
            VGA = str(config.get("TV_COMMANDS", "VGA"))
            PCSALA = str(config.get("TV_COMMANDS", "SALAPC"))

        # ROOM DATA

        global NOMBRE
        global ID

        NOMBRE = str(config.get("ROOM_DATA", "NAME"))
        ID = str(config.get("ROOM_DATA", "ID"))

        # COLLABORATION DATA

        global URL
        global EXE

        URL = str(config.get("COLLABORATION", "URL"))
        EXE = str(config.get("COLLABORATION", "EXE"))

        # STATS SERVER DATA

        global RCC_URL
        global RCC_USER
        global RCC_PASS

        RCC_URL = str(config.get("RCC", "URL_EST"))
        RCC_USER = str(config.get("RCC", "USER"))
        RCC_PASS = str(config.get("RCC", "PASS"))

        # AUTOMATIC CLOSE SESSION

        global REBOOT_TIME

        REBOOT_TIME = int(config.get("AUTOREBOOT", "TIME"))

        # OTHER GLOBAL VARIABLES

        global OPEN_PORT
        global VERSION
        global HTTP_PORT
        global BUTTON_OFF
        global STATUS
        global MEETG
        global WEBEXS
        global STATUSF

        STATUSF = ""
        WEBEXS = False
        MEETG = False
        STATUS = ""
        BUTTON_OFF = False
        OPEN_PORT = False
        VERSION = "4.1"
        HTTP_PORT = 8080

    except:
        logger.error("Error al leer los datos del fichero config.ini")
