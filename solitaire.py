import random as rd

class Solitaire:
    def __init__(self,inputStr,inputList):
        self.inputStr = inputStr
        self.list = inputList
    def processer(self):
        temp = self.inputStr
        list = self.list
        randomNum = rd.randint(0,100)
        if temp == '野':
            list += '野'
            randomNum = rd.randint(0,150)
            if randomNum >=30 and randomNum <=120:
                list += '格'
                return '格'
            elif randomNum > 120: 
                list += '獸'
                return '獸'
            else: 
                list = []
                return '斷'
        if temp == '炸':
            list += '炸'
            if randomNum >=30: 
                list += '彈'
                return '彈'
            else: 
                list = []
                return '斷'
        if temp == '我':
            list += "我"
            if list[list.index('我') - 1] == '彈':
                if randomNum >=30 :
                    list += "的"
                    return '的'
                else: 
                    list = []
                    return '斷'
        if temp == '最':
            list += "最"
            if randomNum >=30: 
                list = []
                return '愛'
            else: 
                list = []
                return '斷'
        if temp == '先': 
            list += "先"
            list += "輩"
            return '輩'
        if temp == '唐': 
            list += "唐"
            list += "突"
            return '突'
        if temp == '惡': 
            list += "惡"
            if list[list.index('惡') - 1] == '突': 
                list = []
                return '臭'
        if temp == '田': 
            list += "田"
            list += "勝"
            return '勝'
        if temp == '傑': 
            list += "傑"
            list += "是"
            return '是'
        if temp == '口': 
            list += "口"
            list += "交"
            return '交'
        if temp == '惡': 
            list += "惡"
            if list[list.index('惡') - 1] == '交': 
                list = []
                return '徒'
        if temp == '南': 
            return '一'
        if temp == '中': 
            return '蜜'
        if temp == '蜂': 
            if 0<=randomNum and randomNum <=20: return '是'
            elif 20<randomNum and randomNum <=40: return '喜'
            elif 40<randomNum and randomNum <=60: return '常'
            elif 60<randomNum and randomNum <=80: return '被'
            elif 80<randomNum and randomNum <=100: return '都'
        if temp == '星': 
            list += '星'
            list += '爆'
            return '爆'
        if temp == '氣': 
            list += '氣'
            list += '流'
            return '流'
        if temp == '斬': 
            list += '斬'
            list += '幫'
            return '幫'
        if temp == '我' and list[list.index('我') - 1] == '幫': 
            list += '我'
            list += '撐'
            return '撐'
        if temp == '十': 
            list = []
            return '秒'
        if temp == '七彩的微風': return '側著臉輕輕吹拂'
        if temp == '當天是空的': return '地是乾的'
        if temp == '我難過的是': return '放棄你'

        ### 周杰倫區 ###

        ## Jay ##

        if temp == '漂亮的讓我臉紅的': return '可愛女人'
        if temp == '你的完美主義太徹底': return '讓我連恨都難以下筆'
        if temp == '手牽手': return '一步兩步三步四步望著天'
        if temp == '娘子卻依舊每日折一支楊柳': return '在小村外的溪邊河口默默地在等著我'
        if temp == '三分球': return '它在空中停留'
        if temp == '不懂你的黑色幽默': return '想通卻又再考倒我'
        if temp == '走過了很多地方': return '我來到伊斯坦堡'
        if temp == '沙漠之中怎麼會有泥鰍': return '話說完飛過一隻海鷗'
        if temp == '愛情來得太快就像龍捲風': return '離不開暴風圈來不及逃'
        if temp == '穿梭時間的畫面的鐘': return '從反方向開始移動'

        ## 范特西 ##

        if temp == '我給你的愛寫在西元前': return '深埋在美索不達米亞平原'
        if temp == '麥擱安捏打我媽媽': return '我說的話你甘會聽'
        if temp == '我想就這樣牽著你的手不放開': return '愛能不能夠永遠單純沒有悲哀'
        if temp == '一二三四': return '櫻花落滿地'
        if temp == '就是開不了口讓她知道': return '我一定會呵護著你也逗你笑'
        if temp == '消失的舊時光': return '一九四三'
        if temp == '廣場一枚銅幣': return '悲傷得很隱密'
        if temp == '藤蔓植物': return '爬滿了伯爵的墳墓'
        if temp == '快使用雙截棍': return '哼哼哈兮'
        if temp == '你要我說多難看': return '我真的不想分開'

        ## 八度空間 ##

        if temp == '讓我們半獸人的靈魂翻滾': return '收起殘忍回憶獸化的過程'
        if temp == '為什麼這樣子': return '你拉著我說你有些猶豫'
        if temp == '我害怕你心碎': return '沒人幫你擦眼淚'
        if temp == '我右拳打開了天': return '化身為龍'
        if temp == '你哪會全然攏沒消息': return '我親像一支蜂找無蜜'
        if temp == '趁時間沒發覺': return '讓我帶著你離開'
        if temp == '爺爺泡的茶': return '有一種味道叫做家'
        if temp == '想回到過去': return '試著抱你在懷裡'
        if temp == '跨越了牧場': return '又繞過了村莊'
        if temp == '我留著陪你 強忍著淚滴': return '有些事真的來不及回不去'

        ## 葉惠美 ##

        if temp == '仁慈的父我已墜入': return '看不見罪的國度'
        if temp == '真不該 睜不開': return '別讓我的地球變暗'
        if temp == '颳風這天 我試過握著你手': return '但偏偏 雨漸漸 大到我看你不見'
        if temp == '訓導處報告 訓導處報告': return '三年二班周杰倫 馬上到訓導處來'
        if temp == '誰在用琵琶彈奏': return '一曲東風破'
        if temp == '有誰能比我知道': return '你的溫柔像羽毛'
        if temp == '我很瞭 默契無法偽造': return '我們同一種調調'
        if temp == '她的睫毛 彎的嘴角': return '無預警地對我笑'
        if temp == '我掉進愛情懸崖': return '跌太深爬不出來'
        if temp == '文山啊 等你寫完詞': return '我都要出下張專輯囉'
        if temp == '透過鏡頭重新剪接歷史給人的想像': return '八釐米紀錄片的橋段隔著距離欣賞'

        ## 尋找周杰倫 ##

        if temp == '我會發著呆 然後忘記你': return '接著緊緊閉上眼'
        if temp == '斷了的弦 再彈一遍': return '我的世界 你不在裡面'

        ## 七里香 ##
        
        if temp == '在我地盤這': return '你就得聽我的'
        if temp == '雨下整夜': return '我的愛溢出就像雨水'