# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'log_in.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LOGIN(object):
    def setupUi(self, LOGIN):
        LOGIN.setObjectName("LOGIN")
        LOGIN.resize(421, 221)
        LOGIN.setMinimumSize(QtCore.QSize(421, 221))
        LOGIN.setMaximumSize(QtCore.QSize(421, 221))
        self.groupBox_7 = QtWidgets.QGroupBox(LOGIN)
        self.groupBox_7.setGeometry(QtCore.QRect(0, 0, 421, 221))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setStyleSheet("\n"
"border-color: rgb(0, 0, 0);")
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.user_name_lin = QtWidgets.QLineEdit(self.groupBox_7)
        self.user_name_lin.setGeometry(QtCore.QRect(200, 50, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_name_lin.setFont(font)
        self.user_name_lin.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.user_name_lin.setStyleSheet("color:rgb(0, 0, 0)")
        self.user_name_lin.setObjectName("user_name_lin")
        self.label_21 = QtWidgets.QLabel(self.groupBox_7)
        self.label_21.setGeometry(QtCore.QRect(120, 90, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("\n"
"color:rgb(0, 0, 0);\n"
"border: none;")
        self.label_21.setObjectName("label_21")
        self.user_pw_lin = QtWidgets.QLineEdit(self.groupBox_7)
        self.user_pw_lin.setGeometry(QtCore.QRect(200, 90, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_pw_lin.setFont(font)
        self.user_pw_lin.setStyleSheet("color:rgb(0, 0, 0)")
        self.user_pw_lin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.user_pw_lin.setObjectName("user_pw_lin")
        self.login_btn = QtWidgets.QPushButton(self.groupBox_7)
        self.login_btn.setGeometry(QtCore.QRect(170, 160, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.login_btn.setFont(font)
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btn.setStyleSheet("color:rgb(0, 0, 0);\n"
"border radius 5 px")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/unlock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.login_btn.setIcon(icon)
        self.login_btn.setIconSize(QtCore.QSize(17, 17))
        self.login_btn.setFlat(False)
        self.login_btn.setObjectName("login_btn")
        self.label_28 = QtWidgets.QLabel(self.groupBox_7)
        self.label_28.setGeometry(QtCore.QRect(120, 50, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("border: none;\n"
"color:rgb(0, 0, 0)")
        self.label_28.setWordWrap(False)
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.groupBox_7)
        self.label_29.setGeometry(QtCore.QRect(24, 40, 81, 91))
        self.label_29.setStyleSheet("border: none;")
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/icons8-user-account-96.png"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")

        self.retranslateUi(LOGIN)
        QtCore.QMetaObject.connectSlotsByName(LOGIN)

    def retranslateUi(self, LOGIN):
        _translate = QtCore.QCoreApplication.translate
        LOGIN.setWindowTitle(_translate("LOGIN", "LOGIN"))
        self.user_name_lin.setPlaceholderText(_translate("LOGIN", "Enter Username"))
        self.label_21.setText(_translate("LOGIN", "PASSWORD"))
        self.user_pw_lin.setPlaceholderText(_translate("LOGIN", "Enter Password"))
        self.login_btn.setText(_translate("LOGIN", "  Login"))
        self.label_28.setText(_translate("LOGIN", "USERNAME"))

