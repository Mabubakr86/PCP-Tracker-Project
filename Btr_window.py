# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Btr_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(580, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 165, 560, 190))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_62 = QtWidgets.QLabel(self.groupBox_2)
        self.label_62.setGeometry(QtCore.QRect(10, 30, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_62.setFont(font)
        self.label_62.setStyleSheet("border:none;\n"
"")
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.groupBox_2)
        self.label_63.setGeometry(QtCore.QRect(10, 70, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_63.setFont(font)
        self.label_63.setStyleSheet("border:none;\n"
"")
        self.label_63.setObjectName("label_63")
        self.label_50 = QtWidgets.QLabel(self.groupBox_2)
        self.label_50.setGeometry(QtCore.QRect(10, 150, 61, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_50.setFont(font)
        self.label_50.setStyleSheet("border:none;\n"
"")
        self.label_50.setObjectName("label_50")
        self.rtr = QtWidgets.QComboBox(self.groupBox_2)
        self.rtr.setGeometry(QtCore.QRect(160, 30, 151, 31))
        self.rtr.setObjectName("rtr")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.rtr.addItem("")
        self.str = QtWidgets.QComboBox(self.groupBox_2)
        self.str.setGeometry(QtCore.QRect(160, 70, 151, 31))
        self.str.setObjectName("str")
        self.str.addItem("")
        self.str.addItem("")
        self.str.addItem("")
        self.str.addItem("")
        self.str.addItem("")
        self.str.addItem("")
        self.label_65 = QtWidgets.QLabel(self.groupBox_2)
        self.label_65.setGeometry(QtCore.QRect(10, 110, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_65.setFont(font)
        self.label_65.setStyleSheet("border:none;\n"
"")
        self.label_65.setObjectName("label_65")
        self.tbar = QtWidgets.QComboBox(self.groupBox_2)
        self.tbar.setGeometry(QtCore.QRect(160, 110, 151, 31))
        self.tbar.setObjectName("tbar")
        self.tbar.addItem("")
        self.tbar.addItem("")
        self.tbar.addItem("")
        self.comm = QtWidgets.QTextEdit(self.groupBox_2)
        self.comm.setGeometry(QtCore.QRect(160, 150, 381, 31))
        self.comm.setObjectName("comm")
        self.addbtr_btn = QtWidgets.QPushButton(self.centralwidget)
        self.addbtr_btn.setGeometry(QtCore.QRect(170, 500, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.addbtr_btn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/icons8-plus-48 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addbtr_btn.setIcon(icon)
        self.addbtr_btn.setIconSize(QtCore.QSize(30, 30))
        self.addbtr_btn.setObjectName("addbtr_btn")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 365, 560, 120))
        self.groupBox_3.setObjectName("groupBox_3")
        self.tqatmax_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.tqatmax_2.setGeometry(QtCore.QRect(560, 40, 41, 31))
        self.tqatmax_2.setText("")
        self.tqatmax_2.setObjectName("tqatmax_2")
        self.get_test_link = QtWidgets.QPushButton(self.groupBox_3)
        self.get_test_link.setEnabled(True)
        self.get_test_link.setGeometry(QtCore.QRect(200, 70, 160, 36))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.get_test_link.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/icons8-attach-filled-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.get_test_link.setIcon(icon1)
        self.get_test_link.setIconSize(QtCore.QSize(30, 30))
        self.get_test_link.setObjectName("get_test_link")
        self.ftrradbtn = QtWidgets.QCheckBox(self.groupBox_3)
        self.ftrradbtn.setGeometry(QtCore.QRect(60, 40, 131, 17))
        self.ftrradbtn.setObjectName("ftrradbtn")
        self.btrradbtn = QtWidgets.QCheckBox(self.groupBox_3)
        self.btrradbtn.setGeometry(QtCore.QRect(390, 40, 131, 17))
        self.btrradbtn.setObjectName("btrradbtn")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 560, 160))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(330, 30, 71, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.serial2_ent_2 = QtWidgets.QLineEdit(self.groupBox)
        self.serial2_ent_2.setGeometry(QtCore.QRect(120, 30, 171, 31))
        self.serial2_ent_2.setToolTip("")
        self.serial2_ent_2.setToolTipDuration(1)
        self.serial2_ent_2.setWhatsThis("")
        self.serial2_ent_2.setObjectName("serial2_ent_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("border: none;")
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(400, 30, 30, 30))
        self.label_11.setStyleSheet("border: none")
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("D:/PROGRAMMING/Images/Icons/icons8-calendar-48 (2).png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.label_53 = QtWidgets.QLabel(self.groupBox)
        self.label_53.setGeometry(QtCore.QRect(10, 70, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_53.setFont(font)
        self.label_53.setStyleSheet("border:none;\n"
"")
        self.label_53.setObjectName("label_53")
        self.ent_capacity_2 = QtWidgets.QComboBox(self.groupBox)
        self.ent_capacity_2.setGeometry(QtCore.QRect(120, 70, 171, 31))
        self.ent_capacity_2.setObjectName("ent_capacity_2")
        self.ent_capacity_2.addItem("")
        self.label_47 = QtWidgets.QLabel(self.groupBox)
        self.label_47.setGeometry(QtCore.QRect(10, 110, 98, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_47.setFont(font)
        self.label_47.setStyleSheet("border:none;\n"
"")
        self.label_47.setObjectName("label_47")
        self.loc_ent_2 = QtWidgets.QLineEdit(self.groupBox)
        self.loc_ent_2.setGeometry(QtCore.QRect(120, 110, 171, 31))
        self.loc_ent_2.setText("")
        self.loc_ent_2.setObjectName("loc_ent_2")
        self.effmaxlif = QtWidgets.QLineEdit(self.groupBox)
        self.effmaxlif.setGeometry(QtCore.QRect(440, 70, 71, 31))
        self.effmaxlif.setText("")
        self.effmaxlif.setObjectName("effmaxlif")
        self.label_52 = QtWidgets.QLabel(self.groupBox)
        self.label_52.setGeometry(QtCore.QRect(330, 70, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_52.setFont(font)
        self.label_52.setStyleSheet("border:none;\n"
"")
        self.label_52.setObjectName("label_52")
        self.label_64 = QtWidgets.QLabel(self.groupBox)
        self.label_64.setGeometry(QtCore.QRect(330, 110, 61, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_64.setFont(font)
        self.label_64.setStyleSheet("border:none;\n"
"")
        self.label_64.setObjectName("label_64")
        self.sum = QtWidgets.QComboBox(self.groupBox)
        self.sum.setGeometry(QtCore.QRect(440, 110, 110, 31))
        self.sum.setObjectName("sum")
        self.sum.addItem("")
        self.sum.addItem("")
        self.sum.addItem("")
        self.sum.addItem("")
        self.label_60 = QtWidgets.QLabel(self.groupBox)
        self.label_60.setGeometry(QtCore.QRect(530, 70, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_60.setFont(font)
        self.label_60.setStyleSheet("border:none;\n"
"")
        self.label_60.setObjectName("label_60")
        self.dte_test = QtWidgets.QDateEdit(self.groupBox)
        self.dte_test.setGeometry(QtCore.QRect(440, 30, 111, 31))
        self.dte_test.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2025, 12, 31), QtCore.QTime(23, 59, 59)))
        self.dte_test.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1950, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dte_test.setCalendarPopup(True)
        self.dte_test.setObjectName("dte_test")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.ftrradbtn.clicked.connect(self.get_test_link.showNormal)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Add test result"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inspection Results"))
        self.label_62.setText(_translate("MainWindow", "Rotor Visual Inspection"))
        self.label_63.setText(_translate("MainWindow", "Stator Boroscope Result"))
        self.label_50.setText(_translate("MainWindow", "Comment"))
        self.rtr.setItemText(0, _translate("MainWindow", "Select status"))
        self.rtr.setItemText(1, _translate("MainWindow", "Good"))
        self.rtr.setItemText(2, _translate("MainWindow", "Bent"))
        self.rtr.setItemText(3, _translate("MainWindow", "Base metal"))
        self.rtr.setItemText(4, _translate("MainWindow", "Pitted"))
        self.rtr.setItemText(5, _translate("MainWindow", "Broken"))
        self.rtr.setItemText(6, _translate("MainWindow", "Cracked"))
        self.str.setItemText(0, _translate("MainWindow", "Select status"))
        self.str.setItemText(1, _translate("MainWindow", "Good"))
        self.str.setItemText(2, _translate("MainWindow", "Swollen Elastomer"))
        self.str.setItemText(3, _translate("MainWindow", "Debonded Elastomer"))
        self.str.setItemText(4, _translate("MainWindow", "Missing Elastomer"))
        self.str.setItemText(5, _translate("MainWindow", "Splitted Elastomer"))
        self.label_65.setText(_translate("MainWindow", "Tag Bar Inspection"))
        self.tbar.setItemText(0, _translate("MainWindow", "Select status"))
        self.tbar.setItemText(1, _translate("MainWindow", "Good"))
        self.tbar.setItemText(2, _translate("MainWindow", "Worn"))
        self.addbtr_btn.setText(_translate("MainWindow", "      ADD TEST RESULT"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Attach Bench Test Report"))
        self.get_test_link.setText(_translate("MainWindow", " Attach report"))
        self.ftrradbtn.setText(_translate("MainWindow", "Factory Test Report"))
        self.btrradbtn.setText(_translate("MainWindow", "Bench Test Report"))
        self.groupBox.setTitle(_translate("MainWindow", "General Data"))
        self.label.setText(_translate("MainWindow", "Test Date"))
        self.serial2_ent_2.setStatusTip(_translate("MainWindow", "Make Sure Pump Serial In Database"))
        self.serial2_ent_2.setPlaceholderText(_translate("MainWindow", "Valid Serial From Pumps DataBase"))
        self.label_10.setText(_translate("MainWindow", "Serial Number"))
        self.label_53.setText(_translate("MainWindow", "Pump Model"))
        self.ent_capacity_2.setItemText(0, _translate("MainWindow", "Select pump capacity"))
        self.label_47.setText(_translate("MainWindow", "Pulled Out From"))
        self.label_52.setText(_translate("MainWindow", "∑ @ Max Lift"))
        self.label_64.setText(_translate("MainWindow", "Summary"))
        self.sum.setItemText(0, _translate("MainWindow", "Select condition"))
        self.sum.setItemText(1, _translate("MainWindow", "A"))
        self.sum.setItemText(2, _translate("MainWindow", "B"))
        self.sum.setItemText(3, _translate("MainWindow", "JUNK"))
        self.label_60.setText(_translate("MainWindow", "%"))
        self.dte_test.setDisplayFormat(_translate("MainWindow", "d-M-yyyy"))

