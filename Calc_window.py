# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Calc_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(311, 321)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 291, 201))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 30, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 81, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.dte_rih = QtWidgets.QDateEdit(self.groupBox)
        self.dte_rih.setGeometry(QtCore.QRect(140, 30, 110, 22))
        self.dte_rih.setCalendarPopup(True)
        self.dte_rih.setObjectName("dte_rih")
        self.dte_pooh = QtWidgets.QDateEdit(self.groupBox)
        self.dte_pooh.setGeometry(QtCore.QRect(140, 70, 110, 22))
        self.dte_pooh.setCalendarPopup(True)
        self.dte_pooh.setObjectName("dte_pooh")
        self.last_run = QtWidgets.QLineEdit(self.groupBox)
        self.last_run.setGeometry(QtCore.QRect(140, 110, 113, 20))
        self.last_run.setObjectName("last_run")
        self.calc_btn = QtWidgets.QPushButton(self.groupBox)
        self.calc_btn.setGeometry(QtCore.QRect(80, 155, 131, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/CTA-Calculator-Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calc_btn.setIcon(icon)
        self.calc_btn.setIconSize(QtCore.QSize(25, 25))
        self.calc_btn.setObjectName("calc_btn")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 209, 291, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 33, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.res_lbl = QtWidgets.QLabel(self.groupBox_2)
        self.res_lbl.setGeometry(QtCore.QRect(130, 33, 91, 31))
        self.res_lbl.setFrameShape(QtWidgets.QFrame.Box)
        self.res_lbl.setText("")
        self.res_lbl.setObjectName("res_lbl")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(230, 33, 31, 31))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Run Life Calculator"))
        self.groupBox.setTitle(_translate("Dialog", "Input "))
        self.label.setText(_translate("Dialog", "RIH Date"))
        self.label_2.setText(_translate("Dialog", "POOH Date"))
        self.label_3.setText(_translate("Dialog", "Last Run Life"))
        self.dte_rih.setDisplayFormat(_translate("Dialog", "yyyy/M/d"))
        self.dte_pooh.setDisplayFormat(_translate("Dialog", "yyyy/M/d"))
        self.calc_btn.setText(_translate("Dialog", " CALCULATE"))
        self.groupBox_2.setTitle(_translate("Dialog", "output"))
        self.label_4.setText(_translate("Dialog", "Cumm.Run Life"))
        self.label_6.setText(_translate("Dialog", "Days"))