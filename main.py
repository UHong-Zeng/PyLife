from PyQt5 import QtWidgets,QtCore
import MainUI
import sys

from Canvas.FirstCanva_Window import MainWindow as FirstMainWindow
class MainWindow(QtWidgets.QMainWindow,MainUI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.OpenFirstCanva)

    def OpenFirstCanva(self):
        self.FirstCanva = FirstMainWindow()
        self.FirstCanva.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MainWindow()
    Form.show()
    sys.exit(app.exec_())