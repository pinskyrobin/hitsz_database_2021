from threading import Thread

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QHeaderView
from UI.AdminHomeWidget import Ui_Form
from Util.DbUtil import DbUtil


class AdminHomeWindow(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self, admin_name):
        super(AdminHomeWindow, self).__init__()
        db = DbUtil()
        self.admin_name = admin_name
        count, res = db.get_admin_info(self.admin_name)
        self.canteen_id = res[0][0]
        self.store_id = res[0][1]
        self.setupUi(self)
        self.init_slot()
        self.init_data()
        self.init_ui()
        self.init_data()

    def init_slot(self):
        self.btn_finish.clicked.connect(self.finish)
        self.btn_refresh.clicked.connect(self.refresh)
        self.query_done_signal.connect(self.show_data)

    def init_data(self):
        self.get_data('order')
        self.get_data('comment')

    def init_ui(self):
        self.tableWidget_order.setColumnCount(6)
        self.tableWidget_order.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_comment.setColumnCount(4)
        self.tableWidget_comment.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_comment.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def finish(self):
        try:
            db = DbUtil()
            row = self.tableWidget_order.currentRow()
            order_id = self.tableWidget_order.item(row, 0).text()
            db.update_order_status(order_id)
            db.db_commit()
            db.instance = None
            del db
            self.tableWidget_order.removeRow(row)
            QMessageBox.information(self, 'Done!', '🥳 提交成功!', QMessageBox.Yes)
        except Exception:
            QMessageBox.warning(self, 'Do nothing!', '🤯 出错!', QMessageBox.Yes)
            return

    def show_data(self, raw_data):
        row = 0
        datas = raw_data[1]
        window = self.tableWidget_comment
        if raw_data[2] == 'order':
            window = self.tableWidget_order
        if len(datas) == 0:
            return
        col_num = len(datas[0])
        for data in datas:
            if window.rowCount() <= row:
                window.insertRow(row)
            for i in range(col_num):
                item_name = data[i]
                if raw_data[2] == 'order' and i == 4:
                    item_name = str(item_name) + " 元"
                if raw_data[2] == 'comment' and i == 2:
                    item_name = str(item_name) + " 分"
                item = QTableWidgetItem(str(item_name))
                window.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num - 1):
                item = window.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def get_data(self, tag):
        th = Thread(target=self.get_data_th(tag))
        th.start()

    def get_data_th(self, tag):
        db = DbUtil()
        if tag == 'order':
            count, res = db.get_not_finished_order(self.canteen_id, self.store_id)
        else:
            count, res = db.get_admin_comment(self.canteen_id, self.store_id)
        self.query_done_signal.emit([count, res, tag])

    def refresh(self):
        self.get_data('order')
        self.get_data('comment')
