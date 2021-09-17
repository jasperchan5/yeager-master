import requests
from bs4 import BeautifulSoup

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
            tempTag = page.find_all("a")
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
    
# a = pixivSearcher(input())
# print(a.searchTitle())