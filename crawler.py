import requests
from bs4 import BeautifulSoup
import random as rd
import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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
        link = page.find_all('a', href=True)[23 + randNum]
        self.__tempStr += "https://nhentai.net" + link['href'] + "\n\n"
        return self.__tempStr

class imageSearcher:
    def __init__(self,crawlNum):
        self.crawlNum = crawlNum if crawlNum <= 5 else 5
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
        self.target=webdriver.Chrome('./chromedriver.exe',chrome_options=options)

    def LoginPixiv(self):
        self.target.maximize_window()
        time.sleep(3)
        self.target.get("https://www.pixiv.net/ranking.php")
        # 點登入按鈕
        self.target.find_element(By.CLASS_NAME,"ui-button._login").click()
        # 輸入帳號密碼
        username, password = self.target.find_elements(By.TAG_NAME,"input")[0], self.target.find_elements(By.TAG_NAME,"input")[1]
        username.send_keys("b09705026@ntu.edu.tw")
        password.send_keys("Db168245")
        self.target.find_element(By.CLASS_NAME,"signup-form__submit").click()
        while(len(self.target.find_elements(By.CLASS_NAME,"ranking-item")) != 500):
            self.target.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        # self.target.close()


    def getNormalImage(self):
        # 首頁找圖
        imgArr = []
        page = BeautifulSoup(self.target.page_source,"html.parser")
        rankingItems = page.find_all("section","ranking-item")
        randRank = rd.randint(0,499)
        imgId = rankingItems[randRank].find("div","ranking-image-item").find("a")['href']
        print(imgId)
        imgLink = rankingItems[randRank].find("img")['src']
        print(imgLink)
        # resData = requests.get(imgLink,headers={'Referer': 'https://www.pixiv.net/'})
        imgArr.append([randRank,imgLink])
        return imgArr
    
    def getHentaiImage(self):

        page = BeautifulSoup(self.target.page_source,"html.parser")
        tempStr = ""
        image = page.findAll("a")
        randNum = rd.randint(0,len(image))
        tempStr += image[20]['href']
        print(tempStr)

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


a = imageSearcher(5)
a.LoginPixiv()
print(a.getNormalImage())