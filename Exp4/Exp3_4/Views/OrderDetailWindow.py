import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from UI.UserOrderDetailWidget import Ui_Form
from Util.DbUtil import DbUtil


class OrderDetailWindow(Ui_Form, QWidget):
    def __init__(self, order_id, loc, total, comment, level, status):
        super(OrderDetailWindow, self).__init__()
        self.order_id = order_id
        self.loc = loc
        self.total = total
        self.comment = comment
        self.level = level
        self.status = status
        self.setupUi(self)
        self.init_ui()
        self.init_slot()

    def init_slot(self):
        self.btn_commit.clicked.connect(self.commit)
        self.btn_close.clicked.connect(self.close)
        self.horizontalSlider.valueChanged.connect(self.slider)

    def init_ui(self):
        if self.status == 0:
            self.btn_commit.hide()
            self.textEdit_comment.setEnabled(False)
            self.textEdit_comment.setPlaceholderText("您的订单正在制作中!")
            self.label_6.hide()
            self.horizontalSlider.hide()
            self.label_level.hide()
        elif self.status == 2:
            self.btn_commit.hide()
            self.horizontalSlider.setEnabled(False)
            self.textEdit_comment.setEnabled(False)
            self.textEdit_comment.setPlainText(self.comment)
        else:
            self.btn_commit.show()
            self.textEdit_comment.setEnabled(True)
        self.horizontalSlider.setValue(self.level)
        self.label_level.setText(str(self.level) + "分")
        self.lineEdit_order_id.setText(str(self.order_id))
        self.lineEdit_loc.setText(self.loc)
        self.lineEdit_total.setText(str(self.total))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def slider(self):
        self.level = self.horizontalSlider.value()
        self.label_level.setText(str(self.level) + "分")

    def commit(self):
        if self.textEdit_comment.toPlainText() == '':
            QMessageBox.warning(self, 'Warning', '🙅🏻 ‍请填写评价!', QMessageBox.Yes)
            return
        db = DbUtil()
        commit_data = (self.order_id, self.textEdit_comment.toPlainText(), self.level)
        db.add_comment(commit_data)
        db.db_commit()
        db.instance = None
        del db
        QMessageBox.information(self, 'Congrats!', '🎉 评论成功!', QMessageBox.Yes)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OrderDetailWindow(1, "loc", 12.5)
    win.show()
    sys.exit(app.exec())
