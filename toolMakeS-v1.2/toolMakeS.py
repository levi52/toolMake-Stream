import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizeGrip

from windowV13 import Ui_MainWindow
class toolMakeW(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.clickPosition = None
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        QSizeGrip(self.size_grip)
        self.minimize_btn.clicked.connect(lambda: self.showMinimized())
        self.close_btn.clicked.connect(lambda: self.close())
        self.maximize_btn.clicked.connect(lambda: self.restore_or_maximize_window())
        self.audio_btn.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.audio))
        self.video_btn.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.video))
        self.chat_btn.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.chat))
        self.setting_btn.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.setting))

        def moveWindow(e):

            if not self.isMaximized():

                if e.buttons() == Qt.LeftButton:

                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()


        self.header_frame.mouseMoveEvent = moveWindow
        self.show()
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setIcon(QtGui.QIcon("asserts/icon/window-maximize.svg"))
        else:
            self.showMaximized()
            self.maximize_btn.setIcon(QtGui.QIcon("asserts/icon/maximize.svg"))
    def mousePressEvent(self, event):

        self.clickPosition = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool_make = toolMakeW()
    sys.exit(app.exec())