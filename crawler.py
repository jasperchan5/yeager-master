import requests
from bs4 import BeautifulSoup
import random as rd
import pixivLogin

class nHentaiSearcher:
    def __init__(self,num):
        self.__target = requests.get("https://nhentai.net/g/"+num)
        self.__num = num
        self.__tempStr = ""
    def searchTitle(self):
        if self.__target.status_code != 200:
            return self.__num + "\n哭啊，查無此本！"
        else: 
            page = BeautifulSoup(self.__target.text,"html.parser")
            title = page.find("h2","title").text
            tempTag = page.find_all("span","name")
            tagCnt = 0
            tags = ["\n"]
            for i in tempTag:
                tags += "[" + tempTag[tagCnt].text + "]"
                tags += " "
                tagCnt += 1
                if tagCnt % 3 == 0:
                    tags += "\n"
            return self.processInfo(title,tags)
    def processInfo(self,title,tags):
        self.__tempStr += self.__num
        self.__tempStr += "\n\n"
        tagCnt = 0
        self.__tempStr += title + "\n"
        for i in tags:
            self.__tempStr += tags[tagCnt]
            tagCnt += 1
        return self.__tempStr

class tagSearcher:
    def __init__(self,inputStr):
        self.__target = requests.get("https://nhentai.net/search/?q=" + inputStr)
        self.__tag = inputStr
        self.__tempStr = ""
    def searchDoujin(self):
        page = BeautifulSoup(self.__target.text,"html.parser")
    
        # 處理本子總數
        totalStr = page.find("h1").text
        quantity = totalStr.split(" ")[1]
        doujinNum = ""
        cnt = 0
        for i in quantity:
            if quantity[cnt] != ',':
                doujinNum += quantity[cnt]
            cnt += 1

        # 總頁數
        totalPageNum = int(int(doujinNum) / 25) + 1
        pageNum = rd.randint(1,int(totalPageNum))
        titles = page.find_all("div","caption")
        # print(len(titles))
        randNum = rd.randint(0,len(titles) - 1)
        self.__target = requests.get("https://nhentai.net/search/?q=" + self.__tag + "&page=" + str(pageNum))
        page = BeautifulSoup(self.__target.text,"html.parser")
        title = titles[randNum].text
        link = page.find_all('a', href=True)[23 + randNum]
        self.__tempStr += "https://nhentai.net" + link['href'] + "\n\n"
        self.__tempStr += title
        return self.__tempStr

class pixivSearcher:
    def __init__(self,mode):
        self.crawlNum = 0
        pixivLogin.login()
        if mode == "不可以色色":
            self.target = requests.Session().get("https://www.pixiv.net/ranking.php?mode=daily")
        elif mode == "可以色色":
            self.target = requests.get("https://www.pixiv.net/ranking.php?mode=daily_r18")
    def getImage(self):
        page = BeautifulSoup(self.target.text,"html.parser")
        tempStr = ""
        titles = page.find_all("a","title")
        images = page.find_all("img")
        imgNum = rd.randint(0,49)
        tempStr += titles[imgNum].text +'\n'
        # 處理 transparent
        tempImg = images[imgNum]['src']
        tempImg = tempImg.replace("s.","i.")
        tempImg = tempImg.replace(
            "/www/images/common/transparent.gif",
            "/img-master/img/2021/09/18/00/00/08/92817111_p0_master1200.jpg")
        tempStr += tempImg
        return tempStr  

class covid19:
    def __init__(self) -> None:
        self.__target = requests.get("https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php")
    def getDailyInfo(self):
        page = BeautifulSoup(self.__target.text,"html.parser")
        tempStr = ""
        totalInfected = page.find("h1","country_recovered mb-1 text-info").text
        newTotalInfected = totalInfected.replace('+','')
        # 日期
        info = page.find("div","col-lg-12 main")
        date = info.find_all("span")[1].text
        newDate = date.split(' ')[18]
        tempStr += newDate + '\n\n'
        # 本土確診
        domesticStr = page.find_all("span","country_confirmed_percent")[1].text
        newDomesticStr = domesticStr.replace('本土病例 ','')
        tempStr += '本土： ' + newDomesticStr + "\n"
        # 境外確診
        foreignStr = str(int(newTotalInfected) - int(newDomesticStr))
        tempStr += '境外： ' + foreignStr + "\n"
        # 死亡人數
        deathStr = page.find("span","country_deaths_change").text
        newDeathStr = deathStr.replace('+','')
        tempStr += '死亡： ' + newDeathStr
        return tempStr

# a = tagSearcher(input())
# print(a.searchDoujin())