#!/usr/bin/env python3
import sys
import time
from ansi2html import Ansi2HTMLConverter
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QMargins, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QSizeGrip, QTextEdit
import sys
import time
import os
import subprocess
 
class Window(QWidget,):
    def __init__(self):
        super().__init__()
        # self.title = "no title"
        self.top = 0
        self.left = 1200
        self.width = 400
        self.height = 210
        self.setWindowTitle("no title")
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.setWindoOpacity(0.7)
        self.setAttribute(Qt.WA_TranslucentBackground)

        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.70) #0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(op)
        # self.setAutoFillBackground(True)


        
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.BypassWindowManagerHint)
        self.setWindowFlags(flags)
        vboxlayout = QGridLayout()

        # sizegrip = QSizeGrip(self)
        # sizegrip.setVisible(True)
        # vboxlayout.addWidget(sizegrip)
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("border: 1px solid grey")
        
        self.textEdit.setAttribute(Qt.WA_TranslucentBackground)
        teOp=QGraphicsOpacityEffect(self.textEdit)
        teOp.setOpacity(0.70) #0 to 1 will cause the fade effect to kick in
        self.textEdit.setGraphicsEffect(teOp)

        self.setContentsMargins(QMargins())
        self.textEdit.verticalScrollBar().setStyleSheet("height:0px")

        self.textEdit.setReadOnly(True)

        self.db = QFontDatabase()
        font = self.db.font("fixed", "", 14)
        self.textEdit.setCurrentFont(font)

#        nowlist=open('../../tug-now.nice').read()
#        todaylist=open('../../tug-today.nice').read()
 #       self.scroll_to_last_line()
 #       self.textEdit.append(todaylist)
 #       self.scroll_to_beginning()

        self.thetext=""
        vboxlayout.addWidget(self.textEdit)

        self.setLayout(vboxlayout)
        self.show()
        while True:
            self.refresh()
            # time.sleep(5) 

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
 
    def refresh(self):

        # what do we want?
        # agenda today inbox now next later handy quick-wins wtf ideas

        now=subprocess.run([os.path.expanduser('~/bin/tugenda')], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # today=subprocess.run([os.path.expanduser('~/bin/agenda'), 'today'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # agenda=subprocess.run([os.path.expanduser('~/bin/agenda'), 'agenda'], stdout=subprocess.PIPE).stdout.decode('utf-8')

        # newtext=open(os.path.expanduser('~/tug-list.nice')).read()
        # if newtext != self.textEdit.text:
        self.textEdit.clear();
        self.textEdit.insertPlainText(now)
        # self.textEdit.insertPlainText(agenda)
        # self.textEdit.insertPlainText(today)

        # self.textEdit.append(newtext)

        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.moveCursor(QtGui.QTextCursor.Start)
        cursor = QtGui.QTextCursor(
            self.textEdit.document().findBlockByLineNumber(0))
# self.edit.document().findBlockByLineNumber(line))
        self.textEdit.setTextCursor(cursor)
# self.scroll_to_beginning()

        for x in range (1,60000):
            QApplication.processEvents() #update gui for pyqt
            time.sleep(0.001)
            
# text=newtext

    # def scroll_to_beginning(self):
    #     cursor = self.textEdit.textCursor()
    #     cursor.movePosition(QTextCursor.Start)
    #     cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else
    #                         QTextCursor.StartOfLine)
        # self.setTextCursor(cursor)
    # def scroll_to_last_line(self):
    #     cursor = self.textCursor()
    #     cursor.movePosition(QTextCursor.End)
    #     cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else
    #                         QTextCursor.StartOfLine)
    #     self.window.setTextCursor(cursor)
#
#    def scroll_to_beginning(self):
#        cursor = self.textCursor()
#        cursor.movePosition(QTextCursor.Start)
#        cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else
#                            QTextCursor.StartOfLine)
#        self.setTextCursor(cursor)

 
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())