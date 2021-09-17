import requests
from bs4 import BeautifulSoup
import random as rd

class nHentaiSearcher:
    def __init__(self,num):
        self.__target = requests.get("https://nhentai.net/g/"+num)
        self.__num = num
        self.__tempStr = ""
    def searchTitle(self):
        if self.__target.status_code != 200:
            return self.__num + "\n哭啊，查無此本"
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
        self.__num = inputStr
        self.__tempStr = ""
    def searchDoujin(self):
        page = BeautifulSoup(self.__target.text,"html.parser")
        totalStr = page.find("h1").text
        totalNum = totalStr.split(" ")[1]
        doujinNum = ""
        cnt = 0
        for i in totalNum:
            if totalNum[cnt] != ',':
                doujinNum += totalNum[cnt]
            cnt += 1
        totalPageNum = int(int(doujinNum) / 25) + 1
        pageNum = rd.randint(1,int(totalPageNum))
        randNum = rd.randint(0,24)
        self.__target = requests.get("https://nhentai.net/search/?q=" + self.__num + "&page=" + str(pageNum))
        page = BeautifulSoup(self.__target.text,"html.parser")
        title = page.find_all("div","caption")[24].text
        self.__tempStr += title
        return self.__tempStr

class pixivSearcher:
    def __init__(self,num):
        self.__target = requests.get("https://www.pixiv.net/artworks/"+num)
        self.__num = num
        self.__tempStr = ""
    def searchTitle(self):
        if self.__target.status_code != 200:
            return self.__num + "\n哭啊，查無此作品"
        else: 
            page = BeautifulSoup(self.__target.text,"html.parser")
            title = page.find("title").text
            tempTag = page.find_all("ul")
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
    
# a = tagSearcher(input())
# print(a.searchDoujin())