from PyQt5.QtWidgets import QMainWindow, QMessageBox
from UI.AdminMainWindow import Ui_MainWindow
from Views.AdminHomeWindow import AdminHomeWindow
from Views.AdminOrderWindow import AdminOrderWindow
from Views.AboutWindow import AboutWindow
from Util.Constants import ROLE_MAP


class AdminMainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self, login=None, username=None, role=None):
        super(AdminMainWindow, self).__init__()
        self.setupUi(self)
        self.is_change_user = False
        self.username = username
        self.login_win = login
        self.role = ROLE_MAP.get(str(role))
        self.init_slot()
        self.init_ui()

    def init_ui(self):
        self.pushButton.setMinimumWidth(60)
        self.treeWidget.setCurrentIndex(self.treeWidget.model().index(0, 0))
        self.current_username_label.setText(self.username)
        self.current_role_label.setText(self.role)
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        self.stackedWidget.addWidget(AdminHomeWindow(self.username))
        self.stackedWidget.addWidget(AdminOrderWindow(self.username))
        self.stackedWidget.addWidget(AboutWindow())

    def init_slot(self):
        self.treeWidget.currentItemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.log_out)

    def item_changed(self):
        if self.treeWidget.currentItem().text(0) == '🧐  主页':
            self.stackedWidget.setCurrentIndex(0)
        elif self.treeWidget.currentItem().text(0) == '🔍  订单管理':
            self.stackedWidget.setCurrentIndex(1)
        elif self.treeWidget.currentItem().text(0) == '💫 关于':
            self.stackedWidget.setCurrentIndex(2)

    def log_out(self):
        self.is_change_user = True
        self.close()

    def closeEvent(self, event):
        if self.is_change_user:
            reply = QMessageBox.question(self, '消息', '确定退出当前账号吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            reply = QMessageBox.question(self, '消息', '确定退出系统吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            if self.is_change_user:
                self.login_win.show()
        else:
            event.ignore()
            self.is_change_user = False
