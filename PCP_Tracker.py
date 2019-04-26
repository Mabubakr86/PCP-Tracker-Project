# Import libraries:
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QDate, Qt
import pandas as pd
import sqlite3 as sql
from xlrd import *
from xlsxwriter import *
import smtplib
import time
# importing additional modules:
import Database           # simple Mnyodule to create data base
# import mail_list          # List of sender mail and receiving mails for security purpose
# importing Windows:
from log_in import *
from MainWindow import *
from Btr_window import *
from Calc_window import *
# from help import *

# Log-in Window:
"""
First Window which asks for user name & Password , then save user name as global variable to 
determine further allowable actions based on role (user or admin)
"""


class Login(QWidget, Ui_LOGIN):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        global user_name
        user_name = self.user_name_lin.text()
        user_password = self.user_pw_lin.text()
        try:
            if user_name== "admin" and user_password== "admin":
                self.window2 = FinalApp()
                self.close()
                self.window2.show() 
            else:
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("select * from Admins where USERNAME = '{}' and PASSWORD='{}'".format(user_name, user_password))
                check_admin = cur.fetchall()
                cur.execute("select * from Users where USERNAME = '{}' and PASSWORD='{}'".format(user_name, user_password))
                check_user = cur.fetchall()
                if len(check_admin) > 0 or len(check_user) > 0:
                    self.window2 = FinalApp()
                    self.close()
                    self.window2.show()         # Main Window would appear
                elif user_name == "" or user_password == "":
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Authentication Error")
                    self.msg.setText("Please enter username and password ")
                    self.msg.exec_()
                else: 
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Authentication Error")
                    self.msg.setText("Username or password might be incorrect")
                    self.msg.exec_()
                    self.user_name_lin.setText("")
                    self.user_pw_lin.setText("")
        except:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Authentication Error")
            self.msg.setText("Username or password might be incorrect")
            self.msg.exec_()
            self.user_name_lin.setText("")
            self.user_pw_lin.setText("")


# Main Window:
"""
Main Window of program which include all options 
"""


class FinalApp(QMainWindow, Ui_QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)         # to be removed after adjusting ui
        self.tabWidget.tabBar().setVisible(False)
        self.db = Database.Database()                 # Create sql lite database if not existing
        self.load_brandcombos()                       # load  brand comboboxes
        self.load_staticmodelcombos()                 # load static model comboboxes which arenot linked to brand changes
        self.load_staticelastomercombos()             # load static elastomer comboboxes which arenot linked to brand changes
        self.ent_brand.currentTextChanged.connect(self.loadfirstlinkedcombo)
        self.ent_brand_3.currentTextChanged.connect(self.loadsecondlinkedcombo)
        self.comboBox_8.currentTextChanged.connect(self.loadthirdlinkedcombo)
        self.comboBox_7.currentTextChanged.connect(self.loadfourthlinkedcombo)
        self.nav_bar()                                  # Navigate between tabs
        self.actions()                                  # Handle main actions (add pumps, add record,...etc)

############ Configuration panel setting ######################
        self.groupBox.hide()
        self.hideconfig.clicked.connect(self.hideconfigpanel)
        self.manageusers.clicked.connect(self.showuserpanel)
        self.managepumps.clicked.connect(self.showspecspanel)
        self.managelocations.clicked.connect(self.showwellpanel)



        self.comboBox_12.currentTextChanged.connect(self.loadwelltoberemoved)   ### load Wells combobox in delete well section ###
        #self.wellnumber_4.currentTextChanged.connect(self.activatedeletingwell)      ### Activate delete button in delete well section ###
        self.loadfieldtoberemoved()             ### load Fields comboboxes in delete field section ###
        self.loadfieldtoaddandremovewell()            ### load Fields comboboxes in add and delete well section ###
       # self.remc_btn_8.setEnabled(False)     ### Well  combobox in delete well section ###

    ###################################################################################
    ##### loading ID combboxes in editing - deleting events #####
        self.serial_del_3.textChanged.connect(self.loadIDtoberemoved)
        self.serial_del_2.textChanged.connect(self.loadIDtobeedited)

    ###################################################################################
    ##### Activating and loading combboxes in adding - editing - searching events #####
        self.field.setEnabled(False)
        self.wellnumber.setEnabled(False)
        self.loc_ent.currentTextChanged.connect(self.setaddeventcombostatus)
        self.loc_ent.currentTextChanged.connect(self.loadaddeventscombos)
        self.field.currentTextChanged.connect(self.loadWellscombos)

        self.field_2.setEnabled(False)
        self.wellnumber_2.setEnabled(False)
        self.loc_ent_2.currentTextChanged.connect(self.setediteventcombostatus)
        self.loc_ent_2.currentTextChanged.connect(self.loadediteventscombos)
        self.field_2.currentTextChanged.connect(self.loadWellsineditcombos)

        self.field_3.setEnabled(False)
        self.wellnumber_3.setEnabled(False)
        self.loc_ent_3.currentTextChanged.connect(self.setsearcheventcombostatus)
        self.loc_ent_3.currentTextChanged.connect(self.loadsearcheventscombos)
        self.field_3.currentTextChanged.connect(self.loadWellsinsearchcombos)

#########  To activate export to Excel buttons in search, view and history tabs ##########
        self.EXPORTTOEX1.setEnabled(False)
        self.label_23.textChanged.connect(self.exportsearchbuttonstatus)
        self.EXPORTTOEX2_2.setEnabled(False)
        self.label_47.textChanged.connect(self.exporthistorybuttonstatus)
        self.EXPORTTOEX2.setEnabled(False)     
        self.res_view.textChanged.connect(self.exportviewbuttonstatus)

########## to activate view report pdf button #################
        self.pushButton_21.setEnabled(False)
        # self.label_79.textChanged.connect(self.viewpdfbuttonstatus)

#########   set date calendars on live date ##################
        self.date_ent.setDate(QDate.currentDate())
        self.date_ent_2.setDate(QDate.currentDate())

######## set auto completers for SN , admins , users ##################
        self.autocompleteserialnumbers()
        self.autocompleteadmins()
        self.autocompleteusers()


####### special charachter detector in SN line edits signals   ###########
        self.add_serial.textChanged.connect(self.specialcharacterdetect)
        self.serial_del_recall.textChanged.connect(self.specialcharacterdetect)
        self.serial_del.textChanged.connect(self.specialcharacterdetect)
        self.serial2_ent.textChanged.connect(self.specialcharacterdetect)
        self.serial_del_2.textChanged.connect(self.specialcharacterdetect)
        self.serial_del_3.textChanged.connect(self.specialcharacterdetect)
        self.pserial_history.textChanged.connect(self.specialcharacterdetect)
        self.serial2_ent_3.textChanged.connect(self.specialcharacterdetect)

####### special charachter detector in adding new fields signals   ###########
        self.capacity_conf_10.textChanged.connect(self.autodetectslashesinaddfield)

####### Non digit characters detector in RL line edits signals   ###########
        self.oper_ent.textChanged.connect(self.nondigitdetector)
        self.oper_ent_2.textChanged.connect(self.nondigitdetector)
        self.runlife_search_2.textChanged.connect(self.nondigitdetector)
        self.label_60.hide()
        self.label_67.hide() 
        self.label_106.hide()   

##########  auto fill location combos in add/update events #################
        self.event_ent.currentTextChanged.connect(self.autofilllocationcombos)
        self.event_ent_3.currentTextChanged.connect(self.autofilllocationcombos)


######### Enable searching options with checking radiobutton option ######
        self.serial_search.setEnabled(False)
        self.comboBox_15.setEnabled(False)
        self.loc_ent_3.setEnabled(False)
        self.event_ent_2.setEnabled(False)
        self.cond_ent_2.setEnabled(False)
        self.comboBox_4.setEnabled(False)
        self.comboBox_5.setEnabled(False)
        self.serial_radio.clicked.connect(self.settypeserialstatus)
        self.runlife_radio_2.clicked.connect(self.settypeserialstatus)
        self.location_radio_5.clicked.connect(self.settypeserialstatus)
        self.event_radio_7.clicked.connect(self.settypeserialstatus)
        self.condition_radio_6.clicked.connect(self.settypeserialstatus)
        self.condbotton.clicked.connect(self.settypeserialstatus)
        self.capbotton.clicked.connect(self.settypeserialstatus)
        self.radioButton_3.clicked.connect(self.settypeserialstatus)

######### Enable view options with checking radiobutton option ######
        self.ent_brand_2.setEnabled(False)
        self.ent_elastomer_3.setEnabled(False)
        self.ent_capacity_3.setEnabled(False)
        self.brand_radio_6.clicked.connect(self.setviewoptionsstatus)
        self.elas_radio.clicked.connect(self.setviewoptionsstatus)
        self.capacity_radio7.clicked.connect(self.setviewoptionsstatus)
        self.all_radio_7.clicked.connect(self.setviewoptionsstatus)

        self.pushButton_16.setDown(True)
        self.pushButton_17.setDown(True)
        self.pushButton_18.setDown(True)
        self.pushButton_20.setDown(True)
        self.pushButton_19.setDown(True)
        self.pushButton_15.setDown(True)
        self.pushButton_13.setDown(True)
        self.pushButton_14.setDown(True)

####### Setting Receipent mail List line edits #########
        self.maillist.hide()
        self.maillist_2.hide()
       
########## to normal set space detectors in email receiver list as hidden ##########       
        self.checkBox_2.clicked.connect(self.setmailliststatus)
        self.checkBox_4.clicked.connect(self.setmailliststatus)
        self.maillist.textChanged.connect(self.setspacewarners)
        self.maillist_2.textChanged.connect(self.setspacewarners)
        self.label_109.hide()
        self.label_110.hide()

    def setspacewarners (self):
        space1 = [self.maillist.text(),self.maillist_2.text()]
        space2 = [self.label_109,self.label_110]
        zipped = zip (space1,space2)
        for x,y in zipped:
            if x.count(" ")==0:
                y.hide()
            elif x.count(" ")!=0:
                y.show()
                y.setStyleSheet("color:rgb(255, 0, 0)")
        
    def setmailliststatus(self):
        r = [self.checkBox_2,self.checkBox_4]
        k = [self.maillist,self.maillist_2]
        j = [self.label_109,self.label_110]
        zipped = zip (r,k,j)
        for w,e,f in zipped:
            if w.isChecked():
                e.show()
            else:
                e.hide()
                f.hide()   

    def setviewoptionsstatus (self):
        if self.brand_radio_6.isChecked():
            self.ent_brand_2.setEnabled(True)
            self.ent_elastomer_3.setEnabled(False)
            self.ent_capacity_3.setEnabled(False)
        elif self.elas_radio.isChecked():
            self.ent_brand_2.setEnabled(False)
            self.ent_elastomer_3.setEnabled(True)
            self.ent_capacity_3.setEnabled(False)
        elif self.capacity_radio7.isChecked():
            self.ent_brand_2.setEnabled(False)
            self.ent_elastomer_3.setEnabled(False)
            self.ent_capacity_3.setEnabled(True)
        elif self.all_radio_7.isChecked():
            self.ent_brand_2.setEnabled(False)
            self.ent_elastomer_3.setEnabled(False)
            self.ent_capacity_3.setEnabled(False)


    def settypeserialstatus (self):
        if self.serial_radio.isChecked():
            self.serial_search.setEnabled(True)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)
        elif self.runlife_radio_2.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(True)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)
        elif self.location_radio_5.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(True)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)        
        elif self.event_radio_7.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(True)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)    
        elif self.condition_radio_6.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(True)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)        
        elif self.condbotton.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(True)
            self.comboBox_5.setEnabled(False)        
        elif self.capbotton.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(True) 
        elif self.radioButton_3.isChecked():
            self.serial_search.setEnabled(False)
            self.comboBox_15.setEnabled(False)
            self.loc_ent_3.setEnabled(False)
            self.event_ent_2.setEnabled(False)
            self.cond_ent_2.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False) 


    def specialcharacterdetect (self):
        LE1 = self.add_serial.text()
        LE2 =self.serial_del_recall.text()
        LE3 = self.serial_del.text()
        LE4 = self.serial2_ent.text()
        LE5 = self.serial_del_2.text()
        LE6 = self.serial_del_3.text()
        LE7 = self.pserial_history.text()
        LE8 = self.serial2_ent_3.text()
        lineedits= [LE1,LE2,LE3,LE4,LE5,LE6,LE7,LE8]
        showcomments = [self.label_54,self.label_92,self.label_96,self.label_51,self.label_71,self.label_105,self.label_108,self.label_107]
        zipped = zip(lineedits, showcomments)
        for a,b in zipped:
            if a =="":
                b.hide()            
            else:
                if a.count('^') !=0 or a.count('%') !=0 or a.count(' ') !=0 or  a.count('/') !=0 or a.count (',')!=0 or a.count ('+')!=0 or a.count ('!')!=0 or a.count ('@')!=0 or a.count ('#')!=0 or a.count ('$')!=0 or a.count ('*')!=0 or a.count ('(')!=0 or a.count (')')!=0 or a.count ('>')!=0 or a.count ('<')!=0 or a.count ('?')!=0:
                    b.show()
                    b.setText("space and other\nspecial characters\nnot allowed")
                    b.setStyleSheet("color:rgb(255, 0, 0)")
                else:
                    b.show()
                    b.setText("Follow serial number\n format as:\nStator-Rotor")
                    b.setStyleSheet("color:rgb(0, 0, 0)")

    def nondigitdetector (self):
        RLD1 = self.oper_ent.text()
        RLD2 = self.oper_ent_2.text()
        RLD3 = self.runlife_search_2.text()
        digitspaces = [RLD1,RLD2,RLD3]
        showcomment = [self.label_60,self.label_67,self.label_106]
        zipped = zip(digitspaces, showcomment)
        for ab,cd in zipped:
            if ab == "":
                cd.hide()
            elif ab.isdigit()!=True :
                cd.show()
            else:
                cd.hide()

######## auto complete serial number line edits #########
    def autocompleteserialnumbers (self):
        conn = sql.connect("PCP_Database")
        df_ser = pd.read_sql('select SERIAL from Pumps', con=conn) 
        serlist = []
        for i in list(df_ser['SERIAL']):
            x= str(i)
            serlist.append(x)
        availableserials = QCompleter (serlist)
        self.serial_del_recall.setCompleter(availableserials)
        self.serial_del.setCompleter(availableserials)
        self.serial2_ent.setCompleter(availableserials)
        self.serial_del_2.setCompleter(availableserials)   
        self.serial_del_3.setCompleter(availableserials)   
        self.serial_search.setCompleter(availableserials)
        self.pserial_history.setCompleter(availableserials)
        self.serial2_ent_3.setCompleter(availableserials)


######## auto complete delete user line edit #########
    def autocompleteusers (self):
        conn = sql.connect("PCP_Database")
        df_user = pd.read_sql('select USERNAME from Users', con=conn) 
        userlist = []
        for j in list(df_user['USERNAME']):
            userlist.append(j)
        availableusers = QCompleter (userlist)
        self.del_user_text.setCompleter(availableusers)


######## auto complete delete admin line edit #########
    def autocompleteadmins (self):
        conn = sql.connect("PCP_Database")
        df_admin = pd.read_sql('select USERNAME from Admins', con=conn) 
        adminlist = []
        for k in list(df_admin['USERNAME']):
            adminlist.append(k)
        availableadmins = QCompleter (adminlist)
        self.del_admin_text.setCompleter(availableadmins)

############# auto load location combos in add event page ########
    def autofilllocationcombos (self):
        events = [self.event_ent.currentText(),self.event_ent_3.currentText()]
        locations = [self.loc_ent,self.loc_ent_2]
        zipped = zip (events,locations)
        for r,s in zipped:
            if r=="Acquired":
                newitem="Warehouse"
            elif r=="Received from bench testing" :
                newitem="Warehouse"
            elif r=="Sent to pumpshop":
                newitem="Pumpshop"
            elif r=="RIH" or r=="POOH":
                newitem="Well location"
            elif r=="Sent for bench testing":
                newitem="Test bench"
            elif r=="Select event":
                newitem="Select location"
            s.clear()
            s.addItem(newitem)
    ##########
    def setaddeventcombostatus(self):    
        if self.loc_ent.currentText() == "Test bench":
            self.field.setEnabled(True)
            self.wellnumber.setEnabled(False)

        elif self.loc_ent.currentText() == "Well location":
            self.field.setEnabled(True)
            self.wellnumber.setEnabled(True)

        else:
            self.field.setEnabled(False)
            self.wellnumber.setEnabled(False)           

    def loadaddeventscombos (self):
        conn = sql.connect("PCP_Database")
        df_fields = pd.read_sql('select * from Fields', con=conn)
        df_benchtestcompanies = pd.read_sql('select * from brand_lib', con=conn)
        if self.loc_ent.currentText()=="Well location":
            self.field.clear()
            self.field.addItems(df_fields['Field'])
        elif self.loc_ent.currentText()=="Test bench":
            self.field.clear()
            self.field.addItems(df_benchtestcompanies['brand'])
        else:
            self.field.clear()


    def loadWellscombos (self):
        conn = sql.connect("PCP_Database")
        df_wells = pd.read_sql('select Wells from Fields_and_Wells where Fields ="{}" order by Wells asc'.format(self.field.currentText()) , con=conn)
        self.wellnumber.clear()
        self.wellnumber.addItems(df_wells['Wells'])

    ############

    def setediteventcombostatus(self):    
        if self.loc_ent_2.currentText() == "Test bench":
            self.field_2.setEnabled(True)
            self.wellnumber_2.setEnabled(False)

        elif self.loc_ent_2.currentText() == "Well location":
            self.field_2.setEnabled(True)
            self.wellnumber_2.setEnabled(True)

        else:
            self.field_2.setEnabled(False)
            self.wellnumber_2.setEnabled(False) 

    def loadediteventscombos (self):
        conn = sql.connect("PCP_Database")
        df_fields = pd.read_sql('select * from Fields', con=conn)
        df_benchtestcompanies = pd.read_sql('select * from brand_lib', con=conn)
        if self.loc_ent_2.currentText()=="Well location":
            self.field_2.clear()
            self.field_2.addItems(df_fields['Field'])
        elif self.loc_ent_2.currentText()=="Test bench":
            self.field_2.clear()
            self.field_2.addItems(df_benchtestcompanies['brand'])
        else:
            self.field_2.clear()

    def loadWellsineditcombos (self):
        conn = sql.connect("PCP_Database")
        df_wells = pd.read_sql('select Wells from Fields_and_Wells where Fields ="{}" order by Wells asc'.format(self.field_2.currentText()) , con=conn)
        self.wellnumber_2.clear()
        self.wellnumber_2.addItems(df_wells['Wells'])

   ################################

    def setsearcheventcombostatus(self):    
        if self.loc_ent_3.currentText() == "Test bench":
            self.field_3.setEnabled(True)
            self.wellnumber_3.setEnabled(False)

        elif self.loc_ent_3.currentText() == "Well location":
            self.field_3.setEnabled(True)
            self.wellnumber_3.setEnabled(True)

        else:
            self.field_3.setEnabled(False)
            self.wellnumber_3.setEnabled(False) 

    def loadsearcheventscombos(self):  
        conn = sql.connect("PCP_Database")
        df_fields = pd.read_sql('select * from Fields', con=conn)
        df_benchtestcompanies = pd.read_sql('select * from brand_lib', con=conn)
        if self.loc_ent_3.currentText()=="Well location":
            self.field_3.clear()
            self.field_3.addItems(df_fields['Field'])
        elif self.loc_ent_3.currentText()=="Test bench":
            self.field_3.clear()
            self.field_3.addItems(df_benchtestcompanies['brand'])
        else:
            self.field_3.clear()

    def loadWellsinsearchcombos (self):
        conn = sql.connect("PCP_Database")
        df_wells = pd.read_sql('select Wells from Fields_and_Wells where Fields ="{}" order by Wells asc'.format(self.field_3.currentText()) , con=conn)
        self.wellnumber_3.clear()
        self.wellnumber_3.addItems(df_wells['Wells'])

    #####################
    def load_brandcombos(self):
        conn = sql.connect("PCP_Database")
        df_brand = pd.read_sql('select * from brand_lib', con=conn)
        self.ent_brand.clear()
        self.ent_brand.addItems(df_brand['brand'])
        self.ent_brand_2.clear()
        self.ent_brand_2.addItems(df_brand['brand'])
        self.ent_brand_3.clear()
        self.ent_brand_3.addItems(df_brand['brand'])
        self.comboBox_2.clear()
        self.comboBox_2.addItems(df_brand['brand'])
        self.comboBox_6.clear()
        self.comboBox_6.addItems(df_brand['brand'])
        self.comboBox_7.clear()
        self.comboBox_7.addItems(df_brand['brand'])
        self.comboBox_8.clear()
        self.comboBox_8.addItems(df_brand['brand'])
        self.comboBox_9.clear()
        self.comboBox_9.addItems(df_brand['brand'])

    def load_staticmodelcombos(self):
        conn = sql.connect("PCP_Database")
        df_capacity = pd.read_sql('select pump_capacity from capacity_lib', con=conn)
        self.ent_capacity_3.clear()
        self.ent_capacity_3.addItems(df_capacity['pump_capacity'])
        self.comboBox_5.clear()
        self.comboBox_5.addItems(df_capacity['pump_capacity'])

    def load_staticelastomercombos(self):
        conn = sql.connect("PCP_Database")
        df_elastomer = pd.read_sql('select elastomer from elastomer_lib ', con=conn)
        x = set(list(df_elastomer['elastomer']))
        self.ent_elastomer_3.clear()
        self.ent_elastomer_3.addItems(x)
####
    def loadIDtobeedited (self):
        conn = sql.connect("PCP_Database")
        df_ID = pd.read_sql('select ID from Records where SERIAL_NO ="{}" '.format(self.serial_del_2.text()), con=conn) 
        IDlist = []
        for i in list(df_ID['ID']):
            x= str(i)
            IDlist.append(x)
        self.recordid.clear()
        self.recordid.addItems(IDlist)
####
    def loadIDtoberemoved (self):
        conn = sql.connect("PCP_Database")
        df_ID = pd.read_sql('select ID from Records where SERIAL_NO ="{}" '.format(self.serial_del_3.text()), con=conn)        
        IDlist = []
        for i in list(df_ID['ID']):
            x= str(i)
            IDlist.append(x)
        self.recordid_2.clear()
        self.recordid_2.addItems(IDlist)

    ##### add specific items to elatomer and model combobox in add pumps #####   
    def loadfirstlinkedcombo(self):
        conn = sql.connect("PCP_Database")
        df_elastomer = pd.read_sql('select elastomer from elastomer_lib where brand="{}"'.format(self.ent_brand.currentText()), con=conn)
        df_capacity = pd.read_sql('select pump_capacity from capacity_lib where brand="{}"'.format(self.ent_brand.currentText()), con=conn)
        self.ent_elastomer.clear()
        self.ent_elastomer.addItems(df_elastomer['elastomer'])
        self.ent_capacity.clear()
        self.ent_capacity.addItems(df_capacity['pump_capacity'])

    ##### add specific items to elatomer and model combobox in edit pumps #####   
    def loadsecondlinkedcombo (self):
        conn = sql.connect("PCP_Database")
        df_elastomer = pd.read_sql('select elastomer from elastomer_lib where brand="{}"'.format(self.ent_brand_3.currentText()), con=conn)
        df_capacity = pd.read_sql('select pump_capacity from capacity_lib where brand="{}"'.format(self.ent_brand_3.currentText()), con=conn)
        self.ent_elastomer_2.clear()
        self.ent_elastomer_2.addItems(df_elastomer['elastomer'])
        self.ent_capacity_2.clear()
        self.ent_capacity_2.addItems(df_capacity['pump_capacity'])

    ##### add specific items to elatomer combobox in delete elastomers #####   
    def loadthirdlinkedcombo (self):
        conn = sql.connect("PCP_Database")
        df_elastomer = pd.read_sql('select elastomer from elastomer_lib where brand="{}"'.format(self.comboBox_8.currentText()), con=conn)
        self.comboBox_3.clear()
        self.comboBox_3.addItems(df_elastomer['elastomer'])

    ##### add specific items to model combobox in delete capacities #####   
    def loadfourthlinkedcombo (self):
        conn = sql.connect("PCP_Database")
        df_capacity = pd.read_sql('select pump_capacity from capacity_lib where brand="{}"'.format(self.comboBox_7.currentText()), con=conn)
        self.comboBox.clear()
        self.comboBox.addItems(df_capacity['pump_capacity'])

    ##### add items to fields and wells combos in configuration ######
    def loadfieldtoberemoved (self):
        conn = sql.connect("PCP_Database")
        df_fields = pd.read_sql('select * from Fields', con=conn)
        self.comboBox_10.clear()
        self.comboBox_10.addItems(df_fields['Field'])

    def loadfieldtoaddandremovewell (self):
        conn = sql.connect("PCP_Database")
        df_fields = pd.read_sql('select * from Fields', con=conn)
        self.comboBox_11.clear()
        self.comboBox_12.clear()
        self.comboBox_11.addItems(df_fields['Field'])
        self.comboBox_12.addItems(df_fields['Field'])


    ##### add items to fields and wells combos in configuration ######
    def loadwelltoberemoved (self):
        conn = sql.connect("PCP_Database")
        df_wells = pd.read_sql('select Wells from Fields_and_Wells where Fields ="{}" order by Wells asc'.format(self.comboBox_12.currentText()) , con=conn)
        self.wellnumber_4.clear()
        self.wellnumber_4.addItems(df_wells['Wells'])

    
    
    # def activatedeletingwell (self):
    #     if self.wellnumber_4.currentText() != "Well No." and self.wellnumber_4.currentText() != "" :
    #         self.remc_btn_8.setEnabled(True)

    def nav_bar(self):
        self.pushButton_16.clicked.connect(self.go_pumps)
        self.pushButton_36.clicked.connect(self.go_pumps)
        self.pushButton_17.clicked.connect(self.go_records)
        self.pushButton_32.clicked.connect(self.go_records)
        self.pushButton_18.clicked.connect(self.go_search)
        self.pushButton_39.clicked.connect(self.go_search)
        self.pushButton_20.clicked.connect(self.go_view)
        self.pushButton_35.clicked.connect(self.go_view)
        self.pushButton_19.clicked.connect(self.go_hist)
        self.pushButton_37.clicked.connect(self.go_hist)
        self.pushButton_15.clicked.connect(self.go_stat)
        self.pushButton_38.clicked.connect(self.go_stat)
        self.pushButton_13.clicked.connect(self.go_bench)
        self.pushButton_34.clicked.connect(self.go_bench)
        self.pushButton_14.clicked.connect(self.go_config)
        self.pushButton_33.clicked.connect(self.go_config)

    def go_pumps(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
        check_admin = cur.fetchall()
        if len(check_admin) > 0 or user_name == "admin":
            self.stackedWidget.setCurrentIndex(1)
            self.tabWidget.setCurrentIndex(0)
            self.pushButton_16.setDown(True)
            self.pushButton_17.setDown(False)
            self.pushButton_18.setDown(False)
            self.pushButton_20.setDown(False)
            self.pushButton_19.setDown(False)
            self.pushButton_15.setDown(False)
            self.pushButton_13.setDown(False)
            self.pushButton_14.setDown(False)
        else:
            QMessageBox.information(self, "Sorry {}".format(user_name),
                                    'For database security, pumps tab can be only accessed by admins')

    def go_records(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
        check_admin = cur.fetchall()
        if len(check_admin) > 0 or user_name == "admin":
            self.stackedWidget.setCurrentIndex(1)
            self.tabWidget.setCurrentIndex(1)
            self.pushButton_16.setDown(False)
            self.pushButton_17.setDown(True)
            self.pushButton_18.setDown(False)
            self.pushButton_20.setDown(False)
            self.pushButton_19.setDown(False)
            self.pushButton_15.setDown(False)
            self.pushButton_13.setDown(False)
            self.pushButton_14.setDown(False)
        else:
            QMessageBox.information(self, "Sorry {}".format(user_name),
                                    'For database security, records tab can be only accessed by admins')

    def go_search(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(2)
        self.pushButton_16.setDown(False)
        self.pushButton_17.setDown(False)
        self.pushButton_18.setDown(True)
        self.pushButton_20.setDown(False)
        self.pushButton_19.setDown(False)
        self.pushButton_15.setDown(False)
        self.pushButton_13.setDown(False)
        self.pushButton_14.setDown(False)

    def go_view(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(3)
        self.gotopumupdt.clicked.connect(self.go_update_pump)
        self.gotopumupdt_2.clicked.connect(self.go_delete_pump)
        self.pushButton_16.setDown(False)
        self.pushButton_17.setDown(False)
        self.pushButton_18.setDown(False)
        self.pushButton_20.setDown(True)
        self.pushButton_19.setDown(False)
        self.pushButton_15.setDown(False)
        self.pushButton_13.setDown(False)
        self.pushButton_14.setDown(False)

    def go_hist(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(4)
        self.gotorecupdt.clicked.connect(self.go_update_record)
        self.gotopumupdt_3.clicked.connect(self.go_delete_record)
        self.pushButton_16.setDown(False)
        self.pushButton_17.setDown(False)
        self.pushButton_18.setDown(False)
        self.pushButton_20.setDown(False)
        self.pushButton_19.setDown(True)
        self.pushButton_15.setDown(False)
        self.pushButton_13.setDown(False)
        self.pushButton_14.setDown(False)

    def go_stat(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(5)
        self.pushButton_16.setDown(False)
        self.pushButton_17.setDown(False)
        self.pushButton_18.setDown(False)
        self.pushButton_20.setDown(False)
        self.pushButton_19.setDown(False)
        self.pushButton_15.setDown(True)
        self.pushButton_13.setDown(False)
        self.pushButton_14.setDown(False)

    def go_bench(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(6)
        self.pushButton_16.setDown(False)
        self.pushButton_17.setDown(False)
        self.pushButton_18.setDown(False)
        self.pushButton_20.setDown(False)
        self.pushButton_19.setDown(False)
        self.pushButton_15.setDown(False)
        self.pushButton_13.setDown(True)
        self.pushButton_14.setDown(False)

    def go_config(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
        check_admin = cur.fetchall()
        if len(check_admin) > 0 or user_name == "admin":
            self.stackedWidget.setCurrentIndex(1)
            self.tabWidget.setCurrentIndex(7)
            self.pushButton_16.setDown(False)
            self.pushButton_17.setDown(False)
            self.pushButton_18.setDown(False)
            self.pushButton_20.setDown(False)
            self.pushButton_19.setDown(False)
            self.pushButton_15.setDown(False)
            self.pushButton_13.setDown(False)
            self.pushButton_14.setDown(True)
        else:
            QMessageBox.information(self, "Sorry {}".format(user_name),
                                    'For database security, configuration tab can be only accessed by admins')

    def actions(self):
        # Pump Tab Actions:
        self.addpump_btn.clicked.connect(self.add_pump)
        self.delpump_btn.clicked.connect(self.del_pump)
        self.updaterec_btn_2.clicked.connect(self.update_pump)
        self.updaterec_btn_5.clicked.connect(self.recallpumpspecs)
        # Record Tab Actions:
        self.calu_btn_2.clicked.connect(self.go_abr)  # show bench test window
        self.calu_btn.clicked.connect(self.go_cal)  # show calculator window
        # self.help_btn.clicked.connect(self.go_help)  # show help window
        self.addrec_btn.clicked.connect(self.add_record)
        self.delrec_btn.clicked.connect(self.del_record)
        self.updaterec_btn.clicked.connect(self.update_record)
        self.updaterec_btn_3.clicked.connect(self.recalleventofthisID)
        # Search Actions:       
        self.search_btn.clicked.connect(self.find_pump)
        self.search_btn_3.clicked.connect(self.search_pumps)
        self.stock_btn.clicked.connect(self.show_stock)
        self.EXPORTTOEX1.clicked.connect(self.export_search)
        # View Actions:
        self.load_btn.clicked.connect(self.view_pumps)
        self.view_table.cellClicked.connect(self.get_from_view_table)
        self.EXPORTTOEX2.clicked.connect(self.export_view)
        # History Actions
        self.show_hist.clicked.connect(self.show_history)
        self.table_history.cellClicked.connect(self.get_from_his_table)
        self.EXPORTTOEX2_2.clicked.connect(self.export_history)
        # Statistics Actions:
        self.plot_btn_3.clicked.connect(self.plot)
        # Test Results Actions:
        self.loadbtr_btn.clicked.connect(self.load_tests)
        self.showbtrres_btn.clicked.connect(self.view_test_result)
        self.pushButton_21.clicked.connect(self.view_test_report)
        self.remc_btn_2.clicked.connect(self.delete_test_result)
        self.btr_search.cellClicked.connect(self.get_from_btrsearch_table)
        # Configuration Actions:
        self.addc_btn_4.clicked.connect(self.add_admin)
        self.remc_btn_4.clicked.connect(self.del_admin)
        self.addc_btn_9.clicked.connect(self.add_user)
        self.remc_btn_9.clicked.connect(self.del_user)
        self.addb_btn.clicked.connect(self.add_brand)
        self.remb_btn.clicked.connect(self.remove_brand)
        self.addc_btn.clicked.connect(self.add_capacity)
        self.remc_btn.clicked.connect(self.remove_capacity)
        self.adde_btn.clicked.connect(self.add_elastomer)
        self.reme_btn.clicked.connect(self.remove_elastomer)
        self.addc_btn_7.clicked.connect(self.addfield)
        self.remc_btn_7.clicked.connect(self.delfield)
        self.addc_btn_8.clicked.connect(self.addwell)
        self.remc_btn_8.clicked.connect(self.delwell)


    def autodetectslashesinaddfield (self):
        a=self.capacity_conf_10.text()
        if a.count('-') != 0:
            self.label_42.show()
            self.label_42.setText("slash (-) is not allowed")
            self.label_42.setStyleSheet("color:rgb(255, 0, 0)")             
        else:
            self.label_42.hide()
    
    def addfield (self):
        try:
            if self.capacity_conf_10.text() !='':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("select * from Fields where Field = '{}'".format(self.capacity_conf_10.text()))
                c= cur.fetchall()
                if self.capacity_conf_10.text().count('-') == 0:
                    if len (c) == 0 :
                        cur.execute("insert into Fields (Field) values  ('{}')".format(self.capacity_conf_10.text()))
                        cur.execute("insert into Fields_and_Wells (Fields,Wells) values  ('{}','')".format(self.capacity_conf_10.text()))
                        self.capacity_conf_10.clear()
                        conn.commit()
                        self.loadfieldtoberemoved()
                        self.loadfieldtoaddandremovewell()
                        self.statusBar().showMessage('New field has been successfully added', 5000)
                    else:
                        QMessageBox.information(self, "Entry error", '[{}] already exists in fields list'.format(self.capacity_conf_10.text()))
                else:
                    QMessageBox.information(self, "Entry error", 'slash (-) is not allowed in field name')

            else:
                QMessageBox.information(self, "Error", 'Enter field to be added')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')


    def delfield (self):
        try:
            if self.comboBox_10.currentText() !='Select field':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("delete from Fields where Field ='{}'".format(self.comboBox_10.currentText()))
                cur.execute("delete from Fields_and_Wells where Fields ='{}'".format(self.comboBox_10.currentText()))
                check = QMessageBox.warning(self, 'Confirm delete field',
                                                " [{}] and all its wells  will be permanently deleted,"
                                                " Do you like to continue?".format(self.comboBox_10.currentText()),
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if check == QMessageBox.Yes:
                    conn.commit()
                    self.statusBar().showMessage('[{}] has been deleted from fields list'.format(self.comboBox_10.currentText()), 5000)
                    self.comboBox_10.clear()
                    self.loadfieldtoberemoved()
                    self.loadfieldtoaddandremovewell()
                else:
                    conn.close()
            else:
                QMessageBox.information(self, "Error", 'Select field to be deleted')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def addwell(self):
        try:
            if self.comboBox_11.currentText() !='Select field' and self.capacity_conf_11.text() !='':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("select * from Fields_and_Wells where Fields = '{}' and Wells ='{}' ".format(self.comboBox_11.currentText(),self.capacity_conf_11.text()))
                c= cur.fetchall()
                if len (c) == 0 :
                    cur.execute("insert into Fields_and_Wells (Fields,Wells) values  ('{}','{}')".format(self.comboBox_11.currentText(),self.capacity_conf_11.text()))
                    conn.commit()
                    self.capacity_conf_11.clear()
                    self.comboBox_11.setCurrentText("Select field")
                    self.statusBar().showMessage('New well has been successfully added', 5000)
                else:
                    QMessageBox.information(self, "Entry error", '[{}] already exists in [{}] wells list'.format(self.capacity_conf_11.text(),self.comboBox_11.currentText()))
            else:
                QMessageBox.information(self, "Error", 'Select field and well to be added')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def delwell (self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.comboBox_12.currentText() !='Select field':
                if self.wellnumber_4.currentText() != '':
                    cur.execute("Delete from Fields_and_Wells where Fields = '{}' and Wells ='{}'".format(self.comboBox_12.currentText(),self.wellnumber_4.currentText()))
                    conn.commit()
                    self.statusBar().showMessage('[{}] has been deleted from [{}] wells list'.format(self.wellnumber_4.currentText(),self.comboBox_12.currentText()), 5000)
                    self.comboBox_12.clear()
                    self.loadfieldtoaddandremovewell()
                    self.loadwelltoberemoved()

                else:
                    conn.close()
            else:
                QMessageBox.information(self, "Error", 'Select field and specify well to be deleted')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')



    def add_pump(self):
        try:
            if self.add_serial.text() != '':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("select * from Pumps where SERIAL = '{}'".format(self.add_serial.text()))
                cap = self.ent_capacity.currentText()
                brand = self.ent_brand.currentText()
                elast = self.ent_elastomer.currentText()
                comm = self.ent_comment.toPlainText()
                k = cur.fetchall()
                if len(k) == 0:
                    if cap != '' and brand != 'Select brand' and elast != '':
                        cur.execute("insert into Pumps (SERIAL,CAPACITY,BRAND,ELASTOMER,COMMENT) values " \
                               "('{}','{}','{}','{}','{}')".format(self.add_serial.text(), cap, brand, elast, comm))
                        check = QMessageBox.question(self, 'Data Confirmation', "Pump will be added to database "
                                                                                ".Do you like to continue?",
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if check == QMessageBox.Yes:
                            conn.commit()
                            self.statusBar().showMessage('New pump has been successfully added', 5000)
                            time.sleep(1)
                            QMessageBox.information(self, "Add Record ", 'Make sure to add acquire record for pump')
                            self.add_serial.clear()
                            self.ent_brand.setCurrentIndex(0)
                            self.ent_capacity.setCurrentIndex(0)
                            self.ent_elastomer.setCurrentIndex(0)
                            self.ent_comment.setText("")
                            self.tabWidget.setCurrentIndex(1)
                            self.serial2_ent.setText('{}'.format(self.add_serial.text()))
                            self.add_serial.clear()
                            self.event_ent.setCurrentIndex(0)
                            self.cond_ent.setCurrentIndex(0)
                            self.oper_ent.setText(str(0))
                            self.autocompleteserialnumbers()

                        else:
                            conn.close()
                            self.add_serial.clear()
                            self.ent_brand.setCurrentIndex(0)
                            self.ent_capacity.setCurrentIndex(0)
                            self.ent_elastomer.setCurrentIndex(0)
                            self.ent_comment.setText("")
                    else:
                        QMessageBox.information(self, "Error", 'Fill mandatory fields')
                else:
                    QMessageBox.information(self, "Entry error ", '[{}] already exists in your database, '
                                                                  'please check again'.format(self.add_serial.text()))
                    self.add_serial.clear()
                    self.ent_brand.setCurrentIndex(0)
                    self.ent_capacity.setCurrentIndex(0)
                    self.ent_elastomer.setCurrentIndex(0)
                    self.ent_comment.setText("")
            else:
                QMessageBox.information(self, "Error", 'Serial Number is a mandatory field')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def del_pump(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.serial_del.text() != '':
                qur3 = "select * from Pumps where SERIAL ='{}'".format(self.serial_del.text())
                cur.execute(qur3)
                if len(cur.fetchall()) > 0:
                    cur.execute("Delete from Pumps where SERIAL ='{}'".format(self.serial_del.text()))
                    cur.execute("Delete from Records where SERIAL_NO ='{}'".format(self.serial_del.text()))
                    check = QMessageBox.warning(self, 'Confirm delete pump',
                                                "pump [{}] and all related events  will be permanently deleted,"
                                                " Do you like to continue?".format(self.serial_del.text()),
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if check == QMessageBox.Yes:
                        conn.commit()
                        self.statusBar().showMessage('Pump has been deleted', 5000)
                        self.serial_del.setText("")
                        self.autocompleteserialnumbers()
                    else:
                        conn.close()
                else:
                    QMessageBox.information(self, "Entry Error",
                                            '{} does not exist in your database, please check again'.format(
                                                self.serial_del.text()))
            else:
                QMessageBox.information(self, "Entry Error", 'Define pump serial number to be deleted')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def recallpumpspecs (self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.serial_del_recall.text() != "":
                cur.execute("select * from Pumps where SERIAL='{}'".format(self.serial_del_recall.text()))
                g = cur.fetchall()
                if len(g) > 0:
                    self.ent_brand_3.setCurrentText(g[0][3])
                    self.ent_capacity_2.setCurrentText(g[0][2])
                    self.ent_elastomer_2.setCurrentText(g[0][4])
                    self.textEdit.setPlainText(g[0][5])

                else:
                    QMessageBox.information(self, "Entry Error",
                            '[{}] does not exist in your database, please check again'.format(self.serial_del_recall.text()))
            else:
                QMessageBox.information(self, "Entry Error", 'Define pump serial number to recall its data')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong ')

                   
    def update_pump(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.serial_del_recall.text() != "":
                cur.execute("select * from Pumps where SERIAL='{}'".format(self.serial_del_recall.text()))
                g = cur.fetchall()
                if len(g) > 0:
                    if self.ent_capacity_2.currentText() != "" and self.ent_brand_3.currentText()!= "Select brand" and self.ent_elastomer_2.currentText() != "":
                        cur.execute(
                            "update Pumps SET CAPACITY='{}' ,BRAND='{}',ELASTOMER='{}',COMMENT='{}' "
                            "WHERE SERIAL ='{}'".format(
                                self.ent_capacity_2.currentText(), self.ent_brand_3.currentText(),
                                self.ent_elastomer_2.currentText(), self.textEdit.toPlainText(),
                                self.serial_del.text()))
                        check = QMessageBox.question(self, 'Data confirmation',
                                                     "[{}] specs will be updated and saved to pumps "
                                                     "database.Do you like to continue?".format(self.serial_del_recall.text()),
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if check == QMessageBox.Yes:
                            conn.commit()
                            self.statusBar().showMessage(
                                '[{}] specifications have been successfully updated and saved to pumps database'.format(self.serial_del_recall.text()), 5000)
                            self.serial_del_recall.clear()
                            self.ent_brand_3.setCurrentIndex(0)
                            self.ent_capacity_2.setCurrentIndex(0)
                            self.ent_elastomer_2.setCurrentIndex(0)
                            self.textEdit.setText("")
                        else:
                            conn.close()
                    else:
                        QMessageBox.information(self, "Entry Error", 'Please enter all mandatory fields')
                else:
                    QMessageBox.information(self, "Entry Error",
                                            '[{}] does not exist in pumps database, please check pump serial '
                                            'number again'.format(self.serial_del_recall.text()))
            else:
                QMessageBox.information(self, "Entry Error", 'Define pump serial number')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong, you might have lost connection')

    def go_abr(self):
        self.window3 = AdBeRe()
        self.window3.show()

    def go_cal(self):
        self.window4 = Calculator()
        self.window4.show()

    # def go_help(self):
    #     self.window5 = Help()
    #     self.window5.show()

    def add_record(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            var1 = self.serial2_ent.text()
            pumps_list = list(pd.read_sql('select SERIAL from Pumps', con=conn)['SERIAL'])
            if self.serial2_ent.text() !="" :
                if var1 in pumps_list:
                    var2 = self.date_ent.date().toString(QtCore.Qt.ISODate)
                    var3 = self.event_ent.currentText()            
                    if self.loc_ent.currentText()=="Well location":
                        var4 = self.field.currentText() + "-" + self.wellnumber.currentText()
                    elif self.loc_ent.currentText()=="Warehouse":
                        var4 = "Warehouse"
                    elif self.loc_ent.currentText()=="Pumpshop":
                        var4 = "Pumpshop"
                    elif self.loc_ent.currentText()=="Test bench":
                        var4 = self.field.currentText()+" test bench" 
                    else:
                        var4 = ""
                    var5 = self.cond_ent.currentText()
                    var7 = self.comment2_ent.toPlainText() 
                    try:
                        var6 = int(self.oper_ent.text())
                        if var3 != 'Select event' and var5 != 'Select condition' and var6 != '' and var4 !='':
                            cur.execute ("select * from Records where SERIAL_NO ='{}' and DATE = '{}' and EVENT='{}' and LOCATION = '{}' and CONDITION='{}' and CUM_RUN_LIFE='{}'".format(var1,var2,var3,var4,var5,var6))
                            checkexist = cur.fetchall()
                            if len (checkexist) == 0:      
                                qur2 = "insert into Records (SERIAL_NO,DATE,EVENT,LOCATION,CONDITION," \
                                    "CUM_RUN_LIFE,COMMENTS) values ('{}','{}','{}','{}','{}','{}'" \
                                    ",'{}')".format (var1, var2,var3, var4, var5, int(var6),var7)
                                cur.execute(qur2)            
                                check = QMessageBox.question(self, 'Data confirmation',
                                                        "Event will be added to pump history."
                                                        "Do you like to continue?",
                                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if check == QMessageBox.Yes:
                                    if self.checkBox_2.isChecked():                                      
                                        try:
                                            sender_mail = "workcloud1986@gmail.com"
                                            sender_pass = "bakr12334"
                                            subject = 'PC PUMP  EVENT NOTIFICATION'
                                            msg = 'Please note the following event for the pump with serial no [{}]:\n\nEvent: {} \nDate: {} \nLocation: {} \nCondition: {} \nCumulative run life: {} days\n\nTo take the necessary action if required.\n\n\nBest regards,'.format(var1, var3,var2,var4,var5,var6)
                                            content = 'Subject: {} \n\n {}'.format(subject, msg)
                                            server = smtplib.SMTP('smtp.gmail.com', 587)
                                            server.ehlo()
                                            server.starttls()                                         
                                            server.login(sender_mail,sender_pass)
                                            x= self.maillist.text()
                                            if x.count(" ")==0:
                                                if x.count(".com")==1 and x.count(";")==0:
                                                    server.sendmail(sender_mail, x, content)
                                                    QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                    server.close()
                                                    conn.commit()         
                                                    self.statusBar().showMessage('Event has been successfully added to pump history', 5000)
                                                    self.serial2_ent.setText("")
                                                    self.event_ent.setCurrentIndex(0)
                                                    self.loc_ent.setCurrentIndex(0)
                                                    self.cond_ent.setCurrentIndex(0)
                                                    self.oper_ent.clear()
                                                    self.comment2_ent.clear()
                                                    self.date_ent.setDate(QDate.currentDate())
                                                    self.mail_list.clear() 
                                                elif x.count(".com")==1 and x.count(";")==1:
                                                    z= x.split(';')
                                                    receiver_mail= z[0]
                                                    server.sendmail(sender_mail, receiver_mail, content)
                                                    QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                    server.close()
                                                    conn.commit()         
                                                    self.statusBar().showMessage('Event has been successfully added to pump history', 5000)
                                                    self.serial2_ent.setText("")
                                                    self.event_ent.setCurrentIndex(0)
                                                    self.loc_ent.setCurrentIndex(0)
                                                    self.cond_ent.setCurrentIndex(0)
                                                    self.oper_ent.clear()
                                                    self.comment2_ent.clear()
                                                    self.date_ent.setDate(QDate.currentDate()) 
                                                    self.mail_list.clear() 
                                                elif x.count(".com")== len(x.split(';')):
                                                    receiver_mail= x.split(';')
                                                    for i in receiver_mail:
                                                        server.sendmail(sender_mail, i, content)
                                                    QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                    server.close()
                                                    conn.commit()         
                                                    self.statusBar().showMessage('Event has been successfully added to pump history', 5000)
                                                    self.serial2_ent.setText("")
                                                    self.event_ent.setCurrentIndex(0)
                                                    self.loc_ent.setCurrentIndex(0)
                                                    self.cond_ent.setCurrentIndex(0)
                                                    self.oper_ent.clear()
                                                    self.comment2_ent.clear()
                                                    self.date_ent.setDate(QDate.currentDate())  
                                                    self.mail_list.clear() 
                                                else:
                                                    QMessageBox.warning(self, "Entry error", 'Please ensure mail distribution list is enetered in proper format')
                                                            
                                            else:
                                                QMessageBox.warning(self, "Entry error", 'Spaces are not allowed')
                                        except:
                                            time.sleep(1)
                                            QMessageBox.information(self, "Mail Failed",
                                                                    'No notification mail has been sent, may be '
                                                                    'no internet connection')
                                        
                                    else:   
                                        conn.commit()   
                                        self.statusBar().showMessage('Event has been successfully added to pump history', 5000)
                                        self.serial2_ent.setText("")
                                        self.event_ent.setCurrentIndex(0)
                                        self.loc_ent.setCurrentIndex(0)
                                        self.cond_ent.setCurrentIndex(0)
                                        self.oper_ent.clear()
                                        self.comment2_ent.clear()
                                        self.date_ent.setDate(QDate.currentDate()) 
                                        self.mail_list.clear() 
                                else:
                                    conn.close()
                            elif len (checkexist) > 0:
                                QMessageBox.information(self, "Entry Error", 'The same event already exists')  
                        else:
                            QMessageBox.information(self, "Entry Error", 'Please enter mandatory fields')
                    except:
                        QMessageBox.information(self, "Entry Error", 'Please enter Run Life in digits')
                else:
                    QMessageBox.information(self, "Entry Error", '[{}] doesnot exist in your pumps database'
                                                                 ', please add pump then add records'.format(var1))
            else:
                QMessageBox.information(self, "Entry Error", 'Enter pump serial number')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong, you might have lost connection')

    def del_record(self):
        try:  
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.serial_del_3.text() != '':
                if self.checkBox_3.isChecked(): 
                    cur.execute("select * from Records where SERIAL_NO ='{}'" .format(self.serial_del_3.text()))
                    qur77 = cur.fetchall()
                    if len(qur77) > 0 :
                        cur.execute("Delete from Records where SERIAL_NO ='{}'" .format(self.serial_del_3.text()))            
                        check = QMessageBox.warning(self, 'Confirm delete pump history', "ALL EVENTS for [{}]"
                                                                                         " will be permanently"
                                                                                         " deleted."
                                                    " Do you like to continue?".format(self.serial_del_3.text()),
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if check == QMessageBox.Yes:
                            conn.commit()
                            self.statusBar().showMessage('All pump events have been deleted',5000)
                            self.serial_del_3.clear()
                        else:
                            conn.close()
                    else:
                        QMessageBox.information(self, "Entry Error", 'No events recorded for [{}]'.format(self.serial_del_3.text()))
                                             
                elif self.delbyrecnobtn.isChecked():
                    cur.execute ("select * from Records where SERIAL_NO ='{}'" .format(self.serial_del_3.text()))
                    qur5=cur.fetchall()
                    if len (qur5) > 0:    
                        cur.execute("select * from Records where SERIAL_NO ='{}' and ID='{}'" .format(self.serial_del_3.text(),self.recordid_2.currentText()))
                        check2=cur.fetchall()
                        if len (check2) > 0:
                            cur.execute("Delete from Records where SERIAL_NO ='{}' and ID='{}'" .format(self.serial_del_3.text(),self.recordid_2.currentText()))              
                            check = QMessageBox.warning(self, 'Confirm delete pump event', "event no. '{}' will be permanently deleted."
                                        " Do you like to continue?".format(self.recordid_2.currentText()),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if check == QMessageBox.Yes:
                                conn.commit()
                                self.statusBar().showMessage('Pump event has been deleted',5000)
                                self.serial_del_3.clear()
                            else:
                                conn.close()
                        else:
                            QMessageBox.information(self, "Entry Error", '[{}] has no recorded event with ID [{}]'.format(self.serial_del_3.text(),self.recordid_2.currentText()))
                    else:
                        QMessageBox.information(self, "Entry Error", 'No events recorded for [{}]'.format(self.serial_del_3.text()))
                else:
                    QMessageBox.information(self, "Entry Error", 'Please select one delete option')    ###delay modify this till make auto fill for ID combo                       
            else:
                QMessageBox.information(self, "Entry Error", 'Define pump serial number')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong, you might have lost connection')

    def update_record(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()  
            SN = self.serial_del_2.text()
            D = self.recordid.currentText()
            if SN != "" and D != "":
                cur.execute("select * from Pumps where SERIAL= '{}'".format(SN))
                f = cur.fetchall()
                if len(f)>0:                
                    cur.execute("select * from Records where SERIAL_NO = '{}'".format(SN))
                    y = cur.fetchall()
                    if len(y)>0:
                        cur.execute("select * from Records where SERIAL_NO ='{}' and ID='{}'" .format(SN,D))
                        z= cur.fetchall()
                        if len (z) > 0 :
                            R = self.oper_ent_2.text()
                            E = self.event_ent_3.currentText()  
                            if self.loc_ent_2.currentText()=="Well location":
                                L = self.field_2.currentText() + "-" + self.wellnumber_2.currentText()
                            elif self.loc_ent_2.currentText()=="Warehouse":
                                L = "Warehouse"
                            elif self.loc_ent_2.currentText()=="Pumpshop":
                                L = "Pumpshop"
                            elif self.loc_ent_2.currentText()=="Test bench":
                                L = self.field_2.currentText()+" test bench" 
                            else:
                                L = ""
                            Con = self.cond_ent_3.currentText()
                            C = self.comment2_ent_2.toPlainText()
                            DT = self.date_ent_2.date().toString(QtCore.Qt.ISODate)
                            if self.oper_ent_2.text() != "":
                                cur.execute ("select * from Records where SERIAL_NO = '{}' and DATE = '{}' and EVENT='{}' and LOCATION = '{}' and CONDITION='{}' and CUM_RUN_LIFE='{}'".format(SN,DT,E,L,Con,R))
                                checkex = cur.fetchall()
                                if len(checkex) == 0 :
                                    try:
                                        x=int(R)
                                        qur44=("UPDATE Records SET DATE='{}' ,EVENT='{}',LOCATION='{}',CONDITION='{}',CUM_RUN_LIFE='{}',COMMENTS='{}' WHERE SERIAL_NO ='{}' AND ID='{}' ".format(DT,E,L,Con,int(x),C,SN,D))
                                        cur.execute(qur44)            
                                        check = QMessageBox.question(self, 'Data confirmation',
                                                            "Event will be updated and added to pump history.Do you like to continue?",
                                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                        if check == QMessageBox.Yes:
                                            if self.checkBox_4.isChecked():                                      
                                                try:
                                                    sender_mail = "workcloud1986@gmail.com"
                                                    sender_pass = "bakr12334"
                                                    subject = 'PC PUMP  EVENT NOTIFICATION'
                                                    msg = 'Please note the following event for the pump with serial no [{}]:\n\nEvent: {} \nDate: {} \nLocation: {} \nCondition: {} \nCumulative run life: {} days\n\nTo take the necessary action if required.\n\nBest regards,'.format(SN, E,DT,L,Con,x)
                                                    content = 'Subject: {} \n\n {}'.format(subject, msg)
                                                    server = smtplib.SMTP('smtp.gmail.com', 587)
                                                    server.ehlo()
                                                    server.starttls()                                          
                                                    server.login(sender_mail,sender_pass)
                                                    x= self.maillist_2.text()
                                                    if x.count(" ")==0:
                                                        if x.count(".com")==1 and x.count(";")==0:
                                                            server.sendmail(sender_mail, x, content)
                                                            QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                            server.close()
                                                            conn.commit()
                                                            self.statusBar().showMessage('Record has been successfully updated and added to pump history',5000)
                                                            self.serial_del_2.clear()
                                                            self.event_ent_3.setCurrentIndex(0)
                                                            self.loc_ent_2.setCurrentIndex(0)
                                                            self.cond_ent_3.setCurrentIndex(0)
                                                            self.comment2_ent_2.clear()
                                                            self.oper_ent_2.clear()
                                                            self.date_ent_2.setDate(QDate.currentDate())
                                                            self.maillist_2.clear()
                                                        elif x.count(".com")==1 and x.count(";")==1:
                                                            z= x.split(';')
                                                            receiver_mail= z[0]
                                                            server.sendmail(sender_mail, receiver_mail, content)
                                                            QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                            server.close()
                                                            conn.commit()
                                                            self.statusBar().showMessage('Record has been successfully updated and added to pump history',5000)
                                                            self.serial_del_2.clear()
                                                            self.event_ent_3.setCurrentIndex(0)
                                                            self.loc_ent_2.setCurrentIndex(0)
                                                            self.cond_ent_3.setCurrentIndex(0)
                                                            self.comment2_ent_2.clear()
                                                            self.oper_ent_2.clear()
                                                            self.date_ent_2.setDate(QDate.currentDate())
                                                            self.maillist_2.clear()
                                                        elif x.count(".com")== len(x.split(';')):
                                                            receiver_mail= x.split(';')
                                                            for i in receiver_mail:
                                                                server.sendmail(sender_mail, i, content)
                                                            QMessageBox.information(self, "Success", 'notification mail has been sent')
                                                            server.close()
                                                            conn.commit()
                                                            self.statusBar().showMessage('Record has been successfully updated and added to pump history',5000)
                                                            self.serial_del_2.clear()
                                                            self.event_ent_3.setCurrentIndex(0)
                                                            self.loc_ent_2.setCurrentIndex(0)
                                                            self.cond_ent_3.setCurrentIndex(0)
                                                            self.comment2_ent_2.clear()
                                                            self.oper_ent_2.clear()
                                                            self.date_ent_2.setDate(QDate.currentDate())
                                                            self.maillist_2.clear()
                                                        else:
                                                            QMessageBox.warning(self, "Entry error", 'Please ensure mail distribution list is enetered in proper format')
                                                            
                                                    else:
                                                        QMessageBox.warning(self, "Entry error", 'Spaces are not allowed')
                                                except:
                                                    time.sleep(1)
                                                    QMessageBox.information(self, "Mail Failed",
                                                                            'No notification mail has been sent, may be '
                                                                            'no internet connection')
                                            else:   
                                                conn.commit()
                                                self.statusBar().showMessage('Record has been successfully updated and added to pump history',5000)
                                                self.serial_del_2.clear()
                                                self.event_ent_3.setCurrentIndex(0)
                                                self.loc_ent_2.setCurrentIndex(0)
                                                self.cond_ent_3.setCurrentIndex(0)
                                                self.comment2_ent_2.clear()
                                                self.oper_ent_2.clear()
                                                self.date_ent_2.setDate(QDate.currentDate()) 
                                                self.maillist_2.clear()

                                        else:
                                            conn.close()
                                    except:
                                        QMessageBox.information(self, "Entry Error", 'Run Life must be in digits')
                                elif len(checkex) > 0 :
                                    QMessageBox.information(self, "Entry Error", 'The same event details already exist')  
                            else:
                                QMessageBox.information(self, "Entry Error", 'Please enter Run Life')
                        else:
                            QMessageBox.information(self, "Entry Error", 'Record No is incorrect, please confirm the no of your target event')
                    else:
                        QMessageBox.information(self, "Entry Error", 'No events recorded for [{}], please check serial number'.format(SN))
                else:
                    QMessageBox.information(self, "Entry Error", '[{}] does not exist in pumps database, please fill the pump specifications first' .format(SN))
            else:
                QMessageBox.information(self, "Entry Error", 'Pump serial number and Record No are mandatory fields to update event')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection to database.')

    def recalleventofthisID (self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.serial_del_2.text() != "" and self.recordid.currentText() !='':
                cur.execute ("select * from Records where SERIAL_NO = '{}'".format(self.serial_del_2.text()))    
                beta=cur.fetchall()
                if len(beta) > 0 :
                    cur.execute("select * from Records where SERIAL_NO='{}' and ID='{}'".format(self.serial_del_2.text(),self.recordid.currentText()))
                    g = cur.fetchall()
                    if len(g) > 0:
                        self.cond_ent_3.setCurrentText(g[0][5])
                        self.oper_ent_2.setText(str(g[0][6]))
                        self.comment2_ent_2.setPlainText(g[0][7])

                        ########
                        cur.execute ("select Date from Records where SERIAL_NO='{}' and ID='{}'".format(self.serial_del_2.text(),self.recordid.currentText()))
                        k =cur.fetchall()
                        DATE = str (k[0][0])
                        qtDate = QtCore.QDate.fromString(DATE, 'yyyy-MM-dd')
                        self.date_ent_2.setDate(qtDate)
                        self.event_ent_3.setCurrentText(g[0][3])
                        
                        #############
                        cur.execute ("select LOCATION from Records where SERIAL_NO='{}' and ID='{}'".format(self.serial_del_2.text(),self.recordid.currentText()))
                        l =cur.fetchall()
                        LOC = str (l[0][0])
                        checkbenchtest = LOC.count("test bench")
                        #getslashloc = LOC.find("-")
                        # getcompany =LOC [:-11]
                        if checkbenchtest >0 :
                            x = "Test bench"
                            y = LOC [:-11]
                            self.loc_ent_2.setCurrentText(x)
                            self.field_2.setCurrentText(y)
                        elif LOC == "Warehouse":
                            x = "Warehouse"
                            self.loc_ent_2.setCurrentText(x)
                        elif LOC == "Pumpshop":
                            x = "Pumpshop"
                            self.loc_ent_2.setCurrentText(x)
                        else:
                            getslashloc = LOC.find("-")
                            field =LOC [0:getslashloc]
                            well =LOC [getslashloc+1: len(LOC)]
                            x = "Well location"
                            y = LOC [0:getslashloc]
                            z = LOC [getslashloc+1: len(LOC)]
                            # self.field_2.setCurrentText("field")
                            # self.wellnumber_2.setCurrentText("well")
                            # self.loc_ent_2.setCurrentText("Well location")
                            self.loc_ent_2.setCurrentText(x)
                            self.field_2.setCurrentText(y)
                            self.wellnumber_2.setCurrentText(z)


                        ############

                       
                    else:
                        QMessageBox.information(self, "Entry Error", '[{}] dosnot have event recorder with ID [{}]'.format(self.serial_del_2.text(),self.recordid.currentText()))  
                else:
                    QMessageBox.information(self, "Entry Error", 'No events recorded for [{}] in database, please check again'.format(self.serial_del_2.text()))
            else:
                QMessageBox.information(self, "Entry Error", 'Define pump serial number to recall its data')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')


    @staticmethod
    def show_table(res, table_name):
        table_name.setRowCount(0)
        for row_num, all_data in enumerate(res):
            table_name.insertRow(row_num)
            for col__num, data in enumerate(all_data):
                table_name.setItem(row_num, col__num, QTableWidgetItem(str(data)))

    def find_pump(self):
        try:
            self.table_search.clearContents()
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()        
            serial = self.serial_search.text()
            if self.serial_radio.isChecked():
                if serial != "":
                    cur.execute("select * from Pumps where SERIAL ='{}'" .format(serial))
                    check1 = cur.fetchall()
                    cur.execute("select * from Records where SERIAL_NO ='{}'" .format(serial))
                    check2 = cur.fetchall()
                    if len(check1) == 0 and len(check2) > 0:
                        QMessageBox.information(self, "Error", 'Some events are recorded for this pump, but there are no technical specifications in your database')
                        self.serial_search.clear()
                    elif len(check1) > 0 and len(check2) == 0:
                        QMessageBox.information(self, "Error", 'There are no events recorded for this pump in your database')
                        self.serial_search.clear()
                    elif len(check1) > 0 and len(check2) > 0:
                        cur.execute("SELECT Pumps.SERIAL,Records.EVENT, Records.LOCATION,Records.DATE,Records."
                                    "CONDITION ,Pumps.BRAND,  Pumps.CAPACITY, Pumps.ELASTOMER,"
                                    "Records.CUM_RUN_LIFE FROM Pumps, Records where Pumps.SERIAL='{}' "
                                    "and Records.SERIAL_NO ='{}' order by Records.DATE DESC LIMIT 1".format
                                    (serial, serial))
                        res = cur.fetchall()
                        FinalApp.show_table(res=res, table_name=self.table_search)
                        result = str(self.table_search.rowCount())
                        self.label_23.setText(result)
                        self.serial_search.clear()
                        conn.close()
                    else:
                            QMessageBox.information(self, "Error", 'Pump does not exist in database,'
                                                                'or no event recorded for this pump')
                            self.serial_search.clear()
                else:
                    QMessageBox.information(self, "Error", 'Enter pump serial number')
            else:
                QMessageBox.information(self, "Error", 'Check serial number option button')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong,you might have lost connection')

    def search_pumps(self):
        try:
            self.table_search.clearContents()
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()

            
            if self.loc_ent_3.currentText()=="":
                LOC = ""
            elif self.loc_ent_3.currentText()=="Well location":######################
                LOC = self.field_3.currentText() + "-" + self.wellnumber_3.currentText()  
            elif self.loc_ent_3.currentText()=="Warehouse":
                LOC = "Warehouse"
            elif self.loc_ent_3.currentText()=="Warehouse":
                LOC = "Warehouse"      
            elif self.loc_ent_3.currentText()=="Pumpshop":
                LOC = "Pumpshop"            
            elif self.loc_ent_3.currentText()=="Test bench":####################
                LOC = self.field_3.currentText()+" test bench"
            
            EV = self.event_ent_2.currentText()
            COND = self.cond_ent_2.currentText()
            pumps = pd.read_sql('select * from Pumps', con=conn)
            records = pd.read_sql('select * from Records', con=conn)
            pumps = pumps.rename(columns={'SERIAL': 'SN'})
            records = records.rename(columns={'SERIAL_NO': 'SN'})
            all = pd.merge(pumps, records, how="inner", on='SN')
            all.set_index('SN')
            grouped = all.groupby('SN')
            if self.runlife_radio_2.isChecked():
                if self.runlife_search_2.text() != '':
                    RL = int(self.runlife_search_2.text())
                else:
                    pass
                    QMessageBox.information(self, "Error", 'Specify value of run life')
                if RL != '':
                    if self.comboBox_15.currentText() == ">":
                        req = pd.DataFrame(columns=list(all.columns))
                        for i in list(all['SN'].unique()):
                            df = grouped.get_group(i)
                            df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['CUM_RUN_LIFE'] > RL)]
                            req = pd.concat([req, df2])
                            req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                            req = req[
                                ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                            res = req.values.tolist()
                            FinalApp.show_table(res=res, table_name=self.table_search)
                            result = str(self.table_search.rowCount())
                            self.label_23.setText(result)
                            conn.close()
                    elif self.comboBox_15.currentText() == "<":
                        req = pd.DataFrame(columns=list(all.columns))
                        for i in list(all['SN'].unique()):
                            df = grouped.get_group(i)
                            df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['CUM_RUN_LIFE'] < RL)]
                            req = pd.concat([req, df2])
                            req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                            req = req[
                                ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                            res = req.values.tolist()
                            FinalApp.show_table(res=res, table_name=self.table_search)
                            result = str(self.table_search.rowCount())
                            self.label_23.setText(result)
                            conn.close()
                else:
                    QMessageBox.information(self, "Error", 'Specify value of run life')
            elif self.location_radio_5.isChecked():
                if LOC != '':
                    req = pd.DataFrame(columns=list(all.columns))
                    for i in list(all['SN'].unique()):
                        df = grouped.get_group(i)
                        df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['LOCATION'] == LOC)]
                        req = pd.concat([req, df2])
                    req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                    req = req[
                        ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                    res = req.values.tolist()
                    FinalApp.show_table(res=res, table_name=self.table_search)
                    res = str(self.table_search.rowCount())
                    self.label_23.setText(res)
                    conn.close()
                else:
                    QMessageBox.information(self, "Error", 'Specify location')
            elif self.event_radio_7.isChecked():
                req = pd.DataFrame(columns=list(all.columns))
                for i in list(all['SN'].unique()):
                    df = grouped.get_group(i)
                    df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['EVENT'] == EV)]
                    req = pd.concat([req, df2])
                req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                req = req[
                    ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                res = req.values.tolist()
                FinalApp.show_table(res=res, table_name=self.table_search)
                res = str(self.table_search.rowCount())
                self.label_23.setText(res)
                conn.close()

            elif self.condition_radio_6.isChecked():
                req = pd.DataFrame(columns=list(all.columns))
                for i in list(all['SN'].unique()):
                    df = grouped.get_group(i)
                    df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['CONDITION'] == COND)]
                    req = pd.concat([req, df2])
                req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                req = req[
                    ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                res = req.values.tolist()
                FinalApp.show_table(res=res, table_name=self.table_search)
                res = str(self.table_search.rowCount())
                self.label_23.setText(res)
                conn.close()
            else:
                QMessageBox.information(self, "Error", 'Check one option')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')

    def show_stock(self):
        self.table_search.clearContents()
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            pumps = pd.read_sql('select * from Pumps', con=conn)
            records = pd.read_sql('select * from Records', con=conn)
            users = pd.read_sql('select * from Users', con=conn)
            admins = pd.read_sql('select * from Admins', con=conn)
            pumps = pumps.rename(columns={'SERIAL': 'SN'})
            records = records.rename(columns={'SERIAL_NO': 'SN'})
            all = pd.merge(pumps, records, how="inner", on='SN')
            all.set_index('SN')
            grouped = all.groupby('SN')
            if self.radioButton_3.isChecked():
                req = pd.DataFrame(columns=list(all.columns))
                for i in list(all['SN'].unique()):
                    df = grouped.get_group(i)
                    df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['LOCATION'] == 'Warehouse')]

                    req = pd.concat([req, df2])
                req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                req = req[
                    ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                res = req.values.tolist()
                FinalApp.show_table(res=res, table_name=self.table_search)
                res = str(self.table_search.rowCount())
                self.label_23.setText(res)
                conn.close()

            elif self.condbotton.isChecked():
                if self.comboBox_4.currentText() == 'B':
                    req = pd.DataFrame(columns=list(all.columns))
                    for i in list(all['SN'].unique()):
                        df = grouped.get_group(i)
                        df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['LOCATION'] == 'Warehouse')
                                 & (df['CONDITION'] == 'B')]
                        req = pd.concat([req, df2])
                    req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                    req = req[
                        ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER','CUM_RUN_LIFE']]
                    res = req.values.tolist()
                    FinalApp.show_table(res=res, table_name=self.table_search)

                    res = str(self.table_search.rowCount())
                    self.label_23.setText(res)
                    conn.close()

                elif self.comboBox_4.currentText() == 'A':
                    req = pd.DataFrame(columns=list(all.columns))
                    for i in list(all['SN'].unique()):
                        df = grouped.get_group(i)
                        df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['LOCATION'] == 'Warehouse')
                                 & (df['CONDITION'] == 'A')]

                        req = pd.concat([req, df2])
                    req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                    req = req[
                        ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER',
                         'CUM_RUN_LIFE']]
                    res = req.values.tolist()
                    FinalApp.show_table(res=res, table_name=self.table_search)
                    res = str(self.table_search.rowCount())
                    self.label_23.setText(res)
                    conn.close()
                else:
                    QMessageBox.information(self, "Error", 'Specify condition')
            elif self.capbotton.isChecked():
                if self.comboBox_5.currentText() != 'Select capacity':
                    req = pd.DataFrame(columns=list(all.columns))
                    for i in list(all['SN'].unique()):
                        df = grouped.get_group(i)
                        df2 = df[(df['ID_y'] == df['ID_y'].max()) & (df['LOCATION'] == 'Warehouse')
                                 & (df['CAPACITY'] == '{}'.format(self.comboBox_5.currentText()))]

                        req = pd.concat([req, df2])
                    req = req.drop(['ID_x', 'COMMENT', 'COMMENTS', 'ID_y'], axis=1)
                    req = req[
                        ['SN', 'EVENT', 'LOCATION', 'DATE', 'CONDITION', 'BRAND', 'CAPACITY', 'ELASTOMER', 'CUM_RUN_LIFE']]
                    res = req.values.tolist()
                    FinalApp.show_table(res=res, table_name=self.table_search)
                    res = str(self.table_search.rowCount())
                    self.label_23.setText(res)
                    conn.close()
                else:
                    QMessageBox.information(self, "Error", 'Specify capacity')
            else:
                QMessageBox.information(self, "Error", 'Check one option')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection')

    
    def exportsearchbuttonstatus (self):
        if self.label_23.text() == "" or self.label_23.text() == "0": 
            self.EXPORTTOEX1.setEnabled(False)
        else:
            self.EXPORTTOEX1.setEnabled(True)
    
    
    def export_search(self):
        try:
            wb = Workbook("search_pumps.xlsx")
            sheet1 = wb.add_worksheet()
            sheet1.write(0, 0, 'SERIAL NO')
            sheet1.write(0, 1, 'EVENT')
            sheet1.write(0, 2, 'LOCATION')
            sheet1.write(0, 3, 'DATE')
            sheet1.write(0, 4, 'CONDITION')
            sheet1.write(0, 5, 'BRAND')
            sheet1.write(0, 6, 'CAPACITY')
            sheet1.write(0, 7, 'ELASTOMER')
            sheet1.write(0, 8, 'RUN LIFE')
            col = 0
            for currentColumn in range(self.table_search.columnCount()):
                row = 1
                for currentRow in range(self.table_search.rowCount()):
                    text = str(self.table_search.item(currentRow, currentColumn).text())
                    sheet1.write(row, col, text)
                    row += 1
                col += 1
            wb.close()
            os.startfile("search_pumps.xlsx")
            QMessageBox.information(self, "Warning", 'Make sure to close the excel file before you proceed to any other query')
        except:
            QMessageBox.information(self, "Warning", 'Close the excel file before you proceed to any other query')


    def show_history(self):
        try:
            if self.pserial_history.text() !="":
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                s = self.pserial_history.text()
                cur.execute("SELECT ID, EVENT, DATE, LOCATION, CONDITION, CUM_RUN_LIFE, COMMENTS from Records "
                            "where SERIAL_NO='{}' order by date".format (s))
                res = cur.fetchall()
                if len(res) > 0:
                    FinalApp.show_table(res=res, table_name=self.table_history)
                    res = str(self.table_history.rowCount())
                    self.label_47.setText(res)
                    
                    conn.close()
                else:
                    QMessageBox.information(self, "Error", 'No events recorded for {}'.format(self.pserial_history.text()))
            else:
                QMessageBox.information(self, "Error", 'Enter pump serial number')                    
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection')

    def get_from_his_table(self, row):
        if self.table_history.item(row, 0) == None: 
            pass
        else:
            global record_update
            item1 = self.table_history.item(row, 0)
            record_update= item1.text()

    def go_update_record(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
            checkadmin = cur.fetchall()
            if record_update != "":
                if len(checkadmin) > 0 or user_name == "admin":
                    self.tabWidget.setCurrentIndex(1)
                    self.serial_del_2.setText(self.pserial_history.text())
                    self.recordid.setCurrentText(str(record_update))

                else:
                    QMessageBox.information(self, "Sorry {}".format(user_name),
                                            'For database security, pumps tab can be only accessed by admins')
            else:
                QMessageBox.information(self, "Error", 'Select record to be updated.')
        except:
            self.tabWidget.setCurrentIndex(4)
            QMessageBox.information(self, "Error", 'No event selected')

    def go_delete_record(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
            checkadmin = cur.fetchall()
            if record_update != "":
                if len(checkadmin) > 0 or user_name == "admin":
                    self.tabWidget.setCurrentIndex(1)
                    self.serial_del_3.setText(self.pserial_history.text())
                    self.recordid_2.setCurrentText(str(record_update))

                else:
                    QMessageBox.information(self, "Sorry {}".format(user_name),
                                            'For database security, pumps tab can be only accessed by admins')
            else:
                QMessageBox.information(self, "Error", 'Select record to be updated.')
        except:
            self.tabWidget.setCurrentIndex(4)
            QMessageBox.information(self, "Error", 'No event selected')


    def exporthistorybuttonstatus (self):
        if self.label_47.text() == "" or self.label_47.text() == "0":
            self.EXPORTTOEX2_2.setEnabled(False)
        else:
            self.EXPORTTOEX2_2.setEnabled(True)
    
    def export_history(self):
        try:
            wb = Workbook("pump_history.xlsx")
            sheet1 = wb.add_worksheet()
            sheet1.write(0, 0, 'PUMP Serial No :')
            sheet1.write(0, 1, '{}'.format(self.pserial_history.text()))
            sheet1.write(2, 0, 'ID')
            sheet1.write(2, 1, 'EVENT')
            sheet1.write(2, 2, 'DATE')
            sheet1.write(2, 3, 'LOCATION')
            sheet1.write(2, 4, 'CONDITION')
            sheet1.write(2, 5, 'RUN LIFE')
            sheet1.write(2, 6, 'COMMENTS')
            col = 0
            for currentColumn in range(self.table_history.columnCount()):
                row = 3
                for currentRow in range(self.table_history.rowCount()):
                    text = str(self.table_history.item(currentRow, currentColumn).text())
                    sheet1.write(row, col, text)
                    row += 1
                col += 1
            wb.close()
            os.startfile("pump_history.xlsx")
            QMessageBox.information(self, "Warning", 'Make sure to close the excel file before you'
                                                    ' proceed to any other query')
        except:
            QMessageBox.information(self, "Warning", 'Close the excel file before you'
                                                    'proceed to any other query')


    def view_pumps(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            if self.all_radio_7.isChecked():
                cur.execute("SELECT SERIAL,CAPACITY,BRAND,ELASTOMER,COMMENT from Pumps order by capacity")
                db = cur.fetchall()
                FinalApp.show_table(res=db, table_name=self.view_table)
                res = str(self.view_table.rowCount())
                self.res_view.setText(res)                
            elif self.brand_radio_6.isChecked():
                if self.ent_brand_2.currentText() != 'Select brand':
                    cur.execute("SELECT SERIAL,CAPACITY,BRAND,ELASTOMER,COMMENT from Pumps "
                                "where pumps.brand ='{}' order by capacity".format
                                                (str(self.ent_brand_2.currentText())))
                    check= cur.fetchall()
                    if len(check) >0 :
                        FinalApp.show_table(res=check, table_name=self.view_table)
                        res = str(self.view_table.rowCount())
                        self.res_view.setText(res)
                    else:
                        QMessageBox.information(self, "Error", 'No pumps of this brand exist in your database')
                else:
                    QMessageBox.information(self, "Error", 'Specify brand ')
            elif self.elas_radio.isChecked():
                if self.ent_elastomer_3.currentText() != 'Select elastomer type':
                    cur.execute("SELECT SERIAL,CAPACITY,BRAND,ELASTOMER,COMMENT from"
                                " Pumps where ELASTOMER = '{}' order by "
                                "capacity".format(self.ent_elastomer_3.currentText()))
                    check15 = cur.fetchall()
                    if len(check15) > 0:
                        FinalApp.show_table(res=check15, table_name=self.view_table)
                        res = str(self.view_table.rowCount())
                        self.res_view.setText(res)
                    else:
                        QMessageBox.information(self, "Error", 'No pumps having this elastomer recorded in your database')
                else:
                    QMessageBox.information(self, "Error", ' Specify elastomer')
            elif self.capacity_radio7.isChecked():
                if self.ent_capacity_3.currentText() != 'Select pump capacity':
                    cur.execute("SELECT SERIAL,CAPACITY,BRAND,ELASTOMER,COMMENT "
                                "from Pumps where CAPACITY = '{}' order by BRAND".format
                                (str(self.ent_capacity_3.currentText())))
                    check16 = cur.fetchall()
                    if len(check16) > 0:
                        FinalApp.show_table(res=check16, table_name=self.view_table)
                        res = str(self.view_table.rowCount())
                        self.res_view.setText(res)
                    else:
                        QMessageBox.information(self, "Error", 'No pumps of this capacity recorded in your database')
                else:
                    QMessageBox.information(self, "Error", 'Specify pump capacity')
            else:
                QMessageBox.information(self, "Error", 'Check one option')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')

    def get_from_view_table(self, row):
        if self.view_table.item(row, 0) == None: 
            pass
        else:
            global pump_update
            item = self.view_table.item(row, 0)
            pump_update = item.text()

    def go_update_pump(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
            checkadmin = cur.fetchall()
            if len(checkadmin) > 0 or user_name == "admin":
                self.tabWidget.setCurrentIndex(0)
                self.serial_del_recall.setText(pump_update)
            else:
                QMessageBox.information(self, "Sorry {}".format(user_name),
                                        'For database security, pumps tab can be only accessed by admins')
        except:
            self.tabWidget.setCurrentIndex(3)
            QMessageBox.information(self, "Error", 'No pump selected')

#
    def go_delete_pump(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
            checkadmin = cur.fetchall()
            if len(checkadmin) > 0 or user_name == "admin":
                self.tabWidget.setCurrentIndex(0)
                self.serial_del.setText(pump_update)
            else:
                QMessageBox.information(self, "Sorry {}".format(user_name),
                                        'For database security, pumps tab can be only accessed by admins')
        except:
            self.tabWidget.setCurrentIndex(3)
            QMessageBox.information(self, "Error", 'No pump selected')
#
    def exportviewbuttonstatus (self):
        if self.res_view.text() == "" or self.res_view.text() == "0":
            self.EXPORTTOEX2.setEnabled(False)
        else:
            self.EXPORTTOEX2.setEnabled(True)


    def export_view(self):
        try:
            wb = Workbook("view_pumps.xlsx")
            sheet1 = wb.add_worksheet()
            sheet1.write(0, 0, 'SERIAL')
            sheet1.write(0, 1, 'CAPACITY')
            sheet1.write(0, 2, 'BRAND')
            sheet1.write(0, 3, 'ELASTOMER')
            sheet1.write(0, 4, 'COMMENT')
            col = 0
            for currentColumn in range(self.view_table.columnCount()):
                row = 1
                for currentRow in range(self.view_table.rowCount()):
                    text = str(self.view_table.item(currentRow, currentColumn).text())
                    sheet1.write(row, col, text)
                    row += 1
                col += 1
            wb.close()
            os.startfile("view_pumps.xlsx")
            QMessageBox.information(self, "Warning", 'Make sure to close the excel file before you '
                                                    'proceed to any other query')
        except:
            QMessageBox.information(self, "Warning", 'Close the excel file before you '
                                                    'proceed to any other query')

    def plot(self):
        try:
            conn = sql.connect('PCP_Database')
            df = pd.read_sql('SELECT tt.SERIAL_NO,CUM_RUN_LIFE, CONDITION FROM  Records tt INNER JOIN '
                            '(SELECT SERIAL_NO, MAX(CUM_RUN_LIFE) AS MaxOper, MAX(ID) AS MaxID '
                             ' FROM Records GROUP BY SERIAL_NO)'
                            ' groupedtt  ON tt.SERIAL_NO = groupedtt.SERIAL_NO '
                             'AND tt.CUM_RUN_LIFE = groupedtt.MaxOper AND tt.ID = groupedtt.MaxID ', con=conn)
            df2 = pd.read_sql('select * from Pumps', con=conn)
            df5 = pd.read_sql('select * from Records', con=conn)
            df2 = df2.rename(columns={'SERIAL': 'SN'})
            df = df.rename(columns={'SERIAL_NO': 'SN'})
            df3 = pd.merge(df, df2, how="inner", on='SN')
            self.MplWidget.canvas.axes.clear()
            if self.brand_radio_stats_3.isChecked():
                brand_df = pd.read_sql('select distinct BRAND from Pumps',con=conn)
                my_brands = []
                perf = []
                explode=[]
                for i in list(brand_df['BRAND']):
                    my_brands.append(i)
                    perf.append(df3[df3['BRAND'] == i]['CUM_RUN_LIFE'].mean())
                    explode.append(0)
                explode[-1]=0.1
                
                self.MplWidget.canvas.axes.pie(perf, labels=my_brands,explode=explode,autopct='%1.1f%%', shadow=True, startangle=140)
                self.MplWidget.canvas.axes.set_title('Brand Performance statistics')
                self.MplWidget.canvas.draw()
            elif self.run_radio_stats_3.isChecked():
                values = [len(df3[(df3['CUM_RUN_LIFE'] > 0) & (df3['CUM_RUN_LIFE'] < 100)].index),
                        len(df3[(df3['CUM_RUN_LIFE'] > 100) & (df3['CUM_RUN_LIFE'] < 365)].index),
                          len(df3[(df3['CUM_RUN_LIFE'] > 365) & (df3['CUM_RUN_LIFE'] < 730)].index),
                          len(df3[df3['CUM_RUN_LIFE'] > 730].index)]
                labels = ['poor (0-100) days', 'normal (100-365) days','good (1-2) years', 'superb > 2 years']
                explode=[0,0,0,0.1]
                self.MplWidget.canvas.axes.pie(values, labels=labels, explode=explode,
                                               autopct='%1.1f%%', shadow=True, startangle=140)
                self.MplWidget.canvas.axes.set_title('OPERATION PERFORMANCE STATISTICS')
                self.MplWidget.canvas.draw()
            elif self.brandc_radio_stats_3.isChecked():
                brand_df = pd.read_sql('select distinct BRAND from Pumps',con=conn)
                brand_count = []
                labels = []
                explode =[]
                for i in list(brand_df['BRAND']):
                    brand_count.append(len(df3[df3['BRAND'] == i].index))
                    labels.append(i)
                    explode.append(0)
                explode[-1]=0.1

                
                self.MplWidget.canvas.axes.pie(brand_count, labels=labels,explode=explode,
                                               autopct='%1.1f%%', shadow=True, startangle=140)
                self.MplWidget.canvas.axes.set_title('BRAND STATISTICS')
                self.MplWidget.canvas.draw()
            elif self.cond_radio_stats_3.isChecked():
                values = [len(df3[df3['CONDITION'] == 'A'].index), len(df3[df3['CONDITION'] == 'B'].index)
                    , len(df3[df3['CONDITION'] == 'JUNK'].index), len(df3[df3['CONDITION'] == 'Waiting test...'].index)]
                labels = ['A', 'B', 'JUNK', 'Waiting Testing']
                explode = [0.1, 0, 0,0]
                self.MplWidget.canvas.axes.pie(values, labels=labels, explode=explode,
                                               autopct='%1.1f%%', shadow=True, startangle=140)
                self.MplWidget.canvas.axes.set_title('CONDITION STATISTICS')
                self.MplWidget.canvas.draw()
            elif self.elast_radio_stats_3.isChecked():
                elastomer_df = pd.read_sql('select distinct ELASTOMER from Pumps',con=conn)
                elastomer_count = []
                labels = []
                explode = []
                for i in list(elastomer_df['ELASTOMER']):
                    elastomer_count.append(len(df3[df3['ELASTOMER'] == i].index))
                    labels.append(i)
                    explode.append(0)
                explode[-1]=0.1

                self.MplWidget.canvas.axes.pie(elastomer_count, labels=labels, explode=explode,
                                               autopct='%1.1f%%', shadow=True, startangle=140)
                self.MplWidget.canvas.axes.set_title('ELASTOMER STATISTICS')
                self.MplWidget.canvas.draw()
        except:
            QMessageBox.information(self, "Error", 'Something went wrong')

    def add_test_results(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        var21 = self.serial2_ent_2.text()            
        var22 = self.ent_capacity_2.currentText()            
        var23 = self.loc_ent_2.text()
        var24 = self.dte_test.date().toString(QtCore.Qt.ISODate)
        var25 = self.effmaxlif.text()
        var26 = self.sum.currentText()
        var27 = self.rtr.currentText()
        var28 = self.str.currentText()
        var29 = self.tbar.currentText()
        var30 = self.comm.text()

        try:    
            if var21 != '':
                if self.ftrradbtn.isChecked():
                    qur20 = "insert into BenchTest (SERIAL_NO,PUMP_MODEL,PO_FROM,TEST_DATE,TEST_TYPE,EFF_MAX_LIFT,SUMMARY,RTR_INSP,STR_INSP,TAGBAR_INSP,COMMENT,TEST_FILE_LINK) values ('{}','{}','{}','{}','Factory test report','{}','{}','{}','{}','{}','{}','{}')".format (var21,var22,var23,var24,int(var25),var26,var27,var28,var29,var30,self.pdf_path)
                    cur.execute(qur20)            
                    check = QMessageBox.question(self, 'Data confirmation',
                                                    "Test results will be added to database.Do you like to continue?",
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if check == QMessageBox.Yes:
                        conn.commit()
                        self.effatzero_2.setText("<h1 >Test result has been successfully added to database </h1>")
                        self.serial2_ent_2.setText("")
                    else:
                        conn.close()
                elif self.btrradbtn.isChecked():
                    qur20 = "insert into BenchTest (SERIAL_NO,PUMP_MODEL,PO_FROM,TEST_DATE,TEST_TYPE,EFF_MAX_LIFT,SUMMARY,RTR_INSP,STR_INSP,TAGBAR_INSP,COMMENT,TEST_FILE_LINK) values ('{}','{}','{}','{}','Bench test report','{}','{}','{}','{}','{}','{}','{}')".format (var21,var22,var23,var24,int(var25),var26,var27,var28,var29,var30,self.pdf_path)
                    cur.execute(qur20)            
                    check = QMessageBox.question(self, 'Data confirmation',
                                                    "Test results will be added to database.Do you like to continue?",
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if check == QMessageBox.Yes:
                        conn.commit()
                        self.effatzero_2.setText("<h1 >Test result has been successfully added to database </h1>")
                        self.serial2_ent_2.setText("")
                    else:
                        conn.close()
                else:
                    QMessageBox.information(self, "Entry Error", 'Select test type')                                                                        

            else:
                QMessageBox.information(self, "Entry Error", 'Pump serial number is a mandatory field')                                                                        
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')

    def load_tests(self):
        try:
            self.label_72.clear()
            if self.serial2_ent_3.text() != '':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("SELECT TEST_DATE,TEST_TYPE,PO_FROM,SUMMARY from BenchTest where SERIAL_NO = '{}' order by TEST_DATE".format(self.serial2_ent_3.text()))
                check30=cur.fetchall()
                self.btr_search.setRowCount(0)
                if len(check30) > 0:
                    row_count= 0
                    for row_num, all_data in enumerate(check30):
                        self.btr_search.insertRow(row_num)
                        for col__num, data in enumerate(all_data):
                            self.btr_search.setItem(row_num, col__num, QTableWidgetItem(str(data)))
                    res = str(self.btr_search.rowCount())
                    self.label_79.setText(res)
                    conn.close()    
                else:
                    self.label_79.setText("0")
                    QMessageBox.information(self, "Error", 'No tests for this pump serial saved in database')   
            else:
                QMessageBox.information(self, "Error", 'Define pump serial number')     

        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')


    def get_from_btrsearch_table (self, row):
        if self.btr_search.item(row, 0) == None: 
            pass
        else:
            global date_of_test_result_of_interest
            item1 = self.btr_search.item(row, 0)
            date_of_test_result_of_interest= item1.text()
            self.pushButton_21.setEnabled(True)


    def view_test_result(self):
        try:
            if self.serial2_ent_3.text() != '':
                conn = sql.connect("PCP_Database")
                cur = conn.cursor()
                cur.execute("SELECT * from BenchTest where SERIAL_NO = '{}' and TEST_DATE= '{}'".format(self.serial2_ent_3.text(),date_of_test_result_of_interest))              
                qur105 = cur.fetchall()                             
                if len(qur105) > 0:
                    self.label_69.setText(qur105[0][1])       
                    self.label_74.setText(str(qur105[0][5]))       
                    self.textBrowser_13.setText(qur105[0][10])           
                    self.label_57.setText(qur105[0][7])
                    self.label_58.setText(qur105[0][8])
                    self.label_59.setText(qur105[0][9])
                else:
                    QMessageBox.information(self, "Error", 'No tests available, Check test date')     
            else:
                QMessageBox.information(self, "Error", 'Define pump serial number')     
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')

    
    def display_get_file_path_dialog(self):        
        self.pdf_path , val =QFileDialog.getOpenFileName(None , 'choose file',os.getcwd(),'Pdf Files(*.pdf)')


    def viewpdfbuttonstatus (self):
        if self.label_79.text() == ""  or self.label_79.text() == "0":
            self.pushButton_21.setEnabled(False)
        else:
            self.pushButton_21.setEnabled(True)

    def view_test_report (self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        cur.execute("SELECT TEST_FILE_LINK from BenchTest where SERIAL_NO = '{}' and TEST_DATE='{}'".format(self.serial2_ent_3.text(),date_of_test_result_of_interest))     
        records = cur.fetchone()
        if records[0] != '':
            file_path = records[0]
            os.startfile(file_path)
        elif records[0]=='':
            QMessageBox.information(self, "Error", 'No reports attached')

    def delete_test_result(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        cur.execute("select * from Admins where USERNAME = '{}'".format(user_name))
        check_admin = cur.fetchall()
        if len(check_admin) > 0 or user_name == "admin":
            try:
                if self.serial2_ent_3.text() != '':
                    conn = sql.connect("PCP_Database")
                    cur = conn.cursor()
                    cur.execute("select * from BenchTest where SERIAL_NO = '{}' and TEST_DATE= '{}'".format(self.serial2_ent_3.text(),date_of_test_result_of_interest))              
                    qur105 = cur.fetchall()                             
                    if len(qur105) > 0:
                        cur.execute("Delete from BenchTest where SERIAL_NO = '{}' and TEST_DATE= '{}'".format(self.serial2_ent_3.text(),date_of_test_result_of_interest))              
                        conn.commit()
                    else:
                        QMessageBox.information(self, "Error", 'No tests available, Check test date')     
                else:
                    QMessageBox.information(self, "Error", 'Define pump serial number')     
            except:
                QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection')     
        else:
            QMessageBox.information(self, "Sorry {}".format(user_name),
                                    'For database security, deleting test results can be only accessed by admins')      

    def add_admin(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_admin = self.capacity_conf_4.text()
            new_pass = self.capacity_conf_5.text()
            if new_admin != '' and new_pass !='':
                cur.execute("select * from Admins where USERNAME = '{}' ".format(new_admin))
                check33 = cur.fetchall()
                cur.execute("select * from Users where USERNAME = '{}' ".format(new_admin))
                check34 = cur.fetchall()
                if len(check33) == 0 and len(check34)==0 :
                    cur.execute("insert into Admins (USERNAME,PASSWORD) values ('{}','{}')".format(new_admin,new_pass))
                    conn.commit()
                    QMessageBox.information(self, "Success", '[{}] has been added'.format(new_admin))
                    self.autocompleteadmins()
                    self.capacity_conf_4.clear()
                    self.capacity_conf_5.clear()
                else:
                    QMessageBox.information(self, "Entry error", '[{}] already exist in database'.format(new_admin))
            else:
                QMessageBox.information(self, "Error", 'Type username and password')
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    def del_admin(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            admin = self.del_admin_text.text()
            if admin != '' :
                cur.execute("select * from Admins where USERNAME = '{}' ".format(admin))
                check34 = cur.fetchall()
                if len(check34) > 0:
                    cur.execute("delete from Admins  where USERNAME = '{}' ".format(admin))
                    conn.commit()
                    QMessageBox.information(self, "Success", '[{}] has been removed from database'.format(admin))
                    self.del_admin_text.clear()
                elif len(check34) == 0:
                    QMessageBox.information(self, "Entry error", '[{}] isnot an admin'.format(admin))
            else:
                QMessageBox.information(self, "Error", 'Type admin username to be removed')
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    def add_user(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_user = self.add_user_text.text()
            new_upass = self.userpassword_text.text()
            if new_user != '' and new_upass !='':
                cur.execute("select * from Users where USERNAME = '{}' ".format(new_user))
                check35 = cur.fetchall()
                cur.execute("select * from Admins where USERNAME = '{}' ".format(new_user))
                check36 = cur.fetchall()                
                if len(check35) == 0 and len(check36) == 0:
                    cur.execute("insert into Users (USERNAME,PASSWORD) values ('{}','{}')".format(new_user,new_upass))
                    conn.commit()
                    QMessageBox.information(self, "Success",' [{}] has been added'.format(new_user))
                    self.autocompleteusers()
                    self.add_user_text.clear()
                    self.userpassword_text.clear()
                else:
                    QMessageBox.information(self, "Entry error", '[{}] already exist in users database'.format(new_user))
            else:
                QMessageBox.information(self, "Error", 'Type username and password')
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    def del_user(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            uuser = self.del_user_text.text()
            if uuser != '' :
                cur.execute("select * from Users where USERNAME = '{}' ".format(uuser))
                check36 = cur.fetchall()
                if len(check36) > 0:
                    cur.execute("delete from Users  where USERNAME = '{}' ".format(uuser))
                    conn.commit()
                    QMessageBox.information(self, "Success", '[{}] has been removed from database'.format(uuser))
                    self.del_user_text.clear()
                elif len(check36) == 0:
                    QMessageBox.information(self, "Entry error", '[{}] doesnot exist in users database'.format(uuser))
            else:
                QMessageBox.information(self, "Error", 'Type username to be removed')
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    def add_brand(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_brand = self.brand_conf.text().capitalize()
            if new_brand != '':
                cur.execute("insert into brand_lib (brand) values ('{}')".format(new_brand))
                cur.execute("insert into capacity_lib (brand,pump_capacity) values ('{}','')".format(new_brand))
                cur.execute("insert into elastomer_lib (brand,elastomer) values ('{}','')".format(new_brand))
                conn.commit()
                self.statusBar().showMessage('[{}] has been added to brands list'.format (self.brand_conf.text()), 5000)
                self.brand_conf.clear()
                self.load_brandcombos()                       # load options of all comboboxes

            else:
                QMessageBox.information(self, "Error", 'Type brand to be added')
        except:
            QMessageBox.information(self, "Error", '[{}] already exists in brands list'.format(new_brand))

    def remove_brand(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_brand = self.comboBox_2.currentText()
            if new_brand != 'Select brand':
                cur.execute("delete from brand_lib where brand = '{}'".format(new_brand))
                cur.execute("delete from capacity_lib where brand = '{}'".format(new_brand))
                cur.execute("delete from elastomer_lib where brand = '{}'".format(new_brand))
                check = QMessageBox.warning(self, 'Confirmation',
                        "Brand '{}' and all its related elastomers and models will be permenantly deleted from database.Do you like to continue?".format(new_brand),
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if check == QMessageBox.Yes:    
                    conn.commit()
                    self.statusBar().showMessage('[{}] has been deleted from brands list'.format (self.comboBox_2.currentText()), 5000)
                    self.comboBox_2.clear()
                    self.load_brandcombos()                       # load options of all comboboxes
                else:
                    conn.close()
            else:
                QMessageBox.information(self, "Error", 'Select brand to be deleted.')
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    
    def add_capacity(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_capacity = self.capacity_conf.text()
            if self.comboBox_6.currentText() != "Select brand":
                if new_capacity != "":
                    cur.execute ("select * from capacity_lib where brand='{}' and pump_capacity='{}'".format(self.comboBox_6.currentText(),new_capacity))
                    c=cur.fetchall()
                    if len(c) == 0 :
                        cur.execute("insert into capacity_lib (brand,pump_capacity) values ('{}','{}')".format(self.comboBox_6.currentText(),new_capacity))
                        conn.commit()
                        self.statusBar().showMessage('[{}] has been added to [{}] models list'.format (self.capacity_conf.text(),self.comboBox_6.currentText()), 5000)
                        self.comboBox_6.setCurrentIndex(0)
                        self.capacity_conf.clear()
                        self.loadfourthlinkedcombo()
                    else:
                        QMessageBox.information(self, "Error", '[{}] already exists in [{}] models'.format(self.capacity_conf.text(),self.comboBox_6.currentText()))
                else:
                    QMessageBox.information(self, "Error", 'Enter pump model')
            else:
                QMessageBox.information(self, "Error", 'Select brand')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def remove_capacity(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_capacity = self.comboBox.currentText()
            if self.comboBox_7.currentText() != "Select brand" :
                if new_capacity != '':
                    cur.execute("delete from capacity_lib where brand= '{}' and pump_capacity= '{}'".format(self.comboBox_7.currentText(),self.comboBox.currentText()))
                    conn.commit()
                    self.statusBar().showMessage('[{}] has been deleted from [{}] models list'.format (new_capacity,self.comboBox_7.currentText()), 5000)
                    self.comboBox_7.setCurrentIndex(0)
                    self.comboBox.clear()
                    self.loadfourthlinkedcombo()
                else:
                    QMessageBox.information(self, "Error", 'Select model to be deleted')
            else:
                QMessageBox.information(self, "Error", 'Select brand')                
        except:
            QMessageBox.information(self, "Error", 'Check database connection')

    def add_elastomer(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_elastomer = self.elast_conf.text()
            if new_elastomer != 'Select elastomer type':
                if self.comboBox_9.currentText() != "Select brand":
                    cur.execute ("select * from elastomer_lib where brand='{}' and elastomer='{}'".format(self.comboBox_9.currentText(),new_elastomer))
                    c=cur.fetchall()
                    if len(c) == 0 :
                        cur.execute("insert into elastomer_lib (brand,elastomer) values ('{}','{}')".format(self.comboBox_9.currentText(),new_elastomer))
                        conn.commit()
                        self.statusBar().showMessage('[{}] has been added to [{}] elastomers list'.format (new_elastomer,self.comboBox_9.currentText()), 5000)                    
                        self.elast_conf.clear()
                        self.comboBox_9.setCurrentIndex(0)
                        self.loadthirdlinkedcombo()                   
                    else:
                        QMessageBox.information(self, "Error", '[{}] already exists in [{}] elastomers'.format(new_elastomer,self.comboBox_9.currentText()))
                else:
                    QMessageBox.information(self, "Error", 'Select Brand')
            else:
                QMessageBox.information(self, "Error", 'Type elastomer to be added')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might lost connection to database')

    def remove_elastomer(self):
        try:
            conn = sql.connect("PCP_Database")
            cur = conn.cursor()
            new_elastomer = self.comboBox_3.currentText()
            if self.comboBox_8.currentText() !="Select brand":
                if new_elastomer != 'Select elastomer type':
                    cur.execute("delete from elastomer_lib where brand='{}' and elastomer= '{}'".format(self.comboBox_8.currentText(),new_elastomer))
                    conn.commit()
                    self.statusBar().showMessage('[{}] has been deleted from [{}] elastomers list'.format (new_elastomer,self.comboBox_8.currentText()), 5000)
                    self.comboBox_8.setCurrentIndex(0)
                    self.comboBox_3.clear()
                    self.loadthirdlinkedcombo()
                else:
                    QMessageBox.information(self, "Error", 'Select elastomer type')
            else:
                QMessageBox.information(self, "Error", 'Select Brand')        
        except:
            QMessageBox.information(self, "Error", 'Check database connection')



    def hideconfigpanel (self):
        self.groupBox.hide()

    def showuserpanel (self):
        self.groupBox.show()
        self.stackedWidget_2.setCurrentIndex(0)

    def showspecspanel (self):
        self.groupBox.show()
        self.stackedWidget_2.setCurrentIndex(1)

    def showwellpanel (self):
        self.groupBox.show()
        self.stackedWidget_2.setCurrentIndex(2)

# Help Window
    # class Help(QDialog, Ui_Form):
    #     def __init__(self):
    #         QDialog.__init__(self)
    #         self.setupUi(self)
 

# Calculator Window:
"""
Simple calculator used to calculate life time of pump, to be updated in records
"""


class Calculator(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.calc_btn.clicked.connect(self.calc)

    def calc(self):
        rih_date = self.dte_rih.date().toPyDate()
        pooh_date = self.dte_pooh.date().toPyDate()
        diff = (pooh_date - rih_date).days
        try:
            if self.last_run.text() != "":
                cum = diff + int(self.last_run.text())
                final_cum = str(cum)
            else:
                cum = diff
                final_cum = str(cum)
            self.res_lbl.setText(final_cum)
        except:
            pass


# Bench test Report Window:
"""
Separate Window to upload bench test data, when add bench test report button is pressed from records
"""


class AdBeRe(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.get_test_link.clicked.connect(self.display_get_file_path_dialog)    # Error while applying method
        self.addbtr_btn.clicked.connect(self.add_test)
        self.loadcombobox()   
        conn = sql.connect("PCP_Database")
        df_ser = pd.read_sql('select SERIAL from Pumps', con=conn) 
        serlist = []
        for i in list(df_ser['SERIAL']):
            x= str(i)
            serlist.append(x)
        availableserials = QCompleter (serlist)
        self.serial2_ent_2.setCompleter(availableserials)

    def loadcombobox (self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        df_capacity = pd.read_sql('select * from capacity_lib', con=conn)
        self.ent_capacity_2.addItems(df_capacity['pump_capacity'])
        today = QDate.currentDate()
        self.dte_test.setDate(today)

    def add_test(self):
        conn = sql.connect("PCP_Database")
        cur = conn.cursor()
        var21 = self.serial2_ent_2.text()
        var22 = self.ent_capacity_2.currentText()
        var23 = self.loc_ent_2.text()
        var24 = self.dte_test.date().toString(QtCore.Qt.ISODate)
        var25 = self.effmaxlif.text()
        var26 = self.sum.currentText()
        var27 = self.rtr.currentText()
        var28 = self.str.currentText()
        var29 = self.tbar.currentText()
        var30 = self.comm.toPlainText()
        today = QDate.currentDate()

        try:
            pumps_list = list(pd.read_sql('select SERIAL from Pumps', con=conn)['SERIAL'])
            if var21 != '':
                if var21 in pumps_list:
                    if int(var25) <= 100 and int(var25) >= 0:
                        if self.dte_test.date() <= today :
                            if self.ftrradbtn.isChecked():
                                qur20 = "insert into BenchTest (SERIAL_NO,PUMP_MODEL,PO_FROM,TEST_DATE,TEST_TYPE," \
                                        "EFF_MAX_LIFT,SUMMARY,RTR_INSP,STR_INSP,TAGBAR_INSP,COMMENT,TEST_FILE_LINK) " \
                                        "values ('{}','{}','{}','{}','Factory test report','{}','{}','{}','{}','{}','{}'," \
                                        "'{}')".format (var21,var22,var23,var24,int(var25),var26,var27,var28,var29,var30,
                                                        pdf_path)
                                cur.execute(qur20)
                                check = QMessageBox.question(self, 'Data confirmation',
                                                                "Test results will be added to database.Do you like to continue?",
                                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if check == QMessageBox.Yes:
                                    conn.commit()
                                    self.statusBar().showMessage('Test result has been successfully added to database ',5000)
                                    self.serial2_ent_2.clear()
                                    self.ent_capacity_2.setCurrentIndex(0)
                                    self.dte_test.setDate(today)
                                    self.effmaxlif.clear()
                                    self.loc_ent_2.clear()
                                    self.sum.setCurrentIndex(0)
                                    self.rtr.setCurrentIndex(0)
                                    self.str.setCurrentIndex(0)
                                    self.tbar.setCurrentIndex(0)
                                    self.comm.setPlainText("")
                                else:
                                    conn.close()
                            elif self.btrradbtn.isChecked():
                                qur20 = "insert into BenchTest (SERIAL_NO,PUMP_MODEL,PO_FROM,TEST_DATE,TEST_TYPE," \
                                        "EFF_MAX_LIFT,SUMMARY,RTR_INSP,STR_INSP,TAGBAR_INSP,COMMENT,TEST_FILE_LINK) " \
                                        "values ('{}','{}','{}','{}','Bench test report','{}','{}','{}','{}','{}','{}','{}')"\
                                    .format (var21,var22,var23,var24,int(var25),var26,var27,var28,var29,var30,pdf_path)
                                cur.execute(qur20)
                                check = QMessageBox.question(self, 'Data confirmation',
                                                                "Test results will be added to database.Do you like to continue?",
                                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if check == QMessageBox.Yes:
                                    conn.commit()
                                    self.statusBar().showMessage('Test result has been successfully added to database ',5000)
                                    self.serial2_ent_2.clear()
                                    self.ent_capacity_2.setCurrentIndex(0)
                                    self.effmaxlif.clear()
                                    self.loc_ent_2.clear()
                                    self.sum.setCurrentIndex(0)
                                    self.rtr.setCurrentIndex(0)
                                    self.str.setCurrentIndex(0)
                                    self.tbar.setCurrentIndex(0)
                                    self.comm.setPlainText("")
                                else:
                                    conn.close()
                            elif self.btrradbtn.isChecked() and self.ftrradbtn.isChecked():
                                QMessageBox.information(self, "Entry Error", 'Please select only one test type.')   
                            else:
                                qur20 = "insert into BenchTest (SERIAL_NO,PUMP_MODEL,PO_FROM,TEST_DATE,TEST_TYPE," \
                                        "EFF_MAX_LIFT,SUMMARY,RTR_INSP,STR_INSP,TAGBAR_INSP,COMMENT) " \
                                        "values ('{}','{}','{}','{}','Factory test report','{}','{}','{}','{}','{}','{}')" "\
                                        ".format (var21,var22,var23,var24,int(var25),var26,var27,var28,var29,var30)
                                cur.execute(qur20)
                                check = QMessageBox.question(self, 'Data confirmation',
                                                                "Test results will be added to database without attaching test report.Do you like to continue?",
                                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if check == QMessageBox.Yes:
                                    conn.commit()
                                    self.statusBar().showMessage('Test result has been successfully added to database ',5000)
                                    self.serial2_ent_2.clear()
                                    self.ent_capacity_2.setCurrentIndex(0)
                                    self.effmaxlif.clear()
                                    self.loc_ent_2.clear()
                                    self.sum.setCurrentIndex(0)
                                    self.rtr.setCurrentIndex(0)
                                    self.str.setCurrentIndex(0)
                                    self.tbar.setCurrentIndex(0)
                                    self.comm.setPlainText("")
                                else:
                                    conn.close()
                    
                        else:
                            QMessageBox.information(self, "Entry Error", 'Test date isnot logic')                     
                    else:
                        QMessageBox.information(self, "Entry Error", 'Efficiency must be in the range of [0-100]') 
                else:
                    QMessageBox.information(self, "Entry Error", '{} doesnot exist in your pumps database'
                                                                 ', please add pump then add test result'.format(var21))
            else:
                QMessageBox.information(self, "Entry Error", 'Pump serial number is a mandatory field')
        except:
            QMessageBox.information(self, "Error", 'Something went wrong or you might have lost connection ')

    def display_get_file_path_dialog(self):
        global pdf_path
        pdf_path , val =QFileDialog.getOpenFileName(None , 'choose file',os.getcwd(),'Pdf Files(*.pdf)')



my_app = QApplication([])
my_app_window = Login()
my_app_window.show()
my_app.exec_()