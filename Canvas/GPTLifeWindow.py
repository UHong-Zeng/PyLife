import sys
import sqlite3

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np


class LifeGame:
    def __init__(self, size):
        # 初始化游戏状态为随机的0和1
        self.grid = np.random.choice([0, 1], size=size)
        # self.grid = np.zeros(shape=size)
        self.rows, self.cols = size




    # 定义规则函数，计算下一个状态
    def evolve(self):
        new_grid = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                # 计算每个细胞周围的活细胞数
                neighbors = self.grid[max(0, i - 1):min(i + 2, self.rows), max(0, j - 1):min(j + 2, self.cols)]
                count = np.sum(neighbors) - self.grid[i, j]
                # 应用规则，更新细胞状态
                if self.grid[i, j] == 1 and 2 <= count <= 3:
                    new_grid[i, j] = 1
                elif self.grid[i, j] == 0 and count == 3:
                    new_grid[i, j] = 1
        self.grid = new_grid


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.isStart = False

        # 创建一个大小为50x50的游戏
        self.x, self.y = 50,50
        self.game = LifeGame((self.x, self.y))

        # 创建图像窗口和初始化图像
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # 创建一个包含canvas的QWidget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # 创建一个包含canvas的QVBoxLayout，并将其添加到QWidget中
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.canvas)

        # 将NavigationToolbar添加到QWidget中
        self.toolbar = NavigationToolbar(self.canvas, self.widget)
        self.layout.addWidget(self.toolbar)

        self.ax = self.figure.add_subplot(111)
        # self.ax.set_axis_off()

        # 渲染初始状态
        self.img = self.ax.imshow(self.game.grid, cmap='binary')

        # 创建一个定时器，每0.1秒更新一次状态
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)

        # 綁定用戶點擊事件
        self.cid = self.figure.canvas.mpl_connect('button_press_event', self.onclick)

        self.getLifeState()

    # 設置用戶點擊事件的處理函數
    def onclick(self,event):
        x, y = event.xdata // 1, event.ydata // 1
        y, x = int(x), int(y)
        x = self.fix_number(x)
        y = self.fix_number(y)
        print(x,y)
        self.game.grid[x][y] = 1
        self.img.set_data(self.game.grid)
        self.canvas.draw()
    def fix_number(self,n):
        if n - (n//1) >= 0.5:
            return n//1 + 1
        else:
            return n//1
    def update_game(self):
        if self.isStart:
            # 计算下一个状态并渲染图像
            self.game.evolve()
            self.img.set_data(self.game.grid)
            self.canvas.draw()

    def clearCanva(self):
        self.game.grid = np.zeros((self.x,self.y))
        self.img.set_data(self.game.grid)
        self.canvas.draw()

    def getLifeState(self,table_name="table01"):

        conn = sqlite3.connect("pattern0.db")
        cur = conn.cursor()
        # cur.execute("CREATE TABLE {} (row INTERGER, col INTERGER, isLive INTERGER)".format(table_name))
        cur.execute("delete from {}".format(table_name))
        for row in range(self.x):
            for col in range(self.y):
                cur.execute("insert or replace into {}(row,col,isLive) values ({},{},{})".format(table_name,row,col,self.game.grid[row][col]))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
