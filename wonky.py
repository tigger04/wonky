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
                 top = 0,
                 left = 0,
                 right = 0,
                 bottom = 0,
                 width = 400,
                 height = 400,
                 outputType = OutputType.HTML,
                 period = 60,
                 align = Alignment.TOPLEFT,
                 textAlign =  QtCore.Qt.AlignLeft,
                 textColor =  QColor(128, 128, 128, 128),
                 font = "ProfontIIx Nerd Font Mono",
                 fontsize = 12,
                 title = "wonky"):

        super().__init__()

        self.setWindowTitle(title)
        self.prefAlign = align

        # these might be preferred margins or explicit x, y coordinates
        self.preftop = top
        self.prefleft = left
        self.prefright = right
        self.prefbottom = bottom

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
                self.preftop = screenH - self.prefbottom - height
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
        self.textEdit.insertHtml(displayText)
        # self.textEdit.insertPlainText('\n')
        # self.textEdit.insertHtml(calendar)
        # self.textEdit.insertPlainText('\n')
        # self.textEdit.insertHtml(self.ansi.convert(gitstatus))

        self.textEdit.selectAll()

        self.textEdit.setCurrentFont(self.font)
        self.textEdit.setTextColor(self.textColor)
        self.textEdit.setAlignment(self.textAlign)

        self.textEdit.moveCursor(QtGui.QTextCursor.Start)


        QApplication.processEvents() #update gui for pyqt
            # time.sleep(0.001)
 
async def setmeup():
    agenda = Window( top=75, left=75,
                     title="agenda",
                     command=[home + '/wonky/tugenda', 'today', 'now', 'next'],
                     outputType=OutputType.PLAINTEXT,
                     period=60,
                     textColor=QColor(255, 255, 255, 255),
                    )

    battery = Window ( top=475, left=75,
                       title="battery",
                       command=[home+"/bin/battery-status"],
                       period=60,
                       textColor=QColor(255, 255, 255, 255),
                       font="Noto Color Emoji",
                       )

    timetest = Window ( bottom=100,
                        width=600,
                        align=Alignment.BOTTOMCENTER,
                        title="time",
                        command=["/bin/date", "+%H:%M:%S"],
                        period=1,
                        font="Bohemian Typewriter",
                        fontsize=100,
                        textAlign=QtCore.Qt.AlignLeft,
                        textColor=QColor(255, 255, 255, 127),
                        )

    await asyncio.gather(timetest.start(), battery.start(), agenda.start())


if __name__ == "__main__":
    # window = Window()

    # asyncio.run(battery.start())
    # asyncio.run(agenda.start())
    asyncio.run(setmeup())
    
    sys.exit(app.exec())
