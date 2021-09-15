import random as rd

class Solitaire:
    def __init__(self,inputStr):
        self.inputStr = inputStr
    
    def yeager(self):
        if self.inputStr == '野':
            randomNum = rd.randint(0,100)
            if randomNum >=40:
                return '格'
            else:
                return '斷'