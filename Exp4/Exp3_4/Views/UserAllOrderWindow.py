from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from UI.UserAllOrderWidget import Ui_Form
from Views.OrderDetailWindow import OrderDetailWindow
from Util.DbUtil import DbUtil


class UserAllOrderWindow(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self, user_name):
        super(UserAllOrderWindow, self).__init__()
        self.user_name = user_name
        self.setupUi(self)
        self.init_slot()
        self.init_ui()
        self.init_data()
        self.order_detail_window = None

    def init_ui(self):
        self.tableWidget_order.setColumnCount(6)
        self.tableWidget_order.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_order.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def init_slot(self):
        self.btn_refresh.clicked.connect(self.get_orders)
        self.query_done_signal.connect(self.show_orders)
        self.tableWidget_order.doubleClicked.connect(self.commit)

    def init_data(self):
        self.get_orders()

    def get_orders(self):
        th = Thread(target=self.get_orders_th())
        th.start()

    def get_orders_th(self):
        db = DbUtil()
        count, res = db.get_user_orders(self.user_name)
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
                if i == 3:
                    item_name = str(item_name) + " 元"
                if i == 4:
                    if order[4] == 0:
                        item_name = "已下单"
                    elif order[4] == 1:
                        item_name = "已完成"
                item = QTableWidgetItem(str(item_name))
                self.tableWidget_order.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num):
                item = self.tableWidget_order.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def commit(self):
        row = self.tableWidget_order.currentRow()
        order_id = self.tableWidget_order.item(row, 0).text()
        loc = self.tableWidget_order.item(row, 1).text()
        total = self.tableWidget_order.item(row, 3).text()
        comment = self.tableWidget_order.item(row, 5).text()
        level = 5
        if comment != '':
            comment = comment.split(" ", 2)
            comment = comment[2]
            level = self.tableWidget_order.item(row, 5).text()
            level = int(level[0])
        status = 1
        if self.tableWidget_order.item(row, 4).text() == '已下单':
            status = 0
        if self.tableWidget_order.item(row, 5).text() != '':
            status = 2

        self.order_detail_window = OrderDetailWindow(order_id, loc, total, comment, level, status)
        self.order_detail_window.show()
