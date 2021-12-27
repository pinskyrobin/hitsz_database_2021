from PyQt5.QtWidgets import QMainWindow, QMessageBox
from UI.UserMainWindow import Ui_MainWindow
from Views.UserHomeWindow import UserHomeWindow
from Views.UserAllOrderWindow import UserAllOrderWindow
from Views.CanteenWindow import CanteenWindow
from Views.UserOrderWindow import UserOrderWindow
from Views.AboutWindow import AboutWindow
from Util.Constants import ROLE_MAP
from Util.DbUtil import DbUtil


class UserMainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self, login=None, username=None, role=None):
        super(UserMainWindow, self).__init__()
        self.setupUi(self)
        self.is_change_user = False
        self.username = username
        self.login_win = login
        self.role = ROLE_MAP.get(str(role))
        self.store_111 = UserOrderWindow("酸菜鱼")
        self.store_112 = UserOrderWindow("西北风味")
        self.store_211 = UserOrderWindow("豆花")
        self.store_212 = UserOrderWindow("经典小炒")
        self.store_221 = UserOrderWindow("东北特色菜")
        self.init_slot()
        self.init_ui()

    def init_ui(self):
        self.pushButton.setMinimumWidth(60)
        self.treeWidget.setCurrentIndex(self.treeWidget.model().index(0, 0))
        self.current_username_label.setText(self.username)
        self.current_role_label.setText(self.role)
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)

        self.stackedWidget.addWidget(UserHomeWindow())
        self.stackedWidget.addWidget(CanteenWindow(1))
        self.stackedWidget.addWidget(self.store_111)
        self.stackedWidget.addWidget(self.store_112)
        self.stackedWidget.addWidget(CanteenWindow(2))
        self.stackedWidget.addWidget(self.store_211)
        self.stackedWidget.addWidget(self.store_212)
        self.stackedWidget.addWidget(self.store_221)
        self.stackedWidget.addWidget(UserAllOrderWindow(self.username))
        self.stackedWidget.addWidget(AboutWindow())
        # self.stackedWidget.addWidget(QWidget())

    def init_slot(self):
        self.treeWidget.currentItemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.log_out)
        self.store_111.btn_commit.clicked.connect(lambda: self.commit(111, self.store_111))
        self.store_112.btn_commit.clicked.connect(lambda: self.commit(112, self.store_112))
        self.store_211.btn_commit.clicked.connect(lambda: self.commit(211, self.store_211))
        self.store_212.btn_commit.clicked.connect(lambda: self.commit(212, self.store_212))
        self.store_221.btn_commit.clicked.connect(lambda: self.commit(221, self.store_221))

    def item_changed(self):
        if self.treeWidget.currentItem().text(0) == '👀 主页':
            self.stackedWidget.setCurrentIndex(0)
        elif self.treeWidget.currentItem().text(0) == '🏪 荔园一食堂':
            self.stackedWidget.setCurrentIndex(1)
        elif self.treeWidget.currentItem().text(0) == '🐠 酸菜鱼':
            self.stackedWidget.setCurrentIndex(2)
        elif self.treeWidget.currentItem().text(0) == '🥗 西北风味':
            self.stackedWidget.setCurrentIndex(3)
        elif self.treeWidget.currentItem().text(0) == '🏪 荔园二食堂':
            self.stackedWidget.setCurrentIndex(4)
        elif self.treeWidget.currentItem().text(0) == '🍮 豆花':
            self.stackedWidget.setCurrentIndex(5)
        elif self.treeWidget.currentItem().text(0) == '🥘 经典小炒':
            self.stackedWidget.setCurrentIndex(6)
        elif self.treeWidget.currentItem().text(0) == '👨🏻‍🍳 东北菜':
            self.stackedWidget.setCurrentIndex(7)
        elif self.treeWidget.currentItem().text(0) == '💰 订单管理':
            self.stackedWidget.setCurrentIndex(8)
        elif self.treeWidget.currentItem().text(0) == '🔍 关于':
            self.stackedWidget.setCurrentIndex(9)

    '''
    步骤分析:
        ① 获取 user_id, store_id, total
        ② 构造购物车清单列表
        ③ 将 ① 和 ② 合成一个列表
        ④ 调用 sql, 提交订单
    '''

    def commit(self, store_id, store):
        prds = []
        for i in range(store.tableWidget_cart.rowCount()):
            prd_id = store.tableWidget_cart.item(i, 0).text()
            prds.append(int(prd_id))
        if not prds:
            QMessageBox.warning(self, '骚瑞', '🥲 亲亲还没有点餐哦', QMessageBox.Yes)
            return
        set_prds = set(prds)
        if len(set_prds) != len(prds):
            QMessageBox.warning(self, '骚瑞', '🥲 检测到重复菜品!\n亲亲我们目前还没有支持重复菜品的点单哦!\n感谢李姐!!!🙇🏼', QMessageBox.Yes)
            store.clear()
            return

        db = DbUtil()
        user_id = db.get_user_id(self.username)
        tot = store.lcdNumber_tot.value()
        data = [user_id, int(store_id), round(float(tot), 1), prds]
        db.add_order(data)
        del db
        QMessageBox.information(self, '成功辣', '😎 点单成功!\n请友友耐心等待哦!\n记得到\"订单管理\"随时查看状态~', QMessageBox.Yes)
        store.clear()

    def log_out(self):
        self.is_change_user = True
        self.close()

    def closeEvent(self, event):
        if self.is_change_user:
            reply = QMessageBox.question(self, '尝试确认', '🤔 确定退出当前账号吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            reply = QMessageBox.question(self, '试图挽留', '🥺 确定退出系统吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            if self.is_change_user:
                self.login_win.show()
        else:
            event.ignore()
            self.is_change_user = False
