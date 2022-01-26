import collections
from operator import indexOf
import pymongo
import time
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class SolitaireDB: ## 輸入: <想接的單字>
    def __init__(self,input):
        self.__char = input
        self.__client = pymongo.MongoClient("mongodb+srv://jasperchan:jscnn51011@cluster0.p9bjf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def setSequence(self,category,input):
        soli_db = self.__client['Solitaire']
        collection = soli_db[category]
        if category != 'nowSequence':
            processedInput = [input[i:i+1] for i in range(0, len(input), 1)]
            for i in range(len(processedInput)):
                collection.insert_one({
                    "content": processedInput[i],
                    "number": i
                })
        else:
            collection.insert_one({
                "sequence": input,
                "number":0
                })
    # Set the sequence being said now
    def setNow(self):
        soli_db = self.__client['Solitaire']
        allCollection = soli_db.list_collection_names()
        for i in range(len(allCollection)):
            if allCollection[i] != 'nowSequence':
                tempCollection = soli_db[allCollection[i]]
                if tempCollection.find_one({'content':self.__char,'number':0}):
                    # print("found ",self.__char," in collection ",allCollection[i])
                    self.clearSequence("nowSequence")
                    self.setSequence("nowSequence",allCollection[i])
                    break

    def querySequence(self):
        self.setNow()
        soli_db = self.__client['Solitaire']
        currentSequence = soli_db['nowSequence'].find_one({"number":0})['sequence']
        collection = soli_db[currentSequence]
        matchChar = collection.find_one({"content": self.__char})
        return collection.find({})[matchChar["number"]+1]["content"]

    def clearSequence(self,category):
        soli_db = self.__client['Solitaire']
        collection = soli_db[category]
        collection.delete_many({})
    
    def printCollection(self):
        soli_db = self.__client['Solitaire']
        print(soli_db.list_collection_names())

class LyricDB: # 輸入: 找歌 <歌名> <歌手>
    def __init__(self,input):
        if "找歌" in input:
            self.__song = input.split(" ")[1]
            self.__singer = input.split(" ")[2]
        else:
            self.__song = input
        self.__allLyrics = []
        self.__client = pymongo.MongoClient("mongodb+srv://jasperchan:jscnn51011@cluster0.p9bjf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    def setSequence(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

        browser=webdriver.Chrome('./chromedriver.exe',chrome_options=options)
        browser.maximize_window()
        time.sleep(3)
        browser.get("https://www.google.com/search?q=" + self.__song + "+" + self.__singer + "+歌詞")
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        page = BeautifulSoup(browser.page_source, "html.parser")
        lyricSection = page.find_all("div","ujudUb")
        for i in lyricSection:
            eachPara = i.find_all("span")
            for j in eachPara:
                jp = j.text.split(" ")
                for k in jp:
                    self.__allLyrics.append(k)
        browser.close()
        
    def findLyrics(self):
        collections = self.__client["Lyrics"].list_collection_names()
        try: 
            if collections.index(self.__song) != -1:
                print("找到！")
                return "資料庫已有歌曲：" + self.__song + "。"
        except:
            self.setSequence()
            soli_db = self.__client["Lyrics"]
            collection = soli_db[self.__song]
            collection.insert_one({
                "name": self.__song,
                "lyrics": self.__allLyrics
            })
            print("沒找到！")
            return "資料庫查無歌曲：" + self.__song + "，已創建歌詞資料。"
        
    def findSolitaire(self):
        collections = self.__client["Lyrics"].list_collection_names()
        for eachSong in collections:
            print(eachSong)
            try:
                lyrics = self.__client["Lyrics"][eachSong].find_one({})
                return lyrics["lyrics"][lyrics["lyrics"].index(self.__song)+1]
            except:
                print("不是這首歌")
                continue
        
    def clearSequence(self,category):
        soli_db = self.__client['Lyrics']
        collection = soli_db[category]
        collection.delete_many({})

# soliModel = LyricDB("我難過的是")
# soliModel.findSolitaire()
