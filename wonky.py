#!/usr/bin/env python3
import sys
import time
from ansi2html import Ansi2HTMLConverter
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QMargins, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QSizeGrip, QTextEdit
import sys
import time
import os
import subprocess
import asyncio
from enum import Enum
import datetime
import random

home = os.path.expanduser('~')

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,
                 True)  # enable highdpi scaling
app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

screen = app.primaryScreen()
screenW = screen.size().width()
screenH = screen.size().height()

all_screens = app.screens()

for scr in all_screens:
    print()
    print(scr.name())
    print(scr.availableGeometry())
    print(scr.availableGeometry().width())
    print(scr.availableGeometry().height())
    print(scr.size())
    print(scr.size().width())
    print(scr.size().height())


class OutputType(Enum):
    PLAINTEXT = 1
    HTML = 2
    ANSI = 3


class Alignment(Enum):
    TOPLEFT = 1
    TOPCENTER = 2
    TOPRIGHT = 3
    MIDDLELEFT = 4
    MIDDLECENTER = 5
    MIDDLERIGHT = 6
    BOTTOMLEFT = 7
    BOTTOMCENTER = 8
    BOTTOMRIGHT = 9
    LEFT = 10
    CENTER = 11
    RIGHT = 12
    TOP = 13
    MIDDLE = 14
    BOTTOM = 15


class Window(QWidget,):

    def __init__(self,
                 command,
                 top=0,
                 left=0,
                 right=0,
                 bottom=0,
                 maxwidth=None,
                 maxheight=None,
                 margin=20,
                 outputType=OutputType.HTML,
                 period=60,
                 align=Alignment.TOPLEFT,
                 textAlign=QtCore.Qt.AlignLeft,
                 textColor=QColor(200, 200, 200, 127),
                 bgColor=QColor(255, 255, 255, 0),
                 font="agave",
                 fontsize=14,
                 title="wonky",
                 autoresize=True,
                 linewrap=False,
                 ):

        super().__init__()

        self.isActive = False

        self.setWindowTitle(title)
        self.prefAlign = align
        self.autoresize = autoresize

        # these might be preferred margins or explicit x, y coordinates
        self.preftop = top
        self.prefleft = left
        self.prefright = right
        self.prefbottom = bottom
        self.prefmargin = margin

        self.maxwidth = maxwidth
        self.maxheight = maxheight

        # width and height may change, so prefs do not need to be retained beyond
        # initial setting of geometry

        self.setAlignedGeometry(app.primaryScreen(), 0.2, 0.2)

        self.textColor = textColor
        self.bgColor = bgColor
        self.textAlign = textAlign

        #  bgColor = "",
        # self.setStyleSheet("background-color: " + self.bgColor + "; border:0px;")
        self.setStyleSheet("background-color: rgba(" + str(self.bgColor.red()) + "," + str(self.bgColor.green()
                                                                                           ) + "," + str(self.bgColor.blue()) + "," + str(self.bgColor.alpha()) + "); border:0px;")

        self.command = command
        self.cmdOutputType = outputType
        self.period = period

        op = QGraphicsOpacityEffect(self)
        op.setOpacity(1)  # 0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(op)

        if sys.platform.startswith("darwin"):
            print("setting window flags for DARWIN")
            flags = QtCore.Qt.WindowFlags(
                QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
        else:
            print("setting window flags for non-DARWIN hopefully linux lol")
            # TODO: something explicit for Linux depending on whether a tiling window manager is being used
            flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint |
                                          QtCore.Qt.CustomizeWindowHint | QtCore.Qt.BypassWindowManagerHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowFlags(flags)
        vboxlayout = QGridLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet(
            "background-color: rgba(255,0,0,0%); color: rgba(255,255,255,100%); border:0")

        teOp = QGraphicsOpacityEffect(self.textEdit)
        teOp.setOpacity(1)  # 0 to 1 will cause the fade effect to kick in
        self.textEdit.setGraphicsEffect(teOp)

        # self.setContentsMargins(QMargins())
        self.textEdit.verticalScrollBar().setStyleSheet("height:0px")
        self.textEdit.horizontalScrollBar().setStyleSheet("height:0px")

        self.textEdit.setReadOnly(True)

        self.db = QFontDatabase()
        # self.font = self.db.font(font)
        self.font = QFont(font)

        if isinstance(fontsize, int):
            self.font.setPointSize(fontsize)
        else:
            if fontsize < 1:
                fontsize = screenH * fontsize

            self.font.setPixelSize(int(round(fontsize)))

        if not linewrap:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.thetext = ""
        vboxlayout.addWidget(self.textEdit)

        self.setLayout(vboxlayout)
        # self.show()

        self.ansi = Ansi2HTMLConverter()

    def hideEvent(self, event):
        # doesn't work on macos
        sleepfor = random.uniform(1.0, 3.0)
        print("hideEvent triggered, will sleep for")
        print(sleepfor)
        asyncio.sleep(sleepfor)
        self.setVisible(True)
        self.show()

    def changeEvent(self, event):
        if self.isActive:
            print("something changed while ACTIVE")
            if self.isVisible():
                print("but i am still visible")
            else:
                print("i am no longer visible!")
            self.check_state()
        else:
            print("something changed while inactive")

    async def check_state(self):
        if self.windowState() == Qt.WindowMinimized:
            print("i am somehow minimized ... attempting to restore")
            # Window is minimised. Restore it.
            self.setWindowState(Qt.WindowNoState)
        else:
            print("i am not minimized")

    def closeEvent(self, event):
        print("I was closed")

    def actionEvent(self, event):
        print("some action occurred")

    def setAlignedGeometry(self, screen, width, height):

        screenW = screen.size().width()
        screenH = screen.size().height()

        t = screenH * self.preftop
        b = screenH * self.prefbottom
        l = screenW * self.prefleft
        r = screenW * self.prefright

        if self.maxwidth and width > self.maxwidth:
            width = self.maxwidth

        if self.maxheight and height > self.maxheight:
            height = self.maxheight

        if width <= 1:
            width = screenW * width

        if height <= 1:
            height = screenH * height

        match self.prefAlign:
            case Alignment.TOPLEFT:
                top = t - b
                left = l - r

            case Alignment.TOPCENTER:
                top = t - b
                left = (screenW - width) / 2 - r

            case Alignment.TOPRIGHT:
                top = t - b
                left = screenW - r - width + l

            case Alignment.MIDDLELEFT:
                top = (screenH - height) / 2 + t - b
                left = l - r

            case Alignment.MIDDLECENTER:
                top = (screenH - height) / 2 + t - b
                left = (screenW - width) / 2 + l - r

            case Alignment.MIDDLERIGHT:
                top = (screenH - height) / 2 + t - b
                left = screenW - r - width + l

            case Alignment.BOTTOMLEFT:
                top = screenH - height + t - b
                left = l - r

            case Alignment.BOTTOMCENTER:
                top = screenH - height + t - b
                left = (screenW - width) / 2 + l - r

            case Alignment.BOTTOMRIGHT:
                top = screenH - height + t - b
                left = screenW - r - width + l

        self.setGeometry(int(left), int(top), int(width), int(height))

    def autoResize(self):
        self.textEdit.document().setTextWidth(self.textEdit.viewport().width())
        margins = self.textEdit.contentsMargins()
        height = int(self.textEdit.document().size().height() +
                     margins.top() + margins.bottom())
        width = int(self.textEdit.document().size().width() +
                    margins.left() + margins.right())

        self.setAlignedGeometry(app.primaryScreen(), width, height)

    async def start(self):
        # if self.autoresize:
        #     self.refresh()
        #     self.autoResize()

        # loop = asyncio.get_event_loop()
        # loop.call_later(10, self.check_state())
        # not callable ^^

        while True:
            self.refresh()

            if self.autoresize:
                self.autoResize()

            self.show()
            self.isActive = True

            await asyncio.sleep(self.period)

    def refresh(self):
        displayText = subprocess.run(
            self.command, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()

        match self.cmdOutputType:
            case OutputType.PLAINTEXT:
                displayText = displayText.replace(
                    "\r", "").replace("\n", "<br />\n")
            case OutputType.ANSI:
                displayText = self.ansi.convert(displayText)
            # case OutputType.HTML:
                # default

        print('-----------------------------------------------')
        print("displayText for command:")
        print(self.command)
        print('-----------------------------------------------')
        print(displayText)
        print('-----------------------------------------------')

        self.textEdit.clear()
        self.textEdit.document().setDocumentMargin(self.prefmargin)
        self.textEdit.insertHtml(displayText)

        self.textEdit.selectAll()
        self.textEdit.setCurrentFont(self.font)

        if self.cmdOutputType == OutputType.PLAINTEXT:
            self.textEdit.setTextColor(self.textColor)

        self.textEdit.setAlignment(self.textAlign)

        self.textEdit.moveCursor(QtGui.QTextCursor.Start)

        # the mysterious error:
        # QPainter::begin: A paint device can only be painted by one painter at a time.
        # QPainter::translate: Painter not active
        # attempted -> bit of a hack to stop all the windows trying to draw at the same time
        # asyncio.sleep(random.uniform(0.0,1.0))
        # then
        # asyncio.sleep(random.uniform(0.0,10.0))
        # then
        # time.sleep(0.1)
        # --> turns out app.processEvents() is not the culprit
        # TODO: check on x86 - maybe this error is constrained to ARM?
        app.processEvents()  # update gui for pyqt


async def setmeup():
    agenda = Window(top=0.05, left=0.03,
                    margin=10,
                    maxheight=0.5,
                    maxwidth=0.15,
                    title="agenda",
                    command=[sys.path[0] + '/tugenda', '--nodate'],
                    outputType=OutputType.PLAINTEXT,
                    period=60,
                    fontsize=16,
                    textColor=QColor(255, 255, 255, 190),
                    bgColor=QColor(0, 0, 0, 30),
                    )

    priorities = Window(
        top=0.2,
        title="priorities",
        maxwidth=0.3,
        command=[home + '/wonky/priorities', '3'],
        outputType=OutputType.PLAINTEXT,
        period=60,
        align=Alignment.TOPCENTER,
        textAlign=QtCore.Qt.AlignCenter,
        fontsize=0.014,
        textColor=QColor(255, 255, 255, 255),
        bgColor=QColor(0, 0, 0, 30),
        autoresize=True,
    )

    nowgenda = Window(
        top=0.3,
        title="nowgenda",
        maxwidth=0.3,
        command=[home + '/wonky/nownow'],
        outputType=OutputType.PLAINTEXT,
        period=300,
        align=Alignment.TOPCENTER,
        textAlign=QtCore.Qt.AlignCenter,
        fontsize=20,
        textColor=QColor(0, 0, 0, 255),
        bgColor=QColor(255, 255, 0, 180),
        autoresize=True,
    )

    tugstats = Window(top=0.03, right=0,
                      # height=250,
                      title="stats",
                      command=[sys.path[0] + "/system-stats"],
                      period=4,
                      align=Alignment.TOPRIGHT,
                      outputType=OutputType.PLAINTEXT,
                      textColor=QColor(255, 255, 255, 255),
                      font="Apple Color Emoji",
                      fontsize=0.01,
                      textAlign=QtCore.Qt.AlignRight,
                      autoresize=True,
                      )

    weather = Window(align=Alignment.MIDDLECENTER,
                     outputType=OutputType.PLAINTEXT,
                     bottom=0.15,
                     command=[sys.path[0] + '/weather', '%condition', ],
                     period=60,
                     font='Apple Color Emoji',
                     fontsize=0.15,
                     textAlign=QtCore.Qt.AlignCenter,
                     autoresize=True,
                     )

    weatherdetail = Window(align=Alignment.MIDDLECENTER,
                           outputType=OutputType.PLAINTEXT,
                           top=0.03,
                           bottom=0.15,
                           # height=100,
                           # width = 400,
                           command=[sys.path[0] + '/weather',
                                    '%feels', '%condition_desc'],
                           period=60,
                           font='bohemian typewriter',
                           fontsize=30,
                           textAlign=QtCore.Qt.AlignCenter,
                           textColor=QColor(127, 127, 127, 255),
                           autoresize=True,
                           )

    weatherdetail2 = Window(align=Alignment.BOTTOMCENTER,
                            outputType=OutputType.PLAINTEXT,
                            command=[sys.path[0] +
                                     '/weather', '--wonkydetail'],
                            period=60,
                            bottom=0,
                            #  margin = 30,
                            # fontsize=0.012,
                            font="White Rabbit",
                            textAlign=QtCore.Qt.AlignCenter,
                            textColor=QColor(200, 200, 200, 255),
                            autoresize=True,
                            )

    calendar = Window(align=Alignment.BOTTOMLEFT,
                      left=0.03, bottom=0.05,
                      maxwidth=0.20,
                      outputType=OutputType.HTML,
                      command=[sys.path[0] + '/calendar.lua'],
                      period=300,
                      autoresize=True,
                      fontsize=16,
                      )

    timedisp = Window(bottom=0,
                      # margin=25,
                      # width=900,
                      align=Alignment.BOTTOMCENTER,
                      title="time",
                      command=[sys.path[0] + "/showtime", "-t",],
                      period=60,
                      font="Bohemian Typewriter",
                      fontsize=0.18,
                      textAlign=QtCore.Qt.AlignCenter,
                      textColor=QColor(200, 200, 200, 90),
                      autoresize=True,
                      outputType=OutputType.PLAINTEXT,
                      )

    datedisp = Window(top=0.02,
                      align=Alignment.TOPCENTER,
                      title="date",
                      command=["/bin/date", "+%A %-d"],
                      period=60,
                      font="Bohemian Typewriter",
                      fontsize=0.1,
                      textAlign=QtCore.Qt.AlignCenter,
                      textColor=QColor(255, 255, 255, 90),
                      autoresize=True,
                      outputType=OutputType.PLAINTEXT,
                      )

    monthdisp = Window(top=0.125,
                       # width=900, height=80,
                       align=Alignment.TOPCENTER,
                       title="date",
                       command=["/bin/date", "+%B %Y"],
                       period=60,
                       font="Bohemian Typewriter",
                       fontsize=0.02,
                       textAlign=QtCore.Qt.AlignCenter,
                       textColor=QColor(255, 255, 255, 127),
                       outputType=OutputType.PLAINTEXT,
                       )

    gitdisp = Window(align=Alignment.TOPRIGHT,
                     top=0.13,
                     right=0,
                     left=0.1,
                     #  fontsize=14,
                     period=45,
                     outputType=OutputType.ANSI,
                     command=[sys.path[0] + '/quick-git-status',
                              '--env'
                              #   home + '/bin',
                              #   home + '/dotfiles',
                              #   home + '/org',
                              #   home + '/wonky',
                              #   home + '/fonting',
                              ],
                     # fontsize = 15,
                     # font="Bohemian Typewriter",
                     # bgColor = QColor(100,100,100,50),
                     autoresize=False,
                     )

    await asyncio.gather(timedisp.start(),
                         datedisp.start(),
                         monthdisp.start(),
                         tugstats.start(),
                         calendar.start(),
                         agenda.start(),
                         #  weather.start(),
                         # weatherdetail.start(),
                         weatherdetail2.start(),
                         gitdisp.start(),
                         priorities.start(),
                         #  nowgenda.start(),
                         )


if __name__ == "__main__":
    # window = Window()

    # asyncio.run(battery.start())
    # asyncio.run(agenda.start())
    asyncio.run(setmeup())

    sys.exit(app.exec())
