import numpy as np
import random as rd

class TicTacToe:
    def __init__(self,select,started,nowCourt):

        if started == False:
            # Initiate the game
            self.court = np.empty([3,3], dtype = object)
            for i in range(0,3):
                for j in range(0,3):
                    self.court[i][j] = "_"
            self.originalCourt = self.court

            # Select player identity
            self.player = [False,""]
            self.bot = [False,""]
            if self.player[0] == False and self.bot[0] == False:
                if select == "O" :
                    self.player = [True,"O"]
                    self.bot = [True,"X"]
                elif select == "X":
                    self.player = [True,"X"]
                    self.bot = [True,"O"]

        else:
            # Re-Initiate the game
            self.court = np.empty([3,3], dtype = object)
            for i in range(0,3):
                for j in range(0,3):
                    self.court[i][j] = "_"
            self.originalCourt = self.court
            # Load records
            print(len(nowCourt))
            nowCourtCnt = 0
            for i in range(0,3):
                for j in range(0,3):
                    self.court[i][j] = nowCourt[nowCourtCnt]
                    nowCourtCnt += 1
                    if i < 2 and nowCourt[nowCourtCnt] == '\n':
                        nowCourtCnt += 1
            
    def loadInfo(self,infos,started):
        if started == False:
            infos += self.player[1]
            infos += self.bot[1]
        else:
            self.player = ["True",infos[0]]
            self.bot = ["True",infos[1]]

    def recordCourt(self): # 回傳string格式的棋盤
        tempStr = ""
        for i in range(0,3):
            for j in range(0,3):
                tempStr += self.court[i][j]
            if i < 2:
                tempStr += "\n"
        return tempStr

    def displayPlayer(self,coordX,coordY):
        if self.court[int(coordX)][int(coordY)]  == "_": 
            self.court[int(coordX)][int(coordY)] = self.player[1]
        else:
            if self.court[int(coordX)][int(coordY)]  == "X": 
                print("還敢蓋別人啊，bad。")
            else:
                print("這個位置下過了，北七。")
        self.recordCourt()

    def displayBot(self):
        posX = rd.randint(0,2)
        posY = rd.randint(0,2)
        if self.court[posX][posY] == "_":
            self.court[posX][posY] = self.bot[1]
            self.recordCourt()
        else:
            # print("collided")
            self.displayBot()

    def clear(self):
        self.court = self.originalCourt

    def endGame(self):
        # Case row or column
        for i in range(0,3):
            occupiedO = 0
            occupiedX = 0
            for j in range(0,3):
                if self.court[i][j] == "O":
                    occupiedO += 1
                    if occupiedO == 3:
                        print("You win")
                        return True
                elif self.court[i][j] == "X":
                    occupiedX += 1
                    if occupiedX == 3:
                        return True
        for i in range(0,3):
            occupiedO = 0
            occupiedX = 0
            for j in range(0,3):
                if self.court[i][j] == "O":
                    occupiedO += 1
                    if occupiedO == 3:
                        print("You win")
                        return True
                elif self.court[i][j] == "X":
                    occupiedX += 1
                    if occupiedX == 3:
                        return True
        # Case slant
        occupiedO = 0
        occupiedX = 0
        for i in range(0,3):
            for j in range(0,3):
                if i == j:
                    if self.court[i][j] == "O":
                        occupiedO += 1
                        if occupiedO == 3:
                            print("You win")
                            return True
                    elif self.court[i][j] == "X":
                        occupiedX += 1
                        if occupiedX == 3:
                            return True
        return False

# nowCourt = ""
# infos = []
# a = TicTacToe("O",False,"")
# a.loadInfo(infos,False)
# # while(a.endGame() == False):
# b = input()
# b = b.split(" ")
# a.displayPlayer(b[0],b[1])
# # if a.endGame() == True: break
# a.displayBot()
# # if a.endGame() == True: break
# temp = a.recordCourt()
# print(temp)
# c = TicTacToe("O",True,temp)
# c.loadInfo(infos,True)
# # while(a.endGame() == False):
# d = input()
# d = d.split(" ")
# c.displayPlayer(d[0],d[1])
# # if a.endGame() == True: break
# c.displayBot()
# # if a.endGame() == True: break
# temp = c.recordCourt()
# print(temp)