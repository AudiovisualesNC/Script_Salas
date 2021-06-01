import wmi
import platform
import re
import pythoncom
import win32api
import config
from netifaces import interfaces, ifaddresses

from datetime import datetime


def cam_connect():
    c = wmi.WMI()
    wql = "Select * From Win32_USBControllerDevice"
    cam = ""
    for item in c.query(wql):
        q = item.Dependent.Caption
        if item.Dependent.PNPClass == "Camera" or item.Dependent.PNPClass == "MEDIA":
            cam = cam + " " + q

    return cam


def get_ip():
    try:
        return ifaddresses(interfaces()[0])[2][0]['addr']
    except:
        return ""


def room_info(logger):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]

    now = datetime.now()
    my_obj = {"ip": get_ip(), 'host': str(platform.node()), "version": config.VERSION, "room_name": config.NOMBRE,
              "id": config.ID, "port": config.PORT, "open_port": config.OPEN_PORT, "with_button": config.BOTONERA,
              'windows': str(platform.version()), 'device': str(my_system.model), 'cam': str(cam_connect()),
              'time': str(now)
              }

    print("_______________________________")
    print(my_obj)
    print("______________________________")

    return my_obj


def get_idle_time():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
