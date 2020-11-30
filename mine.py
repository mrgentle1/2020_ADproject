from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QFont, QPainter, QColor)
from PyQt5.QtCore import (Qt, QEvent)
import sys
import numpy as np

class gameBoard(QWidget):
    """선택된 난이도에 따라 게임 보드판 생성"""
    mine_list = [10, 40, 99]
    board_size = [(9, 9), (16, 16), (30, 16)]
    location = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]  # 주변 8방향
    del(location[4])  # (0, 0) 제외

    def __init__(self, diff):  # 난이도 0, 1, 2(쉬움, 보통, 어려움)
        super().__init__()
        self.mine = self.mine_list[diff]
        self.w = self.board_size[diff][0]  # board width
        self.h = self.board_size[diff][1]  # board height 
        self.tileSize = self.w * self.h  # 모든 타일의 개수
        self.tileLeft = self.w * self.h - self.mine  # 지뢰가 없는 타일 개수
        self.flag = 0  # 사용된 flag의 개수
        self.checked = True

        # 지뢰를 랜덤한 위치에 배치
        self.board = np.zeros(self.w * self.h, dtype='i')
        self.board[:self.mine] = 9
        np.random.shuffle(self.board)
        self.board = self.board.reshape(self.w, self.h)
        self.setBoardInfo()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("지뢰 찾기")
        grid = QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)
        self.butTiles = [[] for _ in range(self.h)]  # 각 타일 버튼 object를 2차원 리스트에 저장

        for i in range(self.h):
            for j in range(self.w):
                self.butTiles[i].append(QPushButton(self))
                self.butTiles[i][j].setMinimumSize(25,25)
                self.butTiles[i][j].setMaximumSize(25,25)

                # self.butTiles[i][j].setStyleSheet(
                # "border-style: outset;"
                # "border-width: 1px;"
                # "border-radius: 15px;"
                # "border-color: grey;"
                # "padding: 4px;"
                # )

                grid.addWidget(self.butTiles[i][j], i, j, 1, 1)
                self.butTiles[i][j].clicked.connect(lambda state, x=i, y=j: self.buttonClicked(x, y))  # 클릭한 버튼의 좌표 값 전달
                self.butTiles[i][j].setContextMenuPolicy(Qt.CustomContextMenu)
                self.butTiles[i][j].customContextMenuRequested.connect(lambda state, x=i, y=j: self.rightClicked(x, y))
        self.show()

    def setBoardInfo(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] == 9:
                    for x, y in self.location:
                        nx, ny = i + x, j + y
                        if(nx >= self.h or nx < 0 or ny >= self.w or ny < 0):
                            continue
                        if (self.board[nx][ny] != 9):
                            self.board[nx][ny] += 1

    def buttonClicked(self, x, y):
        print(x, y)
        self.butTiles[x][y].setText(str(self.board[x][y]))
        self.butTiles[x][y].setDisabled(True)
    
    def rightClicked(self, x, y):
        self.butTiles[x][y].setText('★' if self.checked else '') 
        self.checked = not self.checked


# class saveload:
#     """게임 진행상태와 결과 저장/불러오기"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = gameBoard(0)
    print(test.board)
    sys.exit(app.exec_())