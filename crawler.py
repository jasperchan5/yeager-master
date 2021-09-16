import requests
from bs4 import BeautifulSoup

class nHentaiSearcher:
    def __init__(self,num):
        self.__target = requests.get("https://nhentai.net/g/"+num)
    def searchTitle(self):
        page = BeautifulSoup(self.__target.text,"html.parser")
        title = [page.find("span","before").text,page.find("span","pretty").text,page.find("span","after").text]
        tempStr = ""
        for i in range(0,3):
            tempStr+=title[i]
        return tempStr
    def getPage(self,num):
        return "https://nhentai.net/g/"+num