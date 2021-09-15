import random as rd

class Solitaire:
    def __init__(self,inputStr):
        self.inputStr = inputStr
    
    def processer(self):
        temp = self.inputStr
        randomNum = rd.randint(0,100)
        if temp == '野' or temp == '炸' or temp == '我' or temp == '最':
            if temp == '野':
                randomNum = rd.randint(0,150)
                if randomNum >=40 and randomNum <=120: return '格'
                elif randomNum > 120: return '獸'
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
        elif temp == '先': return '輩'
        elif temp == '雷': return '普'
        elif temp == '田' or temp == '傑' or temp == '口' or temp == '惡':
            if temp == '田': return '勝'
            if temp == '傑': return '是'
            if temp == '口': return '交'
            if temp == '惡': return '徒'
        elif temp == '南' or temp == '中' or temp == '蜂':
            if temp == '南': return '一'
            if temp == '中': return '蜜'
            if temp == '蜂': 
                if 0<=randomNum and randomNum <=20: return '是'
                elif 20<randomNum and randomNum <=40: return '喜'
                elif 40<randomNum and randomNum <=60: return '常'
                elif 60<randomNum and randomNum <=80: return '被'
                elif 80<randomNum and randomNum <=100: return '都'
        elif temp == '星' or temp == '氣' or temp == '斬' or temp == '我' or temp == '十':
            if temp == '星': return '爆'
            if temp == '氣': return '流'
            if temp == '斬': return '幫'
            if temp == '我': return '撐'
            if temp == '十': return '秒'