# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcher.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QStackedWidget,
    QWidget)
import assets_rc
import assets_rc
import assets_rc
import assets_rc
import assets_rc
import assets_rc
import assets_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(801, 500)
        font = QFont()
        font.setFamilies([u"NuberNext"])
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gameLauncherPage = QWidget(self.centralwidget)
        self.gameLauncherPage.setObjectName(u"gameLauncherPage")
        self.gameLauncherPage.setEnabled(True)
        self.gameLauncherPage.setGeometry(QRect(60, 0, 741, 501))
        self.gameLauncherPage.setStyleSheet(u"")
        self.announcementSlider = QStackedWidget(self.gameLauncherPage)
        self.announcementSlider.setObjectName(u"announcementSlider")
        self.announcementSlider.setGeometry(QRect(40, 250, 221, 141))
        self.announcementSlider.setStyleSheet(u"background-color: rgb(20, 20, 20);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setEnabled(True)
        self.label_5 = QLabel(self.page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(44, 18, 131, 111))
        self.label_5.setPixmap(QPixmap(u":/assets/endfield_logo.png"))
        self.label_5.setScaledContents(True)
        self.announcementSlider.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.announcementSlider.addWidget(self.page_2)
        self.announcementList = QFrame(self.gameLauncherPage)
        self.announcementList.setObjectName(u"announcementList")
        self.announcementList.setGeometry(QRect(290, 250, 411, 141))
        self.announcementList.setStyleSheet(u"background-color: rgba(20, 20, 20, 150);")
        self.announcementList.setFrameShape(QFrame.Shape.StyledPanel)
        self.announcementList.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.announcementList)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"NuberNext"])
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setHintingPreference(QFont.PreferNoHinting)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"background-color: rgb(254, 255, 30);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(self.announcementList)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 0, 291, 31))
        self.label_2.setStyleSheet(u"background-color: rgba(20, 20, 20, 150);")
        self.label_3 = QLabel(self.announcementList)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 34, 411, 31))
        font2 = QFont()
        font2.setFamilies([u"NuberNext"])
        font2.setHintingPreference(QFont.PreferNoHinting)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"margin-left: 6px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_4 = QLabel(self.announcementList)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 62, 411, 31))
        self.label_4.setFont(font2)
        self.label_4.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"margin-left: 6px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_10 = QLabel(self.announcementList)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(0, 90, 411, 31))
        self.label_10.setFont(font2)
        self.label_10.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"margin-left: 6px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.gameLaunchButton = QPushButton(self.gameLauncherPage)
        self.gameLaunchButton.setObjectName(u"gameLaunchButton")
        self.gameLaunchButton.setGeometry(QRect(560, 420, 141, 51))
        font3 = QFont()
        font3.setFamilies([u"NuberNext"])
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setKerning(True)
        font3.setHintingPreference(QFont.PreferNoHinting)
        self.gameLaunchButton.setFont(font3)
        self.gameLaunchButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(254, 241, 4);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #dcd414; /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #c3bc12; /* Slightly darker green */\n"
"}")
        self.gameLaunchButton.setFlat(False)
        self.label_6 = QLabel(self.gameLauncherPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 20, 251, 101))
        self.label_6.setPixmap(QPixmap(u":/assets/endfield_logo_v2.png"))
        self.label_6.setScaledContents(True)
        self.gameLaunchInfo = QLabel(self.gameLauncherPage)
        self.gameLaunchInfo.setObjectName(u"gameLaunchInfo")
        self.gameLaunchInfo.setGeometry(QRect(45, 427, 441, 16))
        font4 = QFont()
        font4.setFamilies([u"NuberNext"])
        font4.setPointSize(8)
        font4.setBold(False)
        font4.setHintingPreference(QFont.PreferNoHinting)
        self.gameLaunchInfo.setFont(font4)
        self.gameLaunchInfo.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.gameLaunchProgressBar = QProgressBar(self.gameLauncherPage)
        self.gameLaunchProgressBar.setObjectName(u"gameLaunchProgressBar")
        self.gameLaunchProgressBar.setGeometry(QRect(40, 449, 451, 16))
        self.gameLaunchProgressBar.setStyleSheet(u"QProgressBar {\n"
"	border: 1px solid rgb(100, 100, 100);\n"
"	border-radius: 8px;\n"
"	background-color: #ffffff;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"	background-color: #f4eb16;\n"
"	border-radius: 7px;\n"
"}")
        self.gameLaunchProgressBar.setValue(24)
        self.gameLaunchProgressBar.setTextVisible(False)
        self.gameLaunchProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.gameLaunchProgressBar.setInvertedAppearance(False)
        self.backgroundImage = QLabel(self.centralwidget)
        self.backgroundImage.setObjectName(u"backgroundImage")
        self.backgroundImage.setGeometry(QRect(0, 0, 801, 501))
        self.backgroundImage.setPixmap(QPixmap(u":/assets/launcher_bg_a.png"))
        self.backgroundImage.setScaledContents(True)
        self.navbar = QWidget(self.centralwidget)
        self.navbar.setObjectName(u"navbar")
        self.navbar.setGeometry(QRect(0, 0, 61, 501))
        self.navbar.setStyleSheet(u"QWidget {\n"
"    background-color: rgba(25, 25, 25, 220);\n"
"}\n"
"")
        self.gameLauncherNavButton = QPushButton(self.navbar)
        self.gameLauncherNavButton.setObjectName(u"gameLauncherNavButton")
        self.gameLauncherNavButton.setGeometry(QRect(10, 10, 41, 41))
        self.gameLauncherNavButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(254, 241, 4);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-radius: 5px;\n"
"	border-image: url(:/assets/game_icon.png) no-repeat center center fixed;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #dcd414; /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #c3bc12; /* Slightly darker green */\n"
"}")
        self.serverLauncherNavButton = QPushButton(self.navbar)
        self.serverLauncherNavButton.setObjectName(u"serverLauncherNavButton")
        self.serverLauncherNavButton.setGeometry(QRect(10, 70, 41, 41))
        font5 = QFont()
        font5.setFamilies([u"NuberNext"])
        font5.setPointSize(16)
        font5.setBold(True)
        font5.setHintingPreference(QFont.PreferNoHinting)
        self.serverLauncherNavButton.setFont(font5)
        self.serverLauncherNavButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(254, 241, 4);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #dcd414;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #c3bc12; /* Slightly darker green */\n"
"}")
        self.gradientEffect = QLabel(self.centralwidget)
        self.gradientEffect.setObjectName(u"gradientEffect")
        self.gradientEffect.setGeometry(QRect(0, 190, 801, 311))
        self.gradientEffect.setStyleSheet(u"QWidget {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"		x2: 0, y2: 1,\n"
"        stop: 0 rgba(30, 30, 30, 0),\n"
"		stop: 0.2 rgba(30, 30, 30, 200),\n"
"        stop: 0.5 rgba(30, 30, 30, 255)\n"
"    );\n"
"}\n"
"")
        self.serverLauncherPage = QWidget(self.centralwidget)
        self.serverLauncherPage.setObjectName(u"serverLauncherPage")
        self.serverLauncherPage.setEnabled(True)
        self.serverLauncherPage.setGeometry(QRect(60, 0, 741, 501))
        self.serverLauncherPage.setStyleSheet(u"")
        self.announcementSlider_3 = QStackedWidget(self.serverLauncherPage)
        self.announcementSlider_3.setObjectName(u"announcementSlider_3")
        self.announcementSlider_3.setGeometry(QRect(40, 250, 221, 141))
        self.announcementSlider_3.setStyleSheet(u"background-color: rgb(20, 20, 20);")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setEnabled(True)
        self.label_15 = QLabel(self.page_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 32, 71, 71))
        self.label_15.setPixmap(QPixmap(u":/assets/github_logo.png"))
        self.label_15.setScaledContents(True)
        self.label_8 = QLabel(self.page_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(100, 48, 91, 21))
        font6 = QFont()
        font6.setFamilies([u"NuberNext"])
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setHintingPreference(QFont.PreferNoHinting)
        self.label_8.setFont(font6)
        self.label_8.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_9 = QLabel(self.page_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(100, 71, 91, 21))
        font7 = QFont()
        font7.setFamilies([u"NuberNext"])
        font7.setPointSize(10)
        font7.setBold(False)
        font7.setHintingPreference(QFont.PreferNoHinting)
        self.label_9.setFont(font7)
        self.label_9.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.announcementSlider_3.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.announcementSlider_3.addWidget(self.page_6)
        self.announcementList_3 = QFrame(self.serverLauncherPage)
        self.announcementList_3.setObjectName(u"announcementList_3")
        self.announcementList_3.setGeometry(QRect(290, 250, 411, 141))
        self.announcementList_3.setStyleSheet(u"background-color: rgba(20, 20, 20, 150);")
        self.announcementList_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.announcementList_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_16 = QLabel(self.announcementList_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(0, 0, 121, 31))
        self.label_16.setFont(font1)
        self.label_16.setStyleSheet(u"background-color: rgb(254, 255, 30);")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_17 = QLabel(self.announcementList_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(120, 0, 291, 31))
        self.label_17.setStyleSheet(u"background-color: rgba(20, 20, 20, 150);")
        self.label_18 = QLabel(self.announcementList_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(0, 34, 411, 31))
        self.label_18.setFont(font2)
        self.label_18.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"margin-left: 6px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_19 = QLabel(self.announcementList_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(0, 62, 411, 31))
        self.label_19.setFont(font2)
        self.label_19.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"margin-left: 6px;\n"
"background-color: rgba(255, 255, 255, 0);")
        self.serverLaunchButton = QPushButton(self.serverLauncherPage)
        self.serverLaunchButton.setObjectName(u"serverLaunchButton")
        self.serverLaunchButton.setGeometry(QRect(560, 420, 141, 51))
        self.serverLaunchButton.setFont(font3)
        self.serverLaunchButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(254, 241, 4);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #dcd414; /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #c3bc12; /* Slightly darker green */\n"
"}")
        self.serverLaunchButton.setFlat(False)
        self.label_20 = QLabel(self.serverLauncherPage)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(0, 20, 251, 101))
        self.label_20.setPixmap(QPixmap(u":/assets/endfield_logo_v2.png"))
        self.label_20.setScaledContents(True)
        self.serverLaunchInfo = QLabel(self.serverLauncherPage)
        self.serverLaunchInfo.setObjectName(u"serverLaunchInfo")
        self.serverLaunchInfo.setGeometry(QRect(45, 427, 441, 16))
        self.serverLaunchInfo.setFont(font4)
        self.serverLaunchInfo.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.serverLaunchProgressBar = QProgressBar(self.serverLauncherPage)
        self.serverLaunchProgressBar.setObjectName(u"serverLaunchProgressBar")
        self.serverLaunchProgressBar.setGeometry(QRect(40, 449, 451, 16))
        self.serverLaunchProgressBar.setStyleSheet(u"QProgressBar {\n"
"	border: 1px solid rgb(100, 100, 100);\n"
"	border-radius: 8px;\n"
"	background-color: #ffffff;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"	background-color: #f4eb16;\n"
"	border-radius: 7px;\n"
"}")
        self.serverLaunchProgressBar.setTextVisible(False)
        self.serverLaunchProgressBar.setOrientation(Qt.Orientation.Horizontal)
        self.serverLaunchProgressBar.setInvertedAppearance(False)
        self.label_7 = QLabel(self.serverLauncherPage)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(41, 126, 241, 16))
        self.label_7.setFont(font6)
        self.label_7.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.titleBar = QWidget(self.centralwidget)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setGeometry(QRect(60, 0, 741, 41))
        self.closeButton = QPushButton(self.titleBar)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setGeometry(QRect(707, 2, 31, 31))
        self.closeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/close_icon.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(20, 20, 20, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 20, 20, 100); /* Slightly darker green */\n"
"}")
        self.minimizeButton = QPushButton(self.titleBar)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setGeometry(QRect(672, 3, 31, 31))
        self.minimizeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/minimize_icon.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(20, 20, 20, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 20, 20, 100); /* Slightly darker green */\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.backgroundImage.raise_()
        self.gradientEffect.raise_()
        self.gameLauncherPage.raise_()
        self.navbar.raise_()
        self.serverLauncherPage.raise_()
        self.titleBar.raise_()

        self.retranslateUi(MainWindow)

        self.announcementSlider.setCurrentIndex(0)
        self.announcementSlider_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Endfield Launcher", None))
        self.label_5.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Announcements", None))
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Endfield Client [Beyond 0.2.58] is now available!", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Endfield Client [Beyond 0.2.57] is no longer supported!", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Join discord server <span style=\" text-decoration: underline;\">https://discord.gg/4y2wQ5Byzh</span> for more info!</p></body></html>", None))
        self.gameLaunchButton.setText(QCoreApplication.translate("MainWindow", u"Launch", None))
        self.label_6.setText("")
        self.gameLaunchInfo.setText(QCoreApplication.translate("MainWindow", u"Neural Network Connecting.....", None))
        self.backgroundImage.setText("")
        self.gameLauncherNavButton.setText("")
        self.serverLauncherNavButton.setText(QCoreApplication.translate("MainWindow", u"PS", None))
        self.gradientEffect.setText("")
        self.label_15.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"ArkField PS", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"@ SuikoAkari", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Announcements", None))
        self.label_17.setText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"DotNet 8.0 is Required to run the server program!", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"MongoDB is Required to run the server program!", None))
        self.serverLaunchButton.setText(QCoreApplication.translate("MainWindow", u"Launch", None))
        self.label_20.setText("")
        self.serverLaunchInfo.setText(QCoreApplication.translate("MainWindow", u"Neural Network Connecting.....", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"| SERVER by SuikoAkari", None))
        self.closeButton.setText("")
        self.minimizeButton.setText("")
    # retranslateUi

