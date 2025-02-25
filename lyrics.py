from operator import indexOf
import dotenv
import pymongo
import time
import selenium
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import opencc

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
        elif "刪歌" in input:
            self.__song = input.split(" ")[1]
        else:
            self.__song = input
        self.__allLyrics = []
        self.__client = pymongo.MongoClient("mongodb+srv://jasperchan:jscnn51011@cluster0.p9bjf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    def setSequence(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

        browser=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)
        # browser=webdriver.Chrome(executable_path="./chromedriver.exe",chrome_options=options)
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
                    print("轉換前：",k)
                    k2 = opencc.OpenCC('s2t').convert(k)
                    print("轉換後：",k2)
                    self.__allLyrics.append(k2)
        browser.close()
        
    def findLyrics(self):
        collections = self.__client["Lyrics"].list_collection_names()
        try: 
            if collections.index(self.__song) != -1:
                print("找到！")
                return f"資料庫已有歌曲：{self.__song}。"
        except:
            self.setSequence()
            soli_db = self.__client["Lyrics"]
            collection = soli_db[self.__song]
            collection.insert_one({
                "name": self.__song,
                "lyrics": self.__allLyrics
            })
            print("沒找到！")
            if self.__allLyrics == []:
                return f"哭啊，找不到歌曲：{self.__song} 的歌詞！"
            else:
                return f"資料庫查無歌曲：{self.__song}，已創建歌詞資料。"
        
    def findSolitaire(self):
        collections = self.__client["Lyrics"].list_collection_names()
        for eachSong in collections:
            print(eachSong)
            try:
                lyrics = self.__client["Lyrics"][eachSong].find_one({})["lyrics"]
                for i, p in enumerate(lyrics):
                    if p == self.__song:
                        return lyrics[i+1]
                    elif self.__song in p and p != self.__song:
                        return p[len(self.__song):len(p)]
            except:
                print("不是這首歌")
                continue

    def listAllSong(self):
        songList = self.__client["Lyrics"].list_collection_names()
        songList.sort()
        songStr = ""
        for i in songList:
            songStr += i + '\n'
        print(songStr)
        return songStr

    def toTraditional(self):
        collections = self.__client["Lyrics"].list_collection_names()
        for eachSong in collections:
            # print(eachSong)
            lyrics = self.__client["Lyrics"][eachSong].find_one({})["lyrics"]
            # print(lyrics)
            newLyrics = []
            for p in lyrics:
                newLyrics.append(opencc.OpenCC('s2t').convert(p))
            # print(newLyrics)
            self.__client["Lyrics"][eachSong].replace_one({"lyrics": lyrics},{"lyrics": newLyrics})
        return "全部歌曲已轉成繁體。"
        
    def clearSong(self):
        soli_db = self.__client['Lyrics']
        collection = soli_db[self.__song]
        collection.drop()
        print(f"已刪除歌曲 {self.__song}。")
        return f"已刪除歌曲 {self.__song}。"
    
    def clearNull(self):
        collections = self.__client["Lyrics"].list_collection_names()
        removeList = []
        for eachSong in collections:
            print(eachSong)
            lyrics = self.__client["Lyrics"][eachSong].find_one({})["lyrics"]
            if lyrics == []:
                self.__client["Lyrics"][eachSong].drop()
                removeList.append(eachSong)
            # self.__client["Lyrics"][eachSong].find_one_and_update({})["lyrics"]
        print(f"已清除歌詞為空者：{removeList}")
        return f"已清除歌詞為空者：{removeList}"