import os
from threading import Thread

import cv2 as cv
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QGraphicsPixmapItem, QGraphicsScene
from UI.UserCanteenWidget import Ui_Form
from Util.DbUtil import DbUtil


class CanteenWindow(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def __init__(self, canteen_id):
        super(CanteenWindow, self).__init__()
        self.canteen_id = canteen_id
        self.setupUi(self)
        self.init_slot()
        self.init_data()
        self.init_ui()

    def init_slot(self):
        self.query_done_signal.connect(self.show_data)

    def init_data(self):
        self.get_info()
        self.get_data('comment')
        self.get_data('top')

    def init_ui(self):
        self.tableWidget_comment.setColumnCount(3)
        self.tableWidget_comment.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_comment.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_top.setColumnCount(5)
        self.tableWidget_top.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_top.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def get_info(self):
        db = DbUtil()
        count, res = db.get_canteen_info(self.canteen_id)
        self.label_name.setText(res[0][0])
        self.progressBar.setValue(int(res[0][1] * 20))
        self.label_level.setText(str(round(res[0][1], 1)) + " 分")
        paths = res[0][2].split("/")
        path = os.path.join(os.getcwd(), paths[-2], paths[-1])
        image = cv.imread(path)
        height = image.shape[0]
        width = image.shape[1]
        frame = QImage(image, width, height, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    def show_data(self, raw_data):
        datas = raw_data[1]
        window = self.tableWidget_comment
        if raw_data[2] == 'top':
            window = self.tableWidget_top
        col_num = len(datas[0])
        row = 0
        for data in datas:
            if window.rowCount() <= row:
                window.insertRow(row)
            for i in range(col_num):
                item_name = data[i]
                if raw_data[2] == 'comment' and i == 1:
                    item_name = str(item_name) + " 分"
                elif raw_data[2] == 'top' and i == 3:
                    item_name = str(item_name) + " 元"
                item = QTableWidgetItem(str(item_name))
                window.setItem(row, i, item)
            row = row + 1
        for i in range(row):
            for j in range(col_num):
                item = window.item(i, j)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def get_data(self, tag):
        th = Thread(target=self.get_data_th(tag))
        th.start()

    def get_data_th(self, tag):
        db = DbUtil()
        if tag == 'comment':
            count, res = db.get_canteen_comment(self.canteen_id)
        else:
            count, res = db.get_canteen_top(self.canteen_id)
        self.query_done_signal.emit([count, res, tag])
