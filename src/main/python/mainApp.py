# -*- coding: utf-8 -*-
import ast
import json
from builtins import type

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from datetime import datetime, timedelta

import paramiko
import pyperclip

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidgetItem, qApp, QInputDialog, QFrame, QRadioButton, \
    QButtonGroup, QFileDialog, QDialog
import sys

from PyQt5.QtWidgets import QMessageBox

from guiDesign import Ui_MainWindow
from functools import partial
import os
import ThreadGui
from Looding import LoadingScreen


class MainClassGUI(QMainWindow, Ui_MainWindow, ApplicationContext):
    def __init__(self, parent=None):
        super(MainClassGUI, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.setGeometry(0, 0, 1200, 700)
        self.center()
        self.setWindowIcon(QtGui.QIcon(self.get_resource('images') + '/mcl.png'))

        self.icon_path = self.get_resource("images")
        self.conf_path = self.get_resource('configuration')
        self.configFilePath = self.get_resource('configuration') + "/foc.info"
        self.lang_file_path = self.get_resource('configuration') + "/lang/"
        self.lang_icon_path = self.get_resource('images') + "/lang_icons"
        self.server_info_file_name = self.conf_path + "/servers.info"
        self.person_info_file_name = self.conf_path + "/persons.info"

        self.radioButtonsLang = []
        self.conf_file_content = ""
        self.conf_lang_info = ""
        self.choose_server_text = ""
        self.last_update = ""
        self.synchronous = ""
        self.asynchronous = ""
        self.review = ""
        self.review_and_confirm = ""
        self.active_text = ""
        self.deactive_text = ""
        self.long_chain_blocks = ""

        # Messages
        # --------------------------------------------------
        self.msg_title_warning = ""
        self.msg_title_info = ""
        self.msg_connection_establish = ""
        self.msg_check_info = ""
        self.msg_missing_info = ""
        self.msg_fill_blank = ""
        self.msg_you_did_not_choose_a_server = ""
        self.msg_please_select_server = ""
        self.msg_do_you_want_to_make_changes = ""
        self.msg_success_to_save = ""
        self.msg_do_you_want_to_connect_server = ""
        self.msg_do_you_want_to_request = ""
        self.msg_do_you_want_endorser = ""
        self.msg_do_you_want_to_accept = ""
        self.msg_credit_confirmaiton = ""
        self.msg_do_you_want_to_send_coin = ""
        self.msg_sended_coin = ""
        self.msg_do_you_want_to_acitvate_coins = ""
        self.msg_do_you_want_to_deacitvate_coins = ""
        self.msg_succes_lock = ""
        self.msg_unsucces_lock = ""
        self.msg_succes_unlock = ""
        self.msg_unsucces_unlock = ""
        self.msg_succes_request = ""
        self.msg_unsucces_request = ""
        self.msg_succes_request_aceept = ""
        self.msg_unsucces_request_aceept = ""
        self.msg_start_chain = ""
        self.msg_stop_chain = ""
        self.msg_stop_chain_last = ""
        self.msg_error_loop_details = ""
        self.msg_enter_correct_info = ""
        self.msg_mcl_not_installed = ""
        self.msg_yes = ""
        self.msg_no = ""
        self.msg_accept = ""
        self.msg_ok = ""

        # Saved server info parameters
        self.server_all_info = ""
        self.server_list = []
        self.message_button_return_boolean = False
        self.mcl_install_file_path = ""
        self.is_chain_run = False
        self.is_mcl_install = False
        self.person_list = []

        # Server information to login
        # --------------------------------------------------
        self.server_nickname = ""
        self.server_username = ""
        self.server_hostname = ""
        self.server_password = ""
        self.server_port = 22

        self.pubkey = ""
        self.walletAdress = ""
        self.privkey = ""
        self.chain_info = ""
        self.request_credit_out = ""
        self.first_request_list = []
        self.request_list_in_loop = []
        self.holder_list = []
        self.output_auto_install = "INSTALL LOG\n**********************************\n"
        self.progressBarValue = 0
        self.last_matures_minute = ""

        # Install commands parameters
        # --------------------------------------------------
        self.mcl_compiler_zip_command = "wget http://www.marmara.io/guifiles/Linux-MCL-HF.zip"
        self.mcl_unzip_install_command = "sudo apt-get install unzip"
        self.mcl_compiler_unzip_command = "unzip Linux-MCL-HF.zip"
        self.mcl_permission_command = "sudo chmod +x komodod komodo-cli fetch-params.sh"
        self.mcl_fetch_parameters_command = "./fetch-params.sh"

        # Komodo commands parameters
        # --------------------------------------------------
        self.command_start_mcl_mining_without_pubkey = "komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 -addnode=37.148.210.158 -addnode=37.148.212.36 -addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 -ac_staked=75 -ac_reward=3000000000"
        self.command_get_adress = "komodo-cli -ac_name=MCL getnewaddress"
        self.command_get_pubkey = "komodo-cli -ac_name=MCL validateaddress"
        self.command_get_adress_convertpassphrase = "komodo-cli -ac_name=MCL convertpassphrase "
        self.command_get_privkey = "komodo-cli -ac_name=MCL dumpprivkey  "

        self.command_start_mcl_mining_with_pubkey = "komodod -ac_name=MCL -ac_supply=2000000 -ac_cc=2 " \
                                                    "-addnode=37.148.210.158 -addnode=37.148.212.36 " \
                                                    "-addnode=46.4.238.65 -addressindex=1 -spentindex=1 -ac_marmara=1 " \
                                                    "-ac_staked=75 -ac_reward=3000000000 -gen -genproclimit=-1 " \
                                                    "-pubkey="
        self.command_mcl_get_info = "komodo-cli -ac_name=MCL getinfo"
        self.command_mcl_marmara_get_info = "komodo-cli -ac_name=MCL marmarainfo 0 0 0 0 "
        self.command_mcl_get_stacking_and_mining = "komodo-cli -ac_name=MCL getgenerate"
        self.command_mcl_stop_chain = "komodo-cli -ac_name=MCL stop"

        self.command_mcl_lock_coin = "komodo-cli -ac_name=MCL marmaralock "
        self.command_mcl_unlock_coin = "komodo-cli -ac_name=MCL marmaraunlock "
        self.command_mcl_coin_sendrawtransaction = "komodo-cli -ac_name=MCL sendrawtransaction "
        self.command_mcl_send_coin = "komodo-cli -ac_name=MCL sendtoaddress "
        self.command_mcl_request_creadit_loop = "komodo-cli -ac_name=MCL marmarareceivelist "

        self.command_mcl_set_mining = "komodo-cli -ac_name=MCL setgenerate true "
        self.command_mcl_set_stacking = "komodo-cli -ac_name=MCL setgenerate true 0"
        self.command_mcl_set_off_generate = "komodo-cli -ac_name=MCL setgenerate false"

        self.command_mcl_credit_request = "komodo-cli -ac_name=MCL marmarareceive "
        self.command_mcl_credit_request_countine = """'{"avalcount":"0"}'"""

        self.command_mcl_credit_request_list = "komodo-cli -ac_name=MCL marmarareceivelist "
        self.command_mcl_credit_request_accept = "komodo-cli -ac_name=MCL marmaraissue "
        self.command_mcl_credit_request_accept_countine = """ '{"avalcount":"0", "autosettlement":"true", "autoinsurance":"true", "disputeexpires":"0", "EscrowOn":"false", "BlockageAmount":"0" }' """

        self.command_mcl_marmaratransfer_accept = "komodo-cli -ac_name=MCL marmaratransfer "
        self.command_mcl_marmaratransfer_accept_countine = """'{"avalcount":"0"}'"""

        self.command_mcl_credit_loop_search = "komodo-cli -ac_name=MCL marmaracreditloop "
        self.command_mcl_marmar_holders = "komodo-cli -ac_name=MCL marmaraholderloops "
        self.command_mcl_marmar_holders_min_matures = "0"
        self.command_mcl_marmar_holders_max_matures = "0"
        self.command_mcl_marmar_holders_min_amount = "0"
        self.command_mcl_marmar_holders_max_amount = "0"

        self.command_mcl_wallet_list = "komodo-cli -ac_name=MCL listaddressgroupings"

        # While started, running
        # --------------------------------------------------
        self.readConfFile()
        self.readLangFile()
        self.guiObjectSetStyleSheet()
        self.readServersInfo()
        self.readPersons()


        self.progressBar_2.setValue(self.progressBarValue)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_3.setTabEnabled(7, False)

        # Button Triggers
        # --------------------------------------------------
        self.pushButton_22.clicked.connect(partial(self.buttonClickAddServer))
        self.pushButton_24.clicked.connect(partial(self.buttonClickNewServerInfoSave))
        self.pushButton_21.clicked.connect(partial(self.buttonClickSshConnect))
        self.pushButton_5.clicked.connect(partial(self.buttonClickAutoInstaller))
        self.pushButton_10.clicked.connect(partial(self.buttonClickCreateWallet))
        self.pushButton_36.clicked.connect(partial(self.buttonClickCreateWallet))
        self.pushButton_23.clicked.connect(partial(self.buttonClickGoToLogin))
        self.pushButton_4.clicked.connect(self.buttonClickExitServer)
        self.pushButton_2.clicked.connect(self.buttonClickDeleteServer)
        self.pushButton_12.clicked.connect(self.buttonClickEditServerPage)
        self.pushButton_25.clicked.connect(self.buttonClickGoToLogin)
        self.pushButton_26.clicked.connect(self.buttonClickEdit)
        self.pushButton_8.clicked.connect(self.buttonClickRefreshInformations)
        self.pushButton_17.clicked.connect(self.buttonClickStartChain)
        self.pushButton_11.clicked.connect(self.buttonClickStopChain)
        self.pushButton_13.clicked.connect(self.buttonClickLockCoin)
        self.pushButton_20.clicked.connect(self.buttonClickUnlockCoin)
        self.pushButton_19.clicked.connect(self.buttonClickCopyWalletAdress)
        self.pushButton_18.clicked.connect(self.buttonClickSendCoin)
        self.pushButton_27.clicked.connect(self.buttonClickCreditRequest)
        self.pushButton_14.clicked.connect(self.buttonClickPubkey)
        self.pushButton_7.clicked.connect(self.buttonClickCopyWalletAdress)
        self.pushButton_6.clicked.connect(self.buttonClickMining)
        self.pushButton_9.clicked.connect(self.buttonClickStacking)
        self.pushButton_29.clicked.connect(self.buttonClickRefreshAllCreditRequest)
        self.pushButton_33.clicked.connect(self.buttonClickRefreshAllCreditRequest)
        self.pushButton_30.clicked.connect(self.buttonClickRefreshAllCreditRequestCiranta)
        self.pushButton_32.clicked.connect(self.buttonClickRequestCiranta)
        self.pushButton_31.clicked.connect(self.buttonClickMarmaraCreditLoopDetails)
        self.pushButton_35.clicked.connect(self.buttonClickMarmaraHolders)
        self.pushButton_34.clicked.connect(self.buttonClickActiveLoops)
        self.pushButton_37.clicked.connect(self.buttonClickBackReturn)
        self.pushButton_38.clicked.connect(self.buttonClickSavePubkeyWallet)
        self.pushButton_39.clicked.connect(self.buttonClickNewAdress)
        self.pushButton_40.clicked.connect(self.buttonClickNewPubkey)
        self.pushButton_41.clicked.connect(self.buttonClickNewPersonSave)
        self.tabWidget_4.currentChanged.connect(self.tabWidgetOnChange)
        self.comboBox_3.currentTextChanged.connect(self.on_combobox_changed)

        # Click Enter
        self.lineEdit_6.returnPressed.connect(self.buttonClickSshConnect)
        self.checkBox_2.stateChanged.connect(self.state_changed_checkBox_2)
        self.checkBox_4.stateChanged.connect(self.state_changed_checkBox_4)
        self.checkBox_5.stateChanged.connect(self.state_changed_checkBox_5)
        self.dateTimeEdit.dateTimeChanged.connect(self.start_date_dateedit)
        self.dateTimeEdit_3.dateTimeChanged.connect(self.dateChangedHolderMin)
        self.dateTimeEdit_4.dateTimeChanged.connect(self.dateChangedHolderMax)
        # self.dateTimeEdit.clicked[QtCore.QDate].connect(self.start_date_dateedit)

        # Threads
        # --------------------------------------------------
        self.thread_auto_install = ThreadGui.AutoInstall()
        self.thread_start_chain = ThreadGui.StartChain()
        self.thread_refresh = ThreadGui.RefreshInformations()
        self.thread_stop_chain = ThreadGui.StopChain()
        self.thread_lock_coin = ThreadGui.LockCoin()
        self.thread_unlock_coin = ThreadGui.UnlockCoin()
        self.thread_send_coin = ThreadGui.SendCoin()
        self.thread_first_get_info = ThreadGui.RefreshInformations()
        self.thread_refresh_credit_request = ThreadGui.RefreshCreditRequest()
        self.thread_credit_request_accept = ThreadGui.CreditAccept()
        self.thread_credit_request = ThreadGui.CreditRequest()
        self.thread_credit_request_ciranta = ThreadGui.CreditRequest()
        self.thread_request_search = ThreadGui.SearchRequest()
        self.thread_holder_details_info = ThreadGui.SearchRequest()
        self.thread_list_holders = ThreadGui.SearchHolders()
        self.thread_active_list = ThreadGui.ActiveLoops()
        self.thread_ciranta_request_accept = ThreadGui.CirantaAccept()
        self.thread_create_wallet_after_install = ThreadGui.CreateWalletAdressAfterInstall()
        self.thread_create_wallet_click_button = ThreadGui.CreateWalletAdressClickButton()
        self.thread_create_wallet_convertpassphrase = ThreadGui.CreateWalletAdressConvertpassphrase()

        # Loading Gif
        # --------------------------------------------------
        self.loading_screen = LoadingScreen()

    def dateChangedHolderMin(self, date):
        self.dateTimeEdit_4.setMinimumDateTime(self.dateTimeEdit_3.dateTime().toPyDateTime())

    def dateChangedHolderMax(self, date):
        date_min = self.dateTimeEdit_3.dateTime().toPyDateTime() - datetime.now()
        date_max = self.dateTimeEdit_4.dateTime().toPyDateTime() - datetime.now()

    def state_changed_checkBox_2(self, int):
        if self.checkBox_2.isChecked():
            self.dateTimeEdit.setEnabled(False)
        else:
            self.dateTimeEdit.setEnabled(True)

    def state_changed_checkBox_4(self, int):
        if self.checkBox_4.isChecked():
            self.dateTimeEdit_3.setEnabled(False)
            self.dateTimeEdit_4.setEnabled(False)
        else:
            self.dateTimeEdit_3.setEnabled(True)
            self.dateTimeEdit_4.setEnabled(True)

    def state_changed_checkBox_5(self, int):
        if self.checkBox_5.isChecked():
            self.lineEdit_29.setEnabled(False)
            self.lineEdit_30.setEnabled(False)
        else:
            self.lineEdit_29.setEnabled(True)
            self.lineEdit_30.setEnabled(True)

    def start_date_dateedit(self, date):
        print("Change")

    def buttonClickNewPersonSave(self):
        if self.lineEdit_39.text() != "" and self.lineEdit_10.text() != "" and self.lineEdit_38.text() != "":
            try:
                dosya = open(self.person_info_file_name, 'a')
                person_infos = self.lineEdit_39.text() + ","
                person_infos = person_infos + self.lineEdit_10.text() + ","
                person_infos = person_infos + self.lineEdit_38.text() + "\n"
                dosya.write(person_infos)
            except IOError:
                print("Except error when read server file!")
            finally:
                dosya.close()

            self.readPersons()
            self.lineEdit_39.setText("")
            self.lineEdit_10.setText("")
            self.lineEdit_38.setText("")

            self.showDialogInfo(self.msg_title_info, self.msg_success_to_save, "", self.msg_ok)
        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def readPersons(self):
        isFilesEmpty = os.stat(self.person_info_file_name).st_size == 0
        if not isFilesEmpty:
            if os.path.isfile(self.person_info_file_name):
                try:
                    file = open(self.person_info_file_name, "r")
                    person_all_info = file.read().rstrip()
                    self.person_list = person_all_info.split("\n")
                except IOError:
                    print("Except error when read server file!")
                finally:
                    file.close()

        person_list_atr = []
        for list in self.person_list:
            tmp = list.split(",")
            person_list_atr.append(tmp)

        count_rows = int(self.tableWidget_5.rowCount())

        for index in range(count_rows):
            self.tableWidget_5.removeRow(index)

        self.tableWidget_5.setRowCount(len(self.person_list))
        row_index = 0

        for person in person_list_atr:
            name = QTableWidgetItem(person[0])
            self.tableWidget_5.setItem(row_index, 0, name)

            walletAdress_ = QTableWidgetItem(person[1])
            self.tableWidget_5.setItem(row_index, 1, walletAdress_)

            self.btn_wallet_coppy = QPushButton('')
            self.btn_wallet_coppy.setStyleSheet(
                    "QPushButton          {image: url("+self.icon_path+"/copy_wallet_icon_.png); border: 0; width: 30px; height: 30px;}"
                    "QPushButton::hover   {image: url("+self.icon_path+"/copy_wallet_icon_hover_.png);border:0px}"
                    "QPushButton::pressed {image: url("+self.icon_path+"/copy_wallet_icon_press_.png);border:0px}")
            self.btn_wallet_coppy.clicked.connect(self.buttonClickPersonCopyWalletAdress)
            self.tableWidget_5.setCellWidget(row_index, 2, self.btn_wallet_coppy)

            pubkey_ = QTableWidgetItem(person[2])
            self.tableWidget_5.setItem(row_index, 3, pubkey_)

            self.btn_pubkey_copy = QPushButton('')
            self.btn_pubkey_copy.setStyleSheet(
                                   "QPushButton          {image: url("+self.icon_path+"/copy_key_icon.png); border: 0; width: 15px; height: 15px;}"
                                   "QPushButton::hover   {image: url("+self.icon_path+"/copy_key_icon_hover.png);border:0px}"
                                   "QPushButton::pressed {image: url("+self.icon_path+"/copy_key_icon_press.png);border:0px}"
            )
            self.btn_pubkey_copy.clicked.connect(self.buttonClickPersonCopyPubkey)
            self.tableWidget_5.setCellWidget(row_index, 4, self.btn_pubkey_copy)

            self.btn_delete_person = QPushButton('')
            self.btn_delete_person.setStyleSheet(
                                   "QPushButton          {image: url("+self.icon_path+"/delete_person.png); border: 0; width: 15px; height: 15px;}"
                                   "QPushButton::hover   {image: url("+self.icon_path+"/delete_person_hover.png);border:0px}"
                                   "QPushButton::pressed {image: url("+self.icon_path+"/delete_person_press.png);border:0px}")
            self.btn_delete_person.clicked.connect(self.buttonClickPersonDelete)
            self.tableWidget_5.setCellWidget(row_index, 5, self.btn_delete_person)

            row_index = row_index + 1

    def buttonClickPersonDelete(self):
        button = self.sender()
        index = self.tableWidget_5.indexAt(button.pos())
        del self.person_list[index.row()]

        try:
            dosya = open(self.person_info_file_name, 'w')
            for list in self.person_list:
                dosya.write(list + "\n")
        except IOError:
            print("Except error when read server file!")
        finally:
            dosya.close()

        self.readPersons()

    def buttonClickPersonCopyWalletAdress(self):
        button = self.sender()
        index = self.tableWidget_5.indexAt(button.pos())

        if index.isValid():
            pyperclip.copy(self.tableWidget_5.item(index.row(), 1).text())

    def buttonClickPersonCopyPubkey(self):
        button = self.sender()
        index = self.tableWidget_5.indexAt(button.pos())
        if index.isValid():
            pyperclip.copy(self.tableWidget_5.item(index.row(), 3).text())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def createWalletAdressAfterInstall(self):
        self.thread_create_wallet_after_install = ThreadGui.CreateWalletAdressAfterInstall()

        self.loading_screen.startAnimation()

        self.thread_create_wallet_after_install.change_value_information_adress.connect(
            self.changingInformationCreateWalletAdress)
        self.thread_create_wallet_after_install.change_value_information_pubkey.connect(self.changingInformationPubkey)
        self.thread_create_wallet_after_install.change_value_information_privkey.connect(
            self.changingInformationPrivkey)
        self.thread_create_wallet_after_install.change_value_information_getinfo_check_chain_with_pubkey.connect(
            self.changingInformationGetInfoPubkeyCheck)

        self.thread_create_wallet_after_install.command_mcl_start_chain_without_pubkey = "./" + self.mcl_install_file_path + self.command_start_mcl_mining_without_pubkey
        self.thread_create_wallet_after_install.command_mcl_create_wallet_adress = "./" + self.mcl_install_file_path + self.command_get_adress
        self.thread_create_wallet_after_install.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info
        self.thread_create_wallet_after_install.command_mcl_get_pubkey = "./" + self.mcl_install_file_path + self.command_get_pubkey
        self.thread_create_wallet_after_install.command_mcl_get_privkey = "./" + self.mcl_install_file_path + self.command_get_privkey

        self.thread_create_wallet_after_install.server_username = self.server_username
        self.thread_create_wallet_after_install.server_hostname = self.server_hostname
        self.thread_create_wallet_after_install.server_password = self.server_password

        self.thread_create_wallet_after_install.start()

    def changingInformationPrivkey(self, val):
        self.privkey = val

    def changingInformationPubkey(self, val):
        self.lineEdit_33.setText(val)
        self.loading_screen.stopAnimotion()

    def changingInformationCreateWalletAdress(self, val):
        self.lineEdit_32.setText(val)

    def changingInformationGetInfoPubkeyCheck(self, val):
        y = json.loads(val)
        try:
            self.lineEdit_14.setText(y["pubkey"])
            self.pubkey = y["pubkey"]
            self.pushButton_17.setDisabled(True)
            self.pushButton_11.setDisabled(False)
        except:
            self.lineEdit_14.setText(self.lineEdit_14_withoutPubkey)

            self.thread_start_chain.quit()
            self.thread_refresh.quit()

            self.pushButton_17.setDisabled(True)
            self.pushButton_11.setDisabled(False)

    def buttonClickCreateWallet(self):
        if self.lineEdit_7.text() == "":
            self.thread_create_wallet_click_button = ThreadGui.CreateWalletAdressClickButton()

            self.loading_screen.startAnimation()

            self.thread_create_wallet_click_button.change_value_information_adress.connect(
                self.changingInformationCreateWalletAdress)
            self.thread_create_wallet_click_button.change_value_information_pubkey.connect(
                self.changingInformationPubkey)
            self.thread_create_wallet_click_button.change_value_information_privkey.connect(
                self.changingInformationPrivkey)
            self.thread_create_wallet_click_button.change_value_information_getinfo_check_chain_with_pubkey.connect(
                self.changingInformationGetInfoPubkeyCheck)

            self.thread_create_wallet_click_button.command_mcl_start_chain_without_pubkey = "./" + self.mcl_install_file_path + self.command_start_mcl_mining_without_pubkey
            self.thread_create_wallet_click_button.command_mcl_create_wallet_adress = "./" + self.mcl_install_file_path + self.command_get_adress
            self.thread_create_wallet_click_button.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info
            self.thread_create_wallet_click_button.command_mcl_get_pubkey = "./" + self.mcl_install_file_path + self.command_get_pubkey
            self.thread_create_wallet_click_button.command_mcl_get_privkey = "./" + self.mcl_install_file_path + self.command_get_privkey

            self.thread_create_wallet_click_button.server_username = self.server_username
            self.thread_create_wallet_click_button.server_hostname = self.server_hostname
            self.thread_create_wallet_click_button.server_password = self.server_password

            self.thread_create_wallet_click_button.start()
            self.stackedWidget.setCurrentIndex(1)

        else:
            words_group = self.lineEdit_7.text().split(" ")

            if len(words_group) == 12:
                if self.lineEdit_7.text() == self.lineEdit_3.text():
                    self.thread_create_wallet_convertpassphrase = ThreadGui.CreateWalletAdressConvertpassphrase()

                    self.loading_screen.startAnimation()

                    self.thread_create_wallet_convertpassphrase.change_value_information_adress.connect(
                        self.changingInformationCreateWalletAdress)
                    self.thread_create_wallet_convertpassphrase.change_value_information_pubkey.connect(
                        self.changingInformationPubkey)
                    self.thread_create_wallet_convertpassphrase.change_value_information_privkey.connect(
                        self.changingInformationPrivkey)
                    self.thread_create_wallet_convertpassphrase.change_value_information_getinfo_check_chain_with_pubkey.connect(
                        self.changingInformationGetInfoPubkeyCheck)

                    self.thread_create_wallet_convertpassphrase.command_mcl_start_chain_without_pubkey = "./" + self.mcl_install_file_path + self.command_start_mcl_mining_without_pubkey
                    self.thread_create_wallet_convertpassphrase.command_mcl_create_convertpassphrase = "./" + self.mcl_install_file_path + self.command_get_adress_convertpassphrase + "\"" + self.lineEdit_7.text() + "\""
                    self.thread_create_wallet_convertpassphrase.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info

                    self.thread_create_wallet_convertpassphrase.server_username = self.server_username
                    self.thread_create_wallet_convertpassphrase.server_hostname = self.server_hostname
                    self.thread_create_wallet_convertpassphrase.server_password = self.server_password

                    self.thread_create_wallet_convertpassphrase.start()
                    self.stackedWidget.setCurrentIndex(1)
                else:
                    self.showDialogInfo(self.msg_title_warning, "Girdiğiniz kelimeler uyuşmamamktadır.", "",
                                        self.msg_ok)
            else:
                self.showDialogInfo(self.msg_title_warning, "12 Kelime girmeniz gerekmektedir.", "", self.msg_ok)

    def buttonClickBackReturn(self):
        self.stackedWidget.setCurrentIndex(0)

    def buttonClickSavePubkeyWallet(self):
        dialog = QFileDialog()
        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
        dialog.setDefaultSuffix('txt')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['Text files (*.txt)'])
        if dialog.exec_() == QDialog.Accepted:
            file = open(dialog.selectedFiles()[0], 'w')
            text = "Agamapassphrase:  " + self.lineEdit_7.text() + "\n" + "Privkey:          " + self.privkey + "\n" + "Wallet Adress:    " + self.lineEdit_32.text() + "\n" + "Pubkey:           " + self.lineEdit_33.text()
            file.write(text)
            file.close()
        else:
            print('Cancelled')

    def buttonClickNewPubkey(self):
        pyperclip.copy(self.lineEdit_33.text())

    def buttonClickNewAdress(self):
        pyperclip.copy(self.lineEdit_32.text())

    def readLangFile(self):
        entries = os.listdir(self.lang_file_path)
        entries.sort()

        self.button_group = QButtonGroup()
        count_ = 0
        for i in entries:
            self.button_name = QRadioButton(i)
            self.radioButtonsLang.append(self.button_name)
            self.button_name.setIcon(QtGui.QIcon(self.lang_icon_path + "/" + i + ".png"))
            self.button_name.setIconSize(QtCore.QSize(32, 24))
            self.button_name.setObjectName("radiobtn_{}".format(count_))
            self.verticalLayout_6.addWidget(self.button_name)
            self.button_group.addButton(self.button_name, count_)
            self.button_name.toggled.connect(self.radio_button_event)

            # Combobox in login
            self.comboBox_3.addItem(i)
            self.comboBox_3.setItemIcon(count_, QtGui.QIcon(self.lang_icon_path + "/" + i + ".png"))

            if self.button_name.text() == self.conf_lang_info:
                self.button_name.setChecked(True)
                self.comboBox_3.setCurrentIndex(count_)
            count_ = count_ + 1

    def on_combobox_changed(self, value):
        self.conf_file_content["selected_lang"] = str(value)
        for radioB in self.radioButtonsLang:
            if radioB.text() == value:
                radioB.setChecked(True)
        tmp = json.dumps(self.conf_file_content)
        tmp = tmp.replace("{", "")
        tmp = tmp.replace("}", "")
        tmp = tmp.replace(",", "\n")
        f_ = open(self.conf_path + "/foc.info", "w")
        f_.write(tmp)
        f_.close()

        f = open(self.lang_file_path + value, "r", encoding="utf8")
        a = f.read()
        a = a.replace("\n", ",")
        res = ast.literal_eval("{" + a + "}")
        f.close()
        self.changeLangValues(res)

    def radio_button_event(self):
        rbtn = self.sender()
        if rbtn.isChecked():
            self.conf_file_content["selected_lang"] = rbtn.text()
            tmp = json.dumps(self.conf_file_content)
            tmp = tmp.replace("{", "")
            tmp = tmp.replace("}", "")
            tmp = tmp.replace(",", "\n")
            f_ = open(self.conf_path + "/foc.info", "w")
            f_.write(tmp)
            f_.close()

            f = open(self.lang_file_path + rbtn.text(), "r", encoding="utf8")
            a = f.read()
            a = a.replace("\n", ",")
            res = ast.literal_eval("{" + a + "}")
            f.close()
            self.changeLangValues(res)

    def changeLangValues(self, res):
        self.setWindowTitle(res["app_title"])
        self.label_2.setText(res["label_server_login"])
        self.pushButton_2.setText(res["button_delete"])
        self.pushButton_12.setText(res["button_edit"])
        self.pushButton_22.setText(res["button_add"])
        self.comboBox_2.setItemText(0, res["place_holder_choose_server"])
        self.choose_server_text = res["place_holder_choose_server"]
        self.lineEdit_6.setPlaceholderText(res["place_holder_password"])
        self.pushButton_21.setText(res["button_connect"])
        self.label_35.setText(res["label_name"])
        self.lineEdit_8.setPlaceholderText(res["label_name"])
        self.label_36.setText(res["label_server_username"])
        self.lineEdit_11.setPlaceholderText(res["label_server_username"])
        self.label_37.setText(res["label_server_ip"])
        self.lineEdit_17.setPlaceholderText(res["label_server_ip"])
        self.pushButton_24.setText(res["button_save"])
        self.pushButton_23.setText(res["button_login_page"])
        self.label_39.setText(res["label_name"])
        self.lineEdit_19.setPlaceholderText(res["label_name"])
        self.label_40.setText(res["label_server_username"])
        self.lineEdit_20.setPlaceholderText(res["label_server_username"])
        self.label_38.setText(res["label_server_ip"])
        self.lineEdit_18.setPlaceholderText(res["label_server_ip"])
        self.pushButton_26.setText(res["button_edit_save"])
        self.pushButton_25.setText(res["button_login_page"])

        self.msg_title_warning = res["msg_title_warning"]
        self.msg_title_info = res["msg_title_info"]
        self.msg_connection_establish = res["msg_connection_establish"]
        self.msg_check_info = res["msg_check_info"]
        self.msg_missing_info = res["msg_missing_info"]
        self.msg_fill_blank = res["msg_fill_blank"]
        self.msg_you_did_not_choose_a_server = res["msg_you_did_not_choose_a_server"]
        self.msg_please_select_server = res["msg_please_select_server"]
        self.msg_do_you_want_to_make_changes = res["msg_do_you_want_to_make_changes"]
        self.msg_success_to_save = res["msg_success_to_save"]
        self.msg_do_you_want_to_connect_server = res["msg_do_you_want_to_connect_server"]
        self.msg_do_you_want_to_request = res["msg_do_you_want_to_request"]
        self.msg_do_you_want_endorser = res["msg_do_you_want_endorser"]
        self.msg_do_you_want_to_accept = res["msg_do_you_want_to_accept"]
        self.msg_credit_confirmaiton = res["msg_credit_confirmaiton"]
        self.msg_do_you_want_to_send_coin = res["msg_do_you_want_to_send_coin"]
        self.msg_sended_coin = res["msg_sended_coin"]
        self.msg_do_you_want_to_acitvate_coins = res["msg_do_you_want_to_acitvate_coins"]
        self.msg_do_you_want_to_deacitvate_coins = res["msg_do_you_want_to_deacitvate_coins"]
        self.msg_succes_lock = res["msg_succes_lock"]
        self.msg_unsucces_lock = res["msg_unsucces_lock"]
        self.msg_succes_unlock = res["msg_succes_unlock"]
        self.msg_unsucces_unlock = res["msg_unsucces_unlock"]
        self.msg_succes_request = res["msg_succes_request"]
        self.msg_unsucces_request = res["msg_unsucces_request"]
        self.msg_succes_request_aceept = res["msg_succes_request_aceept"]
        self.msg_unsucces_request_aceept = res["msg_unsucces_request_aceept"]
        self.msg_start_chain = res["msg_start_chain"]
        self.msg_stop_chain = res["msg_stop_chain"]
        self.msg_stop_chain_last = res["msg_stop_chain_last"]
        self.msg_error_loop_details = res["msg_error_loop_details"]
        self.msg_enter_correct_info = res["msg_enter_correct_info"]
        self.msg_mcl_not_installed = res["msg_mcl_not_installed"]
        self.msg_yes = res["msg_yes"]
        self.msg_no = res["msg_no"]
        self.msg_accept = res["msg_accept"]
        self.msg_ok = res["msg_ok"]

        self.last_update = res["label_last_update"]
        self.label_28.setText(res["choose_language"])
        self.label_19.setText(res["server_informations"])

        self.tabWidget_3.setTabText(0, res["button_chain"])
        self.tabWidget_3.setTabText(1, res["button_wallet"])
        self.tabWidget_3.setTabText(2, res["button_coin_send_recive"])
        self.tabWidget_3.setTabText(3, res["button_credit_transaction"])
        self.tabWidget_3.setTabText(4, res["persons"])
        self.tabWidget_3.setTabText(5, res["button_setting"])
        self.tabWidget_3.setTabText(6, res["button_exit"])

        self.label_27.setText(res["label_pubkey"])
        self.label_56.setText(res["label_wallet_adress"])
        self.pushButton_17.setText(res["button_start"])
        self.pushButton_11.setText(res["button_stop"])
        self.active_text = res["active"]
        self.deactive_text = res["deactive"]
        self.pushButton_10.setText(res["button_create_new_wallet"])
        self.pushButton_8.setText(res["button_refresh"])
        self.label.setText(res["chain_active"])
        self.label_4.setText(res["chain_synchronous"])
        self.label_3.setText(res["block_count"])
        self.label_50.setText(res["all_block_count"])
        self.label_14.setText(res["currency"])
        self.label_12.setText(res["status"])
        self.label_15.setText(res["cpu"])
        self.label_10.setText(res["wallet_amount"])
        self.label_16.setText(res["normal_amount"])
        self.label_8.setText(res["activate_amount"])
        self.label_29.setText(res["copy_pubkey"])
        self.label_9.setText(res["copy_wallet"])
        self.label_64.setText(res["login_lang"])

        self.groupBox_2.setTitle(res["persons"])
        self.currency = res["currency"]

        self.groupBox_5.setTitle(res["active_amount"])
        self.groupBox_9.setTitle(res["unlock_amount"])
        self.label_21.setText(res["amount"])
        self.label_33.setText(res["amount"])
        self.lineEdit_12.setPlaceholderText(res["amount_to_lock"])
        self.lineEdit_16.setPlaceholderText(res["amount_to_unlock"])

        self.groupBox_6.setTitle(res["send_amount"])
        self.groupBox_8.setTitle(res["receive_amount"])
        self.label_30.setText(res["receiver_adress"])
        self.label_31.setText(res["amount"])
        self.label_32.setText(res["my_wallet_adress"])
        self.lineEdit_9.setPlaceholderText(res["label_wallet_adress"])
        self.lineEdit_15.setPlaceholderText(res["amount_to_sent"])

        self.tabWidget_4.setTabText(0, res["issuer_operations"])
        self.tabWidget_4.setTabText(1, res["bearer_operations"])
        self.tabWidget_4.setTabText(2, res["endorser_operations"])
        self.tabWidget_4.setTabText(3, res["loop_info"])
        self.tabWidget_4.setTabText(4, res["activate_loops"])

        self.groupBox_16.setTitle(res["active_loops_groupbox"])

        self.groupBox_13.setTitle(res["list_of_first_credit_request"])
        self.label_18.setText(res["how_many_minutes_previous_request"])

        self.groupBox_10.setTitle(res["first_credit_request"])
        self.groupBox_11.setTitle(res["credit_request_in_loop"])
        self.label_34.setText(res["receiver_pub_key"])
        self.label_51.setText(res["receiver_pub_key"])
        self.label_22.setText(res["amount"])
        self.label_41.setText(res["matures"])
        self.label_42.setText(res["currency_request"])
        self.label_43.setText(res["request_credit"])
        self.label_53.setText(res["request_credit"])
        self.label_49.setText(res["botton_txid"])

        self.lineEdit_2.setPlaceholderText(res["amount"])
        self.lineEdit_21.setPlaceholderText(res["receiver_pub_key"])
        self.lineEdit_24.setPlaceholderText(res["receiver_pub_key"])
        self.lineEdit_25.setPlaceholderText(res["botton_txid"])

        self.groupBox_14.setTitle(res["list_of_credit_requests_in_loop"])
        self.groupBox_15.setTitle(res["bearer_loops"])
        self.pushButton_30.setText(res["button_refresh"])
        self.pushButton_35.setText(res["button_refresh"])

        self.pushButton_41.setText(res["button_save"])

        self.groupBox_7.setTitle(res["detailed_information_about_loops"])
        self.label_46.setText(res["amount"])
        self.label_48.setText(res["currency_loop_info"])
        self.label_7.setText(res["matures"])
        self.label_17.setText(res["issuer_pk"])

        self.label_68.setText(res["label_name"].capitalize())
        self.label_67.setText(res["label_wallet_adress"])

        # Intall Objects
        self.pushButton_5.setText(res["button_install"])
        self.label_71.setText(res["label_notice"])
        self.msg_box_end_1 = res["msg_box_end_1"]
        self.msg_box_end_2 = res["msg_box_end_2"]
        self.label_72.setText(res["label_72_text"])
        self.label_73.setText(res["label_73_text"])
        self.label_74.setText(res["label_74_text"])

        self.pushButton_34.setText(res["button_refresh"])

        self.pushButton_36.setText(res["pushbutton_36"])
        self.label_63.setText(res["label_63"])
        self.label_62.setText(res["label_62"])
        self.lineEdit_7.setPlaceholderText(res["lineEdit_7_palaceholder"])
        self.lineEdit_3.setPlaceholderText(res["lineEdit_3_placeholder"])

        self.pushButton_37.setText(res["pushbutton_37"] + "\n" + res["pushbutton_37_"])
        self.pushButton_38.setText(res["pushbutton_38"] + "\n" + res["pushbutton_38_"])
        self.label_70.setText(res["label_70"])
        self.lineEdit_14_withoutPubkey = res["lineEdit_14_withoutPubkey"]

        self.copy = res["copy"]
        self.amount = res["amount"]
        self.receiver_pubkey = res["receiver_pubkey"]

        self.matures = res["matures"]

        self.checkBox_2.setText(res["checkbox_all"])
        self.checkBox_4.setText(res["checkbox_all"])
        self.checkBox_5.setText(res["checkbox_all"])
        self.checkBox.setText(res["checkbox_withbootstrap"])

        self.label_54.setText(res["min_amount"])
        self.label_55.setText(res["max_amount"])
        self.label_65.setText(res["from"])
        self.label_66.setText(res["to"])

        self.groupBox_3.setTitle(res["matures"])
        self.groupBox_18.setTitle(res["amount"])

        self.groupBox_14.setTitle(res["active_loops_groupbox"])

        self.synchronous = res["synchronous"]
        self.asynchronous = res["asynchronous"]
        self.review = res["review"]
        self.review_and_confirm = res["review_and_confirm"]
        self.tableWidget.setColumnCount(4)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        # self.tableWidget.setHorizontalHeaderLabels(['TXID', 'AMOUNT', "REVIEW AND CONFIRM"])

        self.tableWidget_2.setColumnCount(4)
        header = self.tableWidget_2.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        # self.tableWidget_2.setHorizontalHeaderLabels(['TXID',"REVIEW AND CONFIRM"])

        self.tableWidget_3.setColumnCount(2)
        header = self.tableWidget_3.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # self.tableWidget_3.setHorizontalHeaderLabels(['LOOP ADRESS', 'AMOUNT'])

        self.tableWidget_4.setColumnCount(3)
        header = self.tableWidget_4.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_5.setColumnCount(6)
        header = self.tableWidget_5.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.setHorizontalHeaderLabels(
            ['TXID', res["amount_table_title"], res["matures"].upper(), res["review_and_confirm"]])
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['TXID', res["amount_table_title"], res["matures"].upper(), res["review_and_confirm"]])
        self.tableWidget_3.setHorizontalHeaderLabels([res["loop_adress"], res["amount_table_title"]])
        self.tableWidget_4.setHorizontalHeaderLabels(['TXID', res["copy_txid_table_title"], res["msg_title_info"]])
        self.tableWidget_5.setHorizontalHeaderLabels(
            [res["label_name"].capitalize(), res["label_wallet_adress"].capitalize(), res["copy"].capitalize(),
             "Pubkey", res["label_wallet_adress"].capitalize(), res["button_delete"]])

    def readConfFile(self):
        import ast
        f = open(self.configFilePath, "r")
        a = f.read()
        res = ast.literal_eval("{" + a + "}")

        self.conf_file_content = res
        print(type(self.conf_file_content))
        self.conf_lang_info = res["selected_lang"]

    def tabWidgetOnChange(self, i):
        print("Tab changed")

    def changingInformationMarmaraHoldersList(self, val):
        self.holder_list_json = val
        json_array = json.loads(self.holder_list_json)

        print(len(json_array))
        print(json_array)

        print(self.tableWidget_4.rowCount())
        count_rows = int(self.tableWidget_4.rowCount())

        for index in range(count_rows):
            self.tableWidget_4.removeRow(index)

        self.holder_list = []
        for item in json_array['issuances']:
            self.holder_list.append(item)

        self.tableWidget_4.setRowCount(len(self.holder_list))
        print(self.holder_list)
        print(len(self.holder_list))
        row_index = 0
        for item_json in self.holder_list:
            txid = QTableWidgetItem(item_json)
            print(txid.text())
            self.tableWidget_4.setItem(row_index, 0, txid)

            btn_copy = QPushButton('')
            btn_copy.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_wallet_icon_.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_wallet_icon_hover_.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_wallet_icon_press_.png);border:0px}")
            btn_copy.clicked.connect(self.buttonClickBottonTxidCoppy)
            self.tableWidget_4.setCellWidget(row_index, 1, btn_copy)

            btn_info = QPushButton('')
            btn_info.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/details.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/details_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/details_press.png);border:0px}")
            btn_info.clicked.connect(self.buttonClickHolderDetails)
            self.tableWidget_4.setCellWidget(row_index, 2, btn_info)
            row_index = row_index + 1

        self.loading_screen.stopAnimotion()

    def buttonClickBottonTxidCoppy(self):
        button = self.sender()
        index = self.tableWidget_4.indexAt(button.pos())
        if index.isValid():
            pyperclip.copy(self.tableWidget_4.item(index.row(), 0).text())

    def buttonClickHolderDetails(self):
        self.thread_holder_details_info = ThreadGui.SearchRequest()
        button = self.sender()
        index = self.tableWidget_4.indexAt(button.pos())
        if index.isValid():
            self.loading_screen.startAnimation()
            self.thread_holder_details_info.change_value_information_loop_details.connect(
                self.changingInformationsHolderDetails)

            self.thread_holder_details_info.command_mcl_credit_loop_search = "./" + self.mcl_install_file_path + self.command_mcl_credit_loop_search + " " + self.tableWidget_4.item(
                index.row(), 0).text()

            self.thread_holder_details_info.server_username = self.server_username
            self.thread_holder_details_info.server_hostname = self.server_hostname
            self.thread_holder_details_info.server_password = self.server_password

            self.thread_holder_details_info.start()

    def changingInformationsHolderDetails(self, val):
        y = json.loads(val)
        self.loading_screen.stopAnimotion()
        matures_date = y['matures'] - int(self.long_chain_blocks)
        matures_time = datetime.now() + timedelta(minutes=matures_date)

        matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)
        self.showDialogInfo(self.msg_title_info,
                            "",
                            "TXID: " + y["createtxid"] + "\n" +
                            self.amount.upper() + ": " + str(y["amount"]) + "\n" +
                            self.currency.upper() + ": " + y["currency"] + "\n" +
                            self.matures.upper() + ": " + matures_date_ + "\n" +
                            "BATON PUBBKEY: " + y["batonpk"] + "\n",
                            self.msg_ok)

    def buttonClickMarmaraHolders(self):
        if not self.checkBox_4.isChecked():
            date_min = self.dateTimeEdit_3.dateTime().toPyDateTime() - datetime.now()
            date_max = self.dateTimeEdit_4.dateTime().toPyDateTime() - datetime.now()

            min_mat = int(self.long_chain_blocks) + int(abs(date_min).total_seconds() / 60)
            max_mat = int(self.long_chain_blocks) + int(abs(date_max).total_seconds() / 60)

            self.command_mcl_marmar_holders_min_matures = str(min_mat)
            self.command_mcl_marmar_holders_max_matures = str(max_mat)
        else:
            self.command_mcl_marmar_holders_min_matures = "0"
            self.command_mcl_marmar_holders_max_matures = "0"

        if not self.checkBox_5.isChecked():
            self.command_mcl_marmar_holders_min_amount = self.lineEdit_29.text()
            self.command_mcl_marmar_holders_max_amount = self.lineEdit_30.text()
        else:
            self.command_mcl_marmar_holders_min_amount = "0"
            self.command_mcl_marmar_holders_max_amount = "0"

        self.thread_list_holders = ThreadGui.SearchHolders()

        self.loading_screen.startAnimation()
        self.thread_list_holders.change_value_information.connect(self.changingInformationMarmaraHoldersList)

        self.thread_list_holders.command_mcl_marmara_holders = "./" + self.mcl_install_file_path + self.command_mcl_marmar_holders + self.command_mcl_marmar_holders_min_matures + " " + self.command_mcl_marmar_holders_max_matures + " " + self.command_mcl_marmar_holders_min_amount + " " + self.command_mcl_marmar_holders_max_amount + " " + self.pubkey

        self.thread_list_holders.server_username = self.server_username
        self.thread_list_holders.server_hostname = self.server_hostname
        self.thread_list_holders.server_password = self.server_password

        self.thread_list_holders.start()

    def changingInformationActiveList(self, val):
        self.holder_list_json = val
        json_array = json.loads(self.holder_list_json)

        self.active_loops_list = []
        count_rows = int(self.tableWidget_3.rowCount())

        for index in range(count_rows):
            self.tableWidget_3.removeRow(index)

        for item in json_array['Loops']:
            self.active_loops_list.append(item)

        self.tableWidget_3.setRowCount(len(self.active_loops_list))
        row_index = 0
        for item_json in self.active_loops_list:
            loopAdress = QTableWidgetItem(item_json["LoopAddress"])
            self.tableWidget_3.setItem(row_index, 0, loopAdress)

            amount = QTableWidgetItem(str(item_json["myAmountLockedInLoop"]))
            self.tableWidget_3.setItem(row_index, 1, amount)
            row_index = row_index + 1

        self.loading_screen.stopAnimotion()

    def buttonClickActiveLoops(self):
        self.thread_active_list = ThreadGui.ActiveLoops()

        self.loading_screen.startAnimation()
        self.thread_active_list.change_value_information.connect(self.changingInformationActiveList)

        self.thread_active_list.command_mcl_marmara_info = "./" + self.mcl_install_file_path + self.command_mcl_marmara_get_info + self.pubkey

        self.thread_active_list.server_username = self.server_username
        self.thread_active_list.server_hostname = self.server_hostname
        self.thread_active_list.server_password = self.server_password

        self.thread_active_list.start()

    def buttonClickRefreshAllCreditRequest(self):
        if not self.checkBox_2.isChecked():
            date = self.dateTimeEdit.dateTime()
            minute_ = date.toPyDateTime().minute
            hour_ = date.toPyDateTime().hour
            day_ = date.toPyDateTime().day
            month_ = date.toPyDateTime().month
            year_ = date.toPyDateTime().year

            now = datetime.now()
            minute_ = now.minute - minute_
            hour_ = now.hour - hour_
            day_ = now.day - day_
            month_ = now.month - month_
            year_ = now.year - year_

            block_count = minute_ + (hour_ * 60) + (day_ * 1440) + (month_ * 30 * 1440) + (year_ * 365 * 1440)
            self.last_matures_minute = str(block_count)
        else:
            self.last_matures_minute = ""

        self.thread_refresh_credit_request = ThreadGui.RefreshCreditRequest()

        self.loading_screen.startAnimation()
        self.thread_refresh_credit_request.change_value_information.connect(self.changingInformationCreditRequestList)

        self.thread_refresh_credit_request.command_mcl_credit_request_list = "./" + self.mcl_install_file_path + self.command_mcl_credit_request_list + self.pubkey + " " + self.last_matures_minute

        self.thread_refresh_credit_request.server_username = self.server_username
        self.thread_refresh_credit_request.server_hostname = self.server_hostname
        self.thread_refresh_credit_request.server_password = self.server_password

        self.thread_refresh_credit_request.start()

    def buttonClickRefreshAllCreditRequestCiranta(self):
        self.thread_refresh_credit_request = ThreadGui.RefreshCreditRequest()

        self.loading_screen.startAnimation()
        self.thread_refresh_credit_request.change_value_information.connect(
            self.changingInformationCreditRequestListCiranta)

        self.thread_refresh_credit_request.command_mcl_credit_request_list = "./" + self.mcl_install_file_path + self.command_mcl_credit_request_list + self.pubkey

        self.thread_refresh_credit_request.server_username = self.server_username
        self.thread_refresh_credit_request.server_hostname = self.server_hostname
        self.thread_refresh_credit_request.server_password = self.server_password

        self.thread_refresh_credit_request.start()

    def changingInformationCreditRequestList(self, val):
        self.request_credit_out = val
        json_array = json.loads(self.request_credit_out)
        count_rows = int(self.tableWidget.rowCount())

        self.first_request_list = []

        for index in range(count_rows):
            self.tableWidget.removeRow(index)

        for item in json_array:
            if item["funcid"] == "B":
                json_details_ = {"txid": None, "amount": None, "matures": None, "receivepk": None}
                json_details_['txid'] = item['txid']
                json_details_['amount'] = item['amount']
                json_details_['matures'] = item['matures']
                json_details_['receivepk'] = item['receivepk']
                self.first_request_list.append(json_details_)

        self.tableWidget.setRowCount(len(self.first_request_list))

        row_index = 0
        for item_json in self.first_request_list:
            txid = QTableWidgetItem(item_json['txid'])
            amount = QTableWidgetItem(str(item_json['amount']))
            # matures = QTableWidgetItem(str(item_json['matures']))

            matures_date = item_json['matures'] - int(self.long_chain_blocks)
            matures_time = datetime.now() + timedelta(minutes=matures_date)

            matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)
            matures = QTableWidgetItem(matures_date_)

            self.tableWidget.setItem(row_index, 0, txid)
            self.tableWidget.setItem(row_index, 1, amount)
            self.tableWidget.setItem(row_index, 2, matures)

            self.btn_review_ = QPushButton(self.review.capitalize())
            self.btn_review_.setStyleSheet("\
                                   QPushButton          {background-color: #16A085 ;font: 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px;}\
                                   QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
                                   QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
                                   ")
            self.btn_review_.clicked.connect(self.buttonClickFirstRequestListReview)
            self.tableWidget.setCellWidget(row_index, 3, self.btn_review_)
            row_index = row_index + 1
        self.loading_screen.stopAnimotion()

    def changingInformationCreditRequestListCiranta(self, val):
        self.request_credit_out = val
        json_array = json.loads(self.request_credit_out)

        count_rows = int(self.tableWidget_2.rowCount())

        self.request_list_in_loop = []

        for index in range(count_rows):
            self.tableWidget_2.removeRow(index)

        for item in json_array:
            if item["funcid"] == "R":
                json_details = {"txid": None, "receivepk": None, "amount": None, 'matures': None}
                json_details['txid'] = item['txid']
                json_details['receivepk'] = item['receivepk']
                json_details['amount'] = item['amount']
                json_details['matures'] = item['matures']
                self.request_list_in_loop.append(json_details)

        self.tableWidget_2.setRowCount(len(self.request_list_in_loop))

        row_index = 0
        for item_json in self.request_list_in_loop:
            txid = QTableWidgetItem(item_json['txid'])
            amount = QTableWidgetItem(str(item_json['amount']))

            matures_date = item_json['matures'] - int(self.long_chain_blocks)
            matures_time = datetime.now() + timedelta(minutes=matures_date)

            matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)
            matures = QTableWidgetItem(matures_date_)

            self.tableWidget_2.setItem(row_index, 0, txid)
            self.tableWidget_2.setItem(row_index, 1, amount)
            self.tableWidget_2.setItem(row_index, 2, matures)

            self.btn_rew_ = QPushButton(self.review)
            self.btn_rew_.setStyleSheet("\
                                   QPushButton          {background-color: #16A085 ;font: 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px;}\
                                   QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
                                   QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
                                   ")
            self.btn_rew_.clicked.connect(self.buttonClickRequestListInLoopReview)
            self.tableWidget_2.setCellWidget(row_index, 3, self.btn_rew_)
            row_index = row_index + 1

        self.loading_screen.stopAnimotion()

    def buttonClickMining(self):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(str(self.server_hostname), self.server_port, str(self.server_username),
                    str(self.server_password))

        # cpu_max=0
        # if os.cpu_count() > 4:
        #     cpu_max=4
        # else:
        #     cpu_max = os.cpu_count() -1

        if self.pushButton_6.isChecked():

            text, ok = QInputDialog.getInt(self, 'CPU For Mining', 'Enter numbur of cpu:', 1, 1, 3, 1)
            if ok:
                if self.pushButton_9.isChecked():
                    self.pushButton_9.setChecked(False)
                command = "./" + self.mcl_install_file_path + self.command_mcl_set_mining + str(text)
                self.label_5.setText(str(text))
                stdin, stdout, stderr = ssh.exec_command(command)
                self.label_11.setText("MINING")
        else:
            self.label_5.setText("0")
            if not self.pushButton_9.isChecked():
                self.label_11.setText("(-)")
                command = "./" + self.mcl_install_file_path + self.command_mcl_set_off_generate
                stdin, stdout, stderr = ssh.exec_command(command)

    def buttonClickStacking(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(str(self.server_hostname), self.server_port, str(self.server_username),
                    str(self.server_password))

        if self.pushButton_9.isChecked():
            self.label_5.setText("0")
            self.label_11.setText("STAKING")
            if self.pushButton_6.isChecked():
                self.pushButton_6.setChecked(False)
            command = "./" + self.mcl_install_file_path + self.command_mcl_set_stacking
            stdin, stdout, stderr = ssh.exec_command(command)
        else:
            if not self.pushButton_6.isChecked():
                command = "./" + self.mcl_install_file_path + self.command_mcl_set_off_generate
                self.label_11.setText("(-)")
                stdin, stdout, stderr = ssh.exec_command(command)

    def buttonClickCreditRequest(self):
        if (not self.lineEdit_21.text() == "") and not self.lineEdit_2.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_request, self.msg_yes, self.msg_no)
            if self.message_button_return_boolean:
                date_matures = self.dateTimeEdit_2.dateTime().toPyDateTime() - datetime.now()
                matures_ = int(abs(date_matures).total_seconds() / 60)

                self.thread_credit_request = ThreadGui.CreditRequest()

                self.loading_screen.startAnimation()
                self.thread_credit_request.change_value_information_credit_request.connect(
                    self.changingInformationCreditRequest)
                self.thread_credit_request.change_value_information_get_transactionID.connect(
                    self.changingInformationTransactionID)

                self.thread_credit_request.command_mcl_credit_request = "./" + self.mcl_install_file_path + self.command_mcl_credit_request + \
                                                                        self.lineEdit_21.text() + " " + self.lineEdit_2.text() + " " + self.lineEdit_4.text() + " " + str(
                    matures_) + " " + self.command_mcl_credit_request_countine

                self.thread_credit_request.command_mcl_credit_request_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                self.thread_credit_request.server_username = self.server_username
                self.thread_credit_request.server_hostname = self.server_hostname
                self.thread_credit_request.server_password = self.server_password

                self.thread_credit_request.start()

        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickRequestCiranta(self):
        if (not self.lineEdit_24.text() == "") and not self.lineEdit_25.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_endorser, self.msg_yes, self.msg_no)
            if self.message_button_return_boolean:
                self.thread_credit_request_ciranta = ThreadGui.CreditRequest()

                self.loading_screen.startAnimation()
                self.thread_credit_request_ciranta.change_value_information_credit_request.connect(
                    self.changingInformationCreditRequest)
                self.thread_credit_request_ciranta.change_value_information_get_transactionID.connect(
                    self.changingInformationTransactionID)

                self.thread_credit_request_ciranta.command_mcl_credit_request = "./" + self.mcl_install_file_path + self.command_mcl_credit_request + \
                                                                                self.lineEdit_24.text() + " " + self.lineEdit_25.text() + " " + self.command_mcl_credit_request_countine

                self.thread_credit_request_ciranta.command_mcl_credit_request_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                self.thread_credit_request_ciranta.server_username = self.server_username
                self.thread_credit_request_ciranta.server_hostname = self.server_hostname
                self.thread_credit_request_ciranta.server_password = self.server_password

                self.thread_credit_request_ciranta.start()

        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickFirstRequestListReview(self):
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        if index.isValid():
            for item in self.first_request_list:
                if item['txid'] == self.tableWidget.item(index.row(), 0).text():
                    matures_date = item['matures'] - int(self.long_chain_blocks)
                    matures_time = datetime.now() + timedelta(minutes=matures_date)

                    matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)

                    self.showDialogYesNo(self.msg_credit_confirmaiton,
                                         "TXID: " + item['txid'] + "\n" +
                                         self.amount.upper() + ": " + str(item['amount']) + "\n" +
                                         self.matures.upper() + ": " + matures_date_ + "\n" +
                                         self.receiver_pubkey.upper() + ": " + item['receivepk'] + "\n" +
                                         "\n" + self.msg_do_you_want_to_accept, self.msg_accept, self.msg_no)
                    if self.message_button_return_boolean:
                        self.thread_credit_request_accept = ThreadGui.CreditAccept()

                        self.loading_screen.startAnimation()
                        self.thread_credit_request_accept.change_value_information_accept.connect(
                            self.changingInformationAcceptCreditRequest)
                        self.thread_credit_request_accept.change_value_information_get_transactionID.connect(
                            self.changingInformationTransactionID)

                        self.thread_credit_request_accept.command_mcl_credit_request_accept = "./" + self.mcl_install_file_path + self.command_mcl_credit_request_accept + \
                                                                                              item[
                                                                                                  'receivepk'] + self.command_mcl_credit_request_accept_countine + \
                                                                                              item['txid']
                        self.thread_credit_request_accept.command_mcl_credit_request_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                        self.thread_credit_request_accept.server_username = self.server_username
                        self.thread_credit_request_accept.server_hostname = self.server_hostname
                        self.thread_credit_request_accept.server_password = self.server_password

                        self.thread_credit_request_accept.start()

    def buttonClickRequestListInLoopReview(self):
        button = self.sender()
        index = self.tableWidget_2.indexAt(button.pos())
        if index.isValid():
            for item in self.request_list_in_loop:
                if item['txid'] == (self.tableWidget_2.item(index.row(), 0)).text():
                    self.showDialogYesNo(self.msg_credit_confirmaiton,
                                         "TXID: " + item['txid'] + "\n" +
                                         "AMOUNT: " + str(item['amount']) + "\n"
                                                                            "MATURES: " + str(item['matures']) + "\n"
                                                                                                                 "RECIVER PEUBKEY: " +
                                         item['receivepk'] + "\n" +
                                         "\n" + self.msg_do_you_want_to_accept, self.msg_accept, self.msg_no)
                    if self.message_button_return_boolean:
                        self.thread_ciranta_request_accept = ThreadGui.CirantaAccept()

                        self.loading_screen.startAnimation()
                        self.thread_ciranta_request_accept.change_value_information_accept.connect(
                            self.changingInformationAcceptCreditRequest)
                        self.thread_ciranta_request_accept.change_value_information_get_transactionID.connect(
                            self.changingInformationTransactionID)

                        self.thread_ciranta_request_accept.command_mcl_ciranta_request_accept = "./" + self.mcl_install_file_path + self.command_mcl_marmaratransfer_accept + \
                                                                                                item[
                                                                                                    'receivepk'] + " " + self.command_mcl_marmaratransfer_accept_countine + " " + \
                                                                                                item['txid']
                        self.thread_ciranta_request_accept.command_mcl_credit_request_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                        self.thread_ciranta_request_accept.server_username = self.server_username
                        self.thread_ciranta_request_accept.server_hostname = self.server_hostname
                        self.thread_ciranta_request_accept.server_password = self.server_password

                        self.thread_ciranta_request_accept.start()

    def buttonClickSendCoin(self):
        if (not self.lineEdit_9.text() == "") and not self.lineEdit_15.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_send_coin, self.msg_yes, self.msg_no)
            if self.message_button_return_boolean:
                self.thread_send_coin = ThreadGui.SendCoin()
                self.loading_screen.startAnimation()
                self.thread_send_coin.change_value_information_txid.connect(self.changingInformationSendCoin)

                reciever_wallet_adress = self.lineEdit_9.text()
                number_of_coin = self.lineEdit_15.text()

                self.thread_send_coin.command_mcl_send_coin = "./" + self.mcl_install_file_path + self.command_mcl_send_coin + "\"" + reciever_wallet_adress + "\" " + number_of_coin

                self.thread_send_coin.server_username = self.server_username
                self.thread_send_coin.server_hostname = self.server_hostname
                self.thread_send_coin.server_password = self.server_password

                self.thread_send_coin.start()

        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def changingInformationSendCoin(self, val):
        self.loading_screen.stopAnimotion()
        self.showDialogInfo(self.msg_title_info, self.msg_sended_coin, "", self.msg_ok)

    def buttonClickLockCoin(self):
        if not self.lineEdit_12.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_acitvate_coins, self.msg_yes,
                                 self.msg_no)
            if self.message_button_return_boolean:
                self.thread_lock_coin = ThreadGui.LockCoin()
                self.loading_screen.startAnimation()
                self.thread_lock_coin.change_value_information_get_lock.connect(self.changingInformationLock)
                self.thread_lock_coin.change_value_information_get_transactionID.connect(
                    self.changingInformationTransactionID)

                number_of_coin = self.lineEdit_12.text()

                self.thread_lock_coin.command_mcl_lock_coin = "./" + self.mcl_install_file_path + self.command_mcl_lock_coin + number_of_coin
                self.thread_lock_coin.command_mcl_lock_coin_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                self.thread_lock_coin.pubkey = self.pubkey
                self.thread_lock_coin.server_username = self.server_username
                self.thread_lock_coin.server_hostname = self.server_hostname
                self.thread_lock_coin.server_password = self.server_password

                self.thread_lock_coin.start()
        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickUnlockCoin(self):
        if not self.lineEdit_16.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_deacitvate_coins, self.msg_yes,
                                 self.msg_no)
            if self.message_button_return_boolean:
                self.thread_unlock_coin = ThreadGui.UnlockCoin()
                self.loading_screen.startAnimation()
                self.thread_unlock_coin.change_value_information_get_unlock.connect(self.changingInformationUnlock)
                self.thread_unlock_coin.change_value_information_get_transactionID.connect(
                    self.changingInformationTransactionID)

                number_of_coin = self.lineEdit_16.text()

                self.thread_unlock_coin.command_mcl_unlock_coin = "./" + self.mcl_install_file_path + self.command_mcl_unlock_coin + number_of_coin
                self.thread_unlock_coin.command_mcl_unlock_coin_sendrawtransaction = "./" + self.mcl_install_file_path + self.command_mcl_coin_sendrawtransaction

                self.thread_unlock_coin.pubkey = self.pubkey
                self.thread_unlock_coin.server_username = self.server_username
                self.thread_unlock_coin.server_hostname = self.server_hostname
                self.thread_unlock_coin.server_password = self.server_password

                self.thread_unlock_coin.start()
        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def changingInformationLock(self, val):
        if val:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_succes_lock, "", self.msg_ok)
        else:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_unsucces_lock, "", self.msg_ok)

    def changingInformationUnlock(self, val):
        if val:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_succes_unlock, "", self.msg_ok)
        else:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_unsucces_unlock, "", self.msg_ok)

    def changingInformationAcceptCreditRequest(self, val):
        if val:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_succes_request_aceept, "", self.msg_ok)
        else:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_unsucces_request_aceept, "", self.msg_ok)

    def buttonClickMarmaraCreditLoopDetails(self):
        if not self.lineEdit_13.text() == "":
            self.thread_request_search = ThreadGui.SearchRequest()

            self.loading_screen.startAnimation()
            self.thread_request_search.change_value_information_loop_details.connect(
                self.changingInformationLoopDetails)

            self.thread_request_search.command_mcl_credit_loop_search = "./" + self.mcl_install_file_path + self.command_mcl_credit_loop_search + " " + self.lineEdit_13.text()

            self.thread_request_search.server_username = self.server_username
            self.thread_request_search.server_hostname = self.server_hostname
            self.thread_request_search.server_password = self.server_password

            self.thread_request_search.start()

        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def changingInformationCreditRequest(self, val):

        if val:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_succes_request, "", self.msg_ok)
        else:
            self.loading_screen.stopAnimotion()
            self.showDialogInfo(self.msg_title_info, self.msg_unsucces_request, "", self.msg_ok)

    def changingInformationTransactionID(self, val):
        print("TrasnID")

    def buttonClickStartChain(self):
        if not self.lineEdit_14.text() == "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_start_chain, self.msg_yes, self.msg_no)
            if self.message_button_return_boolean:
                current_time = datetime.now()
                self.label_57.setText(
                    self.last_update + ":   " + str(current_time.hour) + ":" + str(current_time.minute))
                self.thread_start_chain = ThreadGui.StartChain()
                self.loading_screen.startAnimation()
                self.thread_start_chain.change_value_information_get_info.connect(self.changingInformation1)
                self.thread_start_chain.change_value_information_get_marmara_info.connect(self.changingInformation2)
                self.thread_start_chain.change_value_information_get_generate.connect(self.changingInformation3)
                self.thread_start_chain.change_value_did_run_chain.connect(self.changingInformation4)

                self.pubkey = self.lineEdit_14.text().replace(" ", "")
                print(self.pubkey)

                self.thread_start_chain.command_mcl_start_chain = "./" + self.mcl_install_file_path + self.command_start_mcl_mining_with_pubkey
                self.thread_start_chain.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info
                self.thread_start_chain.command_mcl_get_marmara_info = "./" + self.mcl_install_file_path + self.command_mcl_marmara_get_info
                self.thread_start_chain.command_mcl_get_stacking_and_mining = "./" + self.mcl_install_file_path + self.command_mcl_get_stacking_and_mining

                self.thread_start_chain.pubkey = self.pubkey
                self.thread_start_chain.server_username = self.server_username
                self.thread_start_chain.server_hostname = self.server_hostname
                self.thread_start_chain.server_password = self.server_password

                self.thread_start_chain.start()
        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickStopChain(self):
        self.showDialogYesNo(self.msg_title_warning, self.msg_stop_chain, self.msg_yes, self.msg_no)
        if self.message_button_return_boolean:
            self.showDialogYesNo(self.msg_title_warning, self.msg_stop_chain_last, self.msg_yes, self.msg_no)
            if self.message_button_return_boolean:
                self.thread_stop_chain = ThreadGui.StopChain()
                self.loading_screen.startAnimation()
                self.thread_stop_chain.change_value_did_run_chain.connect(self.changingInformation5)

                self.thread_stop_chain.command_mcl_stop_chain = "./" + self.mcl_install_file_path + self.command_mcl_stop_chain
                self.thread_stop_chain.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info

                self.thread_stop_chain.pubkey = self.pubkey
                self.thread_stop_chain.server_username = self.server_username
                self.thread_stop_chain.server_hostname = self.server_hostname
                self.thread_stop_chain.server_password = self.server_password

                self.thread_stop_chain.start()

    def buttonClickRefreshInformations(self):
        current_time = datetime.now()
        self.label_57.setText(self.last_update + ":   " + str(current_time.hour) + ":" + str(current_time.minute))
        self.thread_refresh = ThreadGui.RefreshInformations()
        self.loading_screen.startAnimation()
        self.thread_refresh.change_value_information_get_info.connect(self.changingInformation1)
        self.thread_refresh.change_value_information_get_marmara_info.connect(self.changingInformation2)
        self.thread_refresh.change_value_information_get_generate.connect(self.changingInformation3)
        self.thread_refresh.change_value_did_run_chain.connect(self.changingInformation4)

        self.thread_refresh.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info
        self.thread_refresh.command_mcl_get_marmara_info = "./" + self.mcl_install_file_path + self.command_mcl_marmara_get_info
        self.thread_refresh.command_mcl_get_stacking_and_mining = "./" + self.mcl_install_file_path + self.command_mcl_get_stacking_and_mining

        self.thread_refresh.pubkey = self.pubkey
        self.thread_refresh.server_username = self.server_username
        self.thread_refresh.server_hostname = self.server_hostname
        self.thread_refresh.server_password = self.server_password

        self.thread_refresh.start()

    def buttonClickPubkey(self):
        pyperclip.copy(self.pubkey)

    def buttonClickCopyWalletAdress(self):
        pyperclip.copy(self.walletAdress)

    def changingInformationLoopDetails(self, val):
        y = json.loads(val)
        self.loading_screen.stopAnimotion()
        try:
            if y["result"] == "success":
                b = y["creditloop"]
                a = b[0]
                try:
                    self.lineEdit_22.setText(y["createtxid"])
                    self.lineEdit_5.setText(str(y["amount"]))
                    self.lineEdit_23.setText(y["currency"])

                    matures_date = y['matures'] - int(self.long_chain_blocks)
                    matures_time = datetime.now() + timedelta(minutes=matures_date)

                    matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)
                    self.lineEdit_26.setText(str(matures_date_))
                    self.lineEdit_27.setText(a["issuerpk"])
                except:
                    self.showDialogInfo(self.msg_title_warning, self.msg_error_loop_details,
                                        self.msg_enter_correct_info, self.msg_ok)
            else:
                self.showDialogInfo(self.msg_title_warning, self.msg_error_loop_details, self.msg_enter_correct_info,
                                    self.msg_ok)
        except:
            try:
                self.lineEdit_22.setText(y["createtxid"])
                self.lineEdit_5.setText(str(y["amount"]))
                self.lineEdit_23.setText(y["currency"])

                matures_date = y['matures'] - int(self.long_chain_blocks)
                matures_time = datetime.now() + timedelta(minutes=matures_date)

                matures_date_ = str(matures_time.day) + "/" + str(matures_time.month) + "/" + str(matures_time.year)
                self.lineEdit_26.setText(str(matures_date_))
                self.lineEdit_27.setText(y["issuerpk"])
            except:
                self.showDialogInfo(self.msg_title_warning, self.msg_error_loop_details, self.msg_enter_correct_info,
                                    self.msg_ok)

    def changingInformation1(self, val):
        y = json.loads(val)
        try:
            self.lineEdit_14.setText(y["pubkey"])
            self.pubkey = y["pubkey"]
        except:
            self.loading_screen.stopAnimotion()
            self.lineEdit_14.setText("Pubkeysiz Çalışıyor. Yanlış pubkey girmiş olabilirsiniz.")

            self.thread_start_chain.quit()
            self.thread_refresh.quit()
        if y["synced"]:
            self.pushButton_3.setIcon(QIcon(self.icon_path+'/circle-active.png'))
            self.pushButton_3.setText(self.synchronous)
        else:
            self.pushButton_3.setIcon(QIcon(self.icon_path+'/circle-inactive.png'))
            self.pushButton_3.setText(self.asynchronous)
        self.label_13.setText(y["name"])
        self.label_52.setText(str(y["longestchain"]))
        self.long_chain_blocks = str(y["longestchain"])
        self.label_6.setText(str(y["blocks"]))
        self.label_58.setText(str(y["balance"]))

        self.frame_11.setDisabled(False)
        self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-active.png'))
        self.pushButton_15.setText(self.active_text)
        self.pushButton_16.setIcon(QIcon(self.icon_path+'/circle-active.png'))
        self.pushButton_16.setText(self.active_text)
        self.pushButton_17.setDisabled(True)
        self.pushButton_11.setDisabled(False)

    def changingInformation2(self, val):
        try:
            y = json.loads(val)

            self.walletAdress = y["myNormalAddress"]
            self.lineEdit.setText(self.walletAdress)
            self.lineEdit_31.setText(self.walletAdress)

            self.label_59.setText(str(y["myActivatedAmount"]))
            self.label_45.setText(str(y["myWalletNormalAmount"]))
        except:
            self.lineEdit_31.setText("")

    def changingInformation3(self, val):
        y = json.loads(val)

        if y["staking"]:
            self.label_11.setText("Staking")
            self.label_5.setText("0")
            self.pushButton_9.setChecked(True)
            self.pushButton_6.setChecked(False)

        if y["generate"]:
            self.label_11.setText("Mining")
            self.label_5.setText(str(y["numthreads"]))
            self.pushButton_6.setChecked(True)
            self.pushButton_9.setChecked(False)

        if not y["staking"] and not y["generate"]:
            self.label_11.setText("Close")
            self.label_5.setText("0")
            self.pushButton_9.setChecked(False)
            self.pushButton_9.setChecked(False)

    def changingInformation4(self, val):
        self.is_chain_run = val
        if self.is_chain_run:
            self.frame_11.setDisabled(False)
            self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-active.png'))
            self.pushButton_15.setText(self.active_text)
            self.pushButton_17.setDisabled(True)
            self.pushButton_11.setDisabled(False)
            self.tabWidget_3.setTabEnabled(1, True)
            self.tabWidget_3.setTabEnabled(2, True)
            self.tabWidget_3.setTabEnabled(3, True)
            self.tabWidget_3.setTabEnabled(4, True)
            self.tabWidget_3.setTabEnabled(5, True)
            self.tabWidget_3.setTabEnabled(6, True)
            self.loading_screen.stopAnimotion()

        else:
            self.frame_11.setDisabled(True)
            self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-inactive.png'))
            self.pushButton_15.setText(self.deactive_text)
            self.pushButton_11.setDisabled(True)
            self.pushButton_17.setDisabled(False)

    def changingInformation5(self, val):
        self.is_chain_run = val
        if not self.is_chain_run:
            self.loading_screen.stopAnimotion()
            self.frame_11.setDisabled(True)
            self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-inactive.png'))
            self.pushButton_15.setText("INACTIVE")
            self.pushButton_11.setDisabled(True)
            self.pushButton_17.setDisabled(False)

    def firstLoginController(self):
        print("İlk kontrl loaad")
        self.checkMclInstall()
        print("Check mcl")
        self.checkRunningChain()
        print("Check run")

        if self.is_mcl_install:
            print("Mcl kurulu")
            if self.is_chain_run:
                self.tabWidget_3.setTabEnabled(1, True)
                self.tabWidget_3.setTabEnabled(2, True)
                self.tabWidget_3.setTabEnabled(3, True)
                self.tabWidget_3.setTabEnabled(4, True)
                self.tabWidget_3.setTabEnabled(5, True)
                self.tabWidget_3.setTabEnabled(6, True)
                self.loading_screen.startAnimation()
                current_time = datetime.now()
                self.thread_first_get_info = ThreadGui.RefreshInformations()
                self.label_57.setText(
                    self.last_update + ":   " + str(current_time.hour) + ":" + str(current_time.minute))
                self.thread_first_get_info.change_value_information_get_info.connect(self.changingInformation1)
                self.thread_first_get_info.change_value_information_get_marmara_info.connect(self.changingInformation2)
                self.thread_first_get_info.change_value_information_get_generate.connect(self.changingInformation3)
                self.thread_first_get_info.change_value_did_run_chain.connect(self.changingInformation4)

                self.thread_first_get_info.command_mcl_get_info = "./" + self.mcl_install_file_path + self.command_mcl_get_info
                self.thread_first_get_info.command_mcl_get_marmara_info = "./" + self.mcl_install_file_path + self.command_mcl_marmara_get_info
                self.thread_first_get_info.command_mcl_get_stacking_and_mining = "./" + self.mcl_install_file_path + self.command_mcl_get_stacking_and_mining

                self.thread_first_get_info.pubkey = self.pubkey
                self.thread_first_get_info.server_username = self.server_username
                self.thread_first_get_info.server_hostname = self.server_hostname
                self.thread_first_get_info.server_password = self.server_password

                self.thread_first_get_info.start()
                print("Zincir çalıyor.")

            elif not self.is_chain_run:
                self.label_57.setText(self.last_update + ":   " + "00:00")
                print("Zincir çalışmıyor")
                self.frame_11.setDisabled(True)
                self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-inactive.png'))
                self.pushButton_15.setText(self.deactive_text)
                self.pushButton_11.setDisabled(True)
                self.pushButton_17.setDisabled(False)

            self.tabWidget.setCurrentIndex(2)
            self.tabWidget_3.setCurrentIndex(0)
        elif not self.is_mcl_install:
            self.label_57.setText(self.last_update + ":   " + "00:00")
            print("Mcl kurulu değil.")
            self.tabWidget.setCurrentIndex(1)
            self.showDialogInfo(self.msg_title_warning, self.msg_mcl_not_installed, "", self.msg_ok)

    def checkMclInstall(self):
        tmp_file_check_home = []
        tmp_file_check_compilier = []
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.server_hostname), self.server_port, str(self.server_username),
                        str(self.server_password))

            stdin, stdout, stderr = ssh.exec_command(str("ls"))
            lines = stdout.readlines()
            for deger in lines:
                deger = deger.split("\n")
                tmp_file_check_home.append(deger[0])

            self.is_mcl_install = False
            if "komodo-cli" in tmp_file_check_home and "komodod" in tmp_file_check_home:
                self.mcl_install_file_path = ""
                self.is_mcl_install = True

            else:
                # MCL Install Compiler Check
                stdin, stdout, stderr = ssh.exec_command(str("cd komodo/src; ls"))
                lines = stdout.readlines()
                for deger in lines:
                    deger = deger.split("\n")
                    tmp_file_check_compilier.append(deger[0])
                print(tmp_file_check_compilier)

                if "komodo-cli" in tmp_file_check_compilier and "komodod" in tmp_file_check_compilier:
                    self.mcl_install_file_path = "komodo/src/"
                    self.is_mcl_install = True
        except:
            print("Bağlanılamadı")
            return False

    def checkRunningChain(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.server_hostname), self.server_port, str(self.server_username),
                        str(self.server_password))

            asd = "./" + self.mcl_install_file_path + self.command_mcl_get_info
            stdin, stdout, stderr = ssh.exec_command(asd)
            lines = stdout.readlines()
            if not lines:
                self.is_chain_run = False
                print("Zincir Çalışmıyor")
            else:
                out_ = ""
                for deger in lines:
                    deger = deger.split("\n")
                    out_ = out_ + " " + deger[0]
                self.chainGetInfo(out_)
                self.is_chain_run = True
                print("Zincir çalışıyor.")
        except:
            print("Bağlanılamadı")
            return False

    def chainGetInfo(self, val):
        y = json.loads(val)
        try:
            self.lineEdit_14.setText(y["pubkey"])
            self.pubkey = y["pubkey"]
        except:
            self.loading_screen.stopAnimotion()
            self.lineEdit_14.setText("Pubkeysiz Çalışıyor. Yanlış pubkey girmiş olabilirsiniz.")

        if y["synced"]:
            self.pushButton_3.setIcon(QIcon(self.icon_path+'/circle-active.png'))
            self.pushButton_3.setText(self.synchronous)
        else:
            self.pushButton_3.setIcon(QIcon(self.icon_path+'/circle-inactive.png'))
            self.pushButton_3.setText(self.asynchronous)
        self.label_13.setText(y["name"])
        self.label_52.setText(str(y["longestchain"]))
        self.label_6.setText(str(y["blocks"]))
        self.label_58.setText(str(y["balance"]))

        self.frame_11.setDisabled(False)
        self.pushButton_15.setIcon(QIcon(self.icon_path+'/circle-active.png'))
        self.pushButton_15.setText(self.active_text)
        self.pushButton_16.setIcon(QIcon(self.icon_path+'/circle-active.png'))
        self.pushButton_16.setText(self.active_text)
        self.pushButton_17.setDisabled(True)
        self.pushButton_11.setDisabled(False)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def guiObjectSetStyleSheet(self):
        now = QtCore.QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(now)

        self.dateTimeEdit.setMaximumDateTime(QtCore.QDateTime.currentDateTime())
        self.dateTimeEdit.setMinimumDateTime(QtCore.QDateTime(2000, 1, 1, 0, 0, 0))

        self.dateTimeEdit_2.setDateTime(now)
        self.dateTimeEdit_2.setMinimumDateTime(now)

        self.dateTimeEdit_3.setDateTime(now)
        self.dateTimeEdit_3.setMinimumDateTime(now)

        self.dateTimeEdit_4.setDateTime(now)
        self.dateTimeEdit_4.setMinimumDateTime(now)

        self.dateTimeEdit_2.setStyleSheet("QDateTimeEdit::disabled {background-color: rgb(186, 189, 182);color: gray;}"
                                          "QDateTimeEdit::enabled {background-color: rgb(186, 189, 182);color: rgb(0, 0, 0);}")
        self.dateTimeEdit_3.setStyleSheet("QDateTimeEdit::disabled {background-color: rgb(186, 189, 182);color: gray;}"
                                          "QDateTimeEdit::enabled {background-color: rgb(186, 189, 182);color: rgb(0, 0, 0);}")
        self.dateTimeEdit_4.setStyleSheet("QDateTimeEdit::disabled {background-color: rgb(186, 189, 182);color: gray;}"
                                          "QDateTimeEdit::enabled {background-color: rgb(186, 189, 182);color: rgb(0, 0, 0);}")
        self.dateTimeEdit.setStyleSheet("QDateTimeEdit::disabled {background-color: rgb(186, 189, 182);color: gray;}"
                                        "QDateTimeEdit::enabled {background-color: rgb(186, 189, 182);color: rgb(0, 0, 0);}")

        regex = QtCore.QRegExp("[a-zA-Z ]+")
        validator = QtGui.QRegExpValidator(regex)
        self.lineEdit_7.setValidator(validator)

        self.tableWidget.setColumnCount(4)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_2.setColumnCount(4)
        header = self.tableWidget_2.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_3.setColumnCount(2)
        header = self.tableWidget_3.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_4.setColumnCount(3)
        header = self.tableWidget_4.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget_5.setColumnCount(6)
        header = self.tableWidget_5.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        self.onlyDouble = QDoubleValidator()
        self.lineEdit_2.setValidator(self.onlyDouble)

        self.onlyDouble = QDoubleValidator()
        self.lineEdit_15.setValidator(self.onlyDouble)

        self.onlyDouble = QDoubleValidator()
        self.lineEdit_12.setValidator(self.onlyDouble)

        self.onlyDouble = QDoubleValidator()
        self.lineEdit_16.setValidator(self.onlyDouble)

        # Tabwidget
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.tableWidget_2.setShowGrid(False)
        self.tableWidget_2.verticalHeader().setVisible(False)

        self.tableWidget_3.setShowGrid(False)
        self.tableWidget_3.verticalHeader().setVisible(False)

        self.tableWidget_4.setShowGrid(False)
        self.tableWidget_4.verticalHeader().setVisible(False)

        self.tableWidget_5.setShowGrid(False)
        self.tableWidget_5.verticalHeader().setVisible(False)

        stylesheet = "QHeaderView::section{Background-color:#16A085;border-radius:5px;font: 13pt;color: beige; margin:5px}" \
                     "QTableWidget::QTableCornerButton::section {background: red;border: 2px outset red;border: 0;}" \
                     "QTableWidget::indicator:unchecked {background-color: #d7d6d5;border: 0;}" \
                     "QTableWidget {border: 0;}" \
                     "QTableWidget::item { border-radius:12px;font: 15pt;color: beige; }"

        self.tableWidget.setStyleSheet(stylesheet)

        stylesheet_4 = "QHeaderView::section{Background-color:#16A085;border-radius:5px;font: 13pt;color: beige; margin:5px}" \
                       "QTableWidget::QTableCornerButton::section {background: red;border: 2px outset red;border: 0;}" \
                       "QTableWidget::indicator:unchecked {background-color: #d7d6d5;border: 0;}" \
                       "QTableWidget {border: 0;}" \
                       "QTableWidget::item { border-radius:12px;font: 15pt;color: beige; }"

        self.tableWidget_4.setStyleSheet(stylesheet_4)

        stylesheet_5 = "QHeaderView::section{Background-color:#16A085;border-radius:5px;font: 13pt;color: beige; margin:5px}" \
                       "QTableWidget::QTableCornerButton::section {background: red;border: 2px outset red;border: 0;}" \
                       "QTableWidget::indicator:unchecked {background-color: #d7d6d5;border: 0;}" \
                       "QTableWidget {border: 0;}" \
                       "QTableWidget::item { border-radius:12px;font: 15pt;color: beige; }"

        self.tableWidget_5.setStyleSheet(stylesheet_5)

        stylesheet = "QHeaderView::section{Background-color:#16A085;border-radius:5px;font: 13pt;color: beige; margin:5px}" \
                     "QTableWidget::QTableCornerButton::section {background: red;border: 2px outset red;border: 0;}" \
                     "QTableWidget::indicator:unchecked {background-color: #d7d6d5;border: 0;}" \
                     "QTableWidget {border: 0;}" \
                     "QTableWidget::item { border-radius:12px;font: 15pt;color: beige; }"

        self.tableWidget_3.setStyleSheet(stylesheet)

        stylesheet_ = "QHeaderView::section{Background-color:#16A085;border-radius:5px;font: 13pt;color: beige; margin:5px}" \
                      "QTableWidget::QTableCornerButton::section {background: red;border: 2px outset red;border: 0;}" \
                      "QTableWidget::indicator:unchecked {background-color: #d7d6d5;border: 0;}" \
                      "QTableWidget {border: 0;}" \
                      "QTableWidget::item { border-radius:12px;font: 15pt;color: beige; }"

        self.tableWidget_2.setStyleSheet(stylesheet_)

        self.tabWidget_3.setTabIcon(0, QtGui.QIcon(self.icon_path + '/chain_icon.png'))
        self.tabWidget_3.setTabIcon(1, QtGui.QIcon(self.icon_path + '/wallet_icon.png'))
        self.tabWidget_3.setTabIcon(2, QtGui.QIcon(self.icon_path + '/credit.png'))
        self.tabWidget_3.setTabIcon(3, QtGui.QIcon(self.icon_path + '/loop_icon.png'))
        self.tabWidget_3.setTabIcon(4, QtGui.QIcon(self.icon_path + '/persons.png'))
        self.tabWidget_3.setTabIcon(5, QtGui.QIcon(self.icon_path + '/setting_icon.png'))
        self.tabWidget_3.setTabIcon(6, QtGui.QIcon(self.icon_path + '/exit_icon.png'))
        self.tabWidget_3.setTabIcon(7, QtGui.QIcon(self.icon_path + '/log_icon.png'))

        self.tabWidget.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabWidget_3.tabBar().setStyleSheet('''
                                QTabBar { font: bold 15pt; font-family: Courier; color: rgb(238, 238, 236); }
                                QTabBar::tab { border-radius: 10px;   margin: 5px; }
                                QTabBar::tab:selected {background-color:  #2C3E50; color: white}
                                QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;}
                                QTabBar::tab:hover {background-color : #16A085;}
                            ''')
        self.tabWidget_3.setStyleSheet('''
                                 QTabBar { font: bold 12pt; font-family: Courier; color: rgb(238, 238, 236); }
                                 QTabBar::tab { border-radius: 10px;   }
                                 QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;}
                                 QTabWidget::pane {top: 0px;}
                                 QTabWidget::pane { border: 0; }
                                 
                                 QTabBar::tab:selected {background-color:  #2C3E50; color: white}
                                 QTabBar::tab:hover {background-color : #16A085;}
                             ''')

        self.tabWidget_4.setStyleSheet('''
                        QTabWidget { background: transparent;  }
                        QTabWidget::pane {border: 0px solid lightgray;border-radius: 20px;top:-1px;}
                        QTabBar::tab {border: 1px solid beige;padding: 15px;}
                        QTabBar::tab:selected {}''')

        self.tabWidget_4.tabBar().setStyleSheet('''
                                QTabBar { font: 12pt; font-family: Courier; color: rgb(238, 238, 236); }
                                QTabBar::tab { border-radius: 10px; }
                                QTabBar::tab:hover {background-color:  #2C3E50; color: white}
                                QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;}
                                QTabBar::tab:selected {background-color : #16A085;}
                            ''')

        self.tabWidget_3.setIconSize(QtCore.QSize(50, 50))
        # Button
        self.pushButton_21.setIcon(QIcon(self.icon_path+"/connect_icon.png"))
        self.pushButton_21.setIconSize(QtCore.QSize(50, 50))

        self.pushButton_4.setText("")

        self.pushButton_17.setIcon(QIcon(self.icon_path+"/start_icon.png"))
        self.pushButton_17.setIconSize(QtCore.QSize(50, 50))

        self.pushButton_11.setIcon(QIcon(self.icon_path+"/stop_icon.png"))
        self.pushButton_11.setIconSize(QtCore.QSize(60, 60))

        self.pushButton_31.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/search_icon.png); border: 0; width: 40px; height: 40px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/search_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/search_press.png);border:0px}")
        self.pushButton_33.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/search_icon.png); border: 0; width: 40px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/search_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/search_press.png);border:0px}")
        self.pushButton_43.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/search_icon.png); border: 0; width: 40px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/search_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/search_press.png);border:0px}")
        self.pushButton_14.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_key_icon.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_key_icon_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_key_icon_press.png);border:0px}")
        self.pushButton_7.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_wallet_icon_.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_wallet_icon_hover_.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_wallet_icon_press_.png);border:0px}")
        self.pushButton_39.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_wallet_icon_.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_wallet_icon_hover_.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_wallet_icon_press_.png);border:0px}")
        self.pushButton_40.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_key_icon.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_key_icon_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_key_icon_press.png);border:0px}")
        self.pushButton_4.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/exit_icon_reg.png);border:0px; width: 7px; height: 7px;border-radius: 200px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/exit_icon_hoever.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/exit_icon_press.png);border:0px}")
        self.pushButton_13.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/coin_lock_icon.png); border: 0; width: 10px; height: 10px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/coin_lock_icon_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/coin_lock_icon_press.png);border:0px}")
        self.pushButton_20.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/coin_unlock_icon.png); border: 0; width: 10px; height: 10px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/coin_unlock_icon_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/coin_unlock_icon_press.png);border:0px}")
        self.pushButton_18.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/send_coin_icon.png); border: 0; width: 20px; height: 20px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/send_coin_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/send_coin_press.png);border:0px}")

        self.pushButton_19.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/copy_wallet_icon.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/copy_wallet_icon_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/copy_wallet_icon_press.png);border:0px}")

        self.pushButton_27.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/request_credit.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/request_credit_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/request_credit_press.png);border:0px}")

        self.pushButton_32.setStyleSheet(
            "QPushButton          {image: url("+self.icon_path+"/request_credit.png); border: 0; width: 30px; height: 30px;}"
            "QPushButton::hover   {image: url("+self.icon_path+"/request_credit_hover.png);border:0px}"
            "QPushButton::pressed {image: url("+self.icon_path+"/request_credit_press.png);border:0px}")

        self.pushButton_15.setIcon(QIcon(self.icon_path+"/circle-inactive.png"))
        self.pushButton_15.setStyleSheet("border-color: red;border-radius: 10px")

        self.pushButton_16.setIcon(QIcon(self.icon_path+"/circle-inactive.png"))
        self.pushButton_16.setStyleSheet("border-color: red;border-radius: 10px")

        self.pushButton_3.setStyleSheet("border-color: red;border-radius: 10px")

        self.pushButton_22.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color: #5DADE2 ;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")

        self.pushButton_36.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color: #5DADE2 ;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")
        self.pushButton_37.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color: #5DADE2 ;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")
        self.pushButton_38.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color: #5DADE2 ;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")
        self.pushButton_2.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color:  #5DADE2;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")
        self.pushButton_12.setStyleSheet("\
            QPushButton          {color: beige; border: solid; border-style: outset; border-color:  #5DADE2;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")

        self.pushButton_8.setIcon(QIcon(self.icon_path+"/refresh_icon.png"))
        self.pushButton_8.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_8.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: bold 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")

        self.pushButton_29.setIcon(QIcon(self.icon_path+"/refresh_icon.png"))
        self.pushButton_29.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_29.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: bold 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 1px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 1px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 1px; border-radius: 10px;}\
            ")

        self.pushButton_30.setIcon(QIcon(self.icon_path+"/refresh_icon.png"))
        self.pushButton_30.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_30.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: bold 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 1px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 1px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 1px; border-radius: 10px;}\
            ")
        self.pushButton_34.setIcon(QIcon(self.icon_path+"/refresh_icon.png"))
        self.pushButton_34.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_34.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: bold 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 1px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 1px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 1px; border-radius: 10px;}\
            ")

        self.pushButton_35.setIcon(QIcon(self.icon_path+"/refresh_icon.png"))
        self.pushButton_35.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_35.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")

        self.pushButton_41.setStyleSheet("\
                    QPushButton          {background-color: #16A085 ;font: 15pt;color: beige; border: solid; border-style: outset; border-color: blue;border-width: 1px; border-radius: 10px;}\
                    QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 1px; border-radius: 10px;}\
                    QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 1px; border-radius: 10px;}\
                    ")

        self.pushButton_10.setStyleSheet('''
            QPushButton          {background-color: #16A085 ;border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
            QPushButton::hover   {border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px; }
            QPushButton::pressed {border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
            ''')
        self.pushButton_21.setStyleSheet("\
            QPushButton          {background-color: #16A085 ;font: bold 15pt;color: beige; border: solid; border-style: outset; border-color:  #5DADE2;border-width: 2px; border-radius: 10px;}\
            QPushButton::hover   {color: lawngreen; border: solid; border-style: outset; border-color: forestgreen ;border-width: 2px; border-radius: 10px;}\
            QPushButton::pressed {color: lawngreen; border: solid; border-style: outset; border-color: lawngreen ;border-width: 2px; border-radius: 10px;}\
            ")

        self.pushButton_23.setStyleSheet('''
            QPushButton          {background-color: #16A085 ;border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px; }
            QPushButton::hover   {border-style: outset; border-color: green;border-width: 2px; border-radius: 10px; }
            QPushButton::pressed {border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
            ''')

        self.pushButton_24.setStyleSheet('''
                    QPushButton          {background-color: #16A085 ;border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px; }
                    QPushButton::hover   {border-style: outset; border-color: green;border-width: 2px; border-radius: 10px; }
                    QPushButton::pressed {border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
                    ''')
        self.pushButton_25.setStyleSheet('''
                    QPushButton          {background-color: #16A085 ;border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px; }
                    QPushButton::hover   {border-style: outset; border-color: green;border-width: 2px; border-radius: 10px; }
                    QPushButton::pressed {border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
                    ''')
        self.pushButton_26.setStyleSheet('''
                    QPushButton          {background-color: #16A085 ;border-style: outset; border-color: blue;border-width: 2px; border-radius: 10px; }
                    QPushButton::hover   {border-style: outset; border-color: green;border-width: 2px; border-radius: 10px; }
                    QPushButton::pressed {border-style: outset; border-color: red;border-width: 2px; border-radius: 10px; }
                    ''')

        self.pushButton.setIcon(QIcon(self.icon_path + "/mcl_.png"))
        self.pushButton.setIconSize(QtCore.QSize(60, 60))
        self.pushButton.setText("")
        self.pushButton.setStyleSheet("border-color: red;border-radius: 10px")

        # Label
        # ---------------------------------------------
        self.label_20.setStyleSheet("border:0;")
        self.label_23.setStyleSheet("border:0;")
        self.label_24.setStyleSheet("border:0;")

        # Line Edit
        # ---------------------------------------------
        self.lineEdit_12.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_16.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_15.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_14.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_10.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_39.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_38.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_31.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_9.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")

        self.lineEdit_21.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_24.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_13.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_2.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_25.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")
        self.lineEdit_4.setStyleSheet("font-size: 15px;border: 1px solid #16A085; border-radius: 10px;color:white")

        self.lineEdit_31.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_32.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_33.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")

        self.lineEdit_22.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_27.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_5.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_23.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")
        self.lineEdit_26.setStyleSheet("font-size: 15px;border: 1px solid blue; border-radius: 10px;color:white")

        self.lineEdit_29.setStyleSheet(
            "QLineEdit::disabled {font-size: 11px;border: 1px solid blue; border-radius: 5px;color:gray}"
            "QLineEdit::enabled {font-size: 11px;border: 1px solid #16A085; border-radius: 5px;color:white}")

        self.lineEdit_30.setStyleSheet(
            "QLineEdit::disabled {font-size: 11px;border: 1px solid blue; border-radius: 5px;color:gray}"
            "QLineEdit::enabled {font-size: 11px;border: 1px solid #16A085; border-radius: 5px;color:white}")

        self.lineEdit_6.setStyleSheet("border: 1px solid #16A085; border-radius: 10px;color:white")

        self.label_19.setStyleSheet("QLabel {font-size: 20px;background-color: #16A085; border-radius: 20px;}")

        self.label_54.setStyleSheet("QLabel {font-size: 11px; color:white}")
        self.label_55.setStyleSheet("QLabel {font-size: 11px; color:white}")

        self.label_21.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_33.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_31.setStyleSheet("QLabel {font-size: 20px; color:white}")

        self.label_46.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_47.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_48.setStyleSheet("QLabel {font-size: 20px; color:white}")

        self.label_30.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_32.setStyleSheet("QLabel {font-size: 20px; color:white}")

        self.label_34.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_22.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_41.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_42.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_49.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_51.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_43.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_53.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_44.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_7.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_17.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_67.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_68.setStyleSheet("QLabel {font-size: 20px; color:white}")
        self.label_69.setStyleSheet("QLabel {font-size: 20px; color:white}")

        self.label_28.setStyleSheet(
            "QLabel {font: medium; font-size: 25px;background-color: #16A085; border-radius: 10px;}")

        # Frame
        # ---------------------------------------------
        self.frame_2.setStyleSheet(
            "QFrame {border-style: outset;border-width: 2px;border-color: beige;border-radius: 10px;color: rgb(238, 238, 236);}")

        self.frame_16.setStyleSheet(
            '''QFrame {border-style: outset;border-width: 2px;border-color: beige;border-radius: 10px;color: rgb(238, 238, 236);}''')
        self.frame.setStyleSheet('''QFrame {border:0;}''')
        self.frame_20.setStyleSheet(
            '''QFrame {border-style: outset;border-width: 2px;border-color: beige;border-radius: 10px}''')

        self.frame_3.setStyleSheet('''
            QFrame {border-style: outset;border-width: 2px;border-color: blue;border-radius: 30px; background:transparent; ; }
            QLineEdit {border: 1px solid #16A085; border-radius: 10px}
            
            ''')

        self.frame_13.setStyleSheet('''QFrame {border:0;}''')
        self.frame_21.setStyleSheet('''QFrame {border:0;}''')
        self.frame_11.setStyleSheet("border-radius: 20px; background-color: #16A085;color: rgb(238, 238, 236);")

        # Groupbox
        # ---------------------------------------------
        self.groupBox.setTitle("")
        self.groupBox.setStyleSheet("border-radius: 20px; background:transparent;  ")

        self.groupBox_10.setStyleSheet('''
                    QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 1ex;}
                    QGroupBox::title {color:white;top: -8px;left: 10px;}
                    ''')
        self.groupBox_16.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_12.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_17.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_7.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_13.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_14.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_15.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_11.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_5.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_6.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_2.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_8.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_9.setStyleSheet('''
                     QGroupBox {color:white;border: solid;border-width: 2px;border-color: beige;border-radius: 10px;font: 15px consolas;margin-top: 2ex;}
                     QGroupBox::title {color:white;top: -8px;left: 10px;}
                      ''')
        self.groupBox_4.setStyleSheet('''
                QRadioButton {color:beige;font: 20px consolas;}
                QRadioButton::indicator {width: 25px; height: 25px;color:beige;}
                QGroupBox {border:0;}
                ''')
        self.comboBox_2.setStyleSheet('''
                QComboBox::down-arrow{border: solid;border-width: 5px;border-color: #16A085;border-radius: 0px}
                QComboBox{color:beige;border: solid;border-style: outset;border-width: 1px;border-color: #16A085;
                         border-top-left-radius : 0px;
                         border-top-right-radius : 0px;
                         border-bottom-left-radius:0px;
                         border-bottom-right-radius : 0px;}                        
                QListView{background-color: teal;color:white;border: solid;border-style: outset;border-width: 2px;border-color: beige;border-radius: 5px;}
                         ''')
        self.comboBox.setStyleSheet('''
                QComboBox::down-arrow{border: solid;border-width: 1px;border-color: beige;border-radius: 4px}
                QComboBox{color:beige;border: solid;border-style: outset;border-width: 2px;border-color: blue;border-radius: 10px;height:50}
                QListView{background-color: teal;color:white;border: solid;border-style: outset;border-width: 2px;border-color: beige;border-radius: 5px;}
                 ''')

        self.stackedWidget.setStyleSheet('''QFrame {border:0;}''')
        self.stackedWidget_2.setStyleSheet('''
            QStackedWidget > QWidget{border-radius: 10px;}
            QFrame {border:0;}''')

        self.frame_28.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color:  #021C1E}")
        self.frame_37.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color:  #021C1E}")
        self.frame_39.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color: #021C1E; }")
        self.frame_40.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color: #021C1E; }")
        self.frame_41.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color: #021C1E; }")
        self.frame_38.setStyleSheet(
            "QFrame {border-style: outset;border-width: 0px;border-color: beige;border-radius: 10px; background-color: #021C1E; }")

    def readServersInfo(self):
        isFilesEmpty = os.stat(self.server_info_file_name).st_size == 0
        if not isFilesEmpty:
            if os.path.isfile(self.server_info_file_name):
                try:
                    file = open(self.server_info_file_name, "r")
                    self.server_all_info = file.read().rstrip()
                    self.server_list = self.server_all_info.split("\n")
                except IOError:
                    print("Except error when read server file!")
                finally:
                    file.close()

            server_list_name = []
            for list in self.server_list:
                tmp = list.split(",")
                server_list_name.append(tmp[0])

            self.comboBox_2.clear()
            self.comboBox_2.addItem(self.choose_server_text)
            self.comboBox_2.addItems(server_list_name)
            self.comboBox_2.setCurrentIndex(0)
        elif isFilesEmpty:
            self.comboBox_2.clear()
            self.comboBox_2.addItem(self.choose_server_text)
            self.comboBox_2.setCurrentIndex(0)

    def connectSshCheck(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(self.server_hostname), self.server_port, str(self.server_username),
                        str(self.server_password))

            stdin, stdout, stderr = ssh.exec_command(str("ls"))
            lines = stdout.readlines()
            out_ = ""
            for deger in lines:
                deger = deger.split("\n")
                out_ = out_ + " " + deger[0]

            transport = ssh.get_transport()
            transport.send_ignore()
            return True
        except:
            return False

    def buttonClickExitServer(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.server_username = ""
        self.server_password = ""
        self.server_hostname = ""
        self.lineEdit_6.setText("")
        self.label_59.setText("0")
        self.label_5.setText("0")
        self.label_45.setText("0")
        self.label_58.setText("0")
        self.lineEdit_16.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_24.setText("")
        self.lineEdit_25.setText("")
        self.lineEdit.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_31.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_32.setText("")
        self.lineEdit_33.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_26.setText("")
        self.lineEdit_27.setText("")
        self.lineEdit_39.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_38.setText("")
        self.lineEdit_29.setText("0")
        self.lineEdit_30.setText("0")
        self.textEdit.setText("")
        self.checkBox_2.setChecked(True)
        self.checkBox_4.setChecked(True)
        self.checkBox_5.setChecked(True)
        self.checkBox.setChecked(True)
        self.progressBar_2.setValue(0)

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)

        while self.tableWidget_4.rowCount() > 0:
            self.tableWidget_4.removeRow(0)

        while self.tableWidget_3.rowCount() > 0:
            self.tableWidget_3.removeRow(0)

    def buttonClickEditServerPage(self):
        if 0 == self.comboBox_2.currentIndex():
            self.showDialogInfo(self.msg_title_warning, self.msg_you_did_not_choose_a_server,
                                self.msg_please_select_server, self.msg_ok)
        else:
            server_info_index = self.comboBox_2.currentIndex()
            selected_server_info = self.server_list[server_info_index - 1]

            selected_server_info = selected_server_info.split(",")

            self.lineEdit_19.setText(selected_server_info[0])
            self.lineEdit_20.setText(selected_server_info[1])
            self.lineEdit_18.setText(selected_server_info[2])
            self.stackedWidget_2.setCurrentIndex(2)

    def buttonClickEdit(self):
        if self.lineEdit_19.text() != "" and self.lineEdit_20.text() != "" and self.lineEdit_18.text() != "":
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_make_changes, self.msg_yes,
                                 self.msg_no)

            if self.message_button_return_boolean:
                # Delete Change Item
                server_info_index = self.comboBox_2.currentIndex()
                del self.server_list[server_info_index - 1]
                try:
                    dosya = open(self.server_info_file_name, 'w')
                    for list in self.server_list:
                        dosya.write(list + "\n")
                except IOError:
                    print("Except error when read server file!")
                finally:
                    dosya.close()

                # Again Save
                try:
                    dosya = open(self.server_info_file_name, 'a')
                    server_infos = self.lineEdit_19.text() + ","
                    server_infos = server_infos + self.lineEdit_20.text() + ","
                    server_infos = server_infos + self.lineEdit_18.text() + "\n"
                    dosya.write(server_infos)
                except IOError:
                    print("Except error when read server file!")
                finally:
                    dosya.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Değişiklikler kaydedildi.")
                msg.setInformativeText("Please select server!")
                msg.setWindowTitle("WARRNING")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                self.readServersInfo()
                self.lineEdit_19.setText("")
                self.lineEdit_20.setText("")
                self.lineEdit_18.setText("")

                self.stackedWidget_2.setCurrentIndex(0)
                self.comboBox_2.setCurrentIndex(0)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The server has not been selected.")
            msg.setInformativeText("Please select server!")
            msg.setWindowTitle("WARRNING")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def buttonClickDeleteServer(self):
        if 0 == self.comboBox_2.currentIndex():
            self.showDialogInfo(self.msg_title_warning, self.msg_you_did_not_choose_a_server,
                                self.msg_please_select_server, self.msg_ok)
        else:
            self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_make_changes, self.msg_yes,
                                 self.msg_no)
            if self.message_button_return_boolean:
                server_info_index = self.comboBox_2.currentIndex()
                del self.server_list[server_info_index - 1]

                try:
                    dosya = open(self.server_info_file_name, 'w')
                    for list in self.server_list:
                        dosya.write(list + "\n")
                except IOError:
                    print("Except error when read server file!")
                finally:
                    dosya.close()

                self.readServersInfo()
                self.comboBox_2.setCurrentIndex(0)

    def buttonClickGoToLogin(self):
        self.lineEdit_19.setText("")
        self.lineEdit_20.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_17.setText("")
        self.stackedWidget_2.setCurrentIndex(0)

    def buttonClickAddServer(self):
        self.stackedWidget_2.setCurrentIndex(1)

    def buttonClickNewServerInfoSave(self):
        if self.lineEdit_8.text() != "" and self.lineEdit_11.text() != "" and self.lineEdit_17.text() != "":
            try:
                dosya = open(self.server_info_file_name, 'a')
                server_infos = self.lineEdit_8.text() + ","
                server_infos = server_infos + self.lineEdit_11.text() + ","
                server_infos = server_infos + self.lineEdit_17.text() + "\n"
                dosya.write(server_infos)
            except IOError:
                print("Except error when read server file!")
            finally:
                dosya.close()

            self.readServersInfo()
            self.lineEdit_8.setText("")
            self.lineEdit_11.setText("")
            self.lineEdit_17.setText("")

            self.showDialogInfo(self.msg_title_info, self.msg_success_to_save, "", self.msg_ok)

        else:
            self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickSshConnect(self):

        if 0 == self.comboBox_2.currentIndex():
            self.showDialogInfo(self.msg_title_warning, self.msg_you_did_not_choose_a_server,
                                self.msg_please_select_server, self.msg_ok)
        else:
            if self.lineEdit_6.text() != "":
                server_info_index = self.comboBox_2.currentIndex()
                self.server_nickname = self.comboBox_2.currentText()
                selected_server_info = self.server_list[server_info_index - 1]
                selected_server_info = selected_server_info.split(",")

                self.server_username = selected_server_info[1]
                self.server_hostname = selected_server_info[2]
                self.server_password = self.lineEdit_6.text()

                self.label_20.setText(self.server_nickname)
                self.label_23.setText(self.server_username)
                self.label_24.setText(self.server_hostname)

                if self.connectSshCheck():
                    self.showDialogYesNo(self.msg_title_warning, self.msg_do_you_want_to_connect_server, self.msg_yes,
                                         self.msg_no)
                    if self.message_button_return_boolean:
                        self.firstLoginController()
                else:
                    self.showDialogInfo(self.msg_title_warning, self.msg_connection_establish, self.msg_check_info,
                                        self.msg_ok)
            else:
                self.showDialogInfo(self.msg_title_warning, self.msg_missing_info, self.msg_fill_blank, self.msg_ok)

    def buttonClickAutoInstaller(self):
        self.pushButton_5.setEnabled(False)
        self.thread_auto_install = ThreadGui.AutoInstall()
        self.thread_auto_install.change_value_text_edit.connect(self.autoInstallLogSetTextEdit)
        self.thread_auto_install.change_value_progressbar.connect(self.autoInstallProgressbarSetValue)

        self.thread_auto_install.server_username = self.server_username
        self.thread_auto_install.server_hostname = self.server_hostname
        self.thread_auto_install.server_password = self.server_password
        self.thread_auto_install.withBootstrap = self.checkBox.isChecked()

        self.thread_auto_install.start()

    def autoInstallLogSetTextEdit(self, val):
        val = val.replace("b", "")
        self.output_auto_install = self.output_auto_install + val + "\n"
        self.textEdit.setText(self.output_auto_install)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

    def autoInstallProgressbarSetValue(self, val):
        self.progressBar_2.setValue(val)
        if val == 100:
            self.pushButton_5.setEnabled(True)
            self.showDialogInfo(self.msg_title_info, self.msg_box_end_1, "", self.msg_ok)
            self.tabWidget.setCurrentIndex(2)
            self.stackedWidget.setCurrentIndex(1)
            self.showDialogInfo(self.msg_title_warning, self.msg_box_end_2, "", self.msg_ok)
            self.createWalletAdressAfterInstall()

    def showDialogYesNo(self, title, text, button_yes_name, button_no_name):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonY = msgBox.button(QMessageBox.Ok)
        buttonY.setText(button_yes_name)
        buttonN = msgBox.button(QMessageBox.Cancel)
        buttonN.setText(button_no_name)
        msgBox.exec_()

        if msgBox.clickedButton() == buttonY:
            print("Yes")
            self.message_button_return_boolean = True
        elif msgBox.clickedButton() == buttonN:
            print("No")
            self.message_button_return_boolean = False

    def showDialogInfo(self, title, text, explanation, button_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText(explanation)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        buttonY = msg.button(QMessageBox.Ok)
        buttonY.setText(button_text)
        if msg.clickedButton() == buttonY:
            print("Yes")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    # appctxt = ApplicationContext()
    # ui = MainClassGUI()
    # ui.show()
    # sys.exit(appctxt.app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    ui = MainClassGUI()
    ui.show()
    sys.exit(app.exec_())
