from PyQt5.QtWidgets import *
import sys
import numpy as np


class gameBoard(QWidget):
    """선택된 난이도에 따라 게임 보드판 생성"""
    mine_list = [10, 40, 99]
    board_size = [(9, 9), (16, 16), (30, 16)]

    def __init__(self, diff):  # 난이도 0, 1, 2(쉬움, 보통, 어려움)
        super().__init__()

        self.mine = self.mine_list[diff]
        self.w = self.board_size[diff][0]  # board width
        self.h = self.board_size[diff][1]  # board height
        self.tileSize = self.w * self.h  # 모든 타일의 개수
        self.tileLeft = self.w * self.h - self.mine  # 지뢰가 없는 타일 개수
        self.flag = 0  # 사용된 flag의 개수

        # 지뢰를 랜덤한 위치에 배치
        self.board = np.zeros(self.w * self.h, dtype='i')
        self.board[:self.mine] = 9
        np.random.shuffle(self.board)
        self.board = self.board.reshape(self.w, self.h)

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
                self.butTiles[i][j].setMinimumSize(25, 25)
                self.butTiles[i][j].setMaximumSize(25, 25)
                grid.addWidget(self.butTiles[i][j], i, j, 1, 1)
                self.butTiles[i][j].clicked().connect()

        self.show()

    def countMine(self,i,j):
        count = 0;

        for k in range(i-1,i+2):
            for l in range(j-1, j+2):
                if self.board[k][l] == 9:
                    count +=1

        return count

    def showNum(self,i,j):
        if(self.board[i][j]==9):
            print("게임오버") #임의로 넣음

        else :
            k = i
            l = j
            while(1):
                if (self.countMine(self, k, l) != 0):
                    self.butTiles[k][l].setText(self.countMine(self,k,l))
                    break

                else:
                    listLength = 0
                    l1 = []
                    l1 += self.getNumAroundZoro(k,l)
                    listLength = len(l1)
                    while(1):
                        for m,n in l1:
                            l1 += self.getNumAroundZoro(m,n)
                            listLength = len(list(set(l1)))

                        if len(l1)==listLength:
                            break

                        else:
                            continue

                    for m,n in l1:
                        self.butTiles[m][n].setText(self.countMine(self, m, n))





    def getNumAroundZoro (self, i,j):
        l1 = []
        for k in range(i-1,i+2):
            for l in range(j-1, j+2):
                l1.append((k,l))

                return l1




# class mineGame(QWidget):
#     """GUI로 나타냄"""
# class saveload:
#     """게임 진행상태와 결과 저장/불러오기"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = gameBoard(0)
    print(test.board)
    sys.exit(app.exec_())
