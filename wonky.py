#!/usr/bin/env python3
import sys
import time
from ansi2html import Ansi2HTMLConverter
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QMargins, QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QSizeGrip, QTextEdit
import sys
import time
import os
import subprocess
import asyncio
from enum import Enum
import datetime

home = os.path.expanduser('~')

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

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
    TOPLEFT      = 1
    TOPCENTER    = 2
    TOPRIGHT     = 3
    MIDDLELEFT   = 4
    MIDDLECENTER = 5
    MIDDLERIGHT  = 6
    BOTTOMLEFT   = 7
    BOTTOMCENTER = 8
    BOTTOMRIGHT  = 9
    LEFT         = 10
    CENTER       = 11
    RIGHT        = 12
    TOP          = 13
    MIDDLE       = 14
    BOTTOM       = 15


class Window(QWidget,):

    def __init__(self,
                 command,
                 top = 0,
                 left = 0,
                 right = 0,
                 bottom = 0,
                 maxwidth = None,
                 maxheight = None,
                 margin = 20,
                 outputType = OutputType.HTML,
                 period = 60,
                 align = Alignment.TOPLEFT,
                 textAlign =  QtCore.Qt.AlignLeft,
                 textColor =  QColor(200, 200, 200, 127),
                 font = "ProfontIIx Nerd Font Mono",
                 fontsize = 12,
                 title = "wonky",
                 autoresize = True,
                 linewrap = False,
                 ):

        super().__init__()

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
        self.textAlign = textAlign

        self.setStyleSheet("background-color: rgba(255,255,255,0%); border:0px;");

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.command=command
        self.cmdOutputType=outputType
        self.period=period

        op=QGraphicsOpacityEffect(self)
        op.setOpacity(1) #0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(op)
        
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.BypassWindowManagerHint)

        # flags = QtCore.Qt.WindowFlags(QtCore.Qt.BypassWindowManagerHint)

        self.setWindowFlags(flags)
        vboxlayout = QGridLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: rgba(255,0,0,0%); color: rgba(255,255,255,100%); border:0");
        
        teOp=QGraphicsOpacityEffect(self.textEdit)
        teOp.setOpacity(1) #0 to 1 will cause the fade effect to kick in
        self.textEdit.setGraphicsEffect(teOp)

        self.setContentsMargins(QMargins())
        self.textEdit.verticalScrollBar().setStyleSheet("height:0px")
        self.textEdit.horizontalScrollBar().setStyleSheet("height:0px")

        self.textEdit.setReadOnly(True)

        self.db = QFontDatabase()
        self.font = self.db.font(font, "", fontsize)

        if not linewrap:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.thetext=""
        vboxlayout.addWidget(self.textEdit)

        self.setLayout(vboxlayout)
        self.show()
        
        self.ansi = Ansi2HTMLConverter()

    # def getLeft(self):
    #     return self.prefleft

    # def getTop(self):
    #     return self.preftop

    # def getWidth(self):
    #     return self.width

    # def getHeight(self):
    #     return self.height

    def setAlignedGeometry(self, screen, width, height):

        screenW = screen.size().width()
        screenH = screen.size().height()

        t = screenH * self.preftop
        b = screenH * self.prefbottom
        l = screenW * self.prefleft
        r = screenW * self.prefright

        if self.maxwidth and width > self.maxwidth:
            width=self.maxwidth

        if self.maxheight and height > self.maxheight:
            height=self.maxheight

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
                left = ( screenW - width ) / 2 - r
                
            case Alignment.TOPRIGHT:
                top = t - b
                left = screenW - r - width + l

            case Alignment.MIDDLELEFT:
                top = ( screenH - height ) / 2 + t - b
                left = l - r

            case Alignment.MIDDLECENTER:
                top = ( screenH - height ) / 2 + t - b
                left = ( screenW - width ) / 2 + l - r

            case Alignment.MIDDLERIGHT:
                top = ( screenH - height ) / 2 + t - b
                left = screenW - r - width + l

            case Alignment.BOTTOMLEFT:
                top = screenH - height + t - b
                left = l - r
                
            case Alignment.BOTTOMCENTER:
                top = screenH - height + t - b
                left = ( screenW - width ) / 2 + l - r

            case Alignment.BOTTOMRIGHT:
                top = screenH - height + t - b
                left = screenW - r - width + l

        self.setGeometry(int(left), int(top), int(width), int(height))

    def autoResize(self):
        self.textEdit.document().setTextWidth(self.textEdit.viewport().width())
        margins = self.textEdit.contentsMargins()
        height = int(self.textEdit.document().size().height() + margins.top() + margins.bottom())
        width = int(self.textEdit.document().size().width() + margins.left() + margins.right())
        # self.setFixedHeight(height)
        self.setAlignedGeometry(app.primaryScreen(), width, height)

    async def start(self):
        if self.autoresize:
            self.refresh()
            self.autoResize()
        while True:
            self.refresh()

            if self.autoresize:
                self.autoResize()

            await asyncio.sleep(self.period) 

    # def mousePressEvent(self, event):
    #     self.oldPosition = event.globalPos()

    # def mouseMoveEvent(self, event):
    #     delta = QPoint(event.globalPos() - self.oldPosition)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPosition = event.globalPos()
 
    def refresh(self):

        # TODO: relative paths
        displayText=subprocess.run(self.command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        # agenda=subprocess.run([os.path.expanduser('~/wonky/tugenda'), 'today', 'now', 'next'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # # agenda=subprocess.run([os.path.expanduser('~/wonky/tugenda'),], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # calendar=subprocess.run([os.path.expanduser('~/wonky/calendar.lua')], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # weather=subprocess.run([os.path.expanduser('~/wonky/weather'), '--city', '--today'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # gitstatus=subprocess.run([os.path.expanduser('~/wonky/quick-git-status'), os.path.expanduser('~/bin'), os.path.expanduser('~/dotfiles'), os.path.expanduser('~/org'), os.path.expanduser('~/fonting'), os.path.expanduser('~/wonky') ], stdout=subprocess.PIPE).stdout.decode('utf-8')

        match self.cmdOutputType:
            case OutputType.PLAINTEXT:
                displayText=displayText.replace("\r","").replace("\n","<br />\n")
            case OutputType.ANSI:
                displayText=self.ansi.convert(displayText)
            # case OutputType.HTML:
                # default
            
            
        self.textEdit.clear();
        self.textEdit.document().setDocumentMargin(self.prefmargin)
        self.textEdit.insertHtml(displayText)
        # self.textEdit.insertPlainText('\n')
        # self.textEdit.insertHtml(calendar)
        # self.textEdit.insertPlainText('\n')
        # self.textEdit.insertHtml(self.ansi.convert(gitstatus))

        self.textEdit.selectAll()

        self.textEdit.setCurrentFont(self.font)

        if self.cmdOutputType == OutputType.PLAINTEXT:
            self.textEdit.setTextColor(self.textColor)

        self.textEdit.setAlignment(self.textAlign)

        self.textEdit.moveCursor(QtGui.QTextCursor.Start)

        QApplication.processEvents() #update gui for pyqt
            # time.sleep(0.001)
 
async def setmeup():
    agenda = Window( top=0.05, left=0.03,
                     # width = 400,
                     # height = 705,
                     maxheight=0.5,
                     title="agenda",
                     command=[sys.path[0] + '/tugenda'],
                     outputType=OutputType.PLAINTEXT,
                     period=60,
                     textColor=QColor(255, 255, 255, 255),
                    )

    tugstats = Window (top=0.05, right=0,
                       # height=250,
                       title="stats",
                       command=[sys.path[0] + "/system-stats"],
                       period=4,
                       align=Alignment.TOPRIGHT,
                       outputType = OutputType.PLAINTEXT,
                       textColor=QColor(255, 255, 255, 255),
                       font="Noto Color Emoji",
                       textAlign =  QtCore.Qt.AlignRight,
                       autoresize = True,
                       )

    weather = Window  ( align=Alignment.MIDDLECENTER,
                        outputType = OutputType.PLAINTEXT,
                        bottom=0.15,
                        command=[sys.path[0] + '/weather', '%condition', ],
                        period=60,
                        font = 'Noto Color Emoji',
                        fontsize = 200,
                        textAlign = QtCore.Qt.AlignCenter,
                        autoresize = True,
                        )

    weatherdetail = Window( align=Alignment.MIDDLECENTER,
                            outputType = OutputType.PLAINTEXT,
                            top=0.03,
                            bottom=0.15,
                            # height=100,
                            # width = 400,
                            command=[sys.path[0] + '/weather', '%feels', '%condition_desc'],
                            period=60,
                            font = 'bohemian typewriter',
                            fontsize = 30,
                            textAlign = QtCore.Qt.AlignCenter,
                            textColor = QColor(127,127,127, 255),
                            autoresize = True,
                           )

    weatherdetail2 = Window( align=Alignment.BOTTOMCENTER,
                             outputType = OutputType.PLAINTEXT,
                             command=[sys.path[0] + '/weather', '--wonkydetail'],
                             period=60,
                             bottom = 0,
                             margin = 20,
                             fontsize = 16,
                             font = "Bohemian Typewriter",
                             textAlign = QtCore.Qt.AlignCenter,
                             textColor = QColor(200,200,200, 255),
                             autoresize = True,
                           )


    calendar = Window ( align=Alignment.BOTTOMLEFT,
                        left = 0.03, bottom = 0.05,
                        # height=300,
                        outputType = OutputType.HTML,
                        command=[sys.path[0] + '/calendar.lua'],
                        period=300,
                        autoresize = True,
                        )

    timedisp = Window ( bottom=0,
                        # margin=25,
                        # width=900,
                        align=Alignment.BOTTOMCENTER,
                        title="time",
                        command=[sys.path[0] + "/showtime", "-t",],
                        period=60,
                        font="Bohemian Typewriter",
                        fontsize=160,
                        textAlign=QtCore.Qt.AlignCenter,
                        textColor=QColor(200, 200, 200, 90),
                        autoresize = True,
                        outputType = OutputType.PLAINTEXT,
                        )

    datedisp = Window ( top=0.02,
                        # width=900,
                        align=Alignment.TOPCENTER,
                        title="date",
                        command=["/bin/date", "+%A %-d"],
                        period=60,
                        font="Bohemian Typewriter",
                        fontsize=100,
                        textAlign=QtCore.Qt.AlignCenter,
                        textColor=QColor(255, 255, 255, 90),
                        autoresize = True,
                        outputType = OutputType.PLAINTEXT,
                        )

    monthdisp = Window (top=0.135,
                        # width=900, height=80,
                        align=Alignment.TOPCENTER,
                        title="date",
                        command=["/bin/date", "+%B %Y"],
                        period=60,
                        font="Bohemian Typewriter",
                        fontsize=20,
                        textAlign=QtCore.Qt.AlignCenter,
                        textColor=QColor(255, 255, 255, 127),
                        outputType = OutputType.PLAINTEXT,
                        )

    gitdisp = Window (  align = Alignment.TOPRIGHT,
                        top = 0.13,
                        right = 0,
                        # height = 250,
                        # width = 200,
                        period = 45,
                        outputType = OutputType.ANSI,
                        command = [ sys.path[0] + '/quick-git-status',
                                    home + '/bin',
                                    home + '/dotfiles',
                                    home + '/org',
                                    home + '/wonky',
                                    home + '/fonting',
                                    ],
                        fontsize = 10,
                        )



    await asyncio.gather( timedisp.start(),
                          datedisp.start(),
                          monthdisp.start(),
                          # tugstats.start(),
                          calendar.start(),
                          agenda.start(),
                          # weather.start(),
                          # weatherdetail.start(),
                          weatherdetail2.start(),
                          gitdisp.start(),
                         )


if __name__ == "__main__":
    # window = Window()

    # asyncio.run(battery.start())
    # asyncio.run(agenda.start())
    asyncio.run(setmeup())
    
    sys.exit(app.exec())
