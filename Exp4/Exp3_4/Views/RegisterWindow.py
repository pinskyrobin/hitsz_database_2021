from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from UI.Register import Ui_RegisterWindow
from Util.DbUtil import DbUtil
from Util.FuncUtil import get_md5


class RegisterWindow(Ui_RegisterWindow, QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_register.clicked.connect(self.register)

    def init_ui(self):
        self.btn_register.setMinimumWidth(60)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def cancel(self):
        self.close()

    def register(self):
        username = self.lineEdit_user_name.text()
        password = self.lineEdit_password.text()
        confirm = self.lineEdit_confirm.text()
        if '' in [username, password, confirm]:
            QMessageBox.warning(self, 'Warning', '🙅🏻 ‍请填写完整!', QMessageBox.Yes)
            return
        if len(username) > 16:
            QMessageBox.warning(self, 'Warning', '🤯 用户名应小于 16 位!', QMessageBox.Yes)
            return
        if len(password) > 16:
            QMessageBox.warning(self, 'Warning', '🤯 密码应小于 16 位!', QMessageBox.Yes)
            return
        db = DbUtil()
        count, res = db.query(table_name='users', column_name='user_name', condition=username)
        if count != 0:
            QMessageBox.warning(self, 'Warning', '🤯 用户名已存在!', QMessageBox.Yes)
            return
        if password != confirm:
            QMessageBox.warning(self, 'Error', '🤔 两次输入密码不一致!', QMessageBox.Yes)
            return
        user_info = [username, get_md5(password)]
        db.add_user(user_info)
        db.db_commit()
        db.instance = None
        del db
        QMessageBox.warning(self, 'Congrats!', '🎉 注册成功!', QMessageBox.Yes)
        self.close()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Enter or QKeyEvent.key() == Qt.Key_Return:
            self.btn_register.click()
