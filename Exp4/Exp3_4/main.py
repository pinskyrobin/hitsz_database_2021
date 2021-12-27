import sys
from Views.LoginWindow import LoginWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = LoginWindow()
    ui.show()
    sys.exit(app.exec_())
