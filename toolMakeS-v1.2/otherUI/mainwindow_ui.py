import os
import socket
import numpy as np
import threading
import time
import wave
import psycopg2
import os
import cv2
import pyaudio
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog

class Ui_MainWindow(object):
    def __init__(self):
            self.d_name = None
            self.d_pwd = None
            self.d_host = None
            self.d_user = None
            self.d_port = None
            self.video_port = None
            self.video_ip = None
            self.audio_port = None
            self.audio_ip = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        MainWindow.setMinimumSize(QtCore.QSize(600, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
"background-color:rgb(52, 54, 90);\n"
"color:rgb(255, 255, 255)\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setMinimumSize(QtCore.QSize(0, 30))
        self.header_frame.setStyleSheet("background-color:rgb(60, 60, 86)")
        self.header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.header_left_frame = QtWidgets.QFrame(self.header_frame)
        self.header_left_frame.setStyleSheet("margin-right:5px")
        self.header_left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_left_frame.setObjectName("header_left_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header_left_frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo = QtWidgets.QPushButton(self.header_left_frame)
        self.logo.setStyleSheet("QPushButton{\n"
"border:none;\n"
"}")
        self.logo.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("asserts/icon/Tool.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logo.setIcon(icon)
        self.logo.setIconSize(QtCore.QSize(24, 24))
        self.logo.setObjectName("logo")
        self.horizontalLayout_2.addWidget(self.logo)
        self.title = QtWidgets.QLabel(self.header_left_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.horizontalLayout_2.addWidget(self.title)
        self.horizontalLayout.addWidget(self.header_left_frame, 0, QtCore.Qt.AlignLeft)
        self.header_right_frame = QtWidgets.QFrame(self.header_frame)
        self.header_right_frame.setStyleSheet("QPushButton{\n"
"border:none;\n"
"margin-right:5px;\n"
"}")
        self.header_right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_right_frame.setObjectName("header_right_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.header_right_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.minimize_btn = QtWidgets.QPushButton(self.header_right_frame)
        self.minimize_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("asserts/icon/Minimize.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize_btn.setIcon(icon1)
        self.minimize_btn.setIconSize(QtCore.QSize(16, 16))
        self.minimize_btn.setObjectName("minimize_btn")
        self.horizontalLayout_3.addWidget(self.minimize_btn)
        self.maximize_btn = QtWidgets.QPushButton(self.header_right_frame)
        self.maximize_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("asserts/icon/maximize.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.maximize_btn.setIcon(icon2)
        self.maximize_btn.setObjectName("maximize_btn")
        self.horizontalLayout_3.addWidget(self.maximize_btn)
        self.close_btn = QtWidgets.QPushButton(self.header_right_frame)
        self.close_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("asserts/icon/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_btn.setIcon(icon3)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout_3.addWidget(self.close_btn)
        self.horizontalLayout.addWidget(self.header_right_frame, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.header_frame, 0, QtCore.Qt.AlignTop)
        self.center_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_frame.sizePolicy().hasHeightForWidth())
        self.center_frame.setSizePolicy(sizePolicy)
        self.center_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.center_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.center_frame.setObjectName("center_frame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.center_frame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.center_left_frame = QtWidgets.QFrame(self.center_frame)
        self.center_left_frame.setMinimumSize(QtCore.QSize(35, 0))
        self.center_left_frame.setMaximumSize(QtCore.QSize(20, 16777215))
        self.center_left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.center_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.center_left_frame.setObjectName("center_left_frame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.center_left_frame)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.menu_frame = QtWidgets.QFrame(self.center_left_frame)
        self.menu_frame.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.menu_frame.setFont(font)
        self.menu_frame.setStyleSheet("QPushButton{\n"
"border:none;\n"
"}")
        self.menu_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu_frame.setObjectName("menu_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.menu_frame)
        self.gridLayout.setContentsMargins(0, 5, 0, 5)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.audio_btn = QtWidgets.QPushButton(self.menu_frame)
        self.audio_btn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.audio_btn.sizePolicy().hasHeightForWidth())
        self.audio_btn.setSizePolicy(sizePolicy)
        self.audio_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.audio_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.audio_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("asserts/icon/audio.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.audio_btn.setIcon(icon4)
        self.audio_btn.setIconSize(QtCore.QSize(32, 32))
        self.audio_btn.setObjectName("audio_btn")
        self.gridLayout.addWidget(self.audio_btn, 0, 0, 1, 1)
        self.video_btn = QtWidgets.QPushButton(self.menu_frame)
        self.video_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.video_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.video_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("asserts/icon/video.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.video_btn.setIcon(icon5)
        self.video_btn.setIconSize(QtCore.QSize(32, 32))
        self.video_btn.setObjectName("video_btn")
        self.gridLayout.addWidget(self.video_btn, 1, 0, 1, 1)
        self.chat_btn = QtWidgets.QPushButton(self.menu_frame)
        self.chat_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.chat_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.chat_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("asserts/icon/chat.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chat_btn.setIcon(icon6)
        self.chat_btn.setIconSize(QtCore.QSize(32, 32))
        self.chat_btn.setObjectName("chat_btn")
        self.gridLayout.addWidget(self.chat_btn, 2, 0, 1, 1)
        self.setting_btn = QtWidgets.QPushButton(self.menu_frame)
        self.setting_btn.setMinimumSize(QtCore.QSize(32, 32))
        self.setting_btn.setMaximumSize(QtCore.QSize(32, 32))
        self.setting_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("asserts/icon/setting.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setting_btn.setIcon(icon7)
        self.setting_btn.setIconSize(QtCore.QSize(32, 32))
        self.setting_btn.setObjectName("setting_btn")
        self.gridLayout.addWidget(self.setting_btn, 3, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.menu_frame)
        self.pushButton_5.setMinimumSize(QtCore.QSize(32, 32))
        self.pushButton_5.setMaximumSize(QtCore.QSize(32, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.menu_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.menu_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.menu_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.menu_frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.menu_frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        self.horizontalLayout_8.addWidget(self.menu_frame, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_7.addWidget(self.center_left_frame)
        self.center_main_frame = QtWidgets.QFrame(self.center_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_main_frame.sizePolicy().hasHeightForWidth())
        self.center_main_frame.setSizePolicy(sizePolicy)
        self.center_main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.center_main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.center_main_frame.setObjectName("center_main_frame")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.center_main_frame)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.stackedWidget = QtWidgets.QStackedWidget(self.center_main_frame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.audio = QtWidgets.QWidget()
        self.audio.setObjectName("audio")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.audio)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.audio_frame = QtWidgets.QFrame(self.audio)
        self.audio_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audio_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.audio_frame.setObjectName("audio_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.audio_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.audio_frame)
        self.label_6.setMinimumSize(QtCore.QSize(0, 60))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6, 0, QtCore.Qt.AlignLeft)
        self.audio_recorder = QtWidgets.QFrame(self.audio_frame)
        self.audio_recorder.setMinimumSize(QtCore.QSize(200, 120))
        self.audio_recorder.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audio_recorder.setFrameShadow(QtWidgets.QFrame.Raised)
        self.audio_recorder.setObjectName("audio_recorder")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.audio_recorder)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.audio_input = QtWidgets.QFrame(self.audio_recorder)
        self.audio_input.setMinimumSize(QtCore.QSize(100, 120))
        self.audio_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audio_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.audio_input.setObjectName("audio_input")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.audio_input)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.start_audio_btn = QtWidgets.QPushButton(self.audio_input)
        self.start_audio_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.start_audio_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.start_audio_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.start_audio_btn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("asserts/icon/audios.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_audio_btn.setIcon(icon8)
        self.start_audio_btn.setIconSize(QtCore.QSize(32, 32))
        self.start_audio_btn.setObjectName("start_audio_btn")
        self.verticalLayout_6.addWidget(self.start_audio_btn)
        self.audio_time = QtWidgets.QLabel(self.audio_input)
        self.audio_time.setMinimumSize(QtCore.QSize(60, 50))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.audio_time.setFont(font)
        self.audio_time.setObjectName("audio_time")
        self.verticalLayout_6.addWidget(self.audio_time)
        self.horizontalLayout_10.addWidget(self.audio_input, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.audio_output = QtWidgets.QFrame(self.audio_recorder)
        self.audio_output.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.audio_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.audio_output.setObjectName("audio_output")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.audio_output)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.play_audio_btn = QtWidgets.QPushButton(self.audio_output)
        self.play_audio_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.play_audio_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.play_audio_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.play_audio_btn.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("asserts/icon/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_audio_btn.setIcon(icon9)
        self.play_audio_btn.setIconSize(QtCore.QSize(32, 32))
        self.play_audio_btn.setObjectName("play_audio_btn")
        self.verticalLayout_7.addWidget(self.play_audio_btn)
        self.audio_name = QtWidgets.QLabel(self.audio_output)
        self.audio_name.setMinimumSize(QtCore.QSize(60, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.audio_name.setFont(font)
        self.audio_name.setText("")
        self.audio_name.setObjectName("audio_name")
        self.verticalLayout_7.addWidget(self.audio_name)
        self.horizontalLayout_10.addWidget(self.audio_output, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_5.addWidget(self.audio_recorder, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.audio_frame)
        self.stackedWidget.addWidget(self.audio)
        self.video = QtWidgets.QWidget()
        self.video.setObjectName("video")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.video)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.video_frame = QtWidgets.QFrame(self.video)
        self.video_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.video_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video_frame.setObjectName("video_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.video_frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.video_label = QtWidgets.QLabel(self.video_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_label.sizePolicy().hasHeightForWidth())
        self.video_label.setSizePolicy(sizePolicy)
        self.video_label.setMinimumSize(QtCore.QSize(0, 60))
        self.video_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.video_label.setFont(font)
        self.video_label.setObjectName("video_label")
        self.verticalLayout_8.addWidget(self.video_label)
        self.video_btn_frame = QtWidgets.QFrame(self.video_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_btn_frame.sizePolicy().hasHeightForWidth())
        self.video_btn_frame.setSizePolicy(sizePolicy)
        self.video_btn_frame.setMinimumSize(QtCore.QSize(0, 48))
        self.video_btn_frame.setMaximumSize(QtCore.QSize(16777215, 48))
        self.video_btn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.video_btn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video_btn_frame.setObjectName("video_btn_frame")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.video_btn_frame)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.camera_btn = QtWidgets.QPushButton(self.video_btn_frame)
        self.camera_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.camera_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.camera_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.camera_btn.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("asserts/icon/camera.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.camera_btn.setIcon(icon10)
        self.camera_btn.setIconSize(QtCore.QSize(32, 32))
        self.camera_btn.setObjectName("camera_btn")
        self.horizontalLayout_11.addWidget(self.camera_btn)
        self.pause_video_btn = QtWidgets.QPushButton(self.video_btn_frame)
        self.pause_video_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.pause_video_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.pause_video_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.pause_video_btn.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("asserts/icon/pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pause_video_btn.setIcon(icon11)
        self.pause_video_btn.setIconSize(QtCore.QSize(32, 32))
        self.pause_video_btn.setObjectName("pause_video_btn")
        self.horizontalLayout_11.addWidget(self.pause_video_btn)
        self.stop_video_btn = QtWidgets.QPushButton(self.video_btn_frame)
        self.stop_video_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.stop_video_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.stop_video_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.stop_video_btn.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("asserts/icon/stop circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_video_btn.setIcon(icon12)
        self.stop_video_btn.setIconSize(QtCore.QSize(32, 32))
        self.stop_video_btn.setObjectName("stop_video_btn")
        self.horizontalLayout_11.addWidget(self.stop_video_btn)
        self.verticalLayout_8.addWidget(self.video_btn_frame)
        self.verticalLayout_3.addWidget(self.video_frame)
        self.stackedWidget.addWidget(self.video)
        self.chat = QtWidgets.QWidget()
        self.chat.setObjectName("chat")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.chat)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.chat_frame = QtWidgets.QFrame(self.chat)
        self.chat_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chat_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chat_frame.setObjectName("chat_frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.chat_frame)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.chat_label = QtWidgets.QLabel(self.chat_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.chat_label.setFont(font)
        self.chat_label.setObjectName("chat_label")
        self.verticalLayout_9.addWidget(self.chat_label)
        self.chat_btn_frame = QtWidgets.QFrame(self.chat_frame)
        self.chat_btn_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.chat_btn_frame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.chat_btn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chat_btn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chat_btn_frame.setObjectName("chat_btn_frame")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.chat_btn_frame)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.check_frame = QtWidgets.QFrame(self.chat_btn_frame)
        self.check_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.check_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.check_frame.setObjectName("check_frame")
        self.check_frame.setMinimumSize(QtCore.QSize(200,80))

        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.check_frame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.server_btn = QtWidgets.QRadioButton(self.check_frame)
        self.server_btn.setObjectName("server_btn")
        self.verticalLayout_10.addWidget(self.server_btn)
        self.client_btn = QtWidgets.QRadioButton(self.check_frame)
        self.client_btn.setObjectName("client_btn")
        self.verticalLayout_10.addWidget(self.client_btn)
        self.horizontalLayout_12.addWidget(self.check_frame)
        self.choose_frame = QtWidgets.QFrame(self.chat_btn_frame)
        self.choose_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.choose_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.choose_frame.setObjectName("choose_frame")
        self.choose_frame.setMinimumSize(QtCore.QSize(200,80))
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.choose_frame)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.start_chat_btn = QtWidgets.QPushButton(self.choose_frame)
        self.start_chat_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.start_chat_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.start_chat_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.start_chat_btn.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("asserts/icon/call.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_chat_btn.setIcon(icon13)
        self.start_chat_btn.setIconSize(QtCore.QSize(32, 32))
        self.start_chat_btn.setObjectName("start_chat_btn")
        self.horizontalLayout_13.addWidget(self.start_chat_btn)
        self.stop_chat_btn = QtWidgets.QPushButton(self.choose_frame)
        self.stop_chat_btn.setMinimumSize(QtCore.QSize(48, 48))
        self.stop_chat_btn.setMaximumSize(QtCore.QSize(48, 48))
        self.stop_chat_btn.setStyleSheet("QPushButton{\n"
"border-radius:15;\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.stop_chat_btn.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("asserts/icon/stop-call.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_chat_btn.setIcon(icon14)
        self.stop_chat_btn.setIconSize(QtCore.QSize(32, 32))
        self.stop_chat_btn.setObjectName("stop_chat_btn")
        self.horizontalLayout_13.addWidget(self.stop_chat_btn)
        self.horizontalLayout_12.addWidget(self.choose_frame)
        self.verticalLayout_9.addWidget(self.chat_btn_frame)
        self.verticalLayout_4.addWidget(self.chat_frame)
        self.stackedWidget.addWidget(self.chat)
        self.setting = QtWidgets.QWidget()
        self.setting.setObjectName("setting")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.setting)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.setting_frame = QtWidgets.QFrame(self.setting)
        self.setting_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setting_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setting_frame.setObjectName("setting_frame")
        self.info_frame = QtWidgets.QFrame(self.setting_frame)
        self.info_frame.setGeometry(QtCore.QRect(10, 10, 481, 221))
        self.info_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_frame.setObjectName("info_frame")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.info_frame)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.socket_frame = QtWidgets.QFrame(self.info_frame)
        self.socket_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.socket_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.socket_frame.setObjectName("socket_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.socket_frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(self.socket_frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.video_port_lineEdit = QtWidgets.QLineEdit(self.socket_frame)
        self.video_port_lineEdit.setObjectName("video_port_lineEdit")
        self.gridLayout_2.addWidget(self.video_port_lineEdit, 3, 1, 1, 1)
        self.voice_port_lineEdit = QtWidgets.QLineEdit(self.socket_frame)
        self.voice_port_lineEdit.setObjectName("voice_port_lineEdit")
        self.gridLayout_2.addWidget(self.voice_port_lineEdit, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.socket_frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.voice_ip_lineEdit = QtWidgets.QLineEdit(self.socket_frame)
        self.voice_ip_lineEdit.setObjectName("voice_ip_lineEdit")
        self.gridLayout_2.addWidget(self.voice_ip_lineEdit, 0, 1, 1, 1)
        self.video_ip_lineEdit = QtWidgets.QLineEdit(self.socket_frame)
        self.video_ip_lineEdit.setObjectName("video_ip_lineEdit")

        self.voice_ip_lineEdit.setText("192.168.1.100")
        self.video_ip_lineEdit.setText("192.168.1.100")
        self.voice_port_lineEdit.setText("7890")
        self.video_port_lineEdit.setText("7899")

        self.gridLayout_2.addWidget(self.video_ip_lineEdit, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.socket_frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.socket_frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.horizontalLayout_15.addWidget(self.socket_frame)
        self.database_frame = QtWidgets.QFrame(self.info_frame)
        self.database_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.database_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.database_frame.setObjectName("database_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.database_frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.database_frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.database_frame)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.database_frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 3, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.database_frame)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.database_frame)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)
        self.db_host = QtWidgets.QLineEdit(self.database_frame)
        self.db_host.setObjectName("db_host")
        self.gridLayout_3.addWidget(self.db_host, 0, 1, 1, 1)
        self.db_port = QtWidgets.QLineEdit(self.database_frame)
        self.db_port.setObjectName("db_port")
        self.gridLayout_3.addWidget(self.db_port, 1, 1, 1, 1)
        self.db_user = QtWidgets.QLineEdit(self.database_frame)
        self.db_user.setObjectName("db_user")
        self.gridLayout_3.addWidget(self.db_user, 2, 1, 1, 1)
        self.db_pwd = QtWidgets.QLineEdit(self.database_frame)
        self.db_pwd.setObjectName("db_pwd")
        self.gridLayout_3.addWidget(self.db_pwd, 3, 1, 1, 1)
        self.db_name = QtWidgets.QLineEdit(self.database_frame)
        self.db_name.setObjectName("db_name")
        self.gridLayout_3.addWidget(self.db_name, 4, 1, 1, 1)
        self.db_host.setText("192.168.42.129")
        self.db_port.setText("26000")
        self.db_user.setText("dboper")
        self.db_pwd.setText("dboper@123")
        self.db_name.setText("toolMake")
        self.horizontalLayout_15.addWidget(self.database_frame)
        self.submit_btn = QtWidgets.QPushButton(self.setting_frame)
        self.submit_btn.setGeometry(QtCore.QRect(210, 260, 75, 23))
        self.submit_btn.setStyleSheet("QPushButton{\n"
"background-color:rgba(115, 89, 195, 181)\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgba(115, 89, 195, 120)\n"
"}")
        self.submit_btn.setObjectName("submit_btn")
        self.submit_btn.setMinimumSize(QtCore.QSize(50, 40))
        self.horizontalLayout_14.addWidget(self.setting_frame)
        self.stackedWidget.addWidget(self.setting)
        self.horizontalLayout_9.addWidget(self.stackedWidget)
        self.horizontalLayout_7.addWidget(self.center_main_frame)
        self.verticalLayout.addWidget(self.center_frame)
        self.footer_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer_frame.sizePolicy().hasHeightForWidth())
        self.footer_frame.setSizePolicy(sizePolicy)
        self.footer_frame.setMinimumSize(QtCore.QSize(0, 32))
        self.footer_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_frame.setObjectName("footer_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.footer_frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.footer_left_frame = QtWidgets.QFrame(self.footer_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer_left_frame.sizePolicy().hasHeightForWidth())
        self.footer_left_frame.setSizePolicy(sizePolicy)
        self.footer_left_frame.setMinimumSize(QtCore.QSize(0, 32))
        self.footer_left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_left_frame.setObjectName("footer_left_frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.footer_left_frame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.copyright = QtWidgets.QLabel(self.footer_left_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(10)
        self.copyright.setFont(font)
        self.copyright.setObjectName("copyright")
        self.horizontalLayout_6.addWidget(self.copyright, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_4.addWidget(self.footer_left_frame)
        self.footer_right_frame = QtWidgets.QFrame(self.footer_frame)
        self.footer_right_frame.setMinimumSize(QtCore.QSize(0, 32))
        self.footer_right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_right_frame.setObjectName("footer_right_frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.footer_right_frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.version = QtWidgets.QLabel(self.footer_right_frame)
        font = QtGui.QFont()
        font.setFamily("SansSerif")
        font.setPointSize(10)
        self.version.setFont(font)
        self.version.setObjectName("version")
        self.horizontalLayout_5.addWidget(self.version)
        self.horizontalLayout_4.addWidget(self.footer_right_frame, 0, QtCore.Qt.AlignRight)
        self.size_grip = QtWidgets.QFrame(self.footer_frame)
        self.size_grip.setMinimumSize(QtCore.QSize(10, 10))
        self.size_grip.setMaximumSize(QtCore.QSize(10, 10))
        self.size_grip.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.size_grip.setObjectName("size_grip")
        self.horizontalLayout_4.addWidget(self.size_grip, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.footer_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 创建一个关闭事件并设为未触发
        self.continueEvent1 = threading.Event()
        self.continueEvent1.clear()
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.stopChatEvent = threading.Event()
        self.stopChatEvent.clear()

        # 数据
        self.isCamera = True
        self.isPause = False
        self.cameraFlag = 0
        self.pauseFlag = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.recording = False
        self.key = "levi"
        # self.database_info = {
        #         "database": "toolMake",
        #         "user": "dboper",
        #         "password": "dboper@123",
        #         "host": "192.168.42.129",
        #         "port": "26000"
        # }
        self.database_info = {
                "database": "",
                "user": "",
                "password": "",
                "host": "",
                "port": ""
        }
        # 音频参数
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        # 按钮点击
        self.camera_btn.clicked.connect(self.open_camera)
        self.stop_video_btn.clicked.connect(self.stop_camera)
        self.pause_video_btn.clicked.connect(self.pause_camera)
        self.start_audio_btn.clicked.connect(self.audio_click_handler)
        self.play_audio_btn.clicked.connect(self.open_audio)
        self.start_chat_btn.clicked.connect(self.start_video_chat)
        self.stop_chat_btn.clicked.connect(self.stop_video_chat)
        self.submit_btn.clicked.connect(self.setting_info)
    # 设置端口信息
    def setting_info(self):
        self.audio_ip = self.voice_ip_lineEdit.text()
        self.audio_port = self.voice_port_lineEdit.text()
        self.video_ip = self.video_ip_lineEdit.text()
        self.video_port = self.video_port_lineEdit.text()
        # self.d_host = self.db_host.text()
        # self.d_port = self.db_port.text()
        # self.d_user = self.db_user.text()
        # self.d_pwd = self.db_pwd.text()
        # self.d_name = self.db_name.text()
        self.database_info["database"] = self.db_name.text()
        self.database_info["host"] = self.db_host.text()
        self.database_info["port"] = self.db_port.text()
        self.database_info["user"] = self.db_user.text()
        self.database_info["password"] = self.db_pwd.text()
        print("initialize")
    # 数据库连接
    def connect_db(self, database_info):
            database = database_info["database"]  # 选择数据库名称
            user = database_info["user"]
            password = database_info["password"]
            host = database_info["host"]  # 数据库ip
            port = database_info["port"]
            mydb = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)  # 连接数据库
            return mydb
    # 上传数据
    def data_upload(self, input_file, file_size, file_type, file_data):
            print("数据上传中...")
            mydb = self.connect_db(self.database_info)
            cur = mydb.cursor()  # 创建光标
            # 创建数据库表
            cur.execute("""
                CREATE TABLE IF NOT EXISTS t_files (
                     id SERIAL PRIMARY KEY,
                     file_name VARCHAR(255) NOT NULL,
                     file_size BIGINT NOT NULL,
                     storage_time TIMESTAMP NOT NULL,
                     file_type VARCHAR(50) NOT NULL,
                     file_data BYTEA NOT NULL
                )
            """)
            mydb.commit()
            print('表创建成功！')
            fname = input_file.split('/')[-1]
            entime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            cur.execute(
                    "INSERT INTO t_files (file_name, file_size, storage_time, file_type, file_data) VALUES (%s, %s, %s, %s, %s::bytea)",
                    (fname, file_size, entime, file_type, psycopg2.Binary(file_data))
            )
            mydb.commit()
            cur.close()  # 关闭光标
            mydb.close()  # 关闭数据库连接
            print("数据上传成功")
    # 加密文件
    def encrypt_file(self, input_file):
            with open(input_file, "rb") as f:
                    text_data = f.read()
            f.close()
            prefix = input_file.split('.')[0]
            suffix = input_file.split('.')[-1]
            sBox = self.s_box(self.key)
            encrypted_text = self.rc4_encrypt(text_data, sBox)
            output_file = prefix + "-encrypt." + suffix
            with open(output_file, "wb") as f:
                    f.write(encrypted_text)
            f.close()
            print("文件已加密并保存为", output_file.split('/')[-1])
            return output_file
    # 解密文件
    def decrypt_file(self, input_file_path):
            # 文件名
            audioName = str(input_file_path).split('/')[-1]
            # 前缀
            prefix = audioName.split('.')[0]
            # 后缀
            suffix = audioName.split('.')[-1]
            with open(input_file_path, "rb") as f:
                    encrypted_text_data = f.read()
            f.close()
            sBox = self.s_box(self.key)
            decrypted_text = self.rc4_encrypt(encrypted_text_data, sBox)
            audio_output_file = prefix + "-decrypt." + suffix
            with open(audio_output_file, "wb") as f:
                    f.write(decrypted_text)
            f.close()
            print("The file has been decrypted and saved as ", audio_output_file)
            return audio_output_file
    # 录音按钮
    def audio_click_handler(self):
            if self.recording:
                    self.recording = False
                    self.start_audio_btn.setIcon(QIcon("asserts/icon/audios.svg"))
            else:
                    self.recording = True
                    self.start_audio_btn.setIcon(QIcon("asserts/icon/stop circle.svg"))
                    threading.Thread(target=self.record).start()
    # 录音
    def record(self):
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            frames = []
            start = time.time()
            while self.recording:
                    data = stream.read(1024)
                    frames.append(data)
                    passed = time.time() - start
                    secs = passed % 60
                    mins = passed // 60
                    hours = mins // 60
                    self.audio_time.setText(f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
            stream.stop_stream()
            stream.close()
            audio.terminate()
            exists = True
            self.audio_index = 1
            while exists:
                    if os.path.exists(f"./media/recording{self.audio_index}.wav"):
                            self.audio_index += 1
                    else:
                            exists = False
            sound_file = wave.open(f"./media/recording{self.audio_index}.wav", "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(frames))
            sound_file.close()

            input_file = f"media/recording{self.audio_index}.wav"
            output_file = self.encrypt_file(input_file)
            file_size = os.path.getsize(input_file)
            with open(input_file, "rb") as f:
                    file_data = f.read()
            print(file_size)
            self.data_upload(input_file, file_size, "wav", file_data)
    # 打开文件解密
    def open_audio(self):
            # 打开加密文件
            audioPath, oth = QFileDialog.getOpenFileName(self, "Open File")
            print(audioPath)
            if audioPath:
                    self.audio_name.setText(str(audioPath).split('/')[-1])
                    print(str(audioPath).split('/')[-1])
                    audio_output_file = self.decrypt_file(audioPath)
                    print(audio_output_file)
    # 打开摄像头
    def open_camera(self):
            self.fileName = ""
            if not self.isCamera:
                    self.fileName, self.fileType = QFileDialog.getOpenFileName(self, 'Choose file', '',
                                                                               "MP4Files(*.mp4);;AVI Files(*.avi)")
                    self.cap = cv2.VideoCapture(self.fileName)
                    self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
            else:
                    # 下面两种rtsp格式都是支持的
                    #  cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
                    self.cameraFlag = 1
                    self.cap = cv2.VideoCapture(0)
                    exists = True
                    self.video_index = 1
                    while exists:
                            if os.path.exists(f"./media/video{self.video_index}.avi"):
                                    self.video_index += 1
                            else:
                                    exists = False
                    self.video_output = cv2.VideoWriter(f'./media/video{self.video_index}.avi', self.fourcc, 30.0,
                                                        (640, 480))

            # 创建视频显示线程
            if (self.fileName != "") or (self.cameraFlag == 1):
                    th = threading.Thread(target=self.Display)
                    th.start()
    # 关闭摄像头
    def stop_camera(self):
            input_file = f"media/video{self.video_index}.avi"
            output_file = self.encrypt_file(input_file)
            file_size = os.path.getsize(input_file)
            with open(input_file, "rb") as f:
                    file_data = f.read()
            print(file_size)
            self.data_upload(input_file, file_size, "avi", file_data)
            self.cameraFlag = 0
            self.stopEvent.set()
    # 暂停摄像
    def pause_camera(self):
            self.continueEvent1.set()
    # 显示摄像头画面
    def Display(self):
            self.camera_btn.setEnabled(False)
            self.stop_video_btn.setEnabled(True)
            self.pause_video_btn.setEnabled(True)
            while self.cap.isOpened() and True:
                    success, frame = self.cap.read()
                    self.video_output.write(frame)
                    # RGB转BGR
                    if success == False:
                            print("play finished")
                            break
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    self.video_label.setPixmap(QPixmap.fromImage(img))

                    if self.isCamera:
                            cv2.waitKey(1)
                    else:
                            cv2.waitKey(int(1000 / self.frameRate))

                    if True == self.continueEvent1.is_set():
                            self.pause_video_btn.setIcon(QIcon("asserts/icon/play.svg"))
                            self.continueEvent1.clear()
                            self.pauseFlag = 1
                            while self.pauseFlag == 1:
                                    if True == self.continueEvent1.is_set():
                                            self.pause_video_btn.setIcon(QIcon("asserts/icon/pause.svg"))
                                            self.continueEvent1.clear()
                                            self.pauseFlag = 0
                    if True == self.stopEvent.is_set():
                            break
            self.cap.release()
            self.stopEvent.clear()
            self.video_label.clear()
            self.stop_video_btn.setEnabled(False)
            self.camera_btn.setEnabled(True)
            self.video_label.setText("Video")
    # 生成rc4算法S-Box
    def s_box(self, key):
            # S-盒
            sBox = list(range(256))
            # K-盒
            kBox = [ord(char) for char in key]
            j = 0
            for i in range(256):
                    j = (j + sBox[i] + kBox[i % len(kBox)]) % 256
                    sBox[i], sBox[j] = sBox[j], sBox[i]
            return sBox
    # rc4算法加密
    def rc4_encrypt(self, media_data, sBox):
            res = bytearray()
            i = j = 0
            for byte in media_data:
                    i = (i + 1) % 256
                    j = (j + sBox[i]) % 256
                    sBox[i], sBox[j] = sBox[j], sBox[i]
                    t = (sBox[i] + sBox[j]) % 256
                    k = sBox[t]
                    res.append(byte ^ k)
            return res
    # 发送视频帧
    def send_frame(self, sock):
            while self.cap.isOpened() and True:
                    success, self.sframe = self.cap.read()
                    # RGB转BGR
                    if not success:
                            print("play finished")
                            break
                    self.sframe = cv2.cvtColor(self.sframe, cv2.COLOR_RGB2BGR)
                    # img = QImage(self.sframe.data, self.sframe.shape[1], self.sframe.shape[0], QImage.Format_RGB888)
                    # self.chat_label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    # _, self.encoded_frame = cv2.imencode('.jpg', self.sframe)
                    _, self.encoded_frame = cv2.imencode('.jpg', self.sframe, [cv2.IMWRITE_JPEG_QUALITY, 10])
                    print("send frame:" + str(len(self.encoded_frame)))
                    sock.sendto(self.encoded_frame.tobytes(), (self.video_ip, int(self.video_port)))
                    # print(len(self.encoded_frame.tobytes()))
                    if self.stopChatEvent.is_set():
                            break

            self.cap.release()
            self.stopChatEvent.clear()
    # 接收视频帧
    def recv_frame(self, sock):
            while True:
                    data, _ = sock.recvfrom(921600)
                    if not data:  # 检查接收到的数据是否为空
                            print("No data received.")
                            break
                    print("recv frame:" + str(len(data)))
                    self.cframe = np.frombuffer(data, dtype=np.uint8)
                    # 检查解码是否成功
                    if cv2.imdecode(self.cframe, cv2.IMREAD_COLOR) is None:
                            print("Failed to decode image.")
                            continue  # 继续下一次循环，尝试再次接收数据
                    self.cframe = cv2.imdecode(self.cframe, cv2.IMREAD_COLOR)
                    # self.cframe = cv2.cvtColor(self.cframe, cv2.COLOR_RGB2BGR)
                    img = QImage(self.cframe.data, self.cframe.shape[1], self.cframe.shape[0], QImage.Format_RGB888)
                    self.chat_label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    if self.stopChatEvent.is_set():
                            break
            self.cap.release()
            self.stopChatEvent.clear()
    # 开始视频通话
    def start_video_chat(self):
            if self.server_btn.isChecked():
                    # # 创建语音套接字UDP
                    # self.server_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # # 绑定IP端口
                    # self.server_audio.bind(("", int(self.audio_port)))
                    # 创建语音套接字
                    self.server_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 绑定IP端口
                    self.server_audio.bind(("", int(self.audio_port)))
                    # 监听
                    self.server_audio.listen(128)
                    # 连接成功
                    self.sock_audio, client_addr = self.server_audio.accept()
                    print("Client connected:", client_addr)
                    # 创建视频套接字UDP
                    self.server_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # 绑定IP端口
                    self.server_video.bind(("", int(self.video_port)))
                    ps = pyaudio.PyAudio()
                    pr = pyaudio.PyAudio()
                    # 发送接收语音线程
                    sender = threading.Thread(target=self.send_audio, args=(self.sock_audio, ps))
                    recver = threading.Thread(target=self.recv_audio, args=(self.sock_audio, pr))
                    # 发送接收视频线程
                    self.cap = cv2.VideoCapture(0)
                    vds = threading.Thread(target=self.send_frame, args=(self.server_video,))
                    vdr = threading.Thread(target=self.recv_frame, args=(self.server_video,))
                    vds.start()
                    vdr.start()
                    sender.start()
                    recver.start()
            elif self.client_btn.isChecked():
                    # 创建语音套接字
                    # self.client_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # 创建语音套接字
                    self.client_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 连接
                    self.client_audio.connect((self.audio_ip, int(self.audio_port)))
                    # 创建视频套接字
                    self.client_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    ps = pyaudio.PyAudio()
                    pr = pyaudio.PyAudio()
                    # 发送接收语音线程
                    sender = threading.Thread(target=self.send_audio, args=(self.client_audio, ps))
                    recver = threading.Thread(target=self.recv_audio, args=(self.client_audio, pr))
                    # 发送接收视频线程
                    self.cap = cv2.VideoCapture(0)
                    vds = threading.Thread(target=self.send_frame, args=(self.client_video,))
                    vdr = threading.Thread(target=self.recv_frame, args=(self.client_video,))
                    vds.start()
                    vdr.start()
                    sender.start()
                    recver.start()
    # 结束视频通话
    def stop_video_chat(self):
            # self.stopChatEvent.set()

            if self.server_btn.isChecked():
                    self.server_audio.shutdown(socket.SHUT_RDWR)
                    self.server_video.shutdown(socket.SHUT_RDWR)
                    self.server_audio.close()
                    self.server_video.close()

            elif self.client_btn.isChecked():
                    self.client_audio.shutdown(socket.SHUT_RDWR)
                    self.client_video.shutdown(socket.SHUT_RDWR)
                    self.client_audio.close()
                    self.client_video.close()

            self.chat_label.clear()
            self.chat_label.setText("video")
            self.stopChatEvent.set()
    # 发送语音
    def send_audio(self, sock, ps):
            stream = ps.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                             frames_per_buffer=self.CHUNK)
            while True:
                    data = stream.read(self.CHUNK)
                    print("send audio:" + str(len(data)))
                    try:
                            # sock.sendto(data, (self.audio_ip, int(self.audio_port)))
                            sock.send(data)
                    except Exception as e:
                            print(f"Send error: {e}")
                            break
                    time.sleep(0.01)
    # 接收语音
    def recv_audio(self, sock, pr):
            stream = pr.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                             frames_per_buffer=self.CHUNK)
            while True:
                    try:
                            # data, _ = sock.recvfrom(self.CHUNK)
                            data = sock.recv(self.CHUNK)
                            print("recv audio:" + str(len(data)))
                            stream.write(data)
                    except Exception as e:
                            print(f"Receive error: {e}")
                            break
                    time.sleep(0.01)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "tool Make Server"))
        self.title.setText(_translate("MainWindow", "tool Make Server"))
        self.pushButton_5.setText(_translate("MainWindow", "."))
        self.label.setText(_translate("MainWindow", "Audio"))
        self.label_2.setText(_translate("MainWindow", "Video"))
        self.label_3.setText(_translate("MainWindow", "Chat"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "Audio"))
        self.audio_time.setText(_translate("MainWindow", "00:00:00"))
        self.video_label.setText(_translate("MainWindow", "Video"))
        self.chat_label.setText(_translate("MainWindow", "chat"))
        self.server_btn.setText(_translate("MainWindow", "Server"))
        self.client_btn.setText(_translate("MainWindow", "Client"))
        self.label_7.setText(_translate("MainWindow", "voice"))
        self.label_8.setText(_translate("MainWindow", "port"))
        self.label_9.setText(_translate("MainWindow", "video"))
        self.label_10.setText(_translate("MainWindow", "port"))
        self.label_15.setText(_translate("MainWindow", "database"))
        self.label_13.setText(_translate("MainWindow", "user"))
        self.label_14.setText(_translate("MainWindow", "password"))
        self.label_12.setText(_translate("MainWindow", "port"))
        self.label_11.setText(_translate("MainWindow", "host"))
        self.submit_btn.setText(_translate("MainWindow", "submit"))
        self.copyright.setText(_translate("MainWindow", "tool Make"))
        self.version.setText(_translate("MainWindow", "V1.0.0"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
