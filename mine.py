from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (Qt, QEvent)
import sys
import numpy as np
'''
class win(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("( ˘･з･˘)")
        lbLose = QLabel("You Win.")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(lbLose)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.show()

class lose(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("( ˘･з･˘)")
        lbLose = QLabel("You Lose.")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(lbLose)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.show()
'''

class gameLevel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.level = 0

    def initUI(self):
        self.setWindowTitle("난이도 설정")
        self.rbtnLv1 = QRadioButton('쉬움',self)
        self.rbtnLv2 = QRadioButton('보통', self)
        self.rbtnLv3 = QRadioButton('어려움', self)
        self.rbtnLv1.setChecked(True)
        self.qle = QLineEdit(self)
        self.qle.setReadOnly(True)


        self.btn = QPushButton('난이도 선택')
        self.btn.clicked.connect(self.btnClicked)

        self.rbtnLv1.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.rbtnLv1)
        hbox.addStretch(1)
        hbox.addWidget(self.rbtnLv2)
        hbox.addStretch(1)
        hbox.addWidget(self.rbtnLv3)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.btn)
        vbox.addStretch(1)
        vbox.addWidget(self.qle)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def btnClicked(self):
        if self.rbtnLv1.isChecked():
            self.level = 0
        elif self.rbtnLv2.isChecked():
            self.level = 1
        elif self.rbtnLv3.isChecked():
            self.level = 2

        test = gameBoard(self.level)
        print(test.board)
        gameLevel.close(self)

class gameBoard(QWidget):
    """선택된 난이도에 따라 게임 보드판 생성"""
    mine_list = [10, 40, 99]
    board_size = [(9, 9), (16, 16), (30, 30)]
    location = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]  # 주변 8방향
    del (location[4])  # (0, 0) 제외

    def __init__(self, diff):  # 난이도 0, 1, 2(쉬움, 보통, 어려움)
        super().__init__()
        self.mine = self.mine_list[diff]
        self.w = self.board_size[diff][0]  # board width
        self.h = self.board_size[diff][1]  # board height
        self.tileSize = self.w * self.h  # 모든 타일의 개수
        self.tileLeft = self.w * self.h - self.mine  # 지뢰가 없는 타일 개수
        self.flag = 0  # 사용된 flag의 개수
        self.checked = [[True for _ in range(self.w)] for _ in range(self.h)]

        # 지뢰를 랜덤한 위치에 배치
        self.board = np.zeros(self.w * self.h, dtype='i')
        self.board[:self.mine] = 9
        np.random.shuffle(self.board)
        self.board = self.board.reshape(self.w, self.h)
        self.setBoardInfo()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("지뢰 찾기")
        #self.btnStart = QPushButton("게임 시작")
        #self.btnStart.move(self, 0,0)
        #self.btnStart.clicked().connect(self.clickedStart)
        grid = QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)
        self.butTiles = [[] for _ in range(self.h)]  # 각 타일 버튼 object를 2차원 리스트에 저장
        self.mineLabel = QLabel(f'남은 지뢰: {self.mine}')
        grid.addWidget(self.mineLabel, 0, 0, 1, 7)

        for i in range(self.h):
            for j in range(self.w):
                self.butTiles[i].append(QPushButton(self))
                self.butTiles[i][j].setMinimumSize(25, 25)
                self.butTiles[i][j].setMaximumSize(25, 25)

                # self.butTiles[i][j].setStyleSheet(
                # "border-style: outset;"
                # "border-width: 1px;"
                # "border-radius: 15px;"
                # "border-color: grey;"
                # "padding: 4px;"
                # )
                grid.addWidget(self.butTiles[i][j], i+1, j, 1, 1)
                self.butTiles[i][j].clicked.connect(lambda state, x=i, y=j: self.buttonClicked(x, y))  # 클릭한 버튼의 좌표 값 전달
                self.butTiles[i][j].setContextMenuPolicy(Qt.CustomContextMenu)
                self.butTiles[i][j].customContextMenuRequested.connect(lambda state, x=i, y=j: self.rightClicked(x, y))
        self.show()

    def clickedStart(self):
        gameBoard(self.level)

    def setBoardInfo(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] == 9:
                    for x, y in self.location:
                        nx, ny = i + x, j + y
                        if (nx >= self.h or nx < 0 or ny >= self.w or ny < 0):
                            continue
                        if (self.board[nx][ny] != 9):
                            self.board[nx][ny] += 1

    def findZero(self, x, y):
        if self.board[x][y] != 0:  # base case: 해당 타일이 0이 아닌경우, 해당 타일의 숫자 출력하고 return
            self.butTiles[x][y].setText(str(self.board[x][y]))
            self.butTiles[x][y].setDisabled(True)
            return

        self.butTiles[x][y].setText('')
        self.butTiles[x][y].setDisabled(True)

        for i, j in self.location:
            nx, ny = x + i, y + j
            if (nx >= self.h or nx < 0 or ny >= self.w or ny < 0 or not self.butTiles[nx][ny].isEnabled()):
                continue
            if (self.board[nx][ny] == 0):  # 다음 타일의 숫자가 0일 때 재귀호출
                self.findZero(nx, ny)
            elif (self.board[nx][ny] != 9):  # 다음 타일의 숫자가 지뢰가 아닐 때 해당 타일의 숫자 출력
                self.butTiles[nx][ny].setText(str(self.board[nx][ny]))
                self.butTiles[nx][ny].setDisabled(True)
            else:  # 다음 타일의 숫자가 지뢰(9)일 때는 continue
                continue

    def buttonClicked(self, x, y):
        val = self.board[x][y]
        if val == 0:
            self.findZero(x, y)
        elif val != 9:
            self.butTiles[x][y].setText(str(val))
            self.butTiles[x][y].setDisabled(True)
        else:
            self.loseGame()
            TEST.qle.setText("You Lose")

    def rightClicked(self, x, y):
        self.butTiles[x][y].setText('★' if self.checked[x][y] else '')
        if self.checked[x][y]: self.flag += 1
        else: self.flag -= 1
        self.mineLabel.setText(f'남은 지뢰: {self.mine-self.flag}')
        self.checked[x][y] = not self.checked[x][y]

    def loseGame(self):
        for x in range(self.h):
            for y in range(self.w):
                if self.board[x][y] == 9:
                    self.butTiles[x][y].setStyleSheet(
                        "background-color:red;"
                        "color:pink;"
                    )
                    self.butTiles[x][y].setText('♥')
                    self.butTiles[x][y].setDisabled(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "지뢰 찾기", "종료하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# class saveload:
#     """게임 진행상태와 결과 저장/불러오기"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    TEST = gameLevel()
    # test = gameBoard(TEST)
    # print(test.board)
    sys.exit(app.exec_())