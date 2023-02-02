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

app = QApplication(sys.argv)

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


class Window(QWidget,):

    def __init__(self,
                 command,
                 top = 75,
                 left = 75,
                 right = 0,
                 bottom = 0,
                 width = 400,
                 height = 50,
                 margin = 0,
                 outputType = OutputType.HTML,
                 period = 60,
                 align = Alignment.TOPLEFT,
                 textAlign =  QtCore.Qt.AlignLeft,
                 textColor =  QColor(200, 200, 200, 127),
                 font = "ProfontIIx Nerd Font Mono",
                 fontsize = 12,
                 title = "wonky",
                 autoresize = False,
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

        # width and height may change, so prefs do not need to be retained beyond
        # initial setting of geometry

        self.setAlignedGeometry(width, height)
        
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

        self.textEdit.setReadOnly(True)

        self.db = QFontDatabase()
        self.font = self.db.font(font, "", fontsize)

        self.thetext=""
        vboxlayout.addWidget(self.textEdit)

        self.setLayout(vboxlayout)
        self.show()
        
        self.ansi = Ansi2HTMLConverter()

    def setAlignedGeometry(self, width, height):

        screen = app.primaryScreen()
        screenW = screen.size().width()
        screenH = screen.size().height()

        match self.prefAlign:
            # case Alignment.TOPLEFT:
                # this is the default

            case Alignment.TOPCENTER:
                # top = top
                self.prefleft = ( screenW - width ) / 2
                
            case Alignment.TOPRIGHT:
                # top = top
                self.prefleft = screenW - self.prefright - width

            case Alignment.MIDDLELEFT:
                self.preftop = (screenH - height) / 2
                # left = left

            case Alignment.MIDDLECENTER:
                self.preftop = ( screenH - height ) / 2
                self.prefleft = ( screenW - width ) / 2

            case Alignment.MIDDLERIGHT:
                self.preftop = screenH - self.prefbottom - height
                self.prefleft = screenW - self.prefright - width

            case Alignment.BOTTOMLEFT:
                self.preftop = screenH - self.prefbottom - height
                # left = left
                
            case Alignment.BOTTOMCENTER:
                self.preftop = screenH - self.prefbottom - height
                self.prefleft = ( screenW - width ) / 2

            case Alignment.BOTTOMRIGHT:
                self.preftop = screenH - self.prefbottom - height
                self.prefleft = screenW - self.prefright - width

        self.setGeometry(int(self.prefleft), int(self.preftop), width, height)

    def autoResize(self):
        self.textEdit.document().setTextWidth(self.textEdit.viewport().width())
        margins = self.textEdit.contentsMargins()
        height = int(self.textEdit.document().size().height() + margins.top() + margins.bottom())
        width = int(self.textEdit.document().size().width() + margins.left() + margins.right())
        # self.setFixedHeight(height)
        self.setAlignedGeometry(width, height)

    async def start(self):
        if self.autoresize:
            self.refresh()
            self.autoResize()
        while True:
            self.refresh()
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
    agenda = Window( top=75, left=75,
                     width = 400,
                     height = 400,
                     title="agenda",
                     command=[sys.path[0] + '/tugenda', 'today', 'now', 'next'],
                     outputType=OutputType.PLAINTEXT,
                     period=60,
                     textColor=QColor(255, 255, 255, 255),
                    )

    tugstats = Window (top=50, right=25,
                       height=250,
                       title="stats",
                       command=[sys.path[0] + "/system-stats"],
                       period=4,
                       align=Alignment.TOPRIGHT,
                       outputType = OutputType.PLAINTEXT,
                       textColor=QColor(255, 255, 255, 255),
                       font="Noto Color Emoji",
                       textAlign =  QtCore.Qt.AlignRight,
                       )

    weather = Window  ( align=Alignment.BOTTOMCENTER,
                        outputType = OutputType.PLAINTEXT,
                        height=100,
                        bottom = 25,
                        width = 500,
                        command=[sys.path[0] + '/weather.sh'],
                        period=600,
                        font = 'Bohemian Typewriter',
                        fontsize = 14,
                        textAlign = QtCore.Qt.AlignRight,
                        )

    calendar = Window ( align=Alignment.BOTTOMLEFT,
                        height=300,
                        outputType = OutputType.HTML,
                        command=[sys.path[0] + '/calendar.lua'],
                        period=300,
                        )

    timedisp = Window ( bottom=100,
                        width=900,
                        align=Alignment.BOTTOMCENTER,
                        title="time",
                        command=["/bin/date", "+%H:%M"],
                        period=4,
                        font="Bohemian Typewriter",
                        fontsize=150,
                        textAlign=QtCore.Qt.AlignCenter,
                        textColor=QColor(255, 255, 255, 90),
                        autoresize = True,
                        outputType = OutputType.PLAINTEXT,
                        )

    datedisp = Window ( top=75,
                        width=900,
                        align=Alignment.TOPCENTER,
                        title="date",
                        command=["/bin/date", "+%A %-d"],
                        period=60,
                        font="Bohemian Typewriter",
                        fontsize=100,
                        textAlign=QtCore.Qt.AlignCenter,
                        textColor=QColor(255, 255, 255, 127),
                        autoresize = True,
                        outputType = OutputType.PLAINTEXT,
                        )

    gitdisp = Window (  align = Alignment.TOPRIGHT,
                        top = 150,
                        right = 25,
                        height = 250,
                        width = 200,
                        period = 45,
                        outputType = OutputType.ANSI,
                        command = [ sys.path[0] + '/quick-git-status',
                                    home + '/bin',
                                    home + '/dotfiles',
                                    home + '/org',
                                    home + '/wonky',
                                    home + '/fonting',
                                    ],
                        left = 75,
                        fontsize = 10
                        )



    await asyncio.gather( timedisp.start(),
                          datedisp.start(),
                          tugstats.start(),
                          calendar.start(),
                          agenda.start(),
                          weather.start(),
                          gitdisp.start(),
                         )


if __name__ == "__main__":
    # window = Window()

    # asyncio.run(battery.start())
    # asyncio.run(agenda.start())
    asyncio.run(setmeup())
    
    sys.exit(app.exec())
