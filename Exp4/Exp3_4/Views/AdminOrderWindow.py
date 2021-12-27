from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from UI.AdminOrderWidget import Ui_Form
from Util.DbUtil import DbUtil


class AdminOrderWindow(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self, admin_name):
        super(AdminOrderWindow, self).__init__()
        db = DbUtil()
        self.admin_name = admin_name
        count, res = db.get_admin_info(self.admin_name)
        self.canteen_id = res[0][0]
        self.store_id = res[0][1]
        self.setupUi(self)
        self.init_ui()
        self.query_done_signal.connect(self.show_orders)
        self.btn_refresh.clicked.connect(self.refresh)
        self.get_orders()

    def init_ui(self):
        self.tableWidget_order.setColumnCount(5)
        self.tableWidget_order.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def get_orders(self):
        th = Thread(target=self.get_orders_th())
        th.start()

    def get_orders_th(self):
        db = DbUtil()
        count, res = db.get_admin_order(self.canteen_id, self.store_id)
        self.query_done_signal.emit([count, res])

    def show_orders(self, res):
        orders = res[1]
        col_num = len(orders[0])
        row = 0
        for order in orders:
            if self.tableWidget_order.rowCount() <= row:
                self.tableWidget_order.insertRow(row)
            for i in range(col_num):
                item_name = order[i]
                if item_name is None:
                    item_name = ''
                item = QTableWidgetItem(str(item_name))
                self.tableWidget_order.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num - 1):
                item = self.tableWidget_order.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def refresh(self):
        self.get_orders()
