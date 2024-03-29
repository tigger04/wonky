#!/usr/bin/env python3
import sys
import time
from ansi2html import Ansi2HTMLConverter
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import (
    Qt,
    QObject,
    QThread,
    pyqtSignal,
    QMargins,
)

import pywinctl as pwc

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QSizeGrip, QTextEdit
import sys
import signal
import threading

import time
from time import sleep
import os
import subprocess
import asyncio
from enum import Enum
import datetime
import random
from math import floor, ceil

from Configs import Configs
import config

home = os.path.expanduser('~')

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,
                          True)  # enable highdpi scaling
QApplication.setAttribute(
    QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

app = QApplication(sys.argv)

# screen = app.primaryScreen()
# screenW = screen.size().width()
# screenH = screen.size().height()

for scr in app.screens():
    print('--- screen man: {} model: {} name: {} ---'.format(scr.manufacturer(),
          scr.model(), scr.name()))
    print("available geometry:")
    print(scr.availableGeometry())
    print(scr.availableGeometry().top())
    print(scr.availableGeometry().left())
    print(scr.availableGeometry().width())
    print(scr.availableGeometry().height())
    print("virtual geometry:")
    print(scr.virtualGeometry())
    print("geometry:")
    print(scr.geometry())
    print(scr.geometry().top())
    print(scr.geometry().left())
    print("size:")
    print(scr.size())
    print(scr.size().width())
    print(scr.size().height())
    print('--------------')



class Worker(QObject):

    def __init__(self,
                 command,
                 period
                 ):
        super().__init__()

        resolveCmd = command.pop(0)

        if resolveCmd.startswith('~/'):
            cmd = os.path.expanduser(resolveCmd)
        elif resolveCmd.startswith('./'):
            cmd = sys.path[0] + resolveCmd.lstrip('.')
        else:
            cmd = resolveCmd

        self.command = [cmd] + command
        self.period = period
        self.currentOutput = ""

    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Async run task"""

        while True:
            stdout = subprocess.run(
                self.command, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()

            if stdout != self.currentOutput:

                # print('-----------------------------------------------')
                print("output for command changed:")
                print(self.command)
                # print('-----------------------------------------------')
                # print(stdout)
                # print('-----------------------------------------------')

                self.currentOutput = stdout
                self.progress.emit(self.currentOutput)

            sleep(self.period)

    def die(self):
        print("attempting to kill worker for: " + self.command[0])
        self.finished.emit()


class Window(QWidget,):

    def __init__(self,
                 conf,
                 screen=app.primaryScreen()):

        super().__init__()

        self.name = str(conf.name)
        self.prefScreen = screen

        self.isActive = False

        self.top = float(conf.top or 0)
        self.left = float(conf.left or 0)
        self.right = float(conf.right or 0)
        self.bottom = float(conf.bottom or 0)

        if conf.minheight:
            self.minheight = float(conf.minheight)
            if self.minheight < 1.0:
                self.minheight = round(
                    float(self.prefScreen.size().height()) * self.minheight)
        else:
            self.minheight = 40

        if conf.minwidth:
            self.minwidth = float(conf.minwidth)
            if self.minwidth < 1.0:
                self.minwidth = round(
                    float(self.prefScreen.size().width()) * self.minwidth)
        else:
            self.minwidth = 40

        if conf.maxheight:
            self.maxheight = float(conf.maxheight)
            if self.maxheight < 1.0:
                self.maxheight = round(
                    float(self.prefScreen.size().height()) * self.maxheight)
            self.setMaximumHeight(self.maxheight)
        else:
            self.maxheight = None

        if conf.maxwidth:
            self.maxwidth = float(conf.maxwidth)
            if self.maxwidth < 1.0:
                self.maxwidth = round(
                    float(self.prefScreen.size().width()) * self.maxwidth)
            self.setMaximumWidth(self.maxwidth)
        else:
            self.maxwidth = None

        self.margin = int(conf.margin or 20)
        self.outputType = str(conf.outputType or "html")
        self.period = int(conf.period or 60)
        self.align = str(conf.align or "topleft")

        if conf.textAlign:
            match conf.textAlign.lower():
                case "left":
                    self.textAlign = QtCore.Qt.AlignLeft
                case "right":
                    self.textAlign = QtCore.Qt.AlignRight
                case "center":
                    self.textAlign = QtCore.Qt.AlignCenter
        else:
            self.textAlign = QtCore.Qt.AlignLeft

        if conf.textColor:
            self.textColor = QColor(
                conf.textColor[0], conf.textColor[1], conf.textColor[2], conf.textColor[3])
        else:
            self.textColor = QColor(200, 200, 200, 127)

        if conf.bgColor:
            self.bgColor = QColor(
                conf.bgColor[0], conf.bgColor[1], conf.bgColor[2], conf.bgColor[3])
        else:
            self.bgColor = QColor(255, 255, 255, 0)

        if conf.font:
            self.fontname = str(conf.font)
        else:
            self.fontname = "agave"

        self.fontsize = float(conf.fontsize or 18.0)

        self.setFont()

        self.autoresize = bool(conf.autoresize or True)
        self.linewrap = bool(conf.linewrap or False)
        self.command = list(conf.command or ["uname"])

        self.setWindowTitle(self.name)

        self.setStyleSheet("background-color: rgba(" + str(self.bgColor.red()) + "," + str(self.bgColor.green()
                                                                                           ) + "," + str(self.bgColor.blue()) + "," + str(self.bgColor.alpha()) + "); border:0px;")

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

        # self.setAlignedGeometry ( screen, self.minwidth, self.minheight)

        self.textEdit = QTextEdit()
        # self.textEdit.width = self.geometry().width
        # self.textEdit.height = self.geometry().height

        self.textEdit.setStyleSheet(
            "background-color: rgba(255,0,0,0%); color: rgba(255,255,255,100%); border:0")

        teOp = QGraphicsOpacityEffect(self.textEdit)
        teOp.setOpacity(1)  # 0 to 1 will cause the fade effect to kick in
        self.textEdit.setGraphicsEffect(teOp)

        # self.setContentsMargins(QMargins())
        self.textEdit.verticalScrollBar().setStyleSheet("height:0px")
        self.textEdit.horizontalScrollBar().setStyleSheet("height:0px")

        self.textEdit.setReadOnly(True)

        # self.db = QFontDatabase()
        # self.font = self.db.font(font)

        if not self.linewrap:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

        vboxlayout.addWidget(self.textEdit)

        self.setLayout(vboxlayout)

        self.worker = Worker(
            command=self.command,
            period=self.period
        )

    def hideEvent(self, event):
        # doesn't work on macos
        # print("hideEvent triggered")
        event.accept()

    # def changeEvent(self, event):
    #     if self.isActive:
    #         print("something changed while ACTIVE")
    #         if self.isVisible():
    #             print("but i am still visible")
    #         else:
    #             print("i am no longer visible!")
    #     else:
    #         print("something changed while inactive")

    def closeEvent(self, event):
        print("I was closed: " + self.name)
        self.worker.die()
        event.accept()

    def actionEvent(self, event):
        print("some action occurred")
        event.accept()

    def setFont(self):
        self.font = QFont(self.fontname)

        if self.fontsize >= 1:
            self.font.setPointSize(int(round(self.fontsize)))
        else:
            fontsize = self.prefScreen.size().height() * self.fontsize
            self.font.setPixelSize(int(round(fontsize)))

    def setAlignedGeometry(self, screen, width, height):

        print("aligning {} to geometry {}".format(
            self.name, screen.availableGeometry()))
        screenL = screen.availableGeometry().left()
        screenT = screen.availableGeometry().top()
        screenW = screen.availableGeometry().width()
        screenH = screen.availableGeometry().height()

        print("using t:{}, b:{}, l:{}, r:{}".format(
            self.top, self.bottom, self.left, self.right))

        t = screenH * self.top
        b = screenH * self.bottom
        l = screenW * self.left
        r = screenW * self.right

        if self.maxwidth and (width > self.maxwidth):
            print("width {} exceeds maxwidth of {}".format(width, self.maxwidth))
            width = self.maxwidth

        if self.maxheight and ( height > self.maxheight ):
            print("height {} exceeds maxheight of {}".format(
                height, self.maxheight))
            height = self.maxheight

        match self.align.lower():
            case "topleft":
                top = t - b
                left = l - r

            case "topcenter":
                top = t - b
                left = (screenW - width) / 2 - r

            case "topright":
                top = t - b
                left = screenW - r - width + l

            case "middleleft":
                top = (screenH - height) / 2 + t - b
                left = l - r

            case "middlecenter":
                top = (screenH - height) / 2 + t - b
                left = (screenW - width) / 2 + l - r

            case "middleright":
                top = (screenH - height) / 2 + t - b
                left = screenW - r - width + l

            case "bottomleft":
                top = screenH - height + t - b
                left = l - r

            case "bottomcenter":
                top = screenH - height + t - b
                left = (screenW - width) / 2 + l - r

            case "bottomright":
                top = screenH - height + t - b
                left = screenW - r - width + l

        top += screenT
        left += screenL

        print("aligning {} to L:{}, T:{}, W:{}, H:{}".format(
            self.name, left, top, width, height))

        self.setGeometry(int(left), int(top), int(width), int(height))

    def autoResize(self):

    #class Editor(QTextEdit):
    # def __init__(self):
    #     super().__init__()
    #     self.setReadOnly(True)
    #     self.setFont(font)
    #     self.textChanged.connect(self.autoResize)

    # def autoResize(self):
    #     self.document().setTextWidth(self.viewport().width())
    #     margins = self.contentsMargins()
    #     height = int(self.document().size().height() + margins.top() + margins.bottom())
    #     self.setFixedHeight(height)

    # def resizeEvent(self, event):
    #     self.autoResize()

        # self.textEdit.document().setTextWidth(self.textEdit.viewport().width())
        self.textEdit.document().adjustSize()

        margins = self.contentsMargins()

        height = int(self.textEdit.document().size().height() +
                    #  self.margin * 2)
                     margins.top() + margins.bottom())
        width = int(self.textEdit.document().size().width() +
                    # self.margin * 2)
                     margins.left() + margins.right())

        if self.maxheight and height > self.maxheight:
            height = self.maxheight
        if self.maxwidth and width > self.maxwidth:
            width = self.maxwidth

        self.textEdit.setFixedHeight(height)
        self.textEdit.setFixedWidth(width)
        # self.textEdit.autoResize()

        self.setAlignedGeometry(self.prefScreen, width, height)

    def start(self):

        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.refresh)
        self.prefScreen.virtualGeometryChanged.connect(self.handleScreenChange)
        # self.prefScreen.geometryChanged.connect(self.handleScreenChange)
        # app.aboutToQuit.connect(self.worker.die)

        self.thread.start()

    def handleScreenChange(self, rect):
        if self.screen == self.prefScreen:
            self.setFont()
            self.autoResize()
        else:
            self.close()

    def refresh(self, displayText):

        match self.outputType.lower():
            case "plaintext":
                displayText = displayText.replace(
                    "\r", "").replace("\n", "<br />\n")
            case "ansi":
                displayText = Ansi2HTMLConverter().convert(displayText)
            # case "html":
                # default

        self.textEdit.clear()

        self.textEdit.insertHtml(displayText)

        self.textEdit.selectAll()
        self.textEdit.setCurrentFont(self.font)

        if self.outputType.lower() == "plaintext":
            self.textEdit.setTextColor(self.textColor)

        self.textEdit.setAlignment(self.textAlign)

        self.textEdit.moveCursor(QtGui.QTextCursor.Start)

        if self.autoresize:
            self.autoResize()

        self.show()

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
        # app.processEvents()  # update gui for pyqt


wonkys = []


def closeall():
    for wonky in wonkys:
        wonky.close()


def signal_handler(signal, frame):
    print("⛔️ got user kill signal")
    closeall()
    sys.exit(0)


def loadconfigs():
    # wonkys = []
    for screen in app.screens():
        for panel in config.panels:
            panelconfig = Configs(**panel)
            wonky = Window(panelconfig, screen)
            wonkys.append(wonky)


def startwonkys():
    for wonky in wonkys:
        wonky.start()


if __name__ == "__main__":

    # bit of a hack, in macos first hide all windows to make sure wonky stays
    # behind all other windows
    # TODO: there is a proper fix i think using pywinctl
    if sys.platform.startswith("darwin"):
       subprocess.run(['mac-hide-windows-all']) 

    loadconfigs()
    startwonkys()

    signal.signal(signal.SIGINT, signal_handler)

    sys.exit(app.exec())
