# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AdminOrderWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(602, 507)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btn_refresh = QtWidgets.QPushButton(Form)
        self.btn_refresh.setStyleSheet("font: 12pt \"宋体\";")
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout_6.addWidget(self.btn_refresh)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.tableWidget_order = QtWidgets.QTableWidget(Form)
        self.tableWidget_order.setStyleSheet("font: 12pt \"宋体\";")
        self.tableWidget_order.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_order.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_order.setAutoScroll(False)
        self.tableWidget_order.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_order.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableWidget_order.setObjectName("tableWidget_order")
        self.tableWidget_order.setColumnCount(5)
        self.tableWidget_order.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_order.setHorizontalHeaderItem(4, item)
        self.tableWidget_order.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget_order.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_order.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_order.verticalHeader().setMinimumSectionSize(23)
        self.verticalLayout.addWidget(self.tableWidget_order)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_refresh.setText(_translate("Form", "这是一个硕大的刷新按钮，想刷新订单状态请用力点我靴靴"))
        self.tableWidget_order.setSortingEnabled(True)
        item = self.tableWidget_order.horizontalHeaderItem(0)
        item.setText(_translate("Form", "食堂名"))
        item = self.tableWidget_order.horizontalHeaderItem(1)
        item.setText(_translate("Form", "商铺名"))
        item = self.tableWidget_order.horizontalHeaderItem(2)
        item.setText(_translate("Form", "菜品名"))
        item = self.tableWidget_order.horizontalHeaderItem(3)
        item.setText(_translate("Form", "总价"))
        item = self.tableWidget_order.horizontalHeaderItem(4)
        item.setText(_translate("Form", "评价"))
