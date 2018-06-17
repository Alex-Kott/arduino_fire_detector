import sys
from PyQt5.QtWidgets import QApplication
import desktop


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = desktop.Desktop()
    sys.exit(app.exec_())
