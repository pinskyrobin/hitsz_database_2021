from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from UI.UserOrderWidget import Ui_Form
from Util.DbUtil import DbUtil


class UserOrderWindow(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self, store_name):
        super(UserOrderWindow, self).__init__()
        self.store_name = store_name
        self.row = 0
        self.tot = 0
        self.cart = []
        self.setupUi(self)
        self.init_slot()
        self.init_ui()
        self.init_data()

    def init_ui(self):
        self.lcdNumber_tot.display(self.tot)
        self.tableWidge_prd.setColumnCount(5)
        self.tableWidge_prd.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidge_prd.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_cart.setColumnCount(2)
        self.tableWidget_cart.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_cart.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def init_slot(self):
        self.query_done_signal.connect(self.show_prd)
        self.tableWidge_prd.doubleClicked.connect(self.add_cart)
        self.btn_clear.clicked.connect(self.clear)

    def init_data(self):
        th = Thread(target=self.get_prd_th())
        th.start()

    def get_prd_th(self):
        db = DbUtil()
        count, res = db.get_store_prd(self.store_name)
        self.query_done_signal.emit([count, res])

    def show_prd(self, res):
        prds = res[1]
        col_num = len(prds[0])
        row = 0
        for prd in prds:
            if self.tableWidge_prd.rowCount() <= row:
                self.tableWidge_prd.insertRow(row)
            for i in range(col_num):
                item_name = prd[i]
                item = QTableWidgetItem(str(item_name))
                self.tableWidge_prd.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num):
                item = self.tableWidge_prd.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def add_cart(self):
        row = self.tableWidge_prd.currentRow()
        prd_id = self.tableWidge_prd.item(row, 0).text()
        prd_name = self.tableWidge_prd.item(row, 1).text()
        prd_price = self.tableWidge_prd.item(row, 3).text()
        self.cart.append([prd_id, prd_price])
        self.tot += round(float(prd_price), 1)

        if self.tableWidget_cart.rowCount() <= self.row:
            self.tableWidget_cart.insertRow(self.row)
        item = QTableWidgetItem(str(prd_id))
        self.tableWidget_cart.setItem(self.row, 0, item)
        item = QTableWidgetItem(str(prd_name))
        self.tableWidget_cart.setItem(self.row, 1, item)
        item = QTableWidgetItem(str(prd_price))
        self.tableWidget_cart.setItem(self.row, 2, item)
        self.lcdNumber_tot.display(self.tot)

        self.row += 1

    def clear(self):
        self.cart = []
        self.tot = 0
        self.row = 0
        self.tableWidget_cart.clearContents()
        self.tableWidget_cart.setRowCount(0)
        self.lcdNumber_tot.display(0)
