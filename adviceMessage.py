import wx
from win32api import GetSystemMetrics

FRAME = None
FRAME_1 = None


def button_close(event):
    FRAME.Hide()
    FRAME_1.Hide()
    pass

def hide():
    global FRAME
    global FRAME_1

    FRAME_1.Hide()
    FRAME.Hide()


def show():
    global FRAME
    global FRAME_1

    FRAME_1.Show()
    FRAME.Show()

def init(logger):
    global FRAME
    global FRAME_1

    try:
        app = wx.App()
        FRAME_1 = wx.Frame(parent=None, title=u'', size=[GetSystemMetrics(0), GetSystemMetrics(1)],
                           style=wx.STAY_ON_TOP | wx.BORDER_NONE | wx.SYSTEM_MENU | wx.MINIMIZE_BOX |
                                wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
        FRAME_1.SetBackgroundColour("Black")
        FRAME_1.SetTransparent(127)

        FRAME = wx.Frame(parent=None, title=u'AVISO DE CIERRE DE SESIÓN',
                         size=[GetSystemMetrics(0), int(GetSystemMetrics(1) / 4)],
                         style=wx.STAY_ON_TOP | wx.BORDER_NONE | wx.SYSTEM_MENU | wx.MINIMIZE_BOX |
                               wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
        FRAME.SetBackgroundColour((4, 50, 99))
        content = wx.StaticText(FRAME, -1, "Estas a punto de cerrar la sesión...",
                                pos=(0, int((GetSystemMetrics(1) / 4) / 8)),
                                size=[GetSystemMetrics(0), int((GetSystemMetrics(1) / 4) / 4)],
                                style=wx.FONTWEIGHT_BOLD | wx.ALIGN_CENTRE)
        content.SetForegroundColour("White")
        font1 = wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        content.SetFont(font1)
        content2 = wx.StaticText(FRAME, -1,
                                 "Se procederá al apagado de la pantalla y se borrarán los archivos almacenados en el equipo. "
                                 "Mueva el cursor o pulse cancelar para abortar.",
                                 pos=(0, int((GetSystemMetrics(1) / 4) / 4) + int((GetSystemMetrics(1) / 4) / 8)),
                                 size=[GetSystemMetrics(0), int((GetSystemMetrics(1) / 4) / 4)],
                                 style=wx.HORIZONTAL | wx.FONTWEIGHT_BOLD | wx.ALIGN_CENTRE)
        content2.SetForegroundColour("White")
        font2 = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        content2.SetFont(font2)
        btn = wx.Button(FRAME, label="Cancelar",
                        size=[int(((GetSystemMetrics(0) / 2) / 8)), int(((GetSystemMetrics(0) / 2) / 8) / 2)], pos=(
                int(GetSystemMetrics(0) / 2) - int(((GetSystemMetrics(0) / 2) / 8) / 2),
                int((GetSystemMetrics(1) / 4) / 4) + int((GetSystemMetrics(1) / 4) / 8) + int(
                    (GetSystemMetrics(1) / 4) / 8) + int(
                    (GetSystemMetrics(1) / 4) / 8)), style=wx.BORDER_NONE)
        btn.SetFont(font2)
        btn.Bind(wx.EVT_BUTTON, button_close)
        btn.SetBackgroundColour((0, 68, 129))
        btn.SetForegroundColour("White")

        # frame1.Centre()
        FRAME.Centre()
        # frame.Show()
        app.MainLoop()
        print("1")

    except:
        print("2")
        logger.error("Error en la ventana de aviso")
