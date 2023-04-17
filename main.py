from PyQt5 import QtWidgets,QtCore
import MainUI
import sys

from Canvas.GPTLifeWindow import MainWindow as lifegame
class MainWindow(QtWidgets.QMainWindow,MainUI.Ui_MainWindow):
    def __init__(self):
        self.isStart = False

        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.CloseWindow)
        self.OpenCanva()
        self.pushButton_2.clicked.connect(self.ChangeSimulationState)
        self.pushButton_3.clicked.connect(self.ClearCanva)

    def ClearCanva(self):
        self.game.clearCanva()
    def ChangeSimulationState(self):
        self.game.isStart = not self.game.isStart
        state = self.game.isStart
        print("SimulationState: " + str(state))
        if state:
            self.pushButton_2.setText("Stop simulation")
        else:
            self.pushButton_2.setText("Start simulation")
    def OpenCanva(self):
        self.game =lifegame()
        self.game.show()

    def CloseWindow(self):
        self.game.close()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MainWindow()
    Form.show()
    sys.exit(app.exec_())