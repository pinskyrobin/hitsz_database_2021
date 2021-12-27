from PyQt5.QtWidgets import QWidget, QMessageBox
from UI.AboutWidget import Ui_AboutWidget
from Util.DbUtil import DbUtil


class AboutWindow(Ui_AboutWidget, QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
        self.btn_flower.clicked.connect(self.flower)

    def flower(self):
        db = DbUtil()
        db.send_flower()
        QMessageBox.information(self, '消息', '😆 送花成功!\n谢谢你!!!', QMessageBox.Yes)
