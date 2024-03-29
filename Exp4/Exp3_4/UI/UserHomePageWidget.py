# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserHomePageWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HomePageWidget(object):
    def setupUi(self, HomePageWidget):
        HomePageWidget.setObjectName("HomePageWidget")
        HomePageWidget.resize(566, 494)
        self.gridLayout = QtWidgets.QGridLayout(HomePageWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(HomePageWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.progressBar_time = QtWidgets.QProgressBar(HomePageWidget)
        self.progressBar_time.setProperty("value", 24)
        self.progressBar_time.setObjectName("progressBar_time")
        self.horizontalLayout_4.addWidget(self.progressBar_time)
        self.time = QtWidgets.QLabel(HomePageWidget)
        self.time.setObjectName("time")
        self.horizontalLayout_4.addWidget(self.time)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(HomePageWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.btn_random = QtWidgets.QPushButton(HomePageWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_random.setFont(font)
        self.btn_random.setObjectName("btn_random")
        self.horizontalLayout_5.addWidget(self.btn_random)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(HomePageWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btn_refresh = QtWidgets.QPushButton(HomePageWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_refresh.setFont(font)
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout_3.addWidget(self.btn_refresh)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableWidget_prd = QtWidgets.QTableWidget(HomePageWidget)
        self.tableWidget_prd.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget_prd.setFont(font)
        self.tableWidget_prd.setStyleSheet("font: 12pt \"宋体\";")
        self.tableWidget_prd.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_prd.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_prd.setAutoScroll(False)
        self.tableWidget_prd.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_prd.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_prd.setObjectName("tableWidget_prd")
        self.tableWidget_prd.setColumnCount(4)
        self.tableWidget_prd.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_prd.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_prd.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_prd.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_prd.setHorizontalHeaderItem(3, item)
        self.tableWidget_prd.horizontalHeader().setMinimumSectionSize(130)
        self.tableWidget_prd.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_prd.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_prd.verticalHeader().setMinimumSectionSize(23)
        self.verticalLayout.addWidget(self.tableWidget_prd)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(HomePageWidget)
        QtCore.QMetaObject.connectSlotsByName(HomePageWidget)

    def retranslateUi(self, HomePageWidget):
        _translate = QtCore.QCoreApplication.translate
        HomePageWidget.setWindowTitle(_translate("HomePageWidget", "Form"))
        self.label_4.setText(_translate("HomePageWidget", "今天已经过去了..."))
        self.time.setText(_translate("HomePageWidget", "24%"))
        self.label_6.setText(_translate("HomePageWidget", "每日灵魂拷问——今天吃什么？🤔"))
        self.btn_random.setText(_translate("HomePageWidget", "帮我选"))
        self.label_3.setText(_translate("HomePageWidget", "或者看看小伙伴们都吃了什么？🤓"))
        self.btn_refresh.setText(_translate("HomePageWidget", "刷新"))
        self.tableWidget_prd.setSortingEnabled(True)
        item = self.tableWidget_prd.horizontalHeaderItem(0)
        item.setText(_translate("HomePageWidget", "菜品名"))
        item = self.tableWidget_prd.horizontalHeaderItem(1)
        item.setText(_translate("HomePageWidget", "位置"))
        item = self.tableWidget_prd.horizontalHeaderItem(2)
        item.setText(_translate("HomePageWidget", "菜品单价"))
        item = self.tableWidget_prd.horizontalHeaderItem(3)
        item.setText(_translate("HomePageWidget", "菜品销量"))
