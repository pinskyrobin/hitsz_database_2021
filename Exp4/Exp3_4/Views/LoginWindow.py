import os
from threading import Thread

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from UI.Login import Ui_LoginWindow
from Util.FuncUtil import *
from Views.RegisterWindow import RegisterWindow
from Util.DbUtil import DbUtil
from Views.UserMainWindow import UserMainWindow
from Views.AdminMainWindow import AdminMainWindow

NOT_EXISTED = 1
WRONG_PSW = 2
PASS = 3


class LoginWindow(Ui_LoginWindow, QMainWindow):
    login_done_signal = pyqtSignal(int)

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.role = None
        self.init_ui()
        self.main_window = None
        self.register_window = None
        self.init_slot()

    def init_ui(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(os.getcwd(), "Image", "icon.ico")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

    def init_slot(self):
        self.btn_register.clicked.connect(lambda: self.btn_slot('register'))
        self.btn_login.clicked.connect(lambda: self.btn_slot('login'))
        self.login_done_signal.connect(self.login_handler)

    def btn_slot(self, tag):

        # 注册
        if tag == 'register':
            self.register_window = RegisterWindow()
            self.register_window.show()
            self.show()

        # 登录
        if tag == 'login':
            user_name = self.lineEdit_user_name.text()
            user_psw = self.lineEdit_password.text()
            if '' in [user_name, user_psw]:
                QMessageBox.warning(self, 'Warning', '请输入用户名或密码!', QMessageBox.Yes)
                return
            if self.radio_admin.isChecked():
                login_th = Thread(target=self.login, args=(user_name, user_psw, True))
            else:
                login_th = Thread(target=self.login, args=(user_name, user_psw))
            login_th.start()

    def login(self, username, password, admin=False):
        db = DbUtil()
        if self.radio_admin.isChecked():
            count, res = db.query(table_name='admin', column_name='admin_name', condition=username)
        else:
            count, res = db.query(table_name='users', column_name='user_name', condition=username)
        if count == 0:
            self.login_done_signal.emit(NOT_EXISTED)
            return
        if get_md5(password) != res[0][2]:
            self.login_done_signal.emit(WRONG_PSW)
            return
        if admin:
            self.role = 0
        else:
            self.role = 1

        self.login_done_signal.emit(PASS)

    def login_handler(self, login_result):
        if login_result == NOT_EXISTED:
            QMessageBox.warning(self, 'Warning', '用户名不存在,请重试!', QMessageBox.Yes)
            return

        if login_result == WRONG_PSW:
            QMessageBox.warning(self, 'Warning', '用户名或密码错误!', QMessageBox.Yes)
            return

        if login_result == PASS:
            username = self.lineEdit_user_name.text()
            if self.role:
                self.main_window = UserMainWindow(login=self, username=username, role=self.role)
            else:
                self.main_window = AdminMainWindow(login=self, username=username, role=self.role)
            self.main_window.show()
            self.close()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Enter or QKeyEvent.key() == Qt.Key_Return:
            self.btn_login.click()
