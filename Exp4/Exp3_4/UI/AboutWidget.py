# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutWidget(object):
    def setupUi(self, AboutWidget):
        AboutWidget.setObjectName("AboutWidget")
        AboutWidget.resize(566, 494)
        self.gridLayout = QtWidgets.QGridLayout(AboutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textBrowser = QtWidgets.QTextBrowser(AboutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_5.addWidget(self.textBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_flower = QtWidgets.QPushButton(AboutWidget)
        self.btn_flower.setObjectName("btn_flower")
        self.horizontalLayout_3.addWidget(self.btn_flower)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AboutWidget)
        QtCore.QMetaObject.connectSlotsByName(AboutWidget)

    def retranslateUi(self, AboutWidget):
        _translate = QtCore.QCoreApplication.translate
        AboutWidget.setWindowTitle(_translate("AboutWidget", "Form"))
        self.textBrowser.setHtml(_translate("AboutWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">本次实验总算是告一段落！</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">首先要向所有老师和助教说一句抱歉！🙇‍</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">高估能力的后果是这个学期选了太多的课，现在来看也是遭到了报应😭这次实验在正式提交后好久才做完，在感叹自己过于繁重的学业压力的同时，也深感愧疚。</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">但是但是！我也有很用心地完成这次实验！没有一点点的敷衍！😝</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">因为只是学过前端的框架，所以没有使用 Java；因为不是很熟悉 QSS 的用法，所以没有做最后的界面美化。</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">说起界面的美观，我发现 QT 在 macOS 和 Windows 下的显示效果真的天差地别😵大概就是卖家秀和买家秀的区别吧呜呜我也不知道为什么会这样！不知道老师/助教是用哪个系统看的呢，如果是 Windows 系统的话可以看一下我的演示视频和实验报告的截图，它其实也不是那么丑的！！！</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">面对有些简陋的 UI，我实在过意不去，于是尝试在里面加了些有趣的内容~希望可以缓解批改的心情，也是想让自己在众多作品中显得有一些不一样吧哈哈哈哈（叉腰）</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">与其说这次实验让我更加熟练地使用 SQL 语句，倒不如说是让我对产品和编码规则有了一定的启发吧。虽然时间仓促，虽然这个小小的软件还有太多的不完美，但是在权衡各门课程之后，我想，我是已经尽力了，至于分数，交给你们就好啦！😬</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Hope everything goes well !</span></p></body></html>"))
        self.btn_flower.setText(_translate("AboutWidget", "送一朵小红花"))
