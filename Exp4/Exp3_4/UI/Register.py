# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Register.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(480, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RegisterWindow.sizePolicy().hasHeightForWidth())
        RegisterWindow.setSizePolicy(sizePolicy)
        RegisterWindow.setMinimumSize(QtCore.QSize(480, 240))
        RegisterWindow.setMaximumSize(QtCore.QSize(480, 240))
        RegisterWindow.setTabletTracking(False)
        RegisterWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 190, 461, 32))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btn_cancel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.btn_register = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btn_register.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btn_register.setAutoDefault(False)
        self.btn_register.setDefault(True)
        self.btn_register.setObjectName("btn_register")
        self.horizontalLayout_2.addWidget(self.btn_register)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 70, 461, 97))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_user_name = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_user_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_user_name.setObjectName("label_user_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_user_name)
        self.lineEdit_user_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_user_name.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_user_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_user_name.setPlaceholderText("")
        self.lineEdit_user_name.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit_user_name.setClearButtonEnabled(False)
        self.lineEdit_user_name.setObjectName("lineEdit_user_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_user_name)
        self.label_password = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_password.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_password.setMaxLength(16)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.label_confirm = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_confirm.setObjectName("label_confirm")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_confirm)
        self.lineEdit_confirm = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_confirm.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEdit_confirm.setMaxLength(16)
        self.lineEdit_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirm.setObjectName("lineEdit_confirm")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_confirm)
        self.horizontalLayout_3.addLayout(self.formLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 0, 461, 61))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.title = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.horizontalLayout_4.addWidget(self.title)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        RegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)
        RegisterWindow.setTabOrder(self.lineEdit_user_name, self.lineEdit_password)
        RegisterWindow.setTabOrder(self.lineEdit_password, self.lineEdit_confirm)
        RegisterWindow.setTabOrder(self.lineEdit_confirm, self.btn_register)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", " 注册"))
        self.btn_cancel.setText(_translate("RegisterWindow", "取消"))
        self.btn_register.setText(_translate("RegisterWindow", "注册"))
        self.label_user_name.setText(_translate("RegisterWindow", "用户名"))
        self.label_password.setText(_translate("RegisterWindow", "密码"))
        self.label_confirm.setText(_translate("RegisterWindow", "确认密码"))
        self.title.setText(_translate("RegisterWindow", "HITsz Canteen"))
