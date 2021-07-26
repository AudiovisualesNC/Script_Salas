import wmi
import platform
import pythoncom
import win32api
import config
from netifaces import interfaces, ifaddresses

from datetime import datetime


def sys_info(logger):
    try:
        cam = ""
        c = wmi.WMI()
        wql = "Select * From Win32_USBControllerDevice"

        for item in c.query(wql):
            q = item.Dependent.Caption
            if item.Dependent.PNPClass == "Camera" or item.Dependent.PNPClass == "MEDIA":
                cam = cam + " " + q

        if cam == "":
            cam = "No detected"

        system = c.Win32_ComputerSystem()[0]

        return cam, system.model
    except:
        config.ERROR = True
        logger.error("Error getting camera, Error getting system")
        return "Error getting camera", "Error getting system"


def get_ip():
    try:
        return ifaddresses(interfaces()[0])[2][0]['addr']
    except:
        config.ERROR = True
        return "Error getting IP"


def room_info(logger):
    pythoncom.CoInitialize()
    cam, my_system = sys_info(logger)

    now = datetime.now()
    my_obj = {"ip": get_ip(), 'host': str(platform.node()), "version": config.VERSION, "room_name": config.NAME,
              "id": config.ID, "port": config.PORT, "open_port": config.OPEN_PORT, "with_button": config.KEYPAD,
              'windows': str(platform.version()), 'device': str(my_system), 'cam': str(cam), 'monitor': config.MONITOR,
              'last_connection': str(now), "zone": config.ZONE,  "province": config.PROVINCE, "office": config.OFFICE,
              "building_name": config.BUILDING_NAME
              }

    print("_______________________________")
    print(my_obj)
    print("______________________________")

    return my_obj


def get_idle_time():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
