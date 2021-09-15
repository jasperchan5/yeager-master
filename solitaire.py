import random as rd

class Solitaire:
    def __init__(self,inputStr):
        self.inputStr = inputStr
    
    def processer(self):
        temp = self.inputStr
        if temp == '野' or temp == '炸' or temp == '我' or temp == '最':
            randomNum = rd.randint(0,100)
            if temp == '野':
                if randomNum >=40: return '格'
                else: return '斷'
            if temp == '炸':
                if randomNum >=40: return '彈'
                else: return '斷'
            if temp == '我':
                if randomNum >=40: return '的'
                else: return '斷'
            if temp == '最':
                if randomNum >=40: return '愛'
                else: return '斷'
        elif temp == '田' or temp == '傑' or temp == '口' or temp == '惡':
            if temp == '田': return '勝'
            if temp == '傑': return '是'
            if temp == '口': return '交'
            if temp == '惡': return '徒'
        