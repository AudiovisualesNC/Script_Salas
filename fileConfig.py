#!/usr/bin/python
# -*- coding: cp1252 -*-
import configparser
import os
import pathlib
import subprocess
import sys
import time

import psutil
import wx
from serial.tools import list_ports
from win32api import GetSystemMetrics


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


'''
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
'''
'''
Crea interfaz de la aplicación para introducir los datos de la sala
'''


class ConfigGui(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title=u'CONFIGURACION DE LA SALA',
                         size=[GetSystemMetrics(0), GetSystemMetrics(1)],
                         style=wx.STAY_ON_TOP | wx.BORDER_NONE | wx.SYSTEM_MENU | wx.MINIMIZE_BOX |
                               wx.MAXIMIZE_BOX | wx.CLOSE_BOX)

        self.SetBackgroundColour((0, 68, 129))

        # Se añade el logo de BBVA

        bmp = wx.Bitmap('ImageConfig/BBVA.png', wx.BITMAP_TYPE_PNG)

        image = bmp.ConvertToImage()

        imageBitmap = wx.StaticBitmap(self, wx.ID_ANY,
                                      wx.Bitmap(image.Rescale(bmp.GetWidth() // 2, bmp.GetHeight() // 2)))
        imageBitmap.SetPosition((GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) // 20),
                                 (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) // 64))))

        # Eslogan

        content6 = wx.StaticText(self, -1, label="Creando Oportunidades", pos=(
            (GetSystemMetrics(0) - (
                    bmp.GetWidth() + (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) // 20)))),
            (GetSystemMetrics(0) - (GetSystemMetrics(0) - GetSystemMetrics(0) // 32))),
                                 size=[bmp.GetWidth(), int(bmp.GetHeight() // 2)],
                                 style=wx.BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        content6.SetForegroundColour("White")
        font4 = wx.Font(27, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        content6.SetFont(font4)

        # Titulo principal

        content = wx.StaticText(self, -1, "CONFIGURACIÓN SALA LIGERA",
                                pos=(0, (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4)),
                                size=[GetSystemMetrics(0), (GetSystemMetrics(1) // 4) // 4],
                                style=wx.FONTWEIGHT_BOLD | wx.ALIGN_CENTRE)
        content.SetForegroundColour("White")

        font1 = wx.Font(45, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        content.SetFont(font1)

        # Nombre de la sala

        content1 = wx.StaticText(self, -1, label="NOMBRE DE LA SALA:",
                                 pos=(0, (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (
                                     int((GetSystemMetrics(1) // 4) // 2))),
                                 size=[GetSystemMetrics(0) // 2 - GetSystemMetrics(0) // 32,
                                       int((GetSystemMetrics(1) // 4) // 8)],
                                 style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        content1.SetForegroundColour("White")
        font2 = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        content1.SetFont(font2)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(content1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t1 = wx.TextCtrl(self, pos=(GetSystemMetrics(0) // 2 + GetSystemMetrics(0) // 24,
                                         (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (
                                             int((GetSystemMetrics(1) // 4) // 2))),
                              size=[GetSystemMetrics(0) // 8 + int(((GetSystemMetrics(0) // 2) // 16)),
                                    int((GetSystemMetrics(1) // 4) // 8)])

        # ID Sala

        content2 = wx.StaticText(self, -1, label="IDENTIFICADOR DE LA SALA:", pos=(0, (bmp.GetHeight() // 2) + (
                bmp.GetHeight() // 4) + (int((GetSystemMetrics(1) // 4) // 4)) + (int((GetSystemMetrics(
            1) // 4) // 2))),
                                 size=[GetSystemMetrics(0) // 2 - GetSystemMetrics(0) // 32,
                                       int((GetSystemMetrics(1) // 4) // 8)],
                                 style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        content2.SetForegroundColour("White")
        content2.SetFont(font2)
        hbox1.Add(content2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t2 = wx.TextCtrl(self, pos=(GetSystemMetrics(0) // 2 + GetSystemMetrics(0) // 24,
                                         (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (
                                             int((GetSystemMetrics(1) // 4) // 4)) + (
                                             int((GetSystemMetrics(1) // 4) // 2))),
                              size=[GetSystemMetrics(0) // 8 + int(((GetSystemMetrics(0) // 2) // 16)),
                                    int((GetSystemMetrics(1) // 4) // 8)])

        # Con o sin botonera

        content5 = wx.StaticText(self, -1, label="TIPO DE SALA:",
                                 pos=(0, (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (
                                     int((GetSystemMetrics(1) // 4) // 4)) + (int((GetSystemMetrics(1) // 4) // 2)) + (
                                          int((GetSystemMetrics(1) // 4) // 4))),
                                 size=[GetSystemMetrics(0) // 2 - GetSystemMetrics(0) // 32,
                                       int((GetSystemMetrics(1) // 4) // 8)],
                                 style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        content5.SetForegroundColour("White")
        content5.SetFont(font2)
        self.cbbox_salatipo = wx.ComboBox(self, -1, choices=["SALA SIN BOTONERA", "SALA CON BOTONERA"], pos=(
            GetSystemMetrics(0) // 2 + GetSystemMetrics(0) // 24,
            (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (int((GetSystemMetrics(1) // 4) // 4)) + (
                int((GetSystemMetrics(1) // 4) // 2)) + (int((GetSystemMetrics(1) // 4) // 4))),
                                          size=[GetSystemMetrics(0) // 8 + int(((GetSystemMetrics(0) // 2) // 16)),
                                                int((GetSystemMetrics(1) // 4) // 8)])

        self.cbbox_salatipo.Bind(wx.EVT_COMBOBOX, self.show_com_ports)

        # Puertos de comunicación, por defecto ocultos a menos que se seleccione SALA CON BOTONERA

        items_list = []

        for puerto in list(list_ports.comports()):
            items_list.append(str(puerto).split(" - ")[0])

        self.content3 = wx.StaticText(self, -1, label=" PUERTO SERIE:",
                                      pos=(0, (bmp.GetHeight() // 2 + (bmp.GetHeight() // 4) + (
                                          int((GetSystemMetrics(1) // 4) // 4)) + (
                                                   int((GetSystemMetrics(1) // 4) // 2)) + (
                                                   int((GetSystemMetrics(1) // 4) // 4))) + + (
                                          int((GetSystemMetrics(1) // 4) // 4))),
                                      size=[GetSystemMetrics(0) // 2 - GetSystemMetrics(0) // 32,
                                            int((GetSystemMetrics(1) // 4) // 8)],
                                      style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        self.content3.SetForegroundColour("White")
        self.content3.SetFont(font2)
        self.content3.Hide()
        self.cbbox_nombres = wx.ComboBox(self, -1, choices=items_list,
                                         pos=(GetSystemMetrics(0) // 2 + GetSystemMetrics(0) // 24,
                                              (bmp.GetHeight() // 2 + (bmp.GetHeight() // 4) + (
                                                  int((GetSystemMetrics(1) // 4) // 4)) + (
                                                   int((GetSystemMetrics(1) // 4) // 2)) + (
                                                   int((GetSystemMetrics(1) // 4) // 4))) + + (
                                                  int((GetSystemMetrics(1) // 4) // 4))),
                                         size=[GetSystemMetrics(0) // 8 + int(((GetSystemMetrics(0) // 2) // 16)),
                                               int((GetSystemMetrics(1) // 4) // 8)])
        self.cbbox_nombres.Hide()

        # Tiempo de reinicio

        content5 = wx.StaticText(self, -1, label="TIEMPO DE INACTIVIDAD:", pos=(0, (bmp.GetHeight() // 2) + (
                bmp.GetHeight() // 4) + (int((GetSystemMetrics(1) // 4) // 4)) + (int((GetSystemMetrics(
            1) // 4) // 2)) + (
                                                                                    int((GetSystemMetrics(
                                                                                        1) // 4) // 4)) + (
                                                                                    int((GetSystemMetrics(
                                                                                        1) // 4) // 4)) + (
                                                                                    int((GetSystemMetrics(
                                                                                        1) // 4) // 4)) + (
                                                                                    int((GetSystemMetrics(
                                                                                        1) // 4) // 4))),
                                 size=[GetSystemMetrics(0) // 2 - GetSystemMetrics(0) // 32,
                                       int((GetSystemMetrics(1) // 4) // 8)],
                                 style=wx.FONTWEIGHT_BOLD | wx.ALIGN_RIGHT | wx.ALIGN_TOP)
        content5.SetForegroundColour("White")
        content5.SetFont(font2)
        self.cbbox_inactividad = wx.ComboBox(self, -1, choices=["5", "10", "15", "20", "0"], pos=(
            GetSystemMetrics(0) // 2 + GetSystemMetrics(0) // 24,
            (bmp.GetHeight() // 2) + (bmp.GetHeight() // 4) + (int((GetSystemMetrics(1) // 4) // 4)) + (
                int((GetSystemMetrics(1) // 4) // 2)) + (int((GetSystemMetrics(1) // 4) // 4)) + (
                int((GetSystemMetrics(1) // 4) // 4)) + (int((GetSystemMetrics(1) // 4) // 4)) + (
                int((GetSystemMetrics(1) // 4) // 4))),
                                             size=[GetSystemMetrics(0) // 8 + int(((GetSystemMetrics(0) // 2) // 16)),
                                                   int((GetSystemMetrics(1) // 4) // 8)])

        # Boton Guardar y Reiniciar
        btn = wx.Button(self, label="Guardar y Reiniciar",
                        size=[int(((GetSystemMetrics(0) // 2) // 4)) + int(((GetSystemMetrics(0) // 2) // 4)),
                              int(((GetSystemMetrics(0) // 2) // 8) // 2)], pos=(
                int(GetSystemMetrics(0) // 2) - int(((GetSystemMetrics(0) // 2) // 4)) + int(
                    ((GetSystemMetrics(0) // 2) // 16)),
                int((GetSystemMetrics(1) // 2)) + int((GetSystemMetrics(1) // 4)) + int(
                    (GetSystemMetrics(1) // 4) // 8) + int(
                    (GetSystemMetrics(1) // 4) // 8) + int((GetSystemMetrics(1) // 4) // 8)), style=wx.BORDER_NONE)
        btn.SetFont(font2)
        btn.Bind(wx.EVT_BUTTON, self.buttonClosePress)
        btn.SetBackgroundColour((20, 100, 165))
        btn.SetForegroundColour("White")

    def show(self):
        self.Show()

    def hide(self):
        self.Hide()

    def show_com_ports(self, event):
        if self.cbbox_salatipo.GetValue() == "SALA CON BOTONERA":
            self.cbbox_nombres.Show()
            self.content3.Show()
        else:
            self.cbbox_nombres.Hide()
            self.content3.Hide()

    def buttonClosePress(self, event):
        name = self.t1.GetValue()
        id = self.t2.GetValue()
        serial = self.cbbox_nombres.GetValue()
        time = self.cbbox_inactividad.GetValue()
        type = self.cbbox_salatipo.GetValue()

        cadena, val = self.MensajeWarning(name, id, serial, time, type)

        if val:
            wx.MessageBox(cadena, 'Warning', wx.OK | wx.ICON_WARNING)
        else:

            if os.path.isfile("config.ini"):
                os.remove("config.ini")

            file = open("config.ini", "w+")
            data = ""
            if type == "SALA CON BOTONERA":
                data = data + "[RS232]\n"
                data = data + "PORT = " + serial + "\n"
                data = data + "\n"

            data = data + "[ROOM_TYPE]\n"
            type = str(True) if type == "SALA CON BOTONERA" else str(False)
            data = data + "KEYPAD = " + type + "\n"
            data = data + "\n"
            data = data + "[ROOM_DATA]\n"
            data = data + "NAME = " + name + "\n"
            data = data + "ID = " + id + "\n"
            data = data + "[RESTART]\n"
            data = data + "TIME = " + time + "\n"
            file.write(data)
            file.close()
            self.Close()
            # os.system(r"shutdown /r")

    def MensajeWarning(self, name, id, serial, time, type):
        cad = "Debe intrioducir los siguientes parámetros de manera satisfactoria para la correcta configuración de " \
              "la sala:\n "
        cad = cad + "\n"
        val = False

        if (name == "" or "sala" not in name.lower() or ("(" not in name) or (")" not in name) or (
                len(name.split(" ")) < 3)):
            val = True
            cad = cad + "*Insertar el nombre de la sala de acuerdo al siguiente patrón:\n"
            cad = cad + "\n"
            cad = cad + "-En oficinas rellenar:'nombre municipio' 'oficina' 'número oficina'(Sala Video 'nombre " \
                        "sala').\n "
            cad = cad + "\n"
            cad = cad + "     Ejemplo: Valencia oficina 6517 (Sala Video Valencia Oeste).\n"
            cad = cad + "\n"
            cad = cad + "-En Edificios centrales rellenar:'nombre municipio'  'nombre de edificio'(Sala  'nombre " \
                        "sala').\n "
            cad = cad + "\n"
            cad = cad + "     Ejemplo:  Madrid Recoletos (Sala 1 Sur).\n"
            cad = cad + "\n"

        if id == "" or not RepresentsInt(id):
            val = True
            cad = cad + "*Insertar el identificador de la sala de acuerdo al siguiente patrón: \n"
            cad = cad + "\n"
            cad = cad + "  -En oficinas rellenar:'número oficina'.\n"
            cad = cad + "\n"
            cad = cad + "     Ejemplo: 6517\n"
            cad = cad + "\n"
            cad = cad + "-En Edificios centrales rellenar:'número de la sala en el inventario de infraestructura " \
                        "europa'.\n "
            cad = cad + "\n"
            cad = cad + "     Ejemplo: 1000571\n"
            cad = cad + "\n"

        if type == "":
            val = True
            cad = cad + "*Insertar el tipo de sala de acuerdo al desplegable proporcionado. \n"
            cad = cad + "\n"
        elif type == "SALA CON BOTONERA" and serial == "":
            val = True
            cad = cad + "*Insertar el puerto serie de acuerdo al desplegable proporcionado.\n"
            cad = cad + "\n"

        if time == "":
            val = True
            cad = cad + "*Insertar el tiempo de reinicio de acuerdo al desplegable proporcionado. \n"
            cad = cad + "\n"

        return cad, val


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
    print(numProcessRunning('rs232control.exe'))
    if numProcessRunning('rs232control.exe') < 1:
        if os.path.isfile("./config.ini"):
            try:
                config = configparser.ConfigParser()
                config.read("./config.ini")
                if not config.has_option("ROOM_TYPE", "KEYPAD") or not config.has_option("ROOM_DATA",
                                                                                         "NAME") or not config.has_option(
                    "ROOM_DATA", "ID") or not config.has_option("RESTART", "TIME"):
                    app = wx.App()
                    frame = ConfigGui()
                    frame.show()
                    app.MainLoop()
                    time.sleep(5)
                elif config.get("ROOM_DATA", "NAME") == "" or config.get("ROOM_DATA", "ID") == "" or config.get(
                        "RESTART", "TIME") == "" or config.has_option("ROOM_TYPE", "KEYPAD") == "":
                    app = wx.App()
                    frame = ConfigGui()
                    frame.show()
                    app.MainLoop()
                    time.sleep(5)
                elif config.get("ROOM_TYPE", "KEYPAD") == "True" and not config.has_option("RS232", "PORT"):
                    app = wx.App()
                    frame = ConfigGui()
                    frame.show()
                    app.MainLoop()
                    time.sleep(5)
                elif config.get("ROOM_TYPE", "KEYPAD") == "True" and config.get("RS232", "PORT") == "":
                    app = wx.App()
                    frame = ConfigGui()
                    frame.show()
                    app.MainLoop()
                    time.sleep(5)
                else:
                    try:
                        ExecuteScript = subprocess.Popen(
                            "cd " + pathlib.Path(__file__).parent.resolve().name + " & rs232control.exe",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                        Script = ExecuteScript.stdout.read()
                        ExecuteScript.stdout.close()
                    except Exception as e:
                        print("Error al establecer cobertura: {}".format(e))
                        pass
            except configparser.ParsingError as e:
                app = wx.App()
                frame = ConfigGui()
                frame.show()
                app.MainLoop()
                time.sleep(5)
        else:
            app = wx.App()
            frame = ConfigGui()
            frame.show()
            app.MainLoop()
            time.sleep(5)

        sys.exit(2)
