import time
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from UI.UserHomePageWidget import Ui_HomePageWidget
from Util.DbUtil import DbUtil


class UserHomeWindow(Ui_HomePageWidget, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self):
        super(UserHomeWindow, self).__init__()
        self.setupUi(self)
        self.time_percent = (int(time.time()) + 28800) % 86400 // 864
        self.init_ui()
        self.init_slot()
        self.get_orders()

    def init_ui(self):
        self.progressBar_time.setValue(self.time_percent)
        self.time.setText(str(self.time_percent) + '%')
        self.tableWidget_prd.setColumnCount(4)
        self.tableWidget_prd.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_prd.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def init_slot(self):
        self.btn_refresh.clicked.connect(self.refresh)
        self.time.setText(str(self.time_percent) + '%')
        self.query_done_signal.connect(self.show_orders)
        self.btn_random.clicked.connect(self.random)

    def refresh(self):
        self.time_percent = (int(time.time()) + 28800) % 86400 // 864
        self.get_orders()

    def get_orders(self):
        th = Thread(target=self.get_orders_th())
        th.start()

    def get_orders_th(self):
        db = DbUtil()
        count, res = db.get_recent_order()
        self.query_done_signal.emit([count, res])

    def show_orders(self, res):
        orders = res[1]
        col_num = len(orders[0])
        row = 0
        for order in orders:
            if self.tableWidget_prd.rowCount() <= row:
                self.tableWidget_prd.insertRow(row)
            for i in range(col_num):
                item = QTableWidgetItem(str(order[i]))
                self.tableWidget_prd.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num):
                item = self.tableWidget_prd.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def random(self):
        db = DbUtil()
        res = db.get_one_prd_randomly()
        msg = '🍲 今日菜单\n' \
              '菜品名:{}\n' \
              '介绍:{}\n' \
              '单价:{}\n' \
              '销量:{}\n' \
              'Enjoy your meal!' \
            .format(res[0][0], res[0][1], res[0][2], res[0][3])
        QMessageBox.information(self, 'Congrats!', msg, QMessageBox.Yes)
