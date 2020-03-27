import sys
from random import randrange, choice
import numpy as np
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from   ui_2048 import Ui_MainWindow
class ProcessImg(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        self.show()
        self.win_value = 2048
        self.pbtn_list=[[self.p1, self.p2, self.p3, self.p4],
                        [self.p5, self.p6, self.p7, self.p8],
                        [self.p9, self.p10, self.p11, self.p12],
                        [self.p13, self.p14, self.p15, self.p16],
                        ]
        self.game_restart()


    def game_restart(self):
          #生成一个4*4 都为零元素的矩阵

        self.field = [[0 for i in range(4)] for j in range(4)]
        QApplication.processEvents()
        for pbtn in self.pbtn_img.buttons():
            pbtn.setText("")
        #print(self.field)
        self.spawn()
        self.left.setEnabled(True)
        self.right.setEnabled(True)
        self.up.setEnabled(True)
        self.down.setEnabled(True)
        self.display(self.field)

    #随机生成一个2或者4
    def spawn(self):
        # 从 100 中取一个随机数，如果这个随机数大于 89，new_element 等于 4，否则等于 2
        new_element = 4 if randrange(100) > 89 else 2
        # 得到一个随机空白位置的元组坐标
        try:
            (i,j) = choice([(i,j) for i in range(4) for j in range(4) if self.field[i][j] == 0])
            self.field[i][j] = new_element
        except:
            pass

        #print(self.field)
        return self.field


    def init(self):
        self.left.clicked.connect(self.move_left)
        self.right.clicked.connect(self.move_right)
        self.up.clicked.connect(self.move_up)
        self.down.clicked.connect(self.move_down)
        self.restart.clicked.connect(self.game_restart)

    def display(self,field):
        QApplication.processEvents()
        for pbtn in self.pbtn_img.buttons():
            pbtn.setText("")
        for i in range(4):
            for j in range(4):
                if field[i][j] != 0:
                    self.pbtn_list[i][j].setText(str(field[i][j]))


    '''数据处理'''
    #矩阵的反转
    def invert(self,field):
        return  [row[::-1] for row in field]

    #矩阵的转秩
    def transpose(self,field):
        return [list(row) for row in zip(*field)]

    #判断是否有能移动的行活着列

    def row_is_movable(self,row):
        '''判断一行里面能否有元素进行左移动或合并
        '''
        def change(i):
            # 当左边有空位（0），右边有数字时，可以向左移动
            if row[i] == 0 and row[i + 1] != 0:
                return True
            # 当左边有一个数和右边的数相等时，可以向左合并
            if row[i] != 0 and row[i + 1] == row[i]:
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    def all_is_movable(self, filed):

        left = any([self.row_is_movable(row) for row in filed])
        right = any([self.row_is_movable(row) for row in self.invert(filed)])
        up = any([self.row_is_movable(row) for row in self.transpose(filed)])
        down = any([self.row_is_movable(row) for row in self.invert(self.transpose(filed))])

        return left or right or up or down


    #棋盘的移动
    def tight(self,row):  #[2,0,2,0]---> [2,2,0,0]
        return sorted(row,key=lambda x:x==0)

    #相加
    def merge(self,row):
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                row[i] *=2
                row[i+1]=0
        return row

    def move_left(self):
        if self.all_is_movable(self.field):
            self.field=[self.tight(self.merge(self.tight(row))) for row in self.field]
            self.field=self.spawn()
            field=self.field
            self.display(field)
            #printprint(self.all_is_movable(field))

            if not self.all_is_movable(field):
                QMessageBox.warning(self, "注意", "游戏输了")
                self.left.setEnabled(False)
                self.right.setEnabled(False)
                self.up.setEnabled(False)
                self.down.setEnabled(False)
                return
            else:
                if any(any(i >= self.win_value for i in row) for row in field):
                    QMessageBox.warning(self, "注意", "游戏赢了")
                    self.left.setEnabled(False)
                    self.right.setEnabled(False)
                    self.up.setEnabled(False)
                    self.down.setEnabled(False)


    def move_right(self):
       # print(self.field)
        self.field=self.invert(self.field)
        if self.all_is_movable(self.field):
            self.field=[self.tight(self.merge(self.tight(row))) for row in self.field]
            self.field=self.invert(self.field)
            self.field=self.spawn()
            #print(self.field)
            field=self.field
            self.display(field)
            if not self.all_is_movable(self.field):
                QMessageBox.warning(self, "注意", "游戏输了")
                self.left.setEnabled(False)
                self.right.setEnabled(False)
                self.up.setEnabled(False)
                self.down.setEnabled(False)
                return
            else:
                if any(any(i >= self.win_value for i in row) for row in self.field):
                    QMessageBox.warning(self, "注意", "游戏赢了")
                    self.left.setEnabled(False)
                    self.right.setEnabled(False)
                    self.up.setEnabled(False)
                    self.down.setEnabled(False)


    def move_up(self):
        self.field=self.transpose(self.field)
        if self.all_is_movable(self.field):
            self.field=[self.tight(self.merge(self.tight(row))) for row in self.field]
            self.field=self.transpose(self.field)
            self.field=self.spawn()
            #print(self.field)
            field=self.field
            self.display(field)
            if not self.all_is_movable(self.field):
                QMessageBox.warning(self, "注意", "游戏输了")
                self.left.setEnable(False)
                self.right.setEnable(False)
                self.up.setEnable(False)
                self.down.setEnable(False)
                return
            else:
                if any(any(i >= self.win_value for i in row) for row in self.field):
                    QMessageBox.warning(self, "注意", "游戏赢了")
                    self.left.setEnabled(False)
                    self.right.setEnabled(False)
                    self.up.setEnabled(False)
                    self.down.setEnabled(False)

    def move_down(self):
        self.field=self.invert(self.transpose(self.field))
        if self.all_is_movable(self.field):
            self.field=[self.tight(self.merge(self.tight(row))) for row in self.field]
            self.field=self.transpose(self.invert(self.field))
            self.field=self.spawn()
            field=self.field
            self.display(field)

            if not self.all_is_movable(self.field):
                QMessageBox.warning(self, "注意", "游戏输了")
                self.left.setEnabled(False)
                self.right.setEnabled(False)
                self.up.setEnabled(False)
                self.down.setEnabled(False)
                return
            else:
                if any(any(i >= self.win_value for i in row) for row in self.field):
                    QMessageBox.warning(self, "注意", "游戏赢了")
                    self.left.setEnabled(False)
                    self.right.setEnabled(False)
                    self.up.setEnabled(False)
                    self.down.setEnabled(False)



if __name__=="__main__":
    app=QApplication(sys.argv)
    window=ProcessImg()
    sys.exit(app.exec_())