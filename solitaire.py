import random as rd

class Solitaire:
    def __init__(self,inputStr):
        self.inputStr = inputStr
    
    def yeager(self):
        randomNum = rd.randint(0,100)
        if self.inputStr == '野':
            if randomNum >=40:
                return '格'
            else:
                return '斷'
        if self.inputStr == '炸':
            if randomNum >=40:
                return '彈'
            else:
                return '斷'
        if self.inputStr == '我':
            if randomNum >=40:
                return '的'
            else:
                return '斷'
        if self.inputStr == '最':
            if randomNum >=40:
                return '愛'
            else:
                return '斷'