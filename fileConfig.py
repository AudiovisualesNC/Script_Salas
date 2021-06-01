#!/usr/bin/python
# -*- coding: cp1252 -*-
import configparser
import os
import subprocess
import sys
import time
from collections import namedtuple

import psutil
import win32api
import win32security
import wx
from ntsecuritycon import *
from serial.tools import list_ports
from win32api import GetSystemMetrics

KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])
listTec = list()

handlers = []
VERSION = "1.3"
CONFIG_FILE = "config.ini"
val = os.path.isfile("config.ini")
print("existe el config: {}".format(val))

'''
Si no existe el fichero se crea uno
'''
if not val:
    file = open(CONFIG_FILE, "w+")
    data = ""
    data = data + "[RS232]\n"
    data = data + "PORT = \n"
    data = data + "BAUD = 9600\n"
    data = data + "SIZE = 8\n"
    data = data + "PARITY = N\n"
    data = data + "STOP = 1\n"
    data = data + "\n"
    data = data + "[COMMANDS]\n"
    data = data + "VOL_UP = \n"
    data = data + "VOL_DOWN = \n"
    data = data + "REBOOT = \n"
    data = data + "WEBEX = \n"
    data = data + "\n"
    data = data + "[TV_COMMANDS]\n"
    data = data + "ON = \n"
    data = data + "OFF = \n"
    data = data + "SOURCE=3\n"
    data = data + "SALAPC = \n"
    data = data + "VGA = \n"
    data = data + "HDMI = \n"
    data = data + "\n"
    data = data + "[TIPO_SALA]\n"
    data = data + "SALA = \n"
    data = data + "PANTALLA = \n"
    data = data + "CONECTOR = \n"
    data = data + "INICIADO = \n"
    data = data + "PATH = " + r"C:\Users\manue\Documents\Funcionalidad de configuraciÃ³n de sistema PCs salas Audivisuales" + "\n"
    data = data + "\n"
    data = data + "[ROOM_DATA]\n"
    data = data + "NAME = \n"
    data = data + "ID = \n"
    data = data + "SAMPLING = 5\n"
    data = data + "ITERATIONS = 5\n"
    data = data + "IP_SERVER = 20.1.13.33\n"
    data = data + "PORT_SERVER = 10000\n"
    data = data + "DEVICE= 0x2574\n"
    data = data + "\n"
    data = data + "\n"
    data = data + "[COLLABORATION]\n"
    data = data + "URL = \n"
    data = data + "EXE = webexmta.exe\n"
    data = data + "\n"
    data = data + "[RCC]\n"
    data = data + "URL_EST = https://rcc.bbva.igrupobbva/scapi/v1\n"
    data = data + "USER = scuser\n"
    data = data + "PASS = scpass\n"
    data = data + "\n"
    data = data + "[AUTOREBOOT]\n"
    data = data + "TIME = 5\n"
    file.write(data)
    file.close()

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
# ---------------------------------------------------
PORT = str(config.get("RS232", "PORT"))
BAUD = int(config.get("RS232", "BAUD"))
SIZE = int(config.get("RS232", "SIZE"))
PARITY = str(config.get("RS232", "PARITY"))
STOP = int(config.get("RS232", "STOP"))
# ---------------------------------------------------
VOL_UP = str(config.get("COMMANDS", "VOL_UP"))
VOL_DOWN = str(config.get("COMMANDS", "VOL_DOWN"))
REBOOT = str(config.get("COMMANDS", "REBOOT"))
WEBEX = str(config.get("COMMANDS", "REBOOT"))
# ---------------------------------------------------
ON = str(config.get("TV_COMMANDS", "ON"))
OFF = str(config.get("TV_COMMANDS", "OFF"))
COMMAND = str(config.get("TV_COMMANDS", "SOURCE"))
PCSALA = str(config.get("TV_COMMANDS", "SALAPC"))
VGA = str(config.get("TV_COMMANDS", "VGA"))
HDMI = str(config.get("TV_COMMANDS", "HDMI"))
# ---------------------------------------------------
SALA = str(config.get("TIPO_SALA", "SALA"))
PANTALLA = str(config.get("TIPO_SALA", "PANTALLA"))
CONECTOR = str(config.get("TIPO_SALA", "CONECTOR"))
INICIADO = str(config.get("TIPO_SALA", "INICIADO"))
PATH = str(config.get("TIPO_SALA", "PATH"))
# ---------------------------------------------------
NOMBRE = str(config.get("ROOM_DATA", "NAME"))
ID = str(config.get("ROOM_DATA", "ID"))
IP_SERVER = str(config.get("ROOM_DATA", "IP_SERVER"))
PORT_SERVER = str(config.get("ROOM_DATA", "PORT_SERVER"))
WAIT = str(config.get("ROOM_DATA", "SAMPLING"))
ITE = str(config.get("ROOM_DATA", "ITERATIONS"))
DEVICE = str(config.get("ROOM_DATA", "DEVICE"))
# ---------------------------------------------------
URL = str(config.get("COLLABORATION", "URL"))
EXE = str(config.get("COLLABORATION", "EXE"))
# ---------------------------------------------------
RCC_URL = str(config.get("RCC", "URL_EST"))
RCC_USER = str(config.get("RCC", "USER"))
RCC_PASS = str(config.get("RCC", "PASS"))
# ---------------------------------------------------
REBOOT_TIME = int(config.get("AUTOREBOOT", "TIME"))
# ---------------------------------------------------
JSONPORT = 8080
BUFFSIZE = 50
items_list = []
val = False
KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])


def MensajeWarning(NameSala, IDSala, PSerie, Conector, TimeInac, TipoSala):
    cad = "Debe intrioducir los siguientes parámetros de manera satisfactoria para la correcta configuración de la sala:\n"
    cad = cad + "\n"
    val = False
    print("value {}".format(len(NameSala.split(" "))))
    if (NameSala == "") or ("sala" not in NameSala.lower()) or ("(" not in NameSala) or (")" not in NameSala) or (
            len(NameSala.split(" ")) < 3):
        val = True
        cad = cad + "*Insertar el nombre de la sala de acuerdo al siguiente patrón:\n"
        cad = cad + "\n"
        cad = cad + "  -En oficinas rellenar:'nombre municipio' 'oficina' 'número oficina'(Sala Video 'nombre sala').\n"
        cad = cad + "\n"
        cad = cad + "     Ejemplo: Valencia oficina 6517 (Sala Video Valencia Oeste).\n"
        cad = cad + "\n"
        cad = cad + "  -En Edificios centrales rellenar:'nombre municipio'  'nombre de edificio'(Sala  'nombre sala').\n"
        cad = cad + "\n"
        cad = cad + "     Ejemplo:  Madrid Recoletos (Sala 1 Sur).\n"
        cad = cad + "\n"
    if IDSala == "":
        val = True
        cad = cad + "*Insertar el identificador de la sala de acuerdo al siguiente patrón: \n"
        cad = cad + "\n"
        cad = cad + "  -En oficinas rellenar:'número oficina'.\n"
        cad = cad + "\n"
        cad = cad + "     Ejemplo: 6517\n"
        cad = cad + "\n"
        cad = cad + "  -En Edificios centrales rellenar:'número de la sala en el inventario de infraestructura europa'.\n"
        cad = cad + "\n"
        cad = cad + "     Ejemplo: 1000571\n"
        cad = cad + "\n"
    if PSerie == "":
        val = True
        cad = cad + "*Insertar el puerto serie de acuerdo al desplegable proporcionado.\n"
        cad = cad + "\n"
    if Conector == "":
        val = True
        cad = cad + "*Insertar el tipo de conexión con la pantalla de acuerdo al desplegable proporcionado. \n"
        cad = cad + "\n"
    if TipoSala == "":
        val = True
        cad = cad + "*Insertar el tipo de sala de acuerdo al desplegable proporcionado. \n"
        cad = cad + "\n"
    return cad, val


def TipoConnSala(Conn, Pantalla):
    PCSALA = ""
    HDMIMESA = ""
    VGA = ""
    if Pantalla == "PANTALLA SAMSUNG":
        if Conn == "CONECTOR DVI":
            # PCSALA  PCSALA (DVI)  MESA (HDMI1) y VGA (HDMI2)
            PCSALA = "AA:14:01:01:18:2E"
            HDMIMESA = "AA:14:01:01:21:37"
            VGA = "AA:14:01:01:23:39"
        elif Conn == "CONECTOR HDMI1":
            # PCSALA HDMI1 (PANTALLA) y MESA (HDMI2)
            PCSALA = "AA:14:01:01:21:37"
            HDMIMESA = "AA:14:01:01:23:39"
            VGA = ""
        elif Conn == "CONECTOR HDMI2":
            # PCSALA HDMI2 (PANTALLA) y MESA (HDMI1)
            PCSALA = "AA:14:01:01:23:39"
            HDMIMESA = "AA:14:01:01:21:37"
            VGA = ""
    else:
        if Conn == "CONECTOR DVI":
            # PCSALA  PCSALA (DVI)  MESA (HDMI1) y VGA (HDMI2)
            PCSALA = "8C:00:02:03:04:04:99"
            HDMIMESA = "8C:00:02:03:04:01:96"
            VGA = "8C:00:02:03:04:02:97"
        elif Conn == "CONECTOR HDMI1":
            # PCSALA HDMI1 (PANTALLA) y MESA (HDMI2)
            PCSALA = "8C:00:02:03:04:01:96"
            HDMIMESA = "8C:00:02:03:04:02:97"
            VGA = ""
        elif Conn == "CONECTOR HDMI2":
            # PCSALA HDMI2 (PANTALLA) y MESA (HDMI1)
            PCSALA = "8C:00:02:03:04:02:97"
            HDMIMESA = "8C:00:02:03:04:01:96"
            VGA = ""
    return PCSALA, HDMIMESA, VGA


def TipoPantalla(Pantalla, SalaTipo, Conn):
    # print("holaaaaaaaaaa")
    if Pantalla == "PANTALLA SAMSUNG" and SalaTipo == "SALA SIN BOTONERA":
        print("samsung")
        PC_, HDMI1_, VGA_ = TipoConnSala(Conn, Pantalla)
        ModificacionTipoSala(SalaTipo, "AA:11:01:01:01:14", "AA:11:01:01:00:13", "https://bbva.webex.com", PC_, HDMI1_,
                             VGA_, Pantalla)
    elif Pantalla == "PANTALLA SAMSUNG" and SalaTipo == "SALA CON BOTONERA":
        print("samsung")
        ModificacionTipoSala(SalaTipo, "8D:00:04:01:92", "8D:00:04:02:93", "https://bbva.webex.com", "8D:00:05:03:95",
                             "8D:00:05:02:94", "8D:00:05:01:93", Pantalla)
    elif Pantalla == "PANTALLA SONY" and SalaTipo == "SALA SIN BOTONERA":
        print("sony")
        PC_, HDMI1_, VGA_ = TipoConnSala(Conn, Pantalla)
        ModificacionTipoSala(SalaTipo, "8C:00:00:02:01:8F", "8C:00:00:02:00:8E", "https://bbva.webex.com", PC_, HDMI1_,
                             VGA_, Pantalla)
    elif Pantalla == "PANTALLA SONY" and SalaTipo == "SALA CON BOTONERA":
        print("sony")
        ModificacionTipoSala(SalaTipo, "8D:00:04:01:92", "8D:00:04:02:93", "https://bbva.webex.com", "8D:00:05:03:95",
                             "8D:00:05:02:94", "8D:00:05:01:93", Pantalla)
    elif Pantalla == "PANTALLA NEXCOM":
        print("nexcom")
        ModificacionTipoSala(SalaTipo, "7F 08 99 A2 B3 C4 02 FF 01 00 CF", "7F 08 99 A2 B3 C4 02 FF 01 01 CF",
                             "https://bbva.webex.com", "", "", "", Pantalla)
    else:
        print("otro")
        ModificacionTipoSala(SalaTipo, "AA:11:01:01:01:14", "AA:11:01:01:00:13", "https://bbva.webex.com",
                             "AA:14:01:01:18:2E", "AA:14:01:01:23:39", "AA:14:01:01:21:37", Pantalla)
    pass


def ModificacionTipoSala(SalaTipo, ON_, OFF_, URL_, PCSALA_, HDMI_, VGA_, Pantalla):
    file = open(CONFIG_FILE, "r")
    data = file.read()
    file.close()
    if INICIADO == "":
        data = data.replace("INICIADO =", u"INICIADO = 1")
        print(SalaTipo)
        if SalaTipo == "SALA SIN BOTONERA":
            print("INFO SALA SIN BOTONERA")
            data = data.replace("ON = ", u"ON = " + ON_)
            data = data.replace("OFF = ", u"OFF = " + OFF_)
            data = data.replace("URL = ", u"URL = " + URL_)
            data = data.replace("SALAPC = ", u"SALAPC = " + PCSALA_)
            data = data.replace("VGA = ", u"VGA = " + VGA_)
            data = data.replace("HDMI = ", u"HDMI = " + HDMI_)
        elif SalaTipo == "SALA CON BOTONERA" and Pantalla != "PANTALLA NEXCOM":
            print("INFO SALA CON BOTONERA")
            data = data.replace("VOL_UP = ", u"VOL_UP = 8D:00:01:01:8F")
            data = data.replace("VOL_DOWN = ", u"VOL_DOWN = 8D:00:01:02:90")
            data = data.replace("REBOOT = ", u"REBOOT = 8D:00:02:01:90")
            data = data.replace("WEBEX = ", u"WEBEX = 8D:00:03:01:91")
            data = data.replace("ON = ", u"ON = " + ON_)
            data = data.replace("OFF = ", u"OFF = " + OFF_)
            data = data.replace("URL = ", u"URL = " + URL_)
            data = data.replace("SALAPC = ", u"SALAPC = " + PCSALA_)
            data = data.replace("VGA = ", u"VGA = " + VGA_)
            data = data.replace("HDMI = ", u"HDMI = " + HDMI_)
    elif INICIADO == "1":
        if SalaTipo == "SALA SIN BOTONERA":
            data = data.replace("ON = " + ON, u"ON = ")
            data = data.replace("OFF = " + OFF, u"OFF = ")
            data = data.replace("URL = " + URL, u"URL = ")
            data = data.replace("SALAPC = " + PCSALA, u"SALAPC = ")
            data = data.replace("VGA = " + VGA, u"VGA = ")
            data = data.replace("HDMI = " + HDMI, u"HDMI = ")
            data = data.replace("VOL_UP = 8D:00:01:01:8F", u"VOL_UP = ")
            data = data.replace("VOL_DOWN = 8D:00:01:02:90", u"VOL_DOWN = ")
            data = data.replace("REBOOT = 8D:00:02:01:90", u"REBOOT = ")
            data = data.replace("WEBEX = 8D:00:03:01:91", u"WEBEX = ")
            data = data.replace("ON = ", u"ON = " + ON_)
            data = data.replace("OFF = ", u"OFF = " + OFF_)
            data = data.replace("URL = ", u"URL = " + URL_)
            data = data.replace("SALAPC = ", u"SALAPC = " + PCSALA_)
            data = data.replace("VGA = ", u"VGA = " + VGA_)
            data = data.replace("HDMI = ", u"HDMI = " + HDMI_)

        elif SalaTipo == "SALA CON BOTONERA":
            if Pantalla == "PANTALLA NEXCOM":
                data = data.replace("ON = " + ON, u"ON = ")
                data = data.replace("OFF = " + OFF, u"OFF = ")
                data = data.replace("URL = " + URL, u"URL = ")
                data = data.replace("SALAPC = " + PCSALA, u"SALAPC = ")
                data = data.replace("VGA = " + VGA, u"VGA = ")
                data = data.replace("HDMI = " + HDMI, u"HDMI = ")
                data = data.replace("VOL_UP = 8D:00:01:01:8F", u"VOL_UP = ")
                data = data.replace("VOL_DOWN = 8D:00:01:02:90", u"VOL_DOWN = ")
                data = data.replace("REBOOT = 8D:00:02:01:90", u"REBOOT = ")
                data = data.replace("WEBEX = 8D:00:03:01:91", u"WEBEX = ")
                data = data.replace("ON = ", u"ON = " + ON_)
                data = data.replace("OFF = ", u"OFF = " + OFF_)
                data = data.replace("URL = ", u"URL = " + URL_)
                data = data.replace("SALAPC = ", u"SALAPC = " + PCSALA_)
                data = data.replace("VGA = ", u"VGA = " + VGA_)
                data = data.replace("HDMI = ", u"HDMI = " + HDMI_)
            else:
                data = data.replace("ON = " + ON, u"ON = ")
                data = data.replace("OFF = " + OFF, u"OFF = ")
                data = data.replace("URL = " + URL, u"URL = ")
                data = data.replace("SALAPC = " + PCSALA, u"SALAPC = ")
                data = data.replace("VGA = " + VGA, u"VGA = ")
                data = data.replace("HDMI = " + HDMI, u"HDMI = ")
                data = data.replace("VOL_UP = 8D:00:01:01:8F", u"VOL_UP = ")
                data = data.replace("VOL_DOWN = 8D:00:01:02:90", u"VOL_DOWN = ")
                data = data.replace("REBOOT = 8D:00:02:01:90", u"REBOOT = ")
                data = data.replace("WEBEX = 8D:00:03:01:91", u"WEBEX = ")
                data = data.replace("VOL_UP = ", u"VOL_UP = 8D:00:01:01:8F")
                data = data.replace("VOL_DOWN =", u"VOL_DOWN = 8D:00:01:02:90")
                data = data.replace("REBOOT =", u"REBOOT = 8D:00:02:01:90")
                data = data.replace("WEBEX =", u"WEBEX = 8D:00:03:01:91")
                data = data.replace("SALAPC = ", u"SALAPC = " + PCSALA_)
                data = data.replace("VGA = ", u"VGA = " + VGA_)
                data = data.replace("HDMI = ", u"HDMI = " + HDMI_)
    file = open(CONFIG_FILE, "w")
    file.write(data)
    file.close()
    pass


def buttonClosePress(event):
    nameSala = t1.GetValue()
    Identificador = t2.GetValue()
    PSerie = cbbox_nombres.GetValue()
    Pantalla = cbbox_pantallas.GetValue()
    TConector = cbbox_conector.GetValue()
    TInact = cbbox_inactividad.GetValue()
    TSala = cbbox_salatipo.GetValue()

    cadena, val = MensajeWarning(nameSala, Identificador, PSerie, TConector, TInact, TSala)

    if val == True:
        wx.MessageBox(cadena, 'Warning', wx.OK | wx.ICON_WARNING)
    else:
        file = open(CONFIG_FILE, "r")
        data = file.read()
        file.close()
        data = data.replace("PORT =", u"PORT = " + PSerie)
        data = data.replace("ID =", u"ID = " + Identificador)
        data = data.replace("NAME =", u"NAME = " + nameSala)
        data = data.replace("PANTALLA =", u"PANTALLA = " + Pantalla)
        data = data.replace("CONECTOR =", u"CONECTOR = " + TConector)
        if TInact != "":
            data = data.replace("TIME = 5", u"TIME = " + TInact)
        data = data.replace("SALA =", u"SALA = " + TSala)
        file = open(CONFIG_FILE, "w")
        file.write(data)
        file.close()
        TipoPantalla(Pantalla, TSala, TConector)
        frame1.Close()
    # RebootServer(u"Iniciando reinicio del sistema",0)
    print("Nombre de la sala : {}".format(t1.GetValue()))
    print("Identificador de la sala : {}".format(t2.GetValue()))
    print("Puerto Serie : {}".format(cbbox_nombres.GetValue()))
    print("Tipo de pantalla : {}".format(cbbox_pantallas.GetValue()))
    print("Tipo de conector : {}".format(cbbox_conector.GetValue()))
    print("Tipo de inactividad : {}".format(cbbox_inactividad.GetValue()))
    print("Tipo de inactividad : {}".format(cbbox_salatipo.GetValue()))
    pass

'''
Crea interfaz de la aplicación para introducir los datos de la sala
'''
app = wx.App()

for puerto in list(list_ports.comports()):
    items_list.append(str(puerto).split(" - ")[0])

frame1 = wx.Frame(parent=None, title=u'CONFIGURACION DE LA SALA', size=[GetSystemMetrics(0), GetSystemMetrics(1)],
                  style=wx.STAY_ON_TOP | wx.BORDER_NONE | wx.SYSTEM_MENU | wx.MINIMIZE_BOX |
                        wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
frame1.SetBackgroundColour((0, 68, 129))

bmp = wx.Bitmap('ImageConfig/BBVA.png', wx.BITMAP_TYPE_PNG)

image = bmp.ConvertToImage()
# GetSystemMetrics(1)-(GetSystemMetrics(1)-GetSystemMetrics(1)/21)
imageBitmap = wx.StaticBitmap(frame1, wx.ID_ANY, wx.Bitmap(image.Rescale(bmp.GetWidth() / 2, bmp.GetHeight() / 2)))
imageBitmap.SetPosition((GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) / 20),
                         (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) / 64))))

# -------------------------------------------------------------
content = wx.StaticText(frame1, -1, "CONFIGURACIÓN SALA LIGERA", pos=(0, (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4)),
                        size=[GetSystemMetrics(0), int((GetSystemMetrics(1) / 4) / 4)],
                        style=wx.FONTWEIGHT_BOLD | wx.ALIGN_CENTRE)
content.SetForegroundColour("White")
font1 = wx.Font(45, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
content.SetFont(font1)
# -------------------------------------------------------------
content1 = wx.StaticText(frame1, -1, label="NOMBRE DE LA SALA:",
                         pos=(0, (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 2))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content1.SetForegroundColour("White")
font2 = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
content1.SetFont(font2)
# vbox = wx.BoxSizer(wx.VERTICAL)
hbox1 = wx.BoxSizer(wx.HORIZONTAL)
hbox1.Add(content1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
t1 = wx.TextCtrl(frame1, pos=(GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
                              (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 2))),
                 size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                       int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content2 = wx.StaticText(frame1, -1, label="IDENTIFICADOR DE LA SALA:", pos=(0, (bmp.GetHeight() / 2) + (
        bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 2))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content2.SetForegroundColour("White")
content2.SetFont(font2)
hbox1.Add(content2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
t2 = wx.TextCtrl(frame1, pos=(GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
                              (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (
                                  int((GetSystemMetrics(1) / 4) / 2))),
                 size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                       int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content3 = wx.StaticText(frame1, -1, label=" PUERTO SERIE:", pos=(0, (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (
    int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 2)) + (int((GetSystemMetrics(1) / 4) / 4))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content3.SetForegroundColour("White")
content3.SetFont(font2)
cbbox_nombres = wx.ComboBox(frame1, -1, choices=items_list, pos=(GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
                                                                 (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 2)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4))),
                            size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                                  int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content4 = wx.StaticText(frame1, -1, label="TIPO DE PANTALLA:", pos=(0,
                                                                     (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (
                                                                         int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                         int((GetSystemMetrics(1) / 4) / 2)) + (
                                                                         int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                         int((GetSystemMetrics(1) / 4) / 4))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content4.SetForegroundColour("White")
content4.SetFont(font2)
cbbox_pantallas = wx.ComboBox(frame1, -1, choices=["PANTALLA SAMSUNG", "PANTALLA SONY", "PANTALLA NEXCOM"], pos=(
    GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
    (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 2)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4))),
                              size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                                    int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content5 = wx.StaticText(frame1, -1, label="CONEXIÓN EQUIPO VS PANTALLA:", pos=(0, (bmp.GetHeight() / 2) + (
        bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 2)) + (int(
    (GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content5.SetForegroundColour("White")
content5.SetFont(font2)
cbbox_conector = wx.ComboBox(frame1, -1, choices=["CONECTOR HDMI1", "CONECTOR HDMI2", "CONECTOR DVI"], pos=(
    GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
    (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 2)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4))),
                             size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                                   int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content5 = wx.StaticText(frame1, -1, label="TIEMPO DE INACTIVIDAD:", pos=(0, (bmp.GetHeight() / 2) + (
        bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 2)) + (
                                                                              int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                              int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                              int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                              int((GetSystemMetrics(1) / 4) / 4))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content5.SetForegroundColour("White")
content5.SetFont(font2)
cbbox_inactividad = wx.ComboBox(frame1, -1, choices=["5", "10", "15", "20", "0"], pos=(
    GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
    (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 2)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4))),
                                size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                                      int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------
content5 = wx.StaticText(frame1, -1, label="TIPO DE SALA:", pos=(0, (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (
    int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 2)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4)) + (
                                                                     int((GetSystemMetrics(1) / 4) / 4))),
                         size=[GetSystemMetrics(0) / 2 - GetSystemMetrics(0) / 32, int((GetSystemMetrics(1) / 4) / 8)],
                         style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content5.SetForegroundColour("White")
content5.SetFont(font2)
cbbox_salatipo = wx.ComboBox(frame1, -1, choices=["SALA SIN BOTONERA", "SALA CON BOTONERA"], pos=(
    GetSystemMetrics(0) / 2 + GetSystemMetrics(0) / 24,
    (bmp.GetHeight() / 2) + (bmp.GetHeight() / 4) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 2)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4)) + (
        int((GetSystemMetrics(1) / 4) / 4)) + (int((GetSystemMetrics(1) / 4) / 4))),
                             size=[GetSystemMetrics(0) / 8 + int(((GetSystemMetrics(0) / 2) / 16)),
                                   int((GetSystemMetrics(1) / 4) / 8)])
# -------------------------------------------------------------

content6 = wx.StaticText(frame1, -1, label="Creando Oportunidades", pos=(
    (GetSystemMetrics(0) - (bmp.GetWidth() + (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) / 20)))),
    (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) / 32))),
                         size=[bmp.GetWidth(), int(bmp.GetHeight() / 2)], style=wx.BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
content6.SetForegroundColour("White")
font4 = wx.Font(27, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
content6.SetFont(font4)

# -------------------------------------------------------------
btn = wx.Button(frame1, label="Guardar y Reiniciar",
                size=[int(((GetSystemMetrics(0) / 2) / 4)) + int(((GetSystemMetrics(0) / 2) / 4)),
                      int(((GetSystemMetrics(0) / 2) / 8) / 2)], pos=(
        int(GetSystemMetrics(0) / 2) - int(((GetSystemMetrics(0) / 2) / 4)) + int(((GetSystemMetrics(0) / 2) / 16)),
        int((GetSystemMetrics(1) / 2)) + int((GetSystemMetrics(1) / 4)) + int((GetSystemMetrics(1) / 4) / 8) + int(
            (GetSystemMetrics(1) / 4) / 8) + int((GetSystemMetrics(1) / 4) / 8)), style=wx.BORDER_NONE)
btn.SetFont(font2)
btn.Bind(wx.EVT_BUTTON, buttonClosePress)
btn.SetBackgroundColour((20, 100, 165))
btn.SetForegroundColour("White")


'''
Ajusta los privilegios para que se pueda reiniciar el sistema
'''
def AdjustPrivilege(priv, enable=1):
    # Get the process token
    flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    # Get the ID for the system shutdown privilege.
    idd = win32security.LookupPrivilegeValue(None, priv)
    # Now obtain the privilege for this process.
    # Create a list of the privileges to be added.
    if enable:
        newPrivileges = [(idd, SE_PRIVILEGE_ENABLED)]
    else:
        newPrivileges = [(idd, 0)]
    # and make the adjustment
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


def RebootServer(message, timeout, user=None, bForce=0, bReboot=1):
    AdjustPrivilege(SE_SHUTDOWN_NAME)
    try:
        win32api.InitiateSystemShutdown(user, message, timeout, bForce, bReboot)
    finally:
        # Now we remove the privilege we just added.
        AdjustPrivilege(SE_SHUTDOWN_NAME, 0)

'''
Detecta si un proceso se esta ejecutando o no
'''
def ProcessRunning(processname):
    found = False
    for proc in psutil.process_iter():
        if proc.name() == processname:
            found = True
    return found

'''
Determina el numero de veces que se esta ejecutando un proceso
'''
def numProcessRunning(processname):
    num = 0
    for proc in psutil.process_iter():
        if proc.name() == processname:
            num = num + 1
    return num


if __name__ == "__main__":

    if numProcessRunning('rs232control_sb.exe') < 3 or numProcessRunning('rs232control_cb.exe') < 3:
        time.sleep(5)
        config.read(CONFIG_FILE)
        NOMBRE = str(config.get("ROOM_DATA", "NAME"))
        ID = str(config.get("ROOM_DATA", "ID"))
        PORT = str(config.get("RS232", "PORT"))
        SALA = str(config.get("TIPO_SALA", "SALA"))
        PANTALLA = str(config.get("TIPO_SALA", "PANTALLA"))
        CONECTOR = str(config.get("TIPO_SALA", "CONECTOR"))
        print("|" + NOMBRE + "|")
        print("|" + ID + "|")
        print("|" + PORT + "|")
        print("|" + SALA + "|")
        print("|" + PANTALLA + "|")
        print("|" + CONECTOR + "|")

        if (NOMBRE == "") and (ID == "") and (PORT == "") and (SALA == "") and (PANTALLA == "") and (CONECTOR == ""):
            frame1.Show()
            app.MainLoop()
            time.sleep(5)
            #RebootServer(u"Iniciando reinicio del sistema", 0)
            sys.exit(2)

        if not ProcessRunning("eCam.exe"):
            os.system("ConfiguraciónDeLaAplicaciónPTZApp.pdf")
            aviso = "La aplicación de control PTZApp encargada del control de la camará y el audio de la sala no esta " \
                    "configurada.\n "
            aviso = aviso + "\n"
            aviso = aviso + "Por favor, realice la configuración de la aplicación acorde lo indicado en el manual de " \
                            "configuración de la sala Ligera. "
            aviso = aviso + ""
            wx.MessageBox(aviso, 'ERROR', wx.OK | wx.ICON_ERROR)

        try:
            ExecuteScript = subprocess.Popen("cd " + PATH + " & rs232control.exe", stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            Script = ExecuteScript.stdout.read()
            ExecuteScript.stdout.close()
        except Exception as e:
            print("Error al establecer cobertura: {}".format(e))
            pass

    else:
        wx.MessageBox(u"No se puede iniciar, existe otro proceso en ejecucion.", 'Warning', wx.OK | wx.ICON_WARNING)
        sys.exit(1)
